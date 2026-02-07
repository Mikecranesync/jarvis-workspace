# Open Source Memory Systems Research

*Captured: 2026-02-06*

## 🎯 Best Fit for FactoryLM Architecture

### Edge (Pi) - Layer 0/1
| System | Why |
|--------|-----|
| **LanceDB** | Fastest on Pi, zero-copy, embedded |
| **Ollama + Qwen 0.5B** | <1 sec summaries on Pi 5 |
| **ChromaDB** | Python-native, embedded mode |

### VPS - Layer 2/3
| System | Why |
|--------|-----|
| **Mem0** | Production-ready, hierarchical, Apache 2.0 |
| **Qdrant** | Best quality, Rust-fast, advanced filtering |

---

## Full Memory Systems (Ready to Use)

### 1. Mem0 (formerly EmbedChain Memory)
- **Repo:** https://github.com/mem0ai/mem0
- **Features:** User/session/agent-level, auto-summarization, vector+graph hybrid
- **Adapters:** ChromaDB, Qdrant, Pinecone, LangChain, LlamaIndex
- **License:** Apache 2.0

```python
from mem0 import Memory
memory = Memory()
memory.add("Mike prefers WhatsApp for FactoryLM", user_id="mike")
results = memory.search("How does Mike want communication?", user_id="mike")
```

### 2. MemGPT (Long-Term Memory for LLMs)
- **Repo:** https://github.com/cpacker/MemGPT
- **Features:** OS-inspired paging, auto-archival, self-editing memory, multi-agent sharing
- **License:** Apache 2.0

### 3. LangMem (LangChain Memory)
- **Repo:** https://github.com/langchain-ai/langchain
- **Types:** ConversationBuffer, ConversationSummary, VectorStoreRetriever, Entity
- **License:** MIT

---

## Vector Databases (Storage Layer)

| DB | Best For | License |
|----|----------|---------|
| **ChromaDB** | Easiest, Python-native, Pi-friendly | Apache 2.0 |
| **LanceDB** | Fastest on Pi, zero-copy | Apache 2.0 |
| **Qdrant** | Production quality, Rust-based | Apache 2.0 |

---

## Edge LLMs for Summarization

| Model | Speed on Pi 5 | Use Case |
|-------|---------------|----------|
| Qwen 0.5B | <1 sec | Memory summaries |
| Llama 1B | ~2 sec | Short-term compression |
| Phi-2 | ~3 sec | Quality summaries |

```bash
# On Pi
ollama run qwen:0.5b
```

---

## Agent Memory Examples (Learn From)

1. **AutoGPT** - Pinecone/Milvus backed, battle-tested
2. **BabyAGI** - Simple task-based, readable code
3. **SuperAGI** - Multi-modal (text, images, code)

---

## FactoryLM Implementation Plan

### Phase 1: Edge (Pi)
- LanceDB for local vector storage
- Qwen 0.5B via Ollama for summarization
- 30-day rolling window

### Phase 2: VPS
- Mem0 for hierarchical memory
- Qdrant for long-term storage
- Cross-device sync via API

### Phase 3: Intelligence Flow
```
Pi (working memory) 
  ↓ summarize daily
VPS (long-term memory)
  ↓ insights extracted
Pi (code/rules updated)
```

This matches the 4-layer architecture: intelligence flows DOWN.
