from azure.identity import AzureCliCredential, get_bearer_token_provider
from dotenv import load_dotenv
from openai import OpenAI
import json
import os
from pathlib import Path
import time

load_dotenv(Path(__file__).resolve().parents[3] / ".env")

endpoint = os.environ["FOUNDRY_OPENAI_ENDPOINT"]
models = [os.environ["FOUNDRY_MODEL_NAME"], os.environ["FOUNDRY_COMPARISON_MODEL_NAME"]]

comparison_runs = [
    {
        "name": "focused",
        "prompt": "What is the capital of France?",
    },
    {
        "name": "concise",
        "prompt": "What is the capital of France? Answer in one short sentence with one landmark.",
    },
]

token_provider = get_bearer_token_provider(
    AzureCliCredential(),
    "https://cognitiveservices.azure.com/.default",
)

client = OpenAI(
    base_url=endpoint,
    api_key=token_provider,
)


def extract_text(response):
    if hasattr(response, "output_text") and response.output_text:
        return response.output_text

    parts = []
    for item in getattr(response, "output", []):
        for content in getattr(item, "content", []):
            text = getattr(content, "text", None)
            if text:
                parts.append(text)
    return "\n".join(parts)


results = []
for run in comparison_runs:
    for model in models:
        started = time.perf_counter()
        response = client.responses.create(
            model=model,
            input=run["prompt"],
        )
        elapsed_seconds = time.perf_counter() - started
        usage = response.usage.model_dump() if getattr(response, "usage", None) else {}

        results.append(
            {
                "run": run["name"],
                "model": model,
                "elapsed_seconds": round(elapsed_seconds, 3),
                "input_tokens": usage.get("input_tokens"),
                "output_tokens": usage.get("output_tokens"),
                "total_tokens": usage.get("total_tokens"),
                "text": extract_text(response),
            }
        )

print(json.dumps(results, indent=2, default=str))
