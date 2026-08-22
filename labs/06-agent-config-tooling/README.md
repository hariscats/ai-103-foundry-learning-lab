# Agent configuration and tooling lab.

Configure a declarative (prompt) agent from a YAML file, attach built-in tools, test it, and clean up. Covers the key concepts from [notes/06-agent-config-tooling.md](../../notes/06-agent-config-tooling.md).

The demo:

1. Loads agent configuration (name, model, instructions, tools) from [config/it_support_agent.yaml](config/it_support_agent.yaml).
2. Provisions grounding data: a vector store for `file_search` (IT policy) and an uploaded CSV for `code_interpreter` (system performance).
3. Creates a new agent version with `PromptAgentDefinition` (core agent properties + tools).
4. Runs a scripted multi-turn conversation and reports which tool fired on each turn.
5. Saves any generated charts to `agent_outputs/` and deletes all demo resources.

## Concept coverage

| Notes concept | Where in the demo |
|---|---|
| Core agent properties (name, model, description, instructions) | `configure_agent` + the YAML config |
| YAML configuration | [config/it_support_agent.yaml](config/it_support_agent.yaml) loaded by `load_agent_config` |
| Built-in tools (file_search, code_interpreter) | `build_tools` |
| Tool execution / validation | `summarize_tool_activity` reports tool calls per turn |
| Testing (multi-turn, tool invocation) | `TEST_PLAN` + `run_test_plan` |
| Agent endpoint / integration (Responses API) | `responses.create(..., extra_body={"agent_reference": ...})` |
| Production: cost control + cleanup | resource cleanup and env-driven config |

## Prerequisites

Set the project endpoint and model deployment name in the repository `.env` file (see the repo README):

```dotenv
FOUNDRY_PROJECT_ENDPOINT=https://<resource-name>.services.ai.azure.com/api/projects/<project-name>
FOUNDRY_MODEL_NAME=gpt-4.1
```

## Run

```powershell
python .\labs\06-agent-config-tooling\src\agent_config_tooling_demo.py
```

By default the agent, conversation, vector store, and uploaded files are deleted at the end. To keep the agent so you can open it under **Prompt Agents** in the Foundry Toolkit for VS Code, set this in `.env`:

```dotenv
FOUNDRY_KEEP_AGENT=1
```
