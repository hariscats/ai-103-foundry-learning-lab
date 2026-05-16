import json
import os

from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from openai import OpenAI

endpoint = os.environ["FOUNDRY_OPENAI_ENDPOINT"]
deployment_name = os.environ["FOUNDRY_MODEL_NAME"]

# Entra token provider replaces an API key.
token_provider = get_bearer_token_provider(
    DefaultAzureCredential(),
    "https://cognitiveservices.azure.com/.default",
)

# The OpenAI-compatible endpoint should end with /openai/v1.
client = OpenAI(
    base_url=endpoint,
    api_key=token_provider,
)

SYSTEM_INSTRUCTIONS = """
You are a concise Azure AI study coach.
Answer directly, then mention one Responses API concept when useful.
""".strip()


def print_response_metadata(response):
    """Print the small shape worth learning from each response."""
    usage = response.usage.model_dump() if getattr(response, "usage", None) else {}
    print(
        json.dumps(
            {
                "id": response.id,
                "status": response.status,
                "model": response.model,
                "usage": usage,
            },
            indent=2,
            default=str,
        )
    )


def create_chat_response(user_text, previous_response_id):
    request = {
        "model": deployment_name,
        "instructions": SYSTEM_INSTRUCTIONS,
        "input": user_text,
        "temperature": 0.3,
        "top_p": 0.9,
        "max_output_tokens": 350,
        "stream": True,
    }

    # previous_response_id lets the service carry the chat state.
    if previous_response_id:
        request["previous_response_id"] = previous_response_id

    return client.responses.create(**request)


def print_streamed_response(stream):
    final_response = None

    # Deltas are the assistant text as it is generated.
    for event in stream:
        if event.type == "response.output_text.delta":
            print(event.delta, end="", flush=True)
        elif event.type == "response.completed":
            final_response = event.response

    print()
    return final_response


def main():
    previous_response_id = None

    print("Responses API chat lab")
    print("Ask about Azure AI. Commands: /new resets state, /exit quits.")

    while True:
        user_text = input("\nYou: ").strip()

        if not user_text:
            continue
        if user_text.lower() in {"/exit", "exit", "quit"}:
            break
        if user_text.lower() == "/new":
            previous_response_id = None
            print("State reset. The next turn starts a new response chain.")
            continue

        print("\nAssistant: ", end="", flush=True)
        stream = create_chat_response(user_text, previous_response_id)
        response = print_streamed_response(stream)

        if response is None:
            print("No completed response event was returned.")
            continue

        # Save this ID for the next turn.
        previous_response_id = response.id

        print("\nResponse metadata")
        print_response_metadata(response)


if __name__ == "__main__":
    main()