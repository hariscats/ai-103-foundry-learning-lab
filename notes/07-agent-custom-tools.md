# Conversation History & Custom Tools in Azure AI Foundry

## Core Principle
Tools are **stateless**. The agent runtime owns conversation history — tools never see it.

## Key Takeaways

**1. Tool selection runs on descriptions alone**
The LLM picks tools based only on `description`, `parameters`, and `instructions`. Write these precisely.

**2. Tool calls become conversation turns**
Request + response are injected into the thread, so past tool results are visible to the model in later turns.

**3. System instructions persist across all turns**
The `instructions` field is prepended to every context window — turn 1 and turn 50 see the same prompt.

**4. Async queues pause the conversation**
Queue-based tools (Example 1) hold thread state while waiting for a response — poor fit for rapid multi-turn exchanges.

**5. No automatic context truncation**
Long threads hit the model's context window limit silently. You must manage this yourself.

**6. No cross-session memory**
`create_version` defines an agent, not a session. History does not persist between separate conversations.

## Design Rules of Thumb
- Tool `description` = the model's only signal for *when* to call it. Be explicit.
- Put tool usage guidance in `instructions`, not just the tool definition.
- Prefer OpenAPI (sync) over queue-based (async) tools for conversational, multi-turn workflows.
