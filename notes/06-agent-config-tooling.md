# Agent Configuration and Tooling in Microsoft Foundry

***

## 1. Configuring Agents in VS Code

### Definition

* Configuration defines how an agent behaves, responds, and operates
* Managed via:
  * **Agent Designer (visual UI)**
  * **YAML configuration file**

***

### Scope

* Applies to **declarative (prompt-based) agents**
* Not applicable to:
  * Hosted agents (code-based configuration)
  * Workflow agents (different YAML schema)

***

### Key Concept

* Designer = ease of use
* YAML = precision and flexibility

***

## 2. Core Agent Properties

### Essential Configuration

* **Agent name**
  * Clear, descriptive identifier
  * Used across logs and team collaboration

* **Model selection**
  * Determines which deployed model powers the agent

* **Description**
  * Concise explanation of the agent’s purpose
  * Improves discoverability

* **System instructions**
  * Define:
    * Behavior
    * Tone
    * Responsibilities

* **Agent ID**
  * Auto-generated unique identifier
  * Used for API interactions

***

### Model Settings

* **Temperature**
  * Controls randomness
  * Low (0.1–0.3) → consistent outputs
  * High (0.7–1.0) → creative outputs
  * Typical: **0.3–0.7**

* **Top P**
  * Controls vocabulary diversity
  * Default: **1.0**
  * Lower values → more predictable output

***

**Key idea:** Configuration determines both *capability and behavior*

***

## 3. YAML Configuration

### Definition

* Structured file containing all agent settings

***

### Structure Overview

* **Metadata**
  * Authors, tags

* **Model configuration**

* **Instructions**

* **Tools**

***

### Example

```yaml
version: 1.0.0
name: research-assistant
description: Helps with research tasks
model:
  id: gpt-4o
  options:
    temperature: 0.5
instructions: |
  You're a research assistant helping users gather information.
tools: []
```

***

### Benefits

* Version control (Git)
* Bulk updates
* Reusable templates
* Code review integration
* Automation support

***

**Key idea:** YAML enables **repeatable and scalable agent design**

***

## 4. Configuration Best Practices

* Store YAML in **version control**
* Use clear **names and tags**
* Document complex instructions with comments
* Test after each change
* Start simple → iterate
* Keep agents **focused and single-purpose**

***

**Key idea:** Simplicity improves reliability

***

# Agent Tools in Microsoft Foundry

***

## 5. What Are Agent Tools?

### Definition

* Programmatic capabilities that allow agents to:
  * Perform actions
  * Retrieve data
  * Integrate with external systems

***

### Tool Execution Flow

1. User sends request
2. Agent evaluates intent
3. Agent selects tool(s)
4. Tool executes
5. Results returned
6. Agent generates response

***

**Key idea:** Tools enable **execution, not just responses**

***

## 6. Tool Categories

### Tool Catalog Types

* **Configured**
  * Built-in, ready-to-use tools

* **Catalog**
  * Additional tools (including MCP servers)

* **Custom**
  * Developer-defined integrations (e.g., OpenAPI)

***

## 7. Common Built-in Tools

### Code Interpreter

* Executes Python in a sandbox
* Use cases:
  * Data analysis
  * Calculations
  * File processing

***

### File Search

* Enables **Retrieval-Augmented Generation (RAG)**
* Uses:
  * Vector stores
  * Semantic search

***

### Bing Web Search

* Provides real-time internet data
* Includes citations

***

### Azure AI Search

* Connects to enterprise search indexes
* Supports structured and unstructured queries

***

### OpenAPI Tools

* Integrate external APIs
* Handles parameter mapping and response parsing

***

### Additional Tools

* Browser automation
* Desktop interaction
* Image generation
* SharePoint integration
* Microsoft Fabric
* Deep research
* Agent-to-agent interactions

***

**Key idea:** Built-in tools accelerate development with **ready-made capabilities**

***

## 8. Adding Tools in VS Code

### Using Agent Designer

1. Open the agent
2. Go to **Tools**
3. Select **Add Tool**
4. Choose tool from catalog
5. Configure settings
6. Save

***

### Using YAML

```yaml
tools:
  - type: code_interpreter
  - type: bing_grounding
    bing_grounding:
      connection_id: "your-connection-id"
  - type: file_search
    file_search:
      vector_store_ids:
        - "vectorstore-123"
```

***

**Key idea:** Tools are declarative and automatically invoked

***

## 9. MCP Servers (Model Context Protocol)

### Definition

* Standardized approach for extending agents with reusable tools

***

### Types

* **Remote** → hosted externally
* **Local** → development/testing
* **Custom** → organization-specific

***

### Benefits

* Standardized integration
* Reusable components
* Reduced complexity
* Access to shared/community tools

***

**Key idea:** MCP enables **plug-and-play extensibility**

***

## 10. Tool Best Practices

* Start with built-in tools
* Add tools with clear purpose only
* Provide explicit usage instructions
* Keep knowledge sources updated
* Test tool behavior thoroughly

***

**Key idea:** Tool design directly impacts performance and reliability

***

# Testing, Deployment, and Integration

***

## 11. Testing Agents

### Recommended Testing Types

* Happy path scenarios
* Edge cases
* Boundary testing
* Multi-turn conversations
* Tool invocation validation

***

**Key idea:** Validate both **behavior and tool usage**

***

## 12. Deployment vs Publishing

### Deployment

* Saves agent to Foundry project
* Enables internal testing

***

### Publishing

* Creates:
  * **Agent Application (Azure resource)**
  * **Stable API endpoint**

***

### Key Difference

* Deployment → internal
* Publishing → external access

***

## 13. Agent Endpoint

### Characteristics

* Uses **Responses API protocol**
* Provides stable URL across versions

***

### Authentication

* Microsoft Entra ID
* Requires:
  * Azure AI User role

***

### Important

* Published agents have a **separate identity**
* RBAC permissions must be reassigned

***

## 14. Integration Patterns

* Web applications
* Backend workflows
* Chat interfaces
* Scheduled automation

***

## 15. Production Considerations

* **Monitoring**
  * Response time, tool success, errors

* **Security**
  * Managed identities
  * Least-privilege access

* **Cost**
  * Token usage control
  * Rate limiting

* **Error handling**
  * Retries and backoff strategies

* **Conversation management**
  * Store history client-side (stateless API)

***

**Key idea:** Production requires **observability, security, and cost control**

***

# Summary

* Agents are configured using:
  * Properties
  * Instructions
  * Tools

* Tools transform agents into:
  * **Actionable systems**

* YAML enables:
  * Versioning
  * Automation
  * Precision

* Lifecycle:
  * Configure → Test → Deploy → Publish → Integrate

