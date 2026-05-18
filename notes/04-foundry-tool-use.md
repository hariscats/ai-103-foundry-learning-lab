# Microsoft Foundry — Tool Use

---

## 1. What Are Tools?
- **Definition**
  - Tools extend model capabilities beyond text generation
  - Allow models to **take actions** or **retrieve external data**

- **Purpose**
  - Execute tasks (code interpreter, API (function) calls, search, etc.)
  - Ground responses in:
    - Real-time data
    - External data sources
    - Private enterprise data

- **Key Concept**
  - Model = reasoning  
  - Tools = execution/action layer  

- **In Microsoft Foundry**
  - Tools are specified in prompts via the **Responses API**
  - Model decides:
    - When to use a tool
    - Which tool to use (default behavior)

**Key idea:** Tools transform models from *answer generators → task performers*

---

## 2. Tool Integration (Responses API)

- Tools are passed in API requests:
  ```python
  tools=[{ "type": "<tool_type>" }]
    ```

* **Important behaviors**
  * Multiple tools can be included in one request
  * Model autonomously selects tools
  * Tool usage can be influenced by:
    * Instructions (system prompt)
    * Tool selection rules

***

## 3. Tool Types

### 3.1 Built-in Tools

* Ready-to-use capabilities
* Managed by Microsoft Foundry
* No custom implementation required

### 3.2 Custom Tools

* Defined by developers
* Typically implemented via **function calling**

***

# Core Tools in Microsoft Foundry

***

## 4. `code_interpreter` Tool

### Definition

* Provides a **sandboxed Python runtime**
* Enables the model to **write, run, and debug code**

### Key Capabilities

* Dynamic Python execution
* File handling (CSV, JSON, images)
* Data analysis and transformations
* Mathematical computation
* Simulations and logic execution
* Iterative debugging based on execution results

### Flow

1. Model detects need for computation
2. Model generates Python code
3. Code executes in sandbox
4. Output returned to model
5. Model generates final response

### Use Cases

* Data analysis (e.g., CSV processing)
* Math and physics problems
* File conversion (JSON ↔ CSV)
* Algorithm prototyping

### Limitations

* No external network access
* Limited memory/runtime
* Some libraries may not be available

**Key idea:** Model can **execute code**, not just explain it

***

## 5. `web_search` Tool

### Definition

* Enables **real-time internet information retrieval**

### Key Capabilities

* Retrieves current data from web
* Automatically generates search queries
* Produces **source-grounded responses**

### Flow

1. Model evaluates query
2. Determines if fresh data is needed
3. Executes search queries
4. Reviews results
5. Generates answer

### Use Cases

* Current events
* Market research
* Policy/regulation updates
* Fact verification

### Benefits

* Reduces hallucinations
* Enables up-to-date answers

### Limitations

* Depends on publicly available content
* Source reliability may vary
* Results may change over time

**Key idea:** Adds **fresh, real-time knowledge**

***

## 6. `file_search` Tool

### Definition

* Enables model to search **user-uploaded documents**

### Key Capabilities

* Semantic search (vector-based retrieval)
* Retrieves relevant document passages
* Grounds responses in private knowledge

### Architecture

* Documents → vector store → embeddings
* Query → semantic search → matched content

### Flow

1. Upload files to a vector store
2. Include vector store ID in tool configuration
3. Model retrieves relevant document chunks
4. Model generates grounded response

### Use Cases

* Policy Q\&A (HR, finance, legal)
* Internal knowledge assistants
* Contract/document lookup
* Technical documentation queries

### Benefits

* High accuracy (organization-specific)
* Transparent grounding (retrieved passages)

### Limitations

* Dependent on document quality
* Requires re-indexing after updates
* Large/mixed datasets may reduce precision

**Key idea:** Enables **RAG (Retrieval-Augmented Generation)**

***

## 7. `function` Tool (Function Calling)

### Definition

* Allows model to call **developer-defined functions**

### Key Concept

* Model DOES NOT execute business logic
* Instead:
  * Requests a function call
  * Application executes it
  * Result returned to model

### Flow

1. Define functions in tools array
2. Model evaluates request
3. Model emits function call
4. Application executes function
5. Return function output
6. Model generates final response

### Use Cases

* API integration
* Task automation (tickets, workflows)
* Data lookup in systems

### Benefits

* Safe execution (developer-controlled)
* Structured and reliable interactions
* Enables real-world system integration

### Limitations

* Requires application-side implementation
* Must validate function inputs
* Adds latency to responses

**Key idea:** Model becomes **orchestrator of external systems**

***

# Unified Tool Execution Model

## 8. General Workflow

1. User sends prompt with tools
2. Model evaluates intent
3. Model selects tool (if needed)
4. Tool executes
5. Results returned to model
6. Model generates final response

***

# Best Practices for Tool Use

* Be explicit in prompts (clarity improves tool use)
* Provide context and expected output format
* Use keywords like **"use python"** for code interpreter
* Validate outputs:
  * Code results
  * API responses
* Monitor:
  * Token usage (cost)
  * Latency (tool execution)
* Design tools to be:
  * Small
  * Focused
  * Single-purpose

***

# Key Limitations

* Tool usage increases:
  * Latency
  * Cost
* Output quality depends on:
  * Tool configuration
  * Data quality
* Human validation still required for:
  * Critical decisions
  * Sensitive workflows

***

# Summary

* **Tools = capability extension layer for models**

* Core tools:
  * `code_interpreter` → execute Python code
  * `web_search` → retrieve real-time web data
  * `file_search` → retrieve private/document data (RAG)
  * `function` → call custom APIs and logic

* **Default behavior**
  * Model automatically decides when to use tools

* **You can control behavior via**
  * Instructions (system prompt)
  * Tool configuration

* **Tools enable**
  * Action
  * Grounding
  * Integration with real-world systems

