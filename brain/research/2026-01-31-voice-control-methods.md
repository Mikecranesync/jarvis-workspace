# Voice Control Methods for Jarvis

**Date:** 2026-01-31
**Request:** Mike asked for ways to control Jarvis more effectively through voice

---

## Category 1: Desktop Voice Input (Global)

### VoiceMode MCP for Claude Code ⭐ RECOMMENDED
- **URL:** https://getvoicemode.com/
- **Install:** `voicemode whisper install` + `voicemode kokoro install`
- Natural voice conversations with Claude
- Local processing = private
- OpenAI API compatible

### Whispering Desktop ⭐ HIGHLY RATED
- **GitHub:** https://github.com/braden-w/whispering/releases
- Global hotkey activation
- Auto-copy to clipboard
- Auto-paste where cursor is
- Works across ALL applications

### Claude's Voice Input
- **GitHub:** https://github.com/420247jake/claudes-voice-input
- Hold F9, speak, release
- Text appears in Claude automatically
- Uses OpenAI Whisper locally

### Claudet (Chrome Extension)
- **GitHub:** https://github.com/unclecode/claudet
- Adds microphone button to Claude.ai
- Speech-to-text via Whisper (Groq or OpenAI)

### Wispr Flow
- **URL:** https://wisprflow.ai/use-cases/claude
- Dictate prompts to Claude

---

## Category 2: Telegram Voice Messages

### n8n Workflow
- **Template:** https://n8n.io/workflows/4528-transcribe-voice-messages-from-telegram-using-openai-whisper-1/
- Telegram receives voice → Whisper transcribes → AI responds

### Self-Hosted Transcription Bot
- **GitHub:** https://github.com/soberhacker/telegram-speech-recognition-bot
- Offline transcription using Whisper or Vosk
- Multi-language support

### TranscribeMe Bot
- **URL:** https://voix-int.netlify.app/
- Forward any voice message → get transcription

---

## Category 3: Wake Word Detection (Always Listening)

### Picovoice Porcupine ⭐ INDUSTRY STANDARD
- **GitHub:** https://github.com/Picovoice/porcupine
- **Install:** `pip install pvporcupine`
- Custom wake words (e.g., "Hey Jarvis")
- Works on Raspberry Pi, Mac, Windows, Linux
- Deep learning powered, low power

### openWakeWord (Fully Open Source)
- **GitHub:** https://github.com/dscripka/openWakeWord
- No API keys needed
- Fully local
- Train custom wake words

### Rhasspy (Home Assistant)
- **Docs:** https://rhasspy.readthedocs.io/
- Full offline voice assistant
- Wake word → STT → Intent → Action
- Supports Porcupine wake words

---

## Category 4: Smart Glasses (Brilliant Labs Halo)

Mike's Halo glasses include:
- Noa AI assistant with voice commands
- Camera for visual context
- "Narrative" memory system
- Whisper integration
- Potential API/webhook integration

---

## Category 5: Mobile Apps

- ChatGPT Voice Mode (example of target UX)
- Saner.AI (multi-model voice assistant)

---

## GitHub Repos to Fork

| Repo | Purpose | URL |
|------|---------|-----|
| Picovoice/porcupine | Wake word | https://github.com/Picovoice/porcupine |
| dscripka/openWakeWord | Open source wake word | https://github.com/dscripka/openWakeWord |
| braden-w/whispering | Desktop voice | https://github.com/braden-w/whispering |
| unclecode/claudet | Claude extension | https://github.com/unclecode/claudet |
| jdpsc/claude-code-voice | Claude Code voice | https://github.com/jdpsc/claude-code-voice |
| soberhacker/telegram-speech-recognition-bot | Telegram | https://github.com/soberhacker/telegram-speech-recognition-bot |

---

## Recommended Architecture

```
┌────────────────────────────────┐
│  WAKE WORD: Porcupine          │
│  "Hey Jarvis"                  │
└───────────────┬────────────────┘
                ↓
┌────────────────────────────────┐
│  SPEECH-TO-TEXT: Whisper       │
│  Local or API                  │
└───────────────┬────────────────┘
                ↓
┌────────────────────────────────┐
│  ROUTING: Telegram/Clawdbot    │
│  or direct API                 │
└───────────────┬────────────────┘
                ↓
┌────────────────────────────────┐
│  AI: Jarvis                    │
│  Process + respond             │
└───────────────┬────────────────┘
                ↓
┌────────────────────────────────┐
│  TEXT-TO-SPEECH: TTS           │
│  Response back                 │
└────────────────────────────────┘
```

---

## Implementation Priority

1. **Immediate:** Continue Telegram voice messages
2. **Quick (30 min):** Whispering Desktop
3. **Medium (2-4h):** n8n workflow for Telegram
4. **Advanced (day):** Porcupine wake word
5. **Future:** Halo glasses integration
