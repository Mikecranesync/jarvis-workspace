# YCB Pipeline Assessment

*Tested: 2026-01-30 05:05 UTC*
*Phase 1, Hour 3 of 10-Hour Plan*

---

## Test Results

### Local LLM Script Generation

**Model:** Qwen 2.5 0.5B via Ollama
**Prompt:** "Write a 3-sentence explanation of what a PLC is for maintenance technicians."
**Time:** ~40 seconds
**Result:** ✅ Works, but slow

**Output Quality:** 
- Grammatically correct
- Factually accurate
- A bit verbose/generic
- Not professional video script quality

**Sample Output:**
> "A Programmable Logic Controller (PLC) is an electronic device that allows operators to control and monitor industrial systems using programming software. It has the ability to process data and automate processes, making it ideal for maintenance technicians in the industrial sector..."

### Manim Rendering
**Status:** ✅ Verified working (tested earlier)
**Output:** 720p30 video from templates

### YCB Template System
**Status:** ✅ All 28 assets available
**Templates:** 6 scene types working

---

## Pipeline Bottlenecks

| Component | Status | Bottleneck |
|-----------|--------|------------|
| Script Generation (Local) | ⚠️ | Too slow (~40s for 3 sentences) |
| Script Generation (Cloud) | ✅ | Fast but costs money |
| Storyboard Planning | ❓ | Needs LLM, same issue |
| Manim Rendering | ✅ | Works, ~30s per scene |
| Voice Generation | ❓ | Not tested yet |
| Video Assembly | ✅ | FFmpeg working |

---

## Recommendations

### Short-Term (This Week)
1. **Use cloud LLM for script generation** (Groq free tier, then Anthropic)
2. **Local LLM for simple tasks only** (classification, formatting)
3. **Batch process videos overnight** when speed doesn't matter

### Medium-Term (This Month)
1. **Upgrade VPS** — Hetzner with 16GB+ RAM for faster local inference
2. **Try larger local models** — Qwen 3B or Llama 7B (need more RAM)
3. **Implement caching** — Don't regenerate scripts we've already made

### Long-Term (Q1 2026)
1. **Fine-tune model for industrial content** — Better quality, less tokens
2. **Edge deployment** — Local inference at customer sites
3. **Multi-GPU setup** — For heavy training/inference

---

## YCB Full Pipeline Roadmap

```
CURRENT STATE
├── ✅ Manim rendering works
├── ✅ Templates work
├── ⚠️ Local LLM too slow for scripts
└── ❓ Voice generation untested

NEXT STEPS (Priority Order)
1. [ ] Configure Groq API key for script generation
2. [ ] Test voice generation (ElevenLabs or Edge TTS)
3. [ ] Run end-to-end test: Topic → Script → Video
4. [ ] Create first real content piece
5. [ ] Set up automated batch processing

DEPENDENCIES
- Groq API key (free tier available)
- ElevenLabs API key (or use free Edge TTS)
- More RAM for better local LLM performance
```

---

## Cost Analysis

### Cloud LLM Options for Script Generation

| Provider | Model | Cost | Speed |
|----------|-------|------|-------|
| Groq | Llama 3 70B | Free tier (limited) | Very fast |
| Anthropic | Claude Haiku | $0.25/1M tokens | Fast |
| OpenAI | GPT-4o-mini | $0.15/1M tokens | Fast |
| Local (Current) | Qwen 0.5B | Free | Very slow |

**Recommendation:** Start with Groq free tier, fall back to Haiku.

### Video Production Cost (per video)

| Component | Cloud Cost | Local Cost |
|-----------|------------|------------|
| Script (500 words) | ~$0.001 | $0 (slow) |
| Voice (60 seconds) | ~$0.10-0.50 | $0 (Edge TTS) |
| Rendering | $0 | $0 |
| **Total** | ~$0.10-0.50 | $0 (slow) |

---

## Action Items

1. [x] Test local LLM — Works but slow
2. [ ] Get Groq API key configured
3. [ ] Test voice generation
4. [ ] Run full pipeline test
5. [ ] Document first successful video

---

*Assessment complete. Pipeline is viable with cloud LLM for scripts.*
