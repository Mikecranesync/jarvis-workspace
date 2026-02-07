# LLM Routing Solutions Research
**Date:** 2026-02-06
**Source:** Mike's research dump
**Purpose:** Tiered routing for FactoryLM (Layer 0-3 architecture)

---

## Top Pick: RouteLLM (lm-sys/Berkeley)

**Repo:** https://github.com/lm-sys/RouteLLM

**What it does:**
- Drop-in OpenAI-compatible router
- Sends simple queries to cheap models, complex to expensive
- Pre-trained routers reduce costs 85% while maintaining 95% GPT-4 performance
- Works as Python library or standalone server

**Why it's perfect:**
- Has trained routing models (Matrix Factorization "mf" router)
- Zero-shot — install, point at models, done
- OpenAI-compatible API (existing code just works)
- Built by LMSys (Chatbot Arena team)

**Setup:**
```bash
pip install "routellm[serve,eval]"

python -m routellm.openai_server \
  --routers mf \
  --strong-model gpt-4 \
  --weak-model llama3-8b \
  --config config.yaml
```

**Usage:**
```python
from routellm.controller import Controller

client = Controller(
    routers=["mf"],
    strong_model="gpt-4-1106-preview",
    weak_model="groq/llama3-8b-8192"
)

response = client.chat.completions.create(
    model="router-mf",
    messages=[{"role": "user", "content": "What's fault E0234?"}]
)
```

**FactoryLM Mapping:**
- Strong model = Layer 3 (Claude Opus)
- Weak model = Layer 2 (Llama 70B on GPU) or Layer 1 (Qwen on Pi)
- Layer 0 = Pre-check before router (vector DB match)

---

## Runner-Up: LiteLLM Router (Most Flexible)

**Repo:** https://github.com/BerriAI/litellm
**Docs:** https://docs.litellm.ai/docs/routing

**What it does:**
- Universal proxy for 100+ LLM providers
- Multiple routing strategies built-in:
  - `simple-shuffle` - Random load balancing
  - `latency-based-routing` - Picks fastest model
  - `cost-based-routing` - Picks cheapest model that works
  - `usage-based-routing` - Balances across rate limits

**Advantages over RouteLLM:**
- More mature ecosystem
- Built-in failover, retries, rate limiting
- Works with local models via Ollama/llama.cpp
- Prometheus metrics out of the box

**Disadvantages:**
- No pre-trained complexity classifier (rules are manual)

**Setup:**
```python
from litellm import Router

model_list = [
    {
        "model_name": "layer3",
        "litellm_params": {"model": "claude-opus-4"},
        "tpm": 100000,
    },
    {
        "model_name": "layer2",
        "litellm_params": {"model": "ollama/llama3:70b"},
        "tpm": 500000,
    },
    {
        "model_name": "layer1",
        "litellm_params": {"model": "ollama/qwen:0.5b"},
        "tpm": 1000000,
    }
]

router = Router(
    model_list=model_list,
    routing_strategy="cost-based-routing"
)
```

---

## Research-Grade: LLMRouter (UIUC)

**Repo:** https://github.com/ulab-uiuc/LLMRouter
**Docs:** https://ulab-uiuc.github.io/LLMRouter/

---

## Recommendation for FactoryLM

**Phase 1 (Quick Win):** RouteLLM with mf router
- Zero config, pre-trained
- Immediate 85% cost reduction

**Phase 2 (Production):** LiteLLM Router
- Better observability
- More routing strategies
- Failover and retries

**Phase 3 (Custom):** Train own router on maintenance queries
- Fine-tune on PLC fault codes, equipment manuals
- Route simple lookups to Pi, complex diagnostics to GPU/Cloud

---

## LLMRouter Details (UIUC)

**16+ routing algorithms:**
- KNN, SVM, MLP
- Matrix Factorization
- Elo Rating
- BERT-based routers
- Graph-based
- Multi-round routers

**Train custom router:**
```bash
pip install llmrouter

# Train on your data
llmrouter train \
  --router knn \
  --data factory_queries.jsonl \
  --output models/factory_router.pkl

# Use trained router  
llmrouter infer \
  --router models/factory_router.pkl \
  --query "Motor overheating, temp 95°C"
```

**When to use:** Post-YC with real usage data

---

## Confidence Calibration (Secret Sauce)

All three solutions support confidence-based cascading:

**How it works:**
- Model returns answer + confidence (0-1)
- If confidence < threshold → escalate
- More accurate than query-complexity routing

**Implementation:**
```python
response = layer1_model.generate(query)
confidence = response.confidence

if confidence < 0.7:  # Not confident, escalate
    response = layer2_model.generate(query)
```

**References:**
- "Calibration and Cascading" (arXiv)
- Amazon's "Label with Confidence" paper
- IBM LLM Router implementation

---

## Observability Options

- **LangSmith** - Trace router decisions
- **Arize Phoenix** - Open-source LLM observability
- **Prometheus + Grafana** - LiteLLM exports metrics

---

## Implementation Timeline

### Phase 1: Tonight (Zero-Shot)
- RouteLLM with pre-trained `mf` router
- Layer 3 = Claude Opus
- Layer 2 = Llama 70B / Claude Haiku
- Layer 0 = Vector DB exact match BEFORE router

### Phase 2: Post-YC (Production)
- Switch to LiteLLM
- Add Prometheus metrics
- Built-in retries/failover
- Cost tracking per query

### Phase 3: 6 Months (Custom)
- Use LLMRouter
- Train on real data: (query, layer, success, latency, cost)
- Domain-specific routing for factory queries
