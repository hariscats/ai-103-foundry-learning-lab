"""Lab 06 - Agent configuration and tooling.

Configure a declarative (prompt) agent from a YAML file, attach built-in tools
(file_search + code_interpreter), test it across a multi-turn conversation, then
clean up. Mirrors the concepts in notes/06-agent-config-tooling.md.
"""

import os
from pathlib import Path

import yaml
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import (
    AutoCodeInterpreterToolParam,
    CodeInterpreterTool,
    FileSearchTool,
    PromptAgentDefinition,
)
from azure.identity import AzureCliCredential
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parents[3] / ".env")

LAB_ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = LAB_ROOT / "config" / "it_support_agent.yaml"
DATA_DIR = LAB_ROOT / "data"
OUTPUT_DIR = LAB_ROOT / "agent_outputs"

# A small test plan. Each turn targets one configured capability so we can
# confirm both the answer (behavior) and that the expected tool was invoked.
TEST_PLAN = [
    {
        "capability": "file_search",
        "prompt": "What's the policy for password resets?",
    },
    {
        "capability": "code_interpreter",
        "prompt": (
            "Analyze the system performance data and identify any periods "
            "where CPU usage exceeded 80%."
        ),
    },
    {
        "capability": "code_interpreter",
        "prompt": "Create a line chart showing memory usage trends over time from the performance data.",
    },
]


def expand_env(value):
    """Expand a ${VAR} placeholder from the environment, otherwise return as-is."""
    if isinstance(value, str) and value.startswith("${") and value.endswith("}"):
        var_name = value[2:-1]
        resolved = os.environ.get(var_name)
        if not resolved:
            raise RuntimeError(
                f"Config references ${{{var_name}}}, but that environment variable is not set."
            )
        return resolved
    return value


def load_agent_config():
    """Load the declarative agent configuration from YAML."""
    with CONFIG_PATH.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def build_tools(config, openai_client, created):
    """Translate the YAML 'tools' section into SDK tools and provision grounding data."""
    tools = []

    for tool_config in config.get("tools", []):
        tool_type = tool_config.get("type")

        if tool_type == "file_search":
            vector_store = openai_client.vector_stores.create(name=f"{config['name']}-knowledge")
            created["vector_store_ids"].append(vector_store.id)

            for file_name in tool_config.get("file_search", {}).get("files", []):
                with (DATA_DIR / file_name).open("rb") as handle:
                    openai_client.vector_stores.files.upload_and_poll(
                        vector_store_id=vector_store.id, file=handle
                    )
                print(f"  file_search: indexed {file_name} (vector store {vector_store.id})")

            tools.append(FileSearchTool(vector_store_ids=[vector_store.id]))

        elif tool_type == "code_interpreter":
            file_ids = []
            for file_name in tool_config.get("code_interpreter", {}).get("files", []):
                with (DATA_DIR / file_name).open("rb") as handle:
                    uploaded = openai_client.files.create(purpose="assistants", file=handle)
                created["file_ids"].append(uploaded.id)
                file_ids.append(uploaded.id)
                print(f"  code_interpreter: uploaded {file_name} (id: {uploaded.id})")

            if file_ids:
                tools.append(
                    CodeInterpreterTool(container=AutoCodeInterpreterToolParam(file_ids=file_ids))
                )
            else:
                tools.append(CodeInterpreterTool())

        else:
            print(f"  Skipping unsupported tool type: {tool_type}")

    return tools


def configure_agent(project_client, config, tools):
    """Create a new version of the prompt agent from the configuration.

    Maps the YAML config onto the core agent properties: name, model,
    description, instructions, and tools.
    """
    definition_kwargs = {
        "model": expand_env(config["model"]["id"]),
        "instructions": config["instructions"],
        "tools": tools,
    }

    return project_client.agents.create_version(
        agent_name=config["name"],
        definition=PromptAgentDefinition(**definition_kwargs),
        description=config.get("description"),
    )


def get_output_path(filename):
    """Return a unique path under the output directory for a generated file."""
    OUTPUT_DIR.mkdir(exist_ok=True)
    name = Path(filename).name
    output_path = OUTPUT_DIR / name

    counter = 1
    while output_path.exists():
        output_path = OUTPUT_DIR / f"{Path(name).stem}_{counter}{Path(name).suffix}"
        counter += 1

    return output_path


def summarize_tool_activity(response):
    """List the tool-call items the service returned for this turn."""
    return [
        getattr(item, "type", "")
        for item in response.output
        if getattr(item, "type", "").endswith("_call")
    ]


def download_generated_files(response, openai_client):
    """Save any container files the agent cited (for example, generated charts)."""
    saved = []
    seen = set()

    for item in response.output:
        if getattr(item, "type", "") != "message":
            continue

        for content_item in getattr(item, "content", []) or []:
            for annotation in getattr(content_item, "annotations", []) or []:
                if getattr(annotation, "type", "") != "container_file_citation":
                    continue

                key = (annotation.container_id, annotation.file_id)
                if key in seen:
                    continue
                seen.add(key)

                file_content = openai_client.containers.files.content.retrieve(
                    file_id=annotation.file_id,
                    container_id=annotation.container_id,
                )
                output_path = get_output_path(annotation.filename or f"{annotation.file_id}.bin")
                with output_path.open("wb") as handle:
                    handle.write(file_content.read())
                saved.append(output_path)

    return saved


def run_test_plan(openai_client, agent):
    """Run the scripted multi-turn conversation against the configured agent."""
    conversation = openai_client.conversations.create()
    print(f"\nConversation created (id: {conversation.id})")

    # The agent endpoint speaks the Responses API protocol; the published agent
    # is targeted by name through agent_reference.
    agent_reference = {"agent_reference": {"name": agent.name, "type": "agent_reference"}}

    for index, turn in enumerate(TEST_PLAN, start=1):
        print("\n" + "=" * 70)
        print(f"Test {index} - expecting {turn['capability']}")
        print(f"You: {turn['prompt']}")
        print("=" * 70)

        response = openai_client.responses.create(
            conversation=conversation.id,
            input=turn["prompt"],
            extra_body=agent_reference,
        )

        activity = summarize_tool_activity(response)
        print(f"Tools invoked: {', '.join(activity) if activity else 'none'}")

        if response.output_text:
            print(f"\nAgent: {response.output_text}")

        for path in download_generated_files(response, openai_client):
            print(f"[saved generated file: {path}]")

    return conversation.id


def cleanup(project_client, openai_client, agent, conversation_id, created):
    """Delete the conversation, agent version, and grounding resources."""
    print("\nCleaning up demo resources...")

    if conversation_id:
        try:
            openai_client.conversations.delete(conversation_id=conversation_id)
        except Exception as error:
            print(f"  Could not delete conversation: {error}")

    try:
        project_client.agents.delete_version(agent_name=agent.name, agent_version=agent.version)
        print(f"  Deleted agent version {agent.version}")
    except Exception as error:
        print(f"  Could not delete agent: {error}")

    for vector_store_id in created["vector_store_ids"]:
        try:
            openai_client.vector_stores.delete(vector_store_id)
        except Exception as error:
            print(f"  Could not delete vector store {vector_store_id}: {error}")

    for file_id in created["file_ids"]:
        try:
            openai_client.files.delete(file_id)
        except Exception as error:
            print(f"  Could not delete file {file_id}: {error}")

    print("Cleanup complete.")


def main():
    project_endpoint = os.environ.get("FOUNDRY_PROJECT_ENDPOINT")
    if not project_endpoint:
        print("Add FOUNDRY_PROJECT_ENDPOINT and FOUNDRY_MODEL_NAME to the repository .env file.")
        return
    if not os.environ.get("FOUNDRY_MODEL_NAME"):
        print("Add FOUNDRY_MODEL_NAME to the repository .env file.")
        return

    config = load_agent_config()
    keep_resources = os.getenv("FOUNDRY_KEEP_AGENT", "").lower() in {"1", "true", "yes"}
    created = {"vector_store_ids": [], "file_ids": []}

    with (
        AzureCliCredential() as credential,
        AIProjectClient(endpoint=project_endpoint, credential=credential) as project_client,
        project_client.get_openai_client() as openai_client,
    ):
        print(f"Configuring agent '{config['name']}' from {CONFIG_PATH.relative_to(LAB_ROOT)}")
        tools = build_tools(config, openai_client, created)
        agent = configure_agent(project_client, config, tools)

        print("\nAgent configured")
        print(f"  name:    {agent.name}")
        print(f"  id:      {agent.id}")
        print(f"  version: {agent.version}")
        print(f"  model:   {expand_env(config['model']['id'])}")
        print(f"  tools:   {[tool.get('type') for tool in config.get('tools', [])]}")

        conversation_id = None
        try:
            conversation_id = run_test_plan(openai_client, agent)
        finally:
            if keep_resources:
                print("\nFOUNDRY_KEEP_AGENT is set - leaving the agent and grounding data in place.")
                print(f"Open '{agent.name}' under Prompt Agents in the Foundry Toolkit to keep testing.")
            else:
                cleanup(project_client, openai_client, agent, conversation_id, created)


if __name__ == "__main__":
    main()
