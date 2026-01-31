# Local LLM Research — January 30, 2026

*Constitution Compliance: 30-minute open source research completed*

---

## VPS Hardware Assessment

| Resource | Value | LLM Feasibility |
|----------|-------|-----------------|
| CPU | AMD EPYC 9354P (1 core) | Limited |
| RAM | 3.8GB (1.8GB free) | Can run small models |
| Disk | 12GB free | Enough for 2-3 models |
| GPU | None | CPU inference only |

**Verdict:** Can run TinyLlama, Qwen 0.5B, or similar. NOT suitable for 7B+ models.

---

## Option 1: Ollama on Current VPS

### Viable Models
| Model | Size | RAM Needed | Quality |
|-------|------|------------|---------|
| Qwen 0.5B | 400MB | ~1GB | Basic tasks only |
| TinyLlama 1.1B | 700MB | ~1.5GB | Light conversations |
| Gemma 2B | 1.5GB | ~2.5GB | Borderline |
| Phi-3 Mini 3.8B | 2GB | ~3GB | Won't fit |

### Setup (5 minutes)
```bash
curl -fsSL https://ollama.com/install.sh | sh
ollama pull tinyllama
ollama run tinyllama
```

### Pros
- Completely free
- Works now
- OpenAI-compatible API

### Cons
- Very limited model size
- Slow inference (CPU only)
- Won't match Claude quality

---

## Option 2: Upgrade VPS or Add GPU Server

### Minimum for Good Local LLM
- 16GB RAM
- 4+ CPU cores
- OR: GPU with 8GB VRAM

### Cloud GPU Options
| Provider | GPU | $/hour | Notes |
|----------|-----|--------|-------|
| RunPod | RTX 4090 | $0.44 | On-demand |
| Vast.ai | Various | $0.20-0.50 | Marketplace |
| Lambda | A10 | $0.75 | Reliable |

### Self-Hosted
- Used RTX 3090: ~$600-800
- Runs 70B models easily
- One-time cost

---

## Option 3: OpenRouter Free Tiers

OpenRouter provides access to multiple models with some free options:

### Free/Cheap Models via OpenRouter
- Google Gemini Flash (near free)
- Mistral models (cheap)
- Some community models (free)

### Setup
1. Create OpenRouter account
2. Get API key
3. Configure Clawdbot to route simple tasks to cheap models

---

## Option 4: Hybrid Architecture (RECOMMENDED)

**Smart routing based on task complexity:**

| Task Type | Route To | Cost |
|-----------|----------|------|
| Trello checks | TinyLlama (local) | Free |
| System monitoring | Gemini Flash | ~Free |
| Simple Q&A | Local or Gemini | Free |
| Complex coding | Claude Sonnet | $$ |
| Critical reasoning | Claude Opus | $$$ |

### Implementation
1. Install Ollama with TinyLlama now (free, 5 min)
2. Create task router in Clawdbot config
3. Use local for 80% of routine tasks
4. Reserve Claude for 20% complex work

---

## Immediate Actions (Can Do Tonight)

### 1. Install Ollama (5 min)
```bash
curl -fsSL https://ollama.com/install.sh | sh
ollama pull tinyllama
```

### 2. Test Local Model
```bash
curl http://localhost:11434/api/chat -d '{
  "model": "tinyllama",
  "messages": [{"role": "user", "content": "Hello"}]
}'
```

### 3. Configure Clawdbot Fallback
Add to config:
```json
"subagents": {
  "model": {
    "primary": "ollama/tinyllama",
    "fallbacks": ["google/gemini-2.5-flash", "anthropic/claude-sonnet-4"]
  }
}
```

---

## Long-Term Recommendation

1. **Now:** Install TinyLlama for basic tasks
2. **This month:** Monitor token usage, see savings
3. **If needed:** Add GPU VPS ($20-50/mo) for Llama 3 70B
4. **Future:** Consider dedicated GPU hardware if heavy use

---

## Token Visibility

Current monitoring options:
- `/status` in Clawdbot shows context usage
- Anthropic Console shows API usage
- Need to set up usage tracking/alerts

---

*Research completed at 2026-01-30 01:40 UTC*
