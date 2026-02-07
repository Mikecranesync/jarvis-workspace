# LLM Routing Solutions Research
*Captured: 2026-02-06*

## Goal
Bootstrap tiered routing for FactoryLM's Layer 0-3 architecture with zero custom code.

---

## Top Pick: RouteLLM (lm-sys/Berkeley)

**Repo:** https://github.com/lm-sys/RouteLLM

### What it does
- Drop-in OpenAI-compatible router that sends simple queries to cheap models, complex ones to expensive models
- Pre-trained routers reduce costs 85% while maintaining 95% GPT-4 performance
- Works as either a Python library or standalone server

### Why it's perfect for FactoryLM
- Already has trained routing models (Matrix Factorization "mf" router)
- Zero-shot — install, point at models, done
- OpenAI-compatible API means existing Claude/GPT code just works
- Built by LMSys (same team as Chatbot Arena benchmarks)

### Setup
```bash
pip install "routellm[serve,eval]"

# Launch server with pre-trained router
python -m routellm.openai_server \
    --routers mf \
    --strong-model gpt-4 \
    --weak-model llama3-8b \
    --config config.yaml
```

### Usage
```python
from routellm.controller import Controller

client = Controller(
    routers=["mf"],  # Pre-trained Matrix Factorization router
    strong_model="gpt-4-1106-preview",
    weak_model="groq/llama3-8b-8192"
)

response = client.chat.completions.create(
    model="router-mf",  # Auto-routes based on complexity
    messages=[{"role": "user", "content": "What's fault E0234?"}]
)
```

### Layer Mapping for FactoryLM
- **Strong model** = Layer 3 (Claude Opus)
- **Weak model** = Layer 2 (Llama 70B on GPU) or Layer 1 (Qwen on Pi)
- **Layer 0** = Pre-check before hitting router (vector DB match)

---

## Runner-Up: LiteLLM Router (Most Flexible)

**Repo:** https://github.com/BerriAI/litellm
**Docs:** https://docs.litellm.ai/docs/routing

### What it does
- Universal proxy for 100+ LLM providers (OpenAI, Anthropic, local models, etc.)
- Multiple routing strategies built-in:
  - `simple-shuffle` - Random load balancing
  - `latency-based-routing` - Picks fastest model
  - `cost-based-routing` - Picks cheapest model that works
  - `usage-based-routing` - Balances across rate limits

### Why it's good
- More mature ecosystem than RouteLLM
- Built-in failover, retries, rate limiting
- Works with local models via Ollama/llama.cpp integration
- Has Prometheus metrics out of the box

### Setup
```python
from litellm import Router

model_list = [
    {
        "model_name": "layer3",
        "litellm_params": {"model": "claude-opus-4"},
        "tpm": 100000,  # Tokens per minute limit
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
    routing_strategy="cost-based-routing"  # Tries cheapest first
)

response = await router.acompletion(
    model="layer3",  # Router picks actual model
    messages=[{"role": "user", "content": "Diagnose conveyor fault"}]
)
```

### Comparison to RouteLLM
| Aspect | RouteLLM | LiteLLM |
|--------|----------|---------|
| Complexity detection | Pre-trained ML router | Manual rules |
| Production features | Basic | Retries, observability, fallbacks |
| Local model support | Good | Better (Ollama native) |
| Setup time | 5 min | 15 min |

---

## Research-Grade: LLMRouter (UIUC)

**Repo:** https://github.com/ulab-uiuc/LLMRouter
**Docs:** https://ulab-uiuc.github.io/LLMRouter/

### What it does
- Academic-grade routing library with 16+ routing algorithms
- Supports KNN, SVM, MLP, Matrix Factorization, Elo Rating, BERT-based routers, Graph-based, multi-round routers
- Unified CLI for training custom routers on your data

### Why it's interesting
- Most sophisticated routing models available
- Can train on your factory data (PLC queries → which layer worked best)
- Multi-round routing (agent tries Layer 1, evaluates, escalates if needed)

### When to use
- Post-YC when you have real usage data
- Want to train custom router on FactoryLM query patterns
- Need multi-step escalation logic

### Setup
```bash
pip install llmrouter

# Train custom router on your data
llmrouter train \
    --router knn \
    --data factory_queries.jsonl \
    --output models/factory_router.pkl

# Use trained router
llmrouter infer \
    --router models/factory_router.pkl \
    --query "Motor overheating, temp 95°C"
```

### Pros/Cons
- ✅ Can learn from YOUR data (not generic benchmarks)
- ✅ 16 different routing strategies to experiment with
- ❌ More complex setup
- ❌ Need training data (don't have this yet)

---

## Confidence Calibration (The Secret Sauce)

All three solutions support confidence-based cascading:

### How it works
- Model returns answer + confidence score (0-1)
- If confidence < threshold → escalate to stronger model
- Uses temperature scaling to calibrate confidence

### Why it matters
- More accurate than just routing by query complexity
- Model KNOWS when it's uncertain
- Reduces unnecessary escalations

### Implementation
```python
# Get answer + confidence from Layer 1
response = layer1_model.generate(query)
confidence = response.confidence  # Model's self-reported confidence

if confidence < 0.7:  # Not confident enough, escalate
    response = layer2_model.generate(query)
```

### References
- "Calibration and Cascading" (arXiv)
- Amazon's "Label with Confidence" cascading ensembles
- IBM LLM Router implementation

---

## Observability Add-Ons

### LangSmith
- Trace every router decision
- See why query escalated
- Compare layer performance

### Arize Phoenix (Open-source)
- Tracks cost, latency, accuracy per layer
- Drift detection (are queries getting harder over time?)

### Prometheus + Grafana
- LiteLLM exports metrics automatically
- Track % queries at each layer over time
- Cost per query trending

---

## Recommendation (Mike's Call - Feb 6, 2026)

### Phase 1: This Weekend (Pre-YC)
**Start with RouteLLM** because:
1. ✅ Zero-shot — pre-trained router works immediately
2. ✅ 2 hours to implement — literally pip install + config file
3. ✅ Proven results — 85% cost savings, 95% quality maintained
4. ✅ Drop-in replacement — works with existing code
5. ✅ Perfect for YC demo — "We use RouteLLM to automatically route queries, reducing costs 85%"

### Layer 0 Integration Pattern
```python
# Before hitting RouteLLM
exact_match = vector_db.search(query, threshold=0.95)
if exact_match:
    return exact_match  # Layer 0 wins

# Otherwise, let RouteLLM decide Layer 1/2/3
response = routellm_client.chat.completions.create(...)
```

### Phase 2: Post-YC Production
**Migrate to LiteLLM** when you need:
- Production reliability (retries, failover)
- Multi-provider support (Claude + local models)
- Better observability

### Phase 3: 6 Months In
**Train custom router with LLMRouter** on real factory data:
- Collect (query, layer used, success/fail, latency, cost)
- Train KNN or BERT router on factory-specific patterns
