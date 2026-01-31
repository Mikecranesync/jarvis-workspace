# Edge LLM Research Update - January 2026
## Best Small Models for ShopTalk Edge Deployment

**Research Date:** 2026-01-31
**Purpose:** Select optimal LLM for $50 edge device deployment

---

## Executive Summary

Based on 2026 research, **Qwen3-0.6B** or **Phi-4-mini (3.8B)** are the top candidates for ShopTalk:

| Model | Params | Best For | Edge Fit |
|-------|--------|----------|----------|
| **Qwen3-0.6B** | 0.6B | Ultra-constrained, multilingual | ⭐⭐⭐⭐⭐ |
| **Qwen3-1.7B** | 1.7B | Balance of size/capability | ⭐⭐⭐⭐ |
| **Phi-4-mini** | 3.8B | Reasoning, 128K context | ⭐⭐⭐ |
| **SmolLM3-3B** | 3B | Dual-mode reasoning | ⭐⭐⭐ |
| **Gemma-3n-E2B** | 2B effective | Multimodal (future) | ⭐⭐⭐ |

---

## Top Recommendation: Qwen3-0.6B

### Why Qwen3-0.6B for ShopTalk:

1. **Tiny footprint** - Runs on very constrained devices
2. **100+ languages** - Spanish support out of the box
3. **Agent/tool-use ready** - Designed for agentic workflows
4. **Apache 2.0 license** - Commercial use allowed
5. **Strong for its class** - Competitive with 8B models on some tasks

### Specs:
- Parameters: 0.6B
- Context: 32K tokens
- License: Apache 2.0
- Quantized size: ~400MB (Q4)

### Caveats:
- Less reliable for deep reasoning
- Can get repetitive without proper sampling settings
- Use presence penalty to avoid loops

---

## Runner-Up: Phi-4-mini-instruct (3.8B)

### Why Phi-4-mini:

1. **MIT License** - Most permissive
2. **128K context** - Great for RAG with equipment manuals
3. **Strong reasoning** - Comparable to 7-9B models
4. **20+ languages** - Good multilingual support

### Specs:
- Parameters: 3.8B
- Context: 128K tokens
- License: MIT
- Quantized size: ~2.5GB (Q4)

### Caveats:
- Limited factual knowledge (pair with RAG)
- Sensitive to prompt format
- Larger = more RAM needed

---

## Deployment Strategy for ShopTalk

### Tier 1: Ultra-Edge (RPi Zero, BeagleBone Black)
**Model:** Qwen3-0.6B (Q4 quantized)
- RAM needed: ~1GB
- Use for: Basic diagnostics, status queries

### Tier 2: Standard Edge (RPi 4/5, Jetson Nano)
**Model:** Qwen3-1.7B or Phi-4-mini (Q4)
- RAM needed: 2-4GB
- Use for: Full diagnostics, reasoning

### Tier 3: Hybrid (Edge + Cloud)
**Edge:** Qwen3-0.6B for real-time
**Cloud:** Full Phi-4 or Claude for complex queries
- Best of both worlds

---

## Fine-Tuning Recommendation

**Base Model:** Qwen3-1.7B
- Good balance of capability and trainability
- Strong multilingual (Spanish support)
- LoRA fine-tuning possible on consumer GPU

**Training Data:** 
- 2400 samples generated ✅
- Mix of EN/ES, normal/fault scenarios
- Real sensor trajectories from world model

---

## Integration with Ollama

All recommended models available via Ollama:

```bash
# Ultra-small
ollama pull qwen2:0.5b

# Small  
ollama pull qwen2:1.5b

# Medium (best quality)
ollama pull phi3:mini

# Test locally
ollama run qwen2:1.5b "Diagnose: Motor current 8.5A, belt speed 30%"
```

---

## Key Insights from Research

1. **"Fine-tuned small > general-purpose large"** - A well fine-tuned SLM can outperform much larger models on domain tasks

2. **Distillation works** - Modern small models benefit from knowledge distilled from frontier models

3. **RAG is essential** - Small models have limited factual knowledge, pair with retrieval

4. **Quantization is mature** - Q4_K_M gives good quality at 4-5x size reduction

5. **Agent-ready models** - Qwen3 and Phi-4 designed with tool-use in mind

---

## Action Items

1. [x] Generate training data (2400 samples)
2. [x] Create fine-tuning script (LoRA)
3. [x] Build Ollama integration
4. [ ] Test Qwen3-0.6B on actual RPi 5
5. [ ] Fine-tune on ShopTalk data
6. [ ] Benchmark vs base model

---

## Sources

- BentoML: "Best Open-Source Small Language Models (SLMs) in 2026"
- HuggingFace model hub
- Qwen3 Technical Report
- LocalLLM.in benchmarks
