# Microsoft Foundry: Responses API Notes

## 1. Core decision: endpoint + SDK

*   Microsoft Foundry projects expose **two main endpoints**:
    *   **Project endpoint**
        *   Used with the **Foundry SDK**
        *   Best when you need Foundry project features
    *   **Azure OpenAI endpoint**
        *   Used with the **OpenAI SDK**
        *   Best for model inference using OpenAI-compatible APIs

```text
Project endpoint:
https://{resource-name}.services.ai.azure.com/api/projects/<project-name>

Azure OpenAI endpoint:
https://{resource-name}.openai.azure.com/openai/v1
```

## 2. Use the Foundry SDK when you need project-level capabilities

*   Use **Foundry SDK + AIProjectClient** when your app needs Foundry-specific features such as:
    *   Agents
    *   Evaluations
    *   Tracing / observability
    *   Project connections
    *   Datasets and indexes
    *   Foundry governance / project metadata

```bash
pip install azure-ai-projects azure-identity openai
```

```python
from azure.identity import AzureCliCredential
from azure.ai.projects import AIProjectClient

project_client = AIProjectClient(
    credential=AzureCliCredential(),
    endpoint="https://{resource-name}.services.ai.azure.com/api/projects/<project-name>"
)

openai_client = project_client.get_openai_client(api_version="2024-10-21")
```

> Foundry SDK is not just for calling models. It gives access to **Foundry-native project capabilities**.

## 3. Use the OpenAI SDK for straightforward model inference

*   Use the **OpenAI SDK** when you want:
    *   Maximum OpenAI API compatibility
    *   Portability between OpenAI and Azure OpenAI
    *   Minimal dependency on Foundry-specific concepts
    *   Responses, Chat Completions, and Images APIs

```bash
pip install openai azure-identity
```

```python
from openai import OpenAI
from azure.identity import AzureCliCredential, get_bearer_token_provider

token_provider = get_bearer_token_provider(
    AzureCliCredential(),
    "https://ai.azure.com/.default"
)

openai_client = OpenAI(
    base_url="https://{resource-name}.openai.azure.com/openai/v1/",
    api_key=token_provider,
)
```

> OpenAI SDK is ideal when your app mainly needs to **send prompts to models and receive outputs**.

## 4. Authentication: prefer Microsoft Entra ID

*   For production apps, prefer **Microsoft Entra ID authentication**.
*   API keys can work, but should be handled carefully.
*   Never hard-code keys in source code.

```python
import os
from openai import OpenAI

openai_client = OpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    base_url="https://{resource-name}.openai.azure.com/openai/v1/"
)
```

> API keys are simpler but riskier. Use managed identity / Entra ID where possible.

## 5. Optional: AzureOpenAI client for version-specific Azure OpenAI APIs

*   Usually use `OpenAI` with the Azure OpenAI v1 endpoint.
*   Use `AzureOpenAI` only when you need a specific Azure OpenAI API version.

```python
import os
from openai import AzureOpenAI

openai_client = AzureOpenAI(
    azure_endpoint="https://{resource-name}.openai.azure.com",
    api_key=os.getenv("AZURE_OPENAI_KEY"),
    api_version="2024-10-21",
)
```

## 6. Recommended API: Responses API

*   The **Responses API** is recommended for most new Foundry apps.
*   It combines patterns from older **Chat Completions** and **Assistants** APIs.
*   It supports:
    *   Stateful conversations
    *   Multi-turn interactions
    *   Foundry direct models
    *   OpenAI-compatible clients

```python
response = openai_client.responses.create(
    model="gpt-4.1",
    input="What is Microsoft Foundry?"
)

print(response.output_text)
```

> Prefer `responses.create()` for new development unless you specifically need Chat Completions compatibility.

## 7. Response object fields worth knowing

*   Useful response properties:
    *   `output_text` — generated answer
    *   `id` — response ID, useful for conversation chaining
    *   `status` — completion status
    *   `usage` — token usage
    *   `model` — model used

```python
response = openai_client.responses.create(
    model="gpt-4.1",
    input="Explain machine learning in simple terms."
)

print(response.output_text)
print(response.id)
print(response.usage.total_tokens)
print(response.status)
```

## 8. Use instructions to control behavior

*   `instructions` act like a system prompt.
*   Use them to define tone, role, and behavior.

```python
response = openai_client.responses.create(
    model="gpt-4.1",
    instructions="You are a helpful assistant that answers clearly and concisely.",
    input="Explain neural networks."
)

print(response.output_text)
```

## 9. Control output with generation parameters

*   Key parameters to remember:
    *   `temperature` — controls randomness / creativity
    *   `max_output_tokens` — limits response length
    *   `top_p` — alternative randomness control

```python
response = openai_client.responses.create(
    model="gpt-4.1",
    instructions="Answer clearly and concisely.",
    input="Write a creative story about AI.",
    temperature=0.8,
    max_output_tokens=200
)

print(response.output_text)
```

## 10. Conversations: easiest approach is `previous_response_id`

*   Use `previous_response_id` to continue a conversation without manually rebuilding full history.

```python
response1 = openai_client.responses.create(
    model="gpt-4.1",
    instructions="Explain technology concepts clearly.",
    input="What is machine learning?"
)

response2 = openai_client.responses.create(
    model="gpt-4.1",
    instructions="Explain technology concepts clearly.",
    input="Can you give me an example?",
    previous_response_id=response1.id
)

print(response2.output_text)
```

> `previous_response_id` links turns together and keeps context.

## 11. Manual conversation history gives more control

*   Use manual history when you need to:
    *   Control exactly what context is sent
    *   Prune old messages
    *   Store and restore history from a database
    *   Manage token usage carefully

```python
conversation_history = [
    {
        "type": "message",
        "role": "user",
        "content": "What is machine learning?"
    }
]

response1 = openai_client.responses.create(
    model="gpt-4.1",
    input=conversation_history
)

conversation_history += response1.output

conversation_history.append({
    "type": "message",
    "role": "user",
    "content": "Can you give me an example?"
})

response2 = openai_client.responses.create(
    model="gpt-4.1",
    input=conversation_history
)

print(response2.output_text)
```

## 12. Token usage matters in conversations

*   Conversation context can include:
    *   Instructions
    *   Current prompt
    *   Previous messages
    *   Tool schemas
    *   Tool outputs
    *   Retrieved documents or memory

> Important idea to retain: stateful conversation support improves usability, but it can increase token usage because more context may be sent with each request.

## 13. Streaming improves app responsiveness

*   Use streaming when responses may take longer.
*   It lets users see partial output as it is generated.

```python
stream = openai_client.responses.create(
    model="gpt-4.1",
    input="Write a short story about a robot learning to paint.",
    stream=True
)

for event in stream:
    if event.type == "response.output_text.delta":
        print(event.delta, end="")
    elif event.type == "response.completed":
        response_id = event.response.id
```

> Important idea to retain: streaming does not necessarily make the model faster, but it makes the app feel more responsive.

## 14. Async clients help with non-blocking apps

*   Use async for high-performance apps or concurrent requests.
*   Import `AsyncOpenAI` instead of `OpenAI`.

```python
import asyncio
from openai import AsyncOpenAI

client = AsyncOpenAI(
    base_url="https://{resource-name}.openai.azure.com/openai/v1/",
    api_key=token_provider,
)

async def main():
    response = await client.responses.create(
        model="gpt-4.1",
        input="Explain quantum computing briefly."
    )
    print(response.output_text)

asyncio.run(main())
```

## 15. Simple decision guide

*   Choose **Foundry SDK** if your app needs:
    *   Agents
    *   Evaluations
    *   Tracing
    *   Project connections
    *   Foundry-specific governance or metadata

*   Choose **OpenAI SDK** if your app needs:
    *   Simple model inference
    *   OpenAI compatibility
    *   Portable code
    *   Responses / Chat Completions / Images APIs

*   Use **Responses API** for most new apps.

*   Use **Chat Completions** mainly for compatibility with existing code or platforms.

## 16. Summary

*   **Foundry SDK** = project and platform capabilities.
*   **OpenAI SDK** = model inference compatibility.
*   **Responses API** = recommended way to generate model responses.
*   **`previous_response_id`** = easiest way to build stateful chat.
*   **Streaming + async** = better user experience for production chat apps.
