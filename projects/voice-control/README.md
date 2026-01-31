# Voice Control System for Jarvis

> "Hey Jarvis" → Speak → AI Responds via Voice

Hands-free voice control using wake word detection, real-time speech-to-text, and Clawdbot integration.

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         INPUT LAYER                              │
├─────────────────────────────────────────────────────────────────┤
│  Mac (Porcupine)  │  Halo Glasses  │  Phone (Telegram voice)    │
└────────┬──────────┴───────┬────────┴────────────┬───────────────┘
         │                  │                     │
         ▼                  ▼                     ▼
┌─────────────────────────────────────────────────────────────────┐
│                    WAKE WORD DETECTION                           │
│              Picovoice Porcupine ("Hey Jarvis")                  │
│              Runs locally on Mac - no cloud needed               │
└─────────────────────────┬───────────────────────────────────────┘
                          │ Audio stream
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│                    SPEECH-TO-TEXT                                │
│              Deepgram API (<300ms latency)                       │
│              OR local Whisper for offline                        │
└─────────────────────────┬───────────────────────────────────────┘
                          │ Transcribed text
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│                    n8n WEBHOOK                                   │
│              Routes to Telegram or direct API                    │
└─────────────────────────┬───────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│                    CLAWDBOT / TELEGRAM                           │
│              Jarvis session processes command                    │
└─────────────────────────┬───────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│                    TEXT-TO-SPEECH                                │
│              ElevenLabs (already configured)                     │
└─────────────────────────┬───────────────────────────────────────┘
                          │ Audio
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│                    OUTPUT                                        │
│              Mac speakers / Phone / Halo glasses                 │
└─────────────────────────────────────────────────────────────────┘
```

## Components

### 1. Wake Word Detection (Porcupine)
- **Library:** Picovoice Porcupine
- **Wake Word:** "Hey Jarvis" (custom, created via web console)
- **Runs:** Locally on Mac (no cloud needed)
- **Cost:** Free tier (3 devices)

### 2. Speech-to-Text (Deepgram)
- **Service:** Deepgram real-time API
- **Latency:** <300ms
- **Cost:** $0.26/hour ($200 free credit)
- **Fallback:** Local Whisper via whisper.cpp

### 3. Integration (n8n)
- **Platform:** n8n (self-hosted on VPS)
- **Webhooks:** Receive transcribed text
- **Routes:** To Telegram bot or direct Clawdbot API
- **Cost:** Free (self-hosted)

### 4. Response (TTS)
- **Service:** ElevenLabs (already configured in Clawdbot)
- **Output:** Voice messages via Telegram or audio playback

## Quick Start

### Prerequisites
- macOS with microphone access
- Python 3.10+
- Picovoice account (free): https://console.picovoice.ai/
- Deepgram account (free $200 credit): https://deepgram.com/

### Installation (Mac)

```bash
# 1. Install dependencies
pip install pvporcupine pyaudio deepgram-sdk requests

# 2. Set environment variables
export PICOVOICE_ACCESS_KEY="your-key-here"
export DEEPGRAM_API_KEY="your-key-here"
export JARVIS_WEBHOOK_URL="https://your-vps.com/webhook/voice"

# 3. Run the listener
python scripts/jarvis_listener.py
```

### 30-Minute MVP

1. **Test Porcupine (10 min)**
   ```bash
   python scripts/test_wake_word.py
   # Say "Hey Jarvis" - should print detection
   ```

2. **Test Deepgram (10 min)**
   ```bash
   python scripts/test_deepgram.py
   # Speak - should print transcription
   ```

3. **Test Telegram Send (10 min)**
   ```bash
   python scripts/test_telegram.py "Hello from voice"
   # Should appear in your Telegram chat
   ```

4. **Full Integration (1-2 hours)**
   - Set up n8n workflow
   - Connect all components
   - Test end-to-end

## Files

```
projects/voice-control/
├── README.md                 # This file
├── scripts/
│   ├── jarvis_listener.py    # Main voice control script
│   ├── test_wake_word.py     # Test Porcupine
│   ├── test_deepgram.py      # Test STT
│   └── test_telegram.py      # Test Telegram send
├── config/
│   ├── .env.example          # Environment variables template
│   └── n8n-workflow.json     # n8n workflow export
└── docs/
    ├── SETUP.md              # Detailed setup guide
    └── HALO_INTEGRATION.md   # Brilliant Labs Halo guide
```

## Cost Estimate

| Component | Monthly Cost |
|-----------|--------------|
| Porcupine | $0 (free tier) |
| Deepgram | $0-30 ($200 credit) |
| n8n | $0 (self-hosted) |
| ElevenLabs | $0-5 (free tier) |
| **Total** | **$0-35/month** |

## Roadmap

- [x] Research and architecture
- [ ] Basic wake word + STT script
- [ ] n8n webhook integration
- [ ] Telegram forwarding
- [ ] End-to-end testing
- [ ] Brilliant Labs Halo integration
- [ ] Continuous listening daemon

## References

- [Picovoice Porcupine](https://picovoice.ai/platform/porcupine/)
- [Deepgram API](https://developers.deepgram.com/)
- [n8n Workflows](https://n8n.io/)
- [whisper.cpp](https://github.com/ggerganov/whisper.cpp)
