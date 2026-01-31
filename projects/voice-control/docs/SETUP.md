# Voice Control Setup Guide

Complete setup instructions for Jarvis voice control on Mac.

## Prerequisites

- macOS 12+ (Monterey or later recommended)
- Python 3.10+
- Microphone access
- Internet connection (for cloud STT)

## Quick Setup (30 minutes)

### 1. Get API Keys (10 min)

#### Picovoice (Wake Word)
1. Go to https://console.picovoice.ai/
2. Sign up for free account
3. Copy your Access Key
4. Set environment variable:
   ```bash
   export PICOVOICE_ACCESS_KEY="your-key-here"
   ```

#### Deepgram (Speech-to-Text)
1. Go to https://deepgram.com/
2. Sign up (get $200 free credit)
3. Create API key in dashboard
4. Set environment variable:
   ```bash
   export DEEPGRAM_API_KEY="your-key-here"
   ```

### 2. Install Dependencies (5 min)

```bash
# Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate

# Install packages
pip install pvporcupine pyaudio deepgram-sdk requests

# On Mac, you may need portaudio for pyaudio:
brew install portaudio
```

### 3. Test Components (10 min)

#### Test Wake Word
```bash
cd projects/voice-control/scripts
python test_wake_word.py
# Say "Jarvis" or "Hey Jarvis"
```

#### Test Deepgram
```bash
python test_deepgram.py
# Speak for 5 seconds
```

#### Test Telegram (optional)
```bash
export TELEGRAM_BOT_TOKEN="your-token"
export TELEGRAM_CHAT_ID="your-chat-id"
python test_telegram.py "Hello from voice!"
```

### 4. Run Full System

```bash
# With webhook
export JARVIS_WEBHOOK_URL="https://your-vps.com/webhook/voice"
python jarvis_listener.py

# Or with direct Telegram
python jarvis_listener.py
```

## Detailed Configuration

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `PICOVOICE_ACCESS_KEY` | Yes | Picovoice API key |
| `DEEPGRAM_API_KEY` | Yes* | Deepgram API key |
| `JARVIS_WEBHOOK_URL` | No | n8n webhook URL |
| `TELEGRAM_BOT_TOKEN` | No | Telegram bot token |
| `TELEGRAM_CHAT_ID` | No | Your Telegram chat ID |

*Not required if using `--offline` mode

### Custom Wake Word

To use "Hey Jarvis" instead of just "Jarvis":

1. Go to https://console.picovoice.ai/ppn
2. Create custom wake word "Hey Jarvis"
3. Download the `.ppn` file
4. Use in script:
   ```python
   porcupine = pvporcupine.create(
       access_key=key,
       keyword_paths=["/path/to/hey-jarvis_mac.ppn"]
   )
   ```

### Adjusting Sensitivity

```python
# Higher = more sensitive (more false positives)
# Lower = less sensitive (may miss detections)
sensitivities = [0.7]  # Default

# For noisy environments:
sensitivities = [0.5]

# For quiet environments:
sensitivities = [0.8]
```

## n8n Workflow Setup

### Install n8n on VPS

```bash
# Using Docker (recommended)
docker run -d \
  --name n8n \
  -p 5678:5678 \
  -v ~/.n8n:/home/node/.n8n \
  n8nio/n8n

# Or npm
npm install n8n -g
n8n start
```

### Import Workflow

1. Open n8n at http://your-vps:5678
2. Go to Workflows → Import
3. Upload `config/n8n-workflow.json`
4. Set environment variables in n8n settings:
   - `TELEGRAM_BOT_TOKEN`
   - `TELEGRAM_CHAT_ID`
5. Activate the workflow

### Webhook URL

Your webhook URL will be:
```
https://your-vps.com/webhook/voice
```

Or with n8n's default path:
```
http://your-vps:5678/webhook/voice
```

## Running as Daemon

### Using launchd (Mac)

Create `~/Library/LaunchAgents/com.jarvis.voice.plist`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.jarvis.voice</string>
    <key>ProgramArguments</key>
    <array>
        <string>/path/to/venv/bin/python</string>
        <string>/path/to/jarvis_listener.py</string>
    </array>
    <key>EnvironmentVariables</key>
    <dict>
        <key>PICOVOICE_ACCESS_KEY</key>
        <string>your-key</string>
        <key>DEEPGRAM_API_KEY</key>
        <string>your-key</string>
        <key>JARVIS_WEBHOOK_URL</key>
        <string>https://your-vps.com/webhook/voice</string>
    </dict>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>StandardOutPath</key>
    <string>/tmp/jarvis-voice.log</string>
    <key>StandardErrorPath</key>
    <string>/tmp/jarvis-voice.error.log</string>
</dict>
</plist>
```

Load it:
```bash
launchctl load ~/Library/LaunchAgents/com.jarvis.voice.plist
```

## Troubleshooting

### "No audio devices found"
```bash
# Check microphone permissions
# System Preferences → Security & Privacy → Microphone
# Add Terminal or your IDE
```

### PyAudio installation fails
```bash
brew install portaudio
pip install --global-option='build_ext' --global-option='-I/opt/homebrew/include' --global-option='-L/opt/homebrew/lib' pyaudio
```

### Wake word not detecting
- Check microphone is working: `rec test.wav`
- Increase sensitivity to 0.8
- Speak clearly and at normal volume
- Try different distance from mic

### Deepgram returns empty
- Check API key is valid
- Check internet connection
- Audio may be too quiet - speak louder
- Try longer recording

## Cost Estimate

| Service | Free Tier | Paid |
|---------|-----------|------|
| Picovoice | 3 devices | $0.05/device/month |
| Deepgram | $200 credit | $0.0043/min |
| n8n | Self-hosted free | Cloud from $20/mo |

**Estimated monthly cost: $0-30**
