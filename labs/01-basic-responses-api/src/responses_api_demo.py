from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from openai import OpenAI
import json
import os

endpoint = os.environ["FOUNDRY_OPENAI_ENDPOINT"]
deployment_name = os.environ["FOUNDRY_MODEL_NAME"]

token_provider = get_bearer_token_provider(
    DefaultAzureCredential(),
    "https://cognitiveservices.azure.com/.default",
)

client = OpenAI(
    base_url=endpoint,
    api_key=token_provider,
)

shared_context = (
    "Use the following reference facts exactly as written when answering: "
    "France is in Western Europe. Paris is the capital of France. "
    "The Seine river flows through Paris. The Louvre is a museum in Paris. "
    "The Eiffel Tower is in Paris. " * 4
)

response = client.responses.create(
    model=deployment_name,
    input=[
        {"role": "user", "content": shared_context},
        {"role": "user", "content": "What is the capital of France?"},
    ],
    temperature=0.2,
    top_p=0.9,
)

print(json.dumps(response.model_dump(), indent=2, default=str))