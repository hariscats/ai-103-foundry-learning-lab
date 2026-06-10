# Optimizing AI Models

## 1. Core Problem
- Base models ≠ production-ready
- Key gaps:
  - **Accuracy** (hallucinations)
  - **Consistency** (style, format)
  - **Relevance** (domain-specific data)

---

## 2. Optimization Spectrum (3 Pillars)
- **Prompt Engineering → guide behavior**
- **RAG (Retrieval Augmented Generation) → add (domain) knowledge**
- **Fine-tuning → enforce consistency**

> Use incrementally: start simple → add complexity only if needed

---

## 3. Prompt Engineering 
### Purpose
- Control **tone, format, behavior**
- Lowest cost, fastest iteration

### Core Components
- **System message** → defines rules (role, tone, constraints)
- **User message** → input/question
- **Assistant message** → conversation memory
- **Examples** → demonstrate expected outputs

### System Message Design 
- Define:
  - **Role** (what the model is)
  - **Boundaries** (what it avoids)
  - **Output format** (explicit)
  - **Fallback behavior** ("ask when unsure")

> Important: Influences behavior but does NOT guarantee compliance

---

### Prompt Patterns 
- **Persona**
  - Shapes tone + expertise
- **Format Template**
  - Ensures structured outputs (e.g., JSON, lists)
- **Chain-of-thought**
  - Improves reasoning accuracy
- **Few-shot learning**
  - Teaches patterns via examples

---

### Prompting Best Practices
- Use **clear delimiters** (e.g., `---`, headings)
- Watch **recency bias** (repeat key instructions at end)
- Keep instructions **explicit and simple**

---

### Model Parameters
- **Temperature**
  - Low → factual, deterministic
  - High → creative, varied
- **Top_p**
  - Probability filtering
- Adjust **one at a time**

---

### When Prompting Is Enough
- Behavior control needed
- No external data required
- Fast iteration + low cost

---

## 4. RAG (Retrieval Augmented Generation)
### Purpose
- Solve **knowledge gap**
- Provide **accurate, real, up-to-date data**

---

### Problem Without RAG
- Model relies only on training data
- Leads to:
  - **Hallucinations**
  - **Outdated answers**
  - **No access to private data**

---

### RAG Flow
1. **Retrieve** relevant data
2. **Augment** prompt with context
3. **Generate** grounded response

---

### Key Enabler: Embeddings
- Convert text → vectors (semantic meaning)
- Similar content = **close vectors**
- Measured using metrics like **cosine similarity**

---

### Retrieval (AI Search)
- Index data using embeddings
- Query using:
  - Keyword search
  - Semantic search
  - Vector search
  - **Hybrid search (combination of above)**

---

### When to Use RAG
- Need:
  - **Private/internal data access**
  - **Frequently updated data**
  - **High factual accuracy**

---

## 5. Fine-Tuning
### Purpose
- Enforce **consistent behavior, tone, format**

---

### What It Does
- Trains model on **example conversations**
- Adjusts weights (via **LoRA**) for efficiency

---

### When to Use
- Prompting fails to:
  - Maintain style/format
  - Follow rules consistently
- Use cases:
  - Brand voice enforcement
  - Unique structured outputs
  - Reducing prompt size
  - Model distillation

---

### Types of Fine-Tuning
- **SFT (Supervised)** → learn from examples
- **RFT (Reinforcement)** → optimize via feedback
- **DPO** → align with preferences

---

### Data Requirements
- High-quality JSONL examples
- Include:
  - Consistent system message
  - Representative scenarios
- Scale: **hundreds+ examples**

---

### Trade-offs
- Pros:
  - High consistency
  - Reduced prompt size
- Cons:
  - High cost (training + hosting)
  - Maintenance (retraining)
  - Risk of overfitting / drift

---

## 6. Strategy Comparison

| Strategy              | Best For                     | Cost | Complexity |
|----------------------|-----------------------------|------|-----------|
| Prompt Engineering   | Behavior, format            | Low  | Low       |
| RAG                  | Accuracy, real data         | Med  | Med       |
| Fine-tuning          | Consistency, style          | High | High      |

---

## 7. Decision Framework
1. Start with **prompt engineering**
2. Add **RAG** if:
   - Model lacks knowledge
3. Add **fine-tuning** if:
   - Behavior is inconsistent
4. Combine as needed

> Key principle: **Minimize cost + complexity while meeting requirements**
