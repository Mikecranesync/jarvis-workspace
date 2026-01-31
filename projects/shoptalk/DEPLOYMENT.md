# ShopTalk Deployment Guide

## Quick Start

### 1. Clone and Install
```bash
git clone <repo>
cd shoptalk
pip install -r requirements.txt
```

### 2. Run Demo (Simulated Data)
```bash
python demo.py
```

### 3. Run Full System
```bash
python main.py --config config/default.yaml
```

---

## Deployment Options

### Option A: Desktop/Server (Development)
- Python 3.9+
- 4GB+ RAM
- Any modern CPU

```bash
# Install
pip install -r requirements.txt

# Run with simulated sensors
python main.py --simulate

# Run with real Modbus connection
python main.py --modbus-host 192.168.1.100 --modbus-port 502
```

### Option B: Edge Device (Production)

#### Supported Devices:
| Device | RAM | Recommended Model |
|--------|-----|-------------------|
| Raspberry Pi 5 | 8GB | Qwen3-1.7B (Q4) |
| Raspberry Pi 4 | 4GB | Qwen3-0.6B (Q4) |
| BeagleBone AI-64 | 4GB | Qwen3-0.6B (Q4) |
| Jetson Nano | 4GB | Phi-4-mini (Q4) |

#### Edge Installation:
```bash
# On edge device
curl -fsSL https://ollama.com/install.sh | sh
ollama pull qwen2:0.5b

# Clone ShopTalk
git clone <repo>
cd shoptalk
pip install -r requirements-edge.txt

# Run
python main.py --edge --model qwen2:0.5b
```

### Option C: Docker
```bash
docker build -t shoptalk .
docker run -p 8000:8000 -p 8765:8765 shoptalk
```

---

## Configuration

### Environment Variables
```bash
# API Settings
SHOPTALK_HOST=0.0.0.0
SHOPTALK_PORT=8000

# Modbus Connection
MODBUS_HOST=192.168.1.100
MODBUS_PORT=502

# LLM Settings
OLLAMA_HOST=http://localhost:11434
SHOPTALK_MODEL=qwen2:1.5b

# Voice Settings (optional)
ELEVENLABS_API_KEY=your_key
TTS_ENABLED=true
```

### Config File (config/default.yaml)
```yaml
equipment:
  name: "Conveyor Line 1"
  type: conveyor
  
sensors:
  motor_current:
    address: 40001
    unit: A
    normal_range: [3.5, 5.5]
  motor_speed:
    address: 40002
    unit: RPM
    normal_range: [1400, 1600]
  temperature:
    address: 40003
    unit: C
    normal_range: [40, 55]
  belt_speed:
    address: 40004
    unit: percent
    normal_range: [75, 85]

alerts:
  telegram_chat_id: "your_chat_id"
  whatsapp_number: "+1234567890"
```

---

## API Endpoints

### REST API (Port 8000)

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Health check |
| `/status` | GET | Current sensor readings |
| `/diagnose` | POST | Get AI diagnosis |
| `/ask` | POST | Ask a question |
| `/speak` | POST | Text-to-speech |

### WebSocket (Port 8000/ws)
```javascript
// Connect
ws = new WebSocket('ws://localhost:8000/ws');

// Receive real-time updates
ws.onmessage = (event) => {
    const data = JSON.parse(event.data);
    console.log(data.readings);
    console.log(data.alerts);
};
```

---

## Monitoring Setup

### 1. WhatsApp Integration
```bash
# Set environment
export WHATSAPP_API_URL=https://your-whatsapp-api
export WHATSAPP_TOKEN=your_token

# Test
python -c "from src.voice.tts import send_whatsapp; send_whatsapp('+1234567890', 'Test')"
```

### 2. Telegram Integration
```bash
# Already configured via Clawdbot
# Messages route through the gateway
```

### 3. Email Alerts
```yaml
# In config
alerts:
  email:
    enabled: true
    smtp_host: smtp.gmail.com
    recipients:
      - maintenance@factory.com
```

---

## Troubleshooting

### "No module named 'src'"
```bash
# Add to PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

### "Connection refused" on Modbus
- Check device IP and port
- Verify firewall allows connection
- Test with `mbpoll` tool

### LLM responses are slow
- Use smaller quantized model (Q4_K_M)
- Reduce context length
- Enable GPU acceleration if available

### High CPU on edge device
- Reduce polling frequency
- Use batch inference
- Consider cloud offload for complex queries

---

## Production Checklist

- [ ] Configure Modbus connection
- [ ] Test all sensor readings
- [ ] Set up alert channels (WhatsApp/Telegram)
- [ ] Configure LLM model
- [ ] Test voice output
- [ ] Set up monitoring dashboard
- [ ] Configure log rotation
- [ ] Set up auto-restart (systemd)
- [ ] Document equipment-specific thresholds
- [ ] Train operators on usage

---

## Support

- Documentation: `/docs`
- Issues: GitHub Issues
- Community: Discord

Built with ❤️ by FactoryLM
