# Edge LLM Research for BeagleBone/Raspberry Pi
## Small Language Models for Industrial Edge Deployment

**Research Date:** 2026-01-31
**Purpose:** Find optimal LLMs for edge world model deployment

---

## Hardware Constraints

| Device | RAM | CPU | Notes |
|--------|-----|-----|-------|
| BeagleBone Black | 512MB | AM335x 1GHz | Very limited |
| BeagleBone AI-64 | 4GB | Dual Cortex-A72 | Better option |
| Raspberry Pi 5 | 8GB | Quad Cortex-A76 | Recommended |
| Raspberry Pi AI HAT+ 2 | 8GB LPDDR4X | Hailo-10H accelerator | New 2026 option |

**Conclusion:** BeagleBone Black (512MB) is too limited for LLM inference. Consider upgrading to RPi 5 or BeagleBone AI-64.

---

## Recommended Models (2026)

### Tier 1: Ultra-Lightweight (< 1B params)
For basic command parsing and simple responses.

| Model | Params | Quantized Size | RAM Needed |
|-------|--------|----------------|------------|
| **Qwen-0.5B** | 0.5B | ~300MB | 512MB |
| **TinyLlama-1.1B** | 1.1B | ~700MB | 1GB |
| **SmolLM-135M** | 135M | ~100MB | 256MB |

### Tier 2: Small (1-4B params)
For conversational AI and diagnostics.

| Model | Params | Quantized Size | RAM Needed |
|-------|--------|----------------|------------|
| **Phi-3-mini** | 3.8B | ~2.5GB (Q4) | 4GB |
| **Qwen-1.8B** | 1.8B | ~1.2GB | 2GB |
| **Gemma-2B** | 2B | ~1.5GB | 2GB |

### Tier 3: Medium (7-9B params) - RPi 5 Only
For full diagnostic capability.

| Model | Params | Quantized Size | RAM Needed |
|-------|--------|----------------|------------|
| **Llama-3.1-8B** | 8B | ~4.5GB (Q4) | 6GB |
| **Qwen3-8B** | 8B | ~4.5GB (Q4) | 6GB |
| **GLM-4-9B** | 9B | ~5GB (Q4) | 8GB |

---

## Best Options for Our Use Case

### For BeagleBone Black (512MB) - NOT RECOMMENDED
- Too constrained for useful LLM inference
- Consider using for protocol gateway only
- Route LLM queries to VPS via WireGuard

### For Raspberry Pi 5 (8GB) - RECOMMENDED
**Primary:** Phi-3-mini-4k-instruct (Q4_K_M quantized)
- 3.8B parameters
- Strong reasoning for size
- Active community support
- ~2.5GB quantized

**Backup:** Qwen-1.8B
- Excellent multilingual (Spanish!)
- Smaller footprint
- Good for constrained scenarios

---

## Deployment Stack

```
┌─────────────────────────────────────┐
│           Ollama                    │
│   (Model serving framework)         │
├─────────────────────────────────────┤
│   llama.cpp / llama-cpp-python      │
│   (Inference engine for ARM)        │
├─────────────────────────────────────┤
│   GGUF Quantized Models             │
│   (Q4_K_M for best size/quality)    │
└─────────────────────────────────────┘
```

**Installation on RPi 5:**
```bash
# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Pull Phi-3 mini
ollama pull phi3:mini

# Test
ollama run phi3:mini "What causes a conveyor jam?"
```

---

## Hybrid Architecture Recommendation

Given BeagleBone limitations, use hybrid approach:

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│ BeagleBone  │────▶│  WireGuard  │────▶│    VPS      │
│ (Gateway)   │     │   Tunnel    │     │  (AI Brain) │
└─────────────┘     └─────────────┘     └─────────────┘
     │                                        │
     │ Protocol Layer                         │ LLM Layer
     │ - Modbus read                          │ - Phi-3/Claude
     │ - Data collection                      │ - World model
     │ - Local caching                        │ - Diagnostics
```

**When Internet Available:** Route to VPS for full AI capability
**When Air-Gapped:** Use tiny local model for basic responses

---

## Performance Expectations (RPi 5)

| Model | Tokens/sec | First Response |
|-------|------------|----------------|
| Qwen-0.5B | 20-30 t/s | ~500ms |
| Phi-3-mini Q4 | 8-15 t/s | ~1-2s |
| Llama-3.1-8B Q4 | 3-6 t/s | ~3-5s |

For real-time maintenance diagnostics, Phi-3-mini is the sweet spot.

---

## Action Items

1. **For Tuesday Demo:** Use VPS for LLM (faster development)
2. **Future:** Upgrade to RPi 5 for true edge deployment
3. **Keep BeagleBone** for protocol gateway only
4. **Install Ollama** on RPi 5 when available

---

## References

- ARM Learning Path: https://learn.arm.com/learning-paths/embedded-and-microcontrollers/raspberry-pi-smart-home/
- MLSysBook SLM Guide: https://mlsysbook.ai/contents/labs/raspi/llm/llm.html
- llama.cpp: https://github.com/ggml-org/llama.cpp
- Ollama: https://ollama.com
