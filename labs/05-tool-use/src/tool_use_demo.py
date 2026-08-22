import json
import os
from pathlib import Path

from azure.identity import AzureCliCredential, get_bearer_token_provider
from dotenv import load_dotenv
from openai import BadRequestError, OpenAI

load_dotenv(Path(__file__).resolve().parents[3] / ".env")

endpoint = os.environ["FOUNDRY_OPENAI_ENDPOINT"]
deployment_name = os.environ["FOUNDRY_MODEL_NAME"]

lab_root = Path(__file__).resolve().parents[1]
brochure_dir = lab_root / "data" / "brochures"
supported_file_types = {".pdf", ".txt", ".md"}

token_provider = get_bearer_token_provider(
    AzureCliCredential(),
    "https://cognitiveservices.azure.com/.default",
)

client = OpenAI(
    base_url=endpoint,
    api_key=token_provider,
)

INSTRUCTIONS = """
You are a travel assistant for Margie's Travel.
Use the uploaded brochures when answering questions about Margie's Travel services.
Use web search only for current public destination context, such as travel advisories,
weather patterns, major events, or other information that may change over time.
When brochure details and web information differ, clearly separate Margie's Travel
package details from current public context.
""".strip()

PROMPTS = [
    "I like food, walkable neighborhoods, and design. Which Margie's Travel package should I choose, and what services are included?",
    "For that destination, add current public travel considerations I should verify before booking.",
]


def find_brochure_files():
    files = [
        path
        for path in sorted(brochure_dir.iterdir())
        if path.is_file() and path.suffix.lower() in supported_file_types
    ]

    if not files:
        raise FileNotFoundError(
            f"No supported brochure files found in {brochure_dir}. "
            "Add .pdf, .txt, or .md files and run the lab again."
        )

    return files


def create_vector_store_with_brochures():
    brochure_files = find_brochure_files()

    print("Creating vector store and uploading brochures...")
    vector_store = client.vector_stores.create(name="margies-travel-brochures")

    completed = 0
    failed = 0

    try:
        # Upload one file at a time; file_batches.upload_and_poll relies on an
        # LRO status endpoint this Foundry resource does not support.
        for path in brochure_files:
            with path.open("rb") as handle:
                vector_store_file = client.vector_stores.files.upload_and_poll(
                    vector_store_id=vector_store.id,
                    file=handle,
                )
            if vector_store_file.status == "completed":
                completed += 1
            else:
                failed += 1
    except Exception:
        client.vector_stores.delete(vector_store.id)
        raise

    print(f"Vector store ready: {completed} completed, {failed} failed.")
    print("Uploaded files:")
    for path in brochure_files:
        print(f"- {path.name}")

    return vector_store


def build_tools(vector_store_id, include_web_search=True):
    tools = [
        {
            "type": "file_search",
            "vector_store_ids": [vector_store_id],
        }
    ]

    if include_web_search:
        tools.append({"type": "web_search"})

    return tools


def create_travel_response(user_text, vector_store_id, previous_response_id, include_web_search=True):
    request = {
        "model": deployment_name,
        "instructions": INSTRUCTIONS,
        "input": user_text,
        "tools": build_tools(vector_store_id, include_web_search=include_web_search),
        "max_output_tokens": 700,
    }

    if previous_response_id:
        request["previous_response_id"] = previous_response_id

    try:
        return client.responses.create(**request)
    except BadRequestError as error:
        if include_web_search and "web_search" in str(error).lower():
            print("Web search was not accepted by this deployment. Retrying with file_search only.")
            return create_travel_response(
                user_text,
                vector_store_id,
                previous_response_id,
                include_web_search=False,
            )
        raise


def print_tool_activity(response):
    tool_items = []

    for item in response.output:
        item_type = getattr(item, "type", "unknown")
        if "search" not in item_type and not item_type.endswith("_call"):
            continue

        item_data = item.model_dump(exclude_none=True)
        compact_item = {
            key: item_data[key]
            for key in ["type", "status", "queries", "query", "results"]
            if key in item_data
        }
        tool_items.append(compact_item or {"type": item_type})

    print("\nTool activity")
    if not tool_items:
        print("- No explicit tool call items were returned.")
        return

    print(json.dumps(tool_items, indent=2, default=str))


def should_keep_vector_store():
    return os.getenv("FOUNDRY_KEEP_VECTOR_STORE", "").lower() in {"1", "true", "yes"}


def delete_vector_store(vector_store_id):
    if should_keep_vector_store():
        print(f"Keeping vector store {vector_store_id} because FOUNDRY_KEEP_VECTOR_STORE is set.")
        return

    try:
        client.vector_stores.delete(vector_store_id)
        print(f"Deleted vector store {vector_store_id}.")
    except Exception as error:
        print(f"Could not delete vector store {vector_store_id}: {error}")


def main():
    vector_store = create_vector_store_with_brochures()
    previous_response_id = None

    try:
        for prompt in PROMPTS:
            print("\nUser")
            print(prompt)

            response = create_travel_response(
                prompt,
                vector_store.id,
                previous_response_id,
            )
            previous_response_id = response.id

            print("\nAssistant")
            print(response.output_text)
            print_tool_activity(response)
    finally:
        delete_vector_store(vector_store.id)


if __name__ == "__main__":
    main()