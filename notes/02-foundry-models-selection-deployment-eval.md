# Microsoft Foundry Models

## 1. Model Catalog

- Central hub to **discover, compare, and select AI models**.
- Includes models from Azure, Microsoft, partners, and community providers.
- Evaluate models by:
  - Capability
  - Provider
  - Task fit
  - Benchmarks
  - Safety
  - Cost
  - Deployment options

## 2. Model Categories

### Azure-Sold Models

- Billed through Azure subscription.
- Includes Azure OpenAI, Microsoft, and other Azure-hosted models.

### Partner / Community Models

- Provided by external providers or community sources.
- May have separate licensing, pricing, and usage terms.

> **Azure-sold = Azure billing**  
> **Partner/community = provider-specific terms**

## 3. Model Cards

Model cards summarize:

- Provider
- Capabilities
- Benchmarks
- Responsible AI notes
- Deployment options

> Use model cards to confirm technical fit before deployment.

## 4. Catalog Filters

Filter models by:

- **Collection** — Azure, Hugging Face, etc.
- **Capabilities** — reasoning, tool calling, multimodal
- **Source** — Azure OpenAI, Microsoft, Meta, Mistral, Cohere, Anthropic
- **Inference task** — text, summarization, translation, image, speech
- **Fine-tuning support**
- **Industry/domain**

## 5. Model Types

### LLMs

Examples:

- GPT-5
- Mistral Large
- Llama 3 70B

Best for:

- Deep reasoning
- Complex generation
- Long-context tasks

Tradeoff:

- Higher cost, compute, and latency

### SLMs

Examples:

- Phi-4
- Mistral OSS
- Llama 3 8B

Best for:

- Common NLP tasks
- Lower cost
- Faster response
- Edge or constrained environments

> **LLM = capability optimized**  
> **SLM = efficiency optimized**

## 6. Chat vs. Reasoning Models

### Chat Completion Models

- Generate context-aware text responses.
- Used for chatbots, assistants, and content generation.

### Reasoning Models

- Optimized for complex problem solving.
- Used for math, coding, science, strategy, and logistics.

> **Chat = respond**  
> **Reasoning = solve**

## 7. Specialized Models

- **Embedding models** — convert text to vectors for semantic search, RAG, and recommendations.
- **Image generation models** — generate images from text.
- **Video generation models** — generate video from text.
- **Image analysis models** — analyze text + image inputs.
- **Text-to-speech models** — convert text to speech.
- **Speech-to-text models** — transcribe speech to text.
- **Domain-specific models** — optimized for languages, regions, industries, or specialized datasets.

---

# Model Benchmarks

## 8. Benchmark Purpose

Benchmarks compare models before deployment across:

- Quality
- Safety
- Cost
- Performance

> Benchmark before deploying.

## 9. Benchmark Views

### Model Leaderboard

- Compare models across the catalog.
- Sort by quality, safety, cost, and throughput.

### Model Card Benchmarks

- View detailed metrics for a specific model.

## 10. Quality Benchmarks

Measure:

- Reasoning
- Knowledge
- Q&A
- Math
- Coding
- Instruction following

Common datasets:

- Arena-Hard
- BIG-Bench Hard
- GPQA
- HumanEval+
- MBPP+
- MATH
- MMLU-Pro
- IFEval

Scores are normalized from **0 to 1**.

> Higher = better quality.

## 11. Safety Benchmarks

Measure harmful or risky output.

Key metrics:

- **HarmBench / ASR** — lower Attack Success Rate is safer.
- **ToxiGen / F1** — higher F1 means better toxic content detection.
- **WMDP** — measures knowledge in sensitive domains like biosecurity, cybersecurity, and chemical security.

> **Safety = lower harmful behavior + stronger risk detection**

## 12. Cost Benchmarks

Track:

- Cost per 1M input tokens
- Cost per 1M output tokens
- Estimated cost using typical input/output ratios

> **Input tokens = prompt cost**  
> **Output tokens = generation cost**

## 13. Performance Benchmarks

### Latency

- Mean
- P50 / P90 / P95 / P99
- Time to first token, or TTFT

### Throughput

- Generated tokens per second, or GTPS
- Total tokens per second, or TTPS
- Time between tokens

> **Latency = responsiveness**  
> **Throughput = token processing rate**

## 14. Comparison Tools

Use:

- **Leaderboards** for top model ranking
- **Scenario leaderboards** for task-specific fit
- **Trade-off charts** for quality vs. cost, throughput, or safety
- **Side-by-side comparison** for detailed model evaluation

Compare:

- Quality
- Safety
- Throughput
- Context window
- Supported languages
- Deployment options
- Function calling
- Structured output
- Vision support

---

# Model Deployment

## 15. Deployment Purpose

Deploying a model makes it available through an endpoint.

Deployment creates:

- Endpoint URL
- Authentication configuration
- Deployment name
- Runtime access path

## 16. Deployment Types

### Global Standard

- Any Azure region
- Pay-per-token
- Best general-purpose option
- Highest quota

### Global Provisioned

- Any Azure region
- Reserved PTUs
- Predictable high throughput

### Global Batch

- Any Azure region
- Discounted async processing
- Large jobs within 24 hours

### Data Zone Standard

- Pay-per-token
- Data remains in a specific data zone
- Useful for EU/US compliance needs

### Data Zone Provisioned

- Reserved PTUs within a data zone

### Data Zone Batch

- Async batch jobs within a data zone

### Standard

- Single-region
- Pay-per-token
- Useful for regional residency or low-volume workloads

### Regional Provisioned

- Reserved PTUs in a single region

### Developer

- Pay-per-token
- Used for fine-tuned model evaluation

> **Standard = pay as you go**  
> **Provisioned = reserved throughput**  
> **Batch = async discount**  
> **Data Zone / Regional = residency control**

## 17. Deployment Guidance

- Prefer **Global Standard** when supported and no residency constraint exists.
- Check the model card for supported deployment types.

## 18. Deployment Settings

Key settings:

- **Deployment name** — used as the `model` value in code.
- **Deployment type** — controls region, residency, billing, and throughput.
- **Managed compute settings** — VM SKU, instance count, and AML quota if applicable.