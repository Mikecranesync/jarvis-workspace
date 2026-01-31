# Voice Control Stack Research

**Source:** Perplexity Pro Deep Research
**Date:** 2026-01-31
**Goal:** Hands-free "Hey Jarvis" → Claude → Voice response

---

## Quick Recommendation

### Winning Stack
```
Mac/Phone → Porcupine wake word → n8n webhook → Deepgram STT → Telegram/Clawdbot → Claude → TTS → Audio
```

### Cost: $5-40/month
| Component | Cost |
|-----------|------|
| Porcupine | $0-5/mo (free tier = 3 devices) |
| Deepgram | $0-30/mo ($200 free credit) |
| n8n | $0 (self-hosted) |
| Telegram | $0 |
| TTS (ElevenLabs) | $0-5/mo |

### Setup Time: 2-4 hours

---

## 1. Wake Word Detection

### Winner: Picovoice Porcupine ⭐

| Solution | Ease | Custom Words | Notes |
|----------|------|--------------|-------|
| **Porcupine** | 5/5 | Web console, seconds | Free tier covers use case |
| openWakeWord | 2/5 | Requires ML training | More complex |
| Rhasspy | 2/5 | Full stack, complex | Overkill |

**Why Porcupine:**
- Custom "Hey Jarvis" created in seconds via web console
- Easiest setup
- Free tier sufficient
- Good documentation

---

## 2. Speech-to-Text

### Winner: Deepgram (Real-time) or Local Whisper (Privacy)

| Solution | Latency | Cost | Best For |
|----------|---------|------|----------|
| **Deepgram** | <300ms | $0.26/hr | Real-time, fastest |
| Local Whisper | 1-3s | Free | Privacy, offline |
| Whisper API | 2-5s | $0.006/min | Not real-time |
| AssemblyAI | 500ms+ | $0.37/hr | Good but pricier |

**Recommendation:** 
- Deepgram for real-time responsiveness
- Local Whisper (whisper.cpp) for offline/privacy on Mac M3

---

## 3. Integration: n8n Workflows ⭐

**Why n8n:**
- Visual workflow builder (no coding)
- Native Telegram integration built-in
- Self-hosted on VPS (free)
- 10x easier than custom Python

**Flow:**
1. Webhook receives audio/text
2. Route to Deepgram for transcription
3. Forward to Telegram (Clawdbot picks up)
4. Response back via webhook
5. TTS and playback

---

## 4. Brilliant Labs Halo: CAN Route to External APIs ✅

**Key findings:**
- Fully open source (hardware + firmware + software)
- "Vibe Mode" lets you create custom apps
- Can forward voice to your VPS webhook
- **Only smart glasses that allows this**

**Integration plan:**
1. Create custom Vibe app
2. Route voice to VPS webhook
3. Process via Claude
4. Return audio response

---

## 5. Complete Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    INPUT DEVICES                         │
├─────────────────────────────────────────────────────────┤
│  Mac (Porcupine)  │  Phone (Telegram)  │  Halo Glasses  │
└────────┬──────────┴────────┬───────────┴───────┬────────┘
         │                   │                   │
         ▼                   ▼                   ▼
┌─────────────────────────────────────────────────────────┐
│                    n8n WEBHOOKS                          │
│              (Self-hosted on DO VPS)                     │
└────────────────────────┬────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────┐
│                    DEEPGRAM STT                          │
│              (<300ms transcription)                      │
└────────────────────────┬────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────┐
│                 TELEGRAM / CLAWDBOT                      │
│              (Routes to Claude session)                  │
└────────────────────────┬────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────┐
│                    CLAUDE OPUS                           │
│              (Process command)                           │
└────────────────────────┬────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────┐
│                 TTS (ElevenLabs)                         │
│              (Generate voice response)                   │
└────────────────────────┬────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────┐
│                   AUDIO PLAYBACK                         │
│        Mac speakers / Phone / Halo glasses               │
└─────────────────────────────────────────────────────────┘
```

---

## 30-Minute MVP

### Step 1: Install Porcupine (10 min)
```bash
pip install pvporcupine
# Run demo with built-in "Jarvis" keyword
```

### Step 2: Test Deepgram (10 min)
```bash
# Sign up for free $200 credit
# Test transcription API
```

### Step 3: Telegram Test (10 min)
```bash
# Verify Clawdbot receives messages
# Test response routing
```

### Step 4: Connect with n8n (1-2 hours)
- Create webhook workflow
- Wire up components
- Test end-to-end

---

## Next Steps

1. [ ] Set up Porcupine on Mac with custom "Hey Jarvis"
2. [ ] Create Deepgram account ($200 free credit)
3. [ ] Install n8n on VPS
4. [ ] Create voice → Telegram workflow
5. [ ] Test Halo glasses integration when they arrive

---

## Resources

- Porcupine: https://picovoice.ai/platform/porcupine/
- Deepgram: https://deepgram.com/
- n8n: https://n8n.io/
- whisper.cpp: https://github.com/ggerganov/whisper.cpp
- Brilliant Labs: https://brilliant.xyz/

---

*Research from Perplexity Pro, compiled 2026-01-31*
