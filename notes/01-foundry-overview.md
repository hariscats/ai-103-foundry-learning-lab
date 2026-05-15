# Microsoft Foundry Overview

## 1. Core

- **Microsoft Foundry** is an Azure-based platform for building AI apps and agent solutions.
- It organizes AI development around:
  - **Foundry resources**
  - **Foundry projects**
  - **Models**
  - **Agents**
  - **Tools**
  - **Knowledge sources**
  - **Endpoints**
  - **SDKs**

---

## 2. Foundry Resource vs. Project

### Foundry Resource

- Azure-backed resource that provides unified access to **models, agents, and tools**. 
- Provides underlying cloud capabilities such as:
  - Compute
  - Storage
  - AI tools
  - Connected services

### Foundry Project

- Solution workspace used to manage:
  - Resource connections
  - Data
  - Code
  - Models
  - Agents
  - Tools
  - Knowledge sources 

### Relationship

- Each project belongs to one Foundry resource. 
- One Foundry resource can support multiple child projects. 
- One child project can be designated as the default project. 
 
> **Foundry resource = Azure container**  
> **Foundry project = AI solution workspace**

---

## 3. Core Foundry Assets

### Models

- Models are LLM deployments available through Foundry Models. 
- Foundry Models includes models from Microsoft OpenAI and other providers. 

### Agents

- Agents are named AI configurations that encapsulate:
  - LLM
  - Instructions
  - Tools 
- Agents are built and consumed through the **Microsoft Foundry Agent service** using the project endpoint. 
  
> **Agent = LLM + instructions + tools**

### Tools

- Tools extend what agents can do.
- Tool examples include:
  - Web search
  - Code interpreter
  - MCP-connected custom or third-party tools
  - Foundry Tools for text analysis, speech, translation, and content understanding 

### Knowledge

- Knowledge sources provide grounding data for prompts.
- Agents can use tools to connect to knowledge stores. 
- Foundry IQ can centralize multiple knowledge sources through an MCP-based knowledge connection. 

### MCP

- **Model Context Protocol**, or **MCP**, connects agents to tools and knowledge sources. 
 
> **MCP = connector layer for tools and knowledge**

---

## 4. Foundry Portal vs. Foundry SDK

| Area | Foundry Portal | Foundry SDK |
|---|---|---|
| Interface | Web-based visual interface | Programmatic interface |
| Best for | Exploration, configuration, testing | Automation, scripting, CI/CD |
| Primary users | Developers, AI engineers, solution builders | Developers, DevOps engineers |
| Common tasks | Deploy/test models, create/test agents, configure connections | Automate project operations and manage assets in code |

---

## 5. Foundry Portal — When to Use

Use the **Foundry Portal** when you need to:

- Find and compare models
- Deploy and test models
- Create and test agents
- Create MCP connections to tools
- Create MCP connections to Foundry IQ knowledge sources
- Explore and test Foundry Tools
- Manage resource configuration
- Manage user access
- Find endpoints and keys for client applications 

---

## 6. Foundry SDK — When to Use

Use the **Foundry SDK** when you need to:

- Build apps with agents
- Use evaluations
- Use Foundry-specific features
- Automate Foundry project operations
- Integrate Foundry into scripts or CI/CD pipelines 

Microsoft Learn describes the Foundry SDK as supporting **Foundry-specific capabilities with OpenAI-compatible interfaces**. 

> **SDK = automate, integrate, repeat**

---

## 7. Model Access Patterns

Microsoft Foundry supports two main model access patterns:

1. **Project endpoint**
2. **Azure OpenAI / OpenAI-compatible endpoint**

---

## 8. Project Endpoint

### What It Is

- The project endpoint is used by the Foundry SDK.
- It is formatted like:

```text
https://<resource-name>.services.ai.azure.com/api/projects/<project-name>
```

### Use It For

*   Foundry-native capabilities
*   Agents
*   Evaluations
*   Project connections
*   Project properties
*   Tracing
*   Foundry direct models through the Responses API

Microsoft Learn states that the SDK exposes a **project client** for Foundry-native operations where OpenAI has no equivalent.

> **Project endpoint = Foundry-native AI app and agent capabilities**

***

## 9. Azure OpenAI / OpenAI-Compatible Endpoint

### What It Is

*   The OpenAI-compatible endpoint is used with OpenAI APIs and SDKs.
*   It is intended for maximum OpenAI compatibility and access to the full OpenAI API surface.

### Use It For

*   Standard model inference
*   OpenAI SDK-based applications
*   Chat Completions-based access patterns
*   Applications that prioritize portability and familiar OpenAI-style APIs
 
> **OpenAI endpoint = standard model calling pattern**

***

## 10. Why Are There Two Model Access Patterns?

### Short Answer

Because Foundry supports both:

*   **Standard model access**
*   **Foundry-native application and agent capabilities**

### OpenAI-Compatible Endpoint

Best when the app needs:

*   Standard OpenAI-style APIs
*   Maximum OpenAI compatibility
*   Familiar SDK patterns
*   Basic model inference

### Project Endpoint

Best when the app needs:

*   Agents
*   Evaluations
*   Project-scoped assets
*   Foundry-specific operations
*   Tool and knowledge integration
*   Capabilities that do not map cleanly to standard OpenAI APIs

> **Key idea:**  
> OpenAI-compatible APIs are strong for inference, but Foundry is broader than inference.

***

## 11. Why Not Standardize Only on OpenAI-Compatible APIs?

### Reason

OpenAI-compatible APIs are useful for calling models, but they do not represent every Foundry capability.

Foundry also includes project-level capabilities such as:

*   Agents
*   Evaluations
*   Project connections
*   Project properties
*   Tracing
*   Foundry-native operations where OpenAI has no equivalent

### Practical Distinction

*   **OpenAI API = call the model**
*   **Project endpoint = manage and run the AI solution**

> **Exam framing:**  
> If the scenario only needs model inference, OpenAI-compatible access may be enough.  
> If the scenario needs agents, tools, evaluations, or project-scoped resources, use the project endpoint.

***

## 12. Does the Project Endpoint Lock In the Customer?

### Balanced Answer

Not necessarily for basic model inference.

A Foundry resource provides multiple endpoints, including the project endpoint and the `/openai/v1` endpoint. An Azure OpenAI resource provides only the `/openai/v1` endpoint.

### What the Project Endpoint Does

Using the project endpoint creates a dependency on Foundry-specific capabilities, such as:

*   Agents
*   Evaluations
*   Project assets
*   Project connections
*   Foundry-native management operations

### How to Think About It

*   If the application only needs standard model calls:
    *   Use the OpenAI-compatible endpoint for greater portability.

*   If the application needs Foundry-native capabilities:
    *   Use the project endpoint.
  
> **OpenAI endpoint reduces coupling.**  
> **Project endpoint unlocks Foundry capabilities.**

***

## 13. Exam-Ready Decision Rules

### Choose Foundry Portal When You See

*   Visual interface
*   Explore models
*   Compare models
*   Test prompts
*   Create agents manually
*   Configure MCP connections
*   Manage access
*   Find keys and endpoints

***

### Choose Foundry SDK When You See

*   Automation
*   Scripts
*   CI/CD
*   Programmatic asset management
*   Repeatable deployment
*   DevOps pipeline integration

***

### Choose Project Endpoint When You See

*   Agents
*   Evaluations
*   Foundry-specific features
*   Project connections
*   Project-scoped resources
*   Foundry-native operations

***

### Choose OpenAI-Compatible Endpoint When You See

*   Maximum OpenAI compatibility
*   OpenAI SDK
*   Standard model calls
*   Chat Completions
*   Portability
*   Existing OpenAI-style app

**Answer:** Azure OpenAI / OpenAI-compatible endpoint

***

## 14. One-Minute Summary

*   **Foundry resource** = Azure AI container.
*   **Foundry project** = AI solution workspace.
*   **Model** = deployed LLM.
*   **Agent** = LLM + instructions + tools.
*   **Tool** = external or built-in capability.
*   **Knowledge** = grounding data.
*   **MCP** = connector layer for tools and knowledge.
*   **Portal** = visual build, test, configure, manage.
*   **SDK** = automate, integrate, repeat.
*   **Project endpoint** = Foundry-native capabilities.
*   **OpenAI endpoint** = standard model inference.

