# VISION.md — The Meta-Layer

*Last Updated: 2026-01-30*

---

## 🎯 The North Star

**Build the Maintenance Intelligence Layer for the Future**

Everything we do feeds this singular goal. Every piece of data, every interaction, every video, every training module—all of it trains our custom industrial maintenance LLM.

---

## The Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                 MAINTENANCE INTELLIGENCE LAYER                       │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌─────────────────────────────────────────────────────────────┐    │
│  │                    CUSTOM LLM (Future)                       │    │
│  │         Fine-tuned on Industrial Maintenance Domain          │    │
│  └─────────────────────────────────────────────────────────────┘    │
│                              ▲                                       │
│                              │ Training Data                         │
│  ┌─────────────────────────────────────────────────────────────┐    │
│  │              NEON VECTOR DATABASE (RAG + GraphRAG)           │    │
│  │                   Knowledge Base Layer                        │    │
│  └─────────────────────────────────────────────────────────────┘    │
│         ▲           ▲           ▲           ▲           ▲           │
│         │           │           │           │           │           │
│  ┌──────┴───┐ ┌─────┴────┐ ┌────┴────┐ ┌────┴────┐ ┌────┴────┐     │
│  │ YouTube  │ │Industrial│ │  Edge   │ │  CMMS   │ │ Jarvis  │     │
│  │ Content  │ │Skills Hub│ │ Adapter │ │ Records │ │ Memory  │     │
│  │  (YCB)   │ │  (ISH)   │ │  (PLC)  │ │         │ │         │     │
│  └──────────┘ └──────────┘ └─────────┘ └─────────┘ └─────────┘     │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Data Streams → Vector DB

**Everything gets captured:**

| Source | Data Type | Status |
|--------|-----------|--------|
| YCB v3 | Video scripts, storyboards, animations | 📋 Resurrect |
| IndustrialSkillsHub | Curriculum, lessons, assessments | 📋 Connect |
| Edge Adapter | PLC data, diagnostics, machine states | 🔄 Building |
| CMMS | Work orders, maintenance history, assets | ✅ Live |
| Jarvis Brain | Research, decisions, conversations | ✅ Active |
| Equipment Manuals | Technical documentation | 📋 Future |
| Customer Support | Tickets, resolutions, FAQs | 📋 Future |

---

## Intelligence Progression

**Stepwise climb from current state to custom LLM:**

```
STEP 1 (Current)
├── TinyLlama / Qwen 0.5B (local)
├── Claude / Gemini (cloud)
└── RAG via Neon Vector DB

STEP 2 (Next)
├── Fine-tune 7B model (Llama 3 / Mistral)
├── Domain: Industrial Maintenance
├── Method: LoRA / QLoRA (parameter-efficient)
└── GPU: Rented (RunPod ~$0.34-2/hr)

STEP 3 (Growth)
├── Fine-tune larger model (13B-70B)
├── Deeper domain specialization
├── Add compute as data grows
└── GPU: Dedicated hardware

STEP 4 (Scale)
├── Custom pre-trained model
├── Continuous learning pipeline
├── Multi-modal (text + diagrams + video)
└── Production deployment
```

---

## Current Priorities (Realigned)

All priorities now serve the meta-layer:

### P0: Data Capture Infrastructure
*Everything must feed the knowledge base*
- [ ] Configure all agents to log to Neon
- [ ] Set up embedding pipeline
- [ ] Create data ingestion standards

### P1: Edge Adapter
*Real-time PLC data → Training data*
- [ ] Flash BeagleBone
- [ ] Deploy WireGuard
- [ ] Start capturing machine data

### P2: YouTube Content Factory
*Content generation + training data*
- [ ] Resurrect YCB v3
- [ ] Connect LLM Quality Judge
- [ ] Feed scripts → Neon

### P2: Angel Funding
*Compute resources for training*
- [ ] Pitch deck focused on intelligence layer
- [ ] Highlight data moat advantage

### P3: Local LLM Infrastructure
*Stepping stone to custom model*
- [x] Ollama installed
- [x] Qwen 0.5B running
- [ ] Configure as primary for simple tasks

---

## Best Practices (AI Engineering 2025)

### Fine-Tuning Strategy
1. **Start with instruction-tuned base** (Llama 3 Instruct)
2. **Use PEFT/LoRA** — Train <1% of parameters
3. **Quality data > quantity** — Curate, don't just collect
4. **Robust evaluation** — Quantitative + human review
5. **Lifecycle mindset** — Version, monitor, retrain

### RAG + GraphRAG Architecture
1. **Neon PostgreSQL** — pgvector for embeddings
2. **Hybrid retrieval** — Vector search + knowledge graph
3. **Chunking strategy** — Semantic, not arbitrary
4. **Context window optimization** — Quality over quantity

### GPU Rental Options
| Provider | GPU | $/hour | Best For |
|----------|-----|--------|----------|
| RunPod | RTX 4090 | $0.34 | Development |
| RunPod | H100 | $1.99 | Training |
| Vast.ai | Various | Variable | Budget |
| Lambda | A100 | $0.75 | Production |

---

## The Flywheel

```
More Content → More Data → Better Model → Better Content → More Users
     ↑                                                          │
     └──────────────────────────────────────────────────────────┘
```

Every piece of content we create:
1. Gets published (revenue, leads, SEO)
2. Gets embedded in vector DB (knowledge)
3. Trains the model (intelligence)
4. Makes better content (quality)

---

## Success Metrics

- **Knowledge Base Size** — Embeddings in Neon
- **Model Quality** — Evaluation benchmarks
- **Content Volume** — Videos/week auto-generated
- **Revenue** — YouTube, training platform, consulting
- **Compute Efficiency** — Cost per training run

---

## Constitutional Alignment

This vision follows:
- **Amendment I**: Open source first (Ollama, Llama, Neon)
- **Amendment II**: Research before building
- **Engineering Commandments**: Document everything, issue-first

---

*This document is the source of truth. All other priorities derive from it.*
