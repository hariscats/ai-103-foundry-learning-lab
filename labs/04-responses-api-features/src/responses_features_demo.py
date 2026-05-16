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


def print_response(label, response):
    usage = response.usage.model_dump() if getattr(response, "usage", None) else {}

    print(f"\n{label}")
    print(response.output_text)
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


instruction_response = client.responses.create(
    model=deployment_name,
    instructions="You explain AI concepts clearly and concisely.",
    input="Explain the Responses API in one sentence.",
    temperature=0.2,
    max_output_tokens=80,
)
print_response("INSTRUCTIONS + BASIC RESPONSE", instruction_response)

sampling_response = client.responses.create(
    model=deployment_name,
    instructions="Return exactly three short bullets.",
    input="Suggest creative ways a student could practice Azure AI model evaluation.",
    temperature=0.8,
    top_p=0.9,
    max_output_tokens=120,
)
print_response("SAMPLING + TOKEN LIMIT", sampling_response)

follow_up_response = client.responses.create(
    model=deployment_name,
    previous_response_id=instruction_response.id,
    input="Now summarize the main benefit in six words or fewer.",
    temperature=0.2,
    max_output_tokens=30,
)
print_response("STATEFUL FOLLOW-UP", follow_up_response)

conversation_history = [
    {"role": "user", "content": "Define prompt caching in one sentence."},
]

manual_response_1 = client.responses.create(
    model=deployment_name,
    input=conversation_history,
    temperature=0.2,
    max_output_tokens=80,
)
print_response("MANUAL HISTORY FIRST TURN", manual_response_1)

conversation_history += manual_response_1.output
conversation_history.append(
    {"role": "user", "content": "Why can that matter for cost and latency?"},
)

manual_response_2 = client.responses.create(
    model=deployment_name,
    input=conversation_history,
    temperature=0.2,
    max_output_tokens=100,
)
print_response("MANUAL HISTORY SECOND TURN", manual_response_2)

print("\nSTREAMING RESPONSE")
streamed_response_id = None
stream = client.responses.create(
    model=deployment_name,
    input="Write one short sentence about why streaming improves chat UX.",
    temperature=0.2,
    max_output_tokens=60,
    stream=True,
)

for event in stream:
    if event.type == "response.output_text.delta":
        print(event.delta, end="", flush=True)
    elif event.type == "response.completed":
        streamed_response_id = event.response.id

print(f"\nstreamed_response_id: {streamed_response_id}")