# Brilliant Labs Halo Integration

Guide for integrating Jarvis voice control with Brilliant Labs Halo smart glasses.

## About Halo

Brilliant Labs Halo is an open-source smart glasses platform with:
- Built-in Noa AI assistant
- "Vibe Mode" for custom apps
- Open hardware/firmware/software
- Can forward voice to external APIs

**Key Advantage:** Only smart glasses that allows routing voice to external webhooks.

## Integration Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    HALO GLASSES                              │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐     │
│  │  Microphone │ →  │  Noa AI or  │ →  │   Webhook   │     │
│  │             │    │  Vibe Mode  │    │   Forward   │     │
│  └─────────────┘    └─────────────┘    └──────┬──────┘     │
└──────────────────────────────────────────────┼──────────────┘
                                               │
                                               ▼
┌─────────────────────────────────────────────────────────────┐
│                    YOUR VPS                                  │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐     │
│  │   Webhook   │ →  │  Deepgram   │ →  │  Clawdbot   │     │
│  │   Receiver  │    │    STT      │    │   /Claude   │     │
│  └─────────────┘    └─────────────┘    └──────┬──────┘     │
└──────────────────────────────────────────────┼──────────────┘
                                               │
                                               ▼
┌─────────────────────────────────────────────────────────────┐
│                    RESPONSE                                  │
│  ┌─────────────┐    ┌─────────────┐                         │
│  │ ElevenLabs  │ →  │   Halo      │                         │
│  │    TTS      │    │  Speakers   │                         │
│  └─────────────┘    └─────────────┘                         │
└─────────────────────────────────────────────────────────────┘
```

## Prerequisites

- Brilliant Labs Halo glasses
- Noa companion app (iOS/Android)
- Brilliant Labs account
- Your VPS with webhook endpoint

## Setup Options

### Option 1: Vibe Mode Custom App

Vibe Mode allows creating custom apps that can:
- Capture voice input
- Process locally or forward to API
- Play audio responses

**Steps:**

1. Install Vibe Mode SDK:
   ```bash
   npm install @brilliantlabs/vibe-sdk
   ```

2. Create custom Jarvis app:
   ```javascript
   // jarvis-vibe.js
   import { Vibe } from '@brilliantlabs/vibe-sdk';
   
   const vibe = new Vibe({
     name: 'Jarvis',
     wakeWord: 'hey jarvis'
   });
   
   vibe.on('voiceInput', async (audio) => {
     // Forward to your webhook
     const response = await fetch('https://your-vps.com/webhook/voice', {
       method: 'POST',
       body: audio,
       headers: { 'Content-Type': 'audio/wav' }
     });
     
     const result = await response.json();
     
     // Play response audio
     if (result.audioUrl) {
       vibe.playAudio(result.audioUrl);
     }
   });
   
   vibe.start();
   ```

3. Deploy to glasses via Noa app

### Option 2: Noa API Integration

If Brilliant Labs exposes Noa API for custom integrations:

1. Register your webhook in Noa dashboard
2. Configure trigger phrase
3. Noa forwards voice to your endpoint

**Check Brilliant Labs documentation for current API availability.**

## Webhook Endpoint for Glasses

Create a dedicated endpoint that handles audio from Halo:

```python
# webhook_halo.py
from fastapi import FastAPI, UploadFile
from deepgram import Deepgram
import httpx

app = FastAPI()

@app.post("/webhook/halo")
async def receive_halo_audio(audio: UploadFile):
    # Read audio
    audio_data = await audio.read()
    
    # Transcribe with Deepgram
    dg = Deepgram(os.environ["DEEPGRAM_API_KEY"])
    response = await dg.transcription.prerecorded(
        {"buffer": audio_data, "mimetype": "audio/wav"},
        {"punctuate": True, "model": "nova-2"}
    )
    
    text = response["results"]["channels"][0]["alternatives"][0]["transcript"]
    
    # Forward to Telegram/Clawdbot
    async with httpx.AsyncClient() as client:
        await client.post(
            f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
            json={"chat_id": CHAT_ID, "text": f"🕶️ Halo: {text}"}
        )
    
    # Wait for Jarvis response and return audio URL
    # (Implementation depends on your response mechanism)
    
    return {"status": "received", "text": text}
```

## Audio Response to Glasses

To send audio back to Halo:

### Option A: Direct Audio URL
Return a URL to the TTS audio file that Halo can play:

```python
return {
    "status": "ok",
    "audioUrl": "https://your-vps.com/audio/response-123.mp3"
}
```

### Option B: Streaming Response
For real-time responses, use WebSocket streaming:

```python
@app.websocket("/ws/halo")
async def halo_websocket(websocket: WebSocket):
    await websocket.accept()
    
    while True:
        # Receive audio from glasses
        audio = await websocket.receive_bytes()
        
        # Process and get response
        response_audio = await process_and_generate_response(audio)
        
        # Stream back to glasses
        await websocket.send_bytes(response_audio)
```

## Testing Without Glasses

Before glasses arrive, test the flow:

```bash
# Simulate Halo sending audio
curl -X POST https://your-vps.com/webhook/halo \
  -H "Content-Type: audio/wav" \
  --data-binary @test-audio.wav
```

## Considerations

### Latency
- Halo → VPS: ~100-200ms
- Deepgram STT: ~300ms
- Claude processing: ~500-2000ms
- ElevenLabs TTS: ~500ms
- VPS → Halo: ~100-200ms
- **Total: ~1.5-3 seconds**

### Battery
- Continuous listening drains battery
- Consider push-to-talk or wake word
- Optimize audio quality (lower bitrate for faster upload)

### Privacy
- Audio processed on your VPS
- Can use local Whisper for offline STT
- No third-party access to conversations

## Resources

- [Brilliant Labs GitHub](https://github.com/brilliantlabs)
- [Noa Documentation](https://docs.brilliant.xyz/)
- [Vibe Mode Guide](https://docs.brilliant.xyz/vibe)
- [Hardware Specs](https://brilliant.xyz/products/halo)

## Status

**Current:** Waiting for Halo delivery (Order #911658)

**Next Steps:**
1. Unbox and pair glasses
2. Explore Vibe Mode SDK
3. Create Jarvis Vibe app
4. Test end-to-end integration
