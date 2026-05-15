# Responses API flow

```mermaid
sequenceDiagram
    autonumber
    actor User
    participant App as Python lab script
    participant Identity as Microsoft Entra ID
    participant API as Foundry /openai/v1 endpoint
    participant Model as gpt-4.1 deployment

    User->>App: Run responses_features_demo.py
    App->>Identity: DefaultAzureCredential requests token
    Identity-->>App: Access token

    App->>API: responses.create(input, instructions)
    API->>Model: Generate response
    Model-->>API: Output text + metadata
    API-->>App: response.id, output_text, status, usage
    App-->>User: Print answer and usage

    App->>API: responses.create(previous_response_id=response.id, input)
    API->>Model: Continue conversation state
    Model-->>API: Follow-up response
    API-->>App: New response.id + usage
    App-->>User: Print stateful follow-up

    App->>App: Build manual conversation_history
    App->>API: responses.create(input=conversation_history)
    API->>Model: Generate with explicit history
    Model-->>API: Response output
    API-->>App: response.output
    App->>App: Append response.output to conversation_history

    App->>API: responses.create(stream=True)
    API->>Model: Generate streamed response
    loop Streaming events
        API-->>App: response.output_text.delta
        App-->>User: Print token delta
    end
    API-->>App: response.completed with response.id
    App-->>User: Print streamed_response_id
```

Key idea: `previous_response_id` lets the service carry conversation state, while manual history gives the app explicit control over what context is sent. Streaming returns text incrementally and still produces a final response ID when the response completes.
