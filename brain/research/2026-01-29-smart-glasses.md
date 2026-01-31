# Research: Open Source Smart Glasses for Industrial AI

**Date:** 2026-01-29  
**Triggered by:** Mike's video reference to Dennis Hassabis/Project Astra glasses

## Context

Google's Project Astra (Demis Hassabis demo) shows AI-powered smart glasses with real-time visual understanding. Can we build something similar for industrial maintenance use cases?

## Top Open Source Projects Found

### 1. OpenSource-Ai-Glasses (BEST FIT 🎯)
**URL:** https://github.com/Iam5tillLearning/OpenSource-Ai-Glasses

**Why it fits:**
- Specifically designed for **industrial and medical applications**
- Mentions **maintenance personnel** use case
- Can display SOPs as AR instructions
- Linux-based, has SDK
- Active development (v0.6.2 as of Jan 2026)

**Specs:**
- 640×480 monocular display (30° FOV)
- 1080P camera
- WiFi + Bluetooth 5.3
- Only 43g weight
- ~$100-150 dev kit on eBay

**Industrial Features:**
- Remote expert assistance (display materials from experts)
- Step-by-step AR instructions for SOPs
- Photo/video capture for documentation
- Voice interaction

### 2. OpenGlass / Omi
**URL:** https://github.com/BasedHardware/omi (moved from OpenGlass)

**Why it fits:**
- Turn any glasses into smart glasses for ~$25
- Object identification
- Translation
- Memory/recall features

**Specs:**
- ESP32-S3 based
- Camera module
- Battery powered
- 3D printed mount

### 3. Brilliant Labs Halo
**URL:** https://brilliant.xyz/products/halo

**Why it fits:**
- Open source AI glasses
- Conversational AI agent with memory
- Commercial quality design

### 4. Wearable Intelligence System
**URL:** https://github.com/topics/smartglasses (various repos)

**Why it fits:**
- Framework for smart glasses apps
- Voice commands, speech recognition
- Computer vision, NLP
- Database, cloud connection

## Recommendation

**Fork OpenSource-Ai-Glasses** for FactoryLM industrial use case:

1. It's specifically designed for maintenance/industrial
2. Has SDK for customization
3. Active community
4. Hardware dev kit available
5. Linux-based = easy integration with our stack

## Integration Plan

```
FactoryLM Smart Glasses
├── Hardware: OpenSource-Ai-Glasses dev kit
├── Software: Fork + customize SDK
├── AI Backend: Connect to our Gemini/Perplexity stack
├── CMMS Integration: Show work orders on display
└── PLC Copilot: Visual equipment diagnostics
```

## Use Cases for FactoryLM

1. **Hands-free work order viewing** — See instructions while working
2. **Visual equipment inspection** — AI identifies issues
3. **Remote expert assistance** — Expert sees what tech sees
4. **Documentation** — Auto-capture photos for work orders
5. **Parts identification** — Scan part, get inventory info
6. **Safety alerts** — Real-time hazard detection

## Next Steps

1. [ ] Fork OpenSource-Ai-Glasses to factorylm repo
2. [ ] Order dev kit (~$100-150)
3. [ ] Prototype basic CMMS integration
4. [ ] Test with real maintenance scenario

---

*Research conducted using Perplexity + web search*
*Constitutional Amendment I applied: Open Source First*
