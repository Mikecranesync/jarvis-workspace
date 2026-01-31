# AI Engineering Best Practices for Custom Industrial LLM

*Research conducted: 2026-01-30 | Constitution: 30+ min open source research*

---

## Executive Summary

Building a custom domain-specific LLM for industrial maintenance requires a structured approach:
1. **Data first** — Quality > Quantity
2. **RAG for fast iteration** — Vector DB + Knowledge Graph
3. **Fine-tuning for specialization** — LoRA/QLoRA on 7B-13B models
4. **Stepwise progression** — Don't jump to training from scratch

---

## The Intelligence Ladder

### Level 1: RAG (Current State)
**What**: Retrieve relevant context from vector DB, feed to base LLM

**Pros**:
- Fast to implement
- No training required
- Knowledge updates instantly
- Works with any LLM

**Cons**:
- Context window limits
- Retrieval quality varies
- No true understanding

**Our Setup**: Neon PostgreSQL + pgvector (already in Rivet-PRO)

---

### Level 2: Fine-Tuned Small Model (Next Step)
**What**: Take a 7B-13B model, fine-tune on our domain data

**Recommended Base Models (2025)**:
| Model | Size | Context | Strength |
|-------|------|---------|----------|
| Llama 3.3 | 8B/70B | 128k | General + coding |
| Mistral 7B | 7B | 32k | Efficiency |
| Qwen 2.5 | 0.5B-72B | 128k | Multilingual |
| DeepSeek R1 | 7B-671B | 64k | Reasoning |

**Fine-Tuning Methods**:

1. **LoRA (Low-Rank Adaptation)**
   - Trains <1% of parameters
   - Adds small learned matrices
   - GPU: 8GB VRAM for 7B model
   - Cost: ~$10-50 for a training run

2. **QLoRA (Quantized LoRA)**
   - 4-bit quantization + LoRA
   - GPU: 4GB VRAM for 7B model
   - Slightly lower quality
   - Perfect for experimentation

3. **Full Fine-Tune**
   - All parameters
   - GPU: 40GB+ VRAM for 7B
   - Best quality, highest cost
   - Risk of catastrophic forgetting

**Recommendation**: Start with QLoRA on 7B, graduate to LoRA on 13B

---

### Level 3: Continuous Pre-Training (Growth)
**What**: Extend pre-training on domain-specific text corpus

**When**: After significant data accumulation (millions of tokens)

**Process**:
1. Collect industrial maintenance text corpus
2. Continue unsupervised pre-training
3. Then apply supervised fine-tuning
4. Align with RLHF if needed

**GPU Needs**: 8x A100 or equivalent, ~$500-2000/run

---

### Level 4: Custom Model (Scale)
**What**: Train from scratch with domain focus

**When**: Data moat is substantial (billions of tokens)

**Reality Check**: Likely not needed. Fine-tuned models match or beat custom for most use cases.

---

## Data Pipeline Architecture

### Embedding Strategy

```
Raw Data → Chunking → Embedding → Vector DB
    │          │          │           │
    │          │          │           └── Neon PostgreSQL + pgvector
    │          │          └── text-embedding-3-small (OpenAI)
    │          │                or nomic-embed-text (local)
    │          └── Semantic chunking (not arbitrary)
    └── All sources: YCB, ISH, CMMS, Edge, Jarvis
```

### GraphRAG Enhancement

Traditional RAG struggles with:
- Multi-hop reasoning
- Entity relationships
- Global context

**Solution**: Hybrid approach
1. Vector search for semantic similarity
2. Knowledge graph for entity relationships
3. Combine retrieved context

**Tools**:
- Neo4j or Neon + graph extensions
- Microsoft GraphRAG library
- LangChain/LlamaIndex orchestration

---

## GPU Rental Comparison

### Development/Experimentation
| Provider | GPU | $/hour | Notes |
|----------|-----|--------|-------|
| RunPod | RTX 4090 | $0.34 | Great for dev |
| Vast.ai | RTX 3090 | $0.20-0.40 | Variable |
| Google Colab | T4/V100 | Free-$10/mo | Limited |

### Training Runs
| Provider | GPU | $/hour | Notes |
|----------|-----|--------|-------|
| RunPod | H100 | $1.99 | Best value |
| Lambda | A100 | $0.75 | Reliable |
| Thunder | A100 | $0.78 | Budget |

### Estimated Costs
- **7B QLoRA fine-tune**: $5-20
- **13B LoRA fine-tune**: $20-100
- **70B LoRA fine-tune**: $100-500
- **Continuous pre-training**: $500-5000

---

## Best Practices Checklist

### Data Quality
- [ ] Curate, don't just collect
- [ ] Remove duplicates and noise
- [ ] Ensure representative coverage
- [ ] Version your datasets
- [ ] Document data sources

### Training
- [ ] Start with instruction-tuned base
- [ ] Use PEFT (LoRA/QLoRA) first
- [ ] Implement early stopping
- [ ] Save checkpoints frequently
- [ ] Monitor for overfitting

### Evaluation
- [ ] Quantitative metrics (perplexity, accuracy)
- [ ] Human evaluation panel
- [ ] A/B testing in production
- [ ] Domain-specific benchmarks
- [ ] Track regression

### Production
- [ ] Version models like code
- [ ] Implement rollback capability
- [ ] Monitor inference quality
- [ ] Set up retraining pipeline
- [ ] Plan for data drift

---

## Tools & Frameworks

### Fine-Tuning
- **Axolotl**: All-in-one fine-tuning tool
- **Hugging Face PEFT**: LoRA/QLoRA library
- **Unsloth**: 2x faster training
- **LMFlow**: Production pipelines

### RAG/Retrieval
- **LangChain**: Orchestration
- **LlamaIndex**: Data framework
- **Neon + pgvector**: Vector storage
- **Neo4j**: Graph database

### Evaluation
- **lm-eval-harness**: Benchmarks
- **Ragas**: RAG evaluation
- **Human-in-the-loop**: Custom panels

---

## Recommended Progression for Mike

### Phase 1: Foundation (Now - Week 2)
1. Audit Neon setup in Rivet-PRO
2. Configure embedding pipeline
3. Start ingesting all data sources
4. Set up eval framework

### Phase 2: First Fine-Tune (Week 3-4)
1. Collect 1000+ high-quality examples
2. Rent RTX 4090 on RunPod (~$5)
3. QLoRA fine-tune Qwen 2.5 7B
4. Evaluate against base model

### Phase 3: Production (Month 2)
1. Iterate on training data
2. Graduate to LoRA on 13B
3. Deploy as inference endpoint
4. Monitor and retrain

### Phase 4: Scale (Month 3+)
1. Continuous pre-training on corpus
2. Add specialized capabilities
3. Multi-modal (diagrams, video)
4. Consider dedicated hardware

---

## Open Source Shortcuts (Constitution-Approved)

- **Axolotl**: https://github.com/OpenAccess-AI-Collective/axolotl
- **Unsloth**: https://github.com/unslothai/unsloth (2x faster)
- **LlamaIndex**: https://github.com/run-llama/llama_index
- **Microsoft GraphRAG**: https://github.com/microsoft/graphrag
- **Neon pgvector**: Already in stack
- **Hugging Face Hub**: Model hosting

---

*Research complete. Ready for implementation.*
