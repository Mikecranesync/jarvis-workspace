# ShopTalk Edge AI

**Industrial equipment diagnostics that run anywhere, speak any language.**

## Vision

A $50 device that:
- Connects to any PLC/sensor
- Runs AI diagnostics locally (no cloud)
- Speaks maintenance insights in any language
- Learns from real equipment behavior

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    ShopTalk Edge                        │
├─────────────────────────────────────────────────────────┤
│  ┌─────────┐  ┌─────────────┐  ┌─────────────────────┐ │
│  │  Data   │→ │ World Model │→ │ Inference Engine    │ │
│  │ Adapter │  │  (Trained)  │  │ (Local Predictions) │ │
│  └─────────┘  └─────────────┘  └──────────┬──────────┘ │
│       ↑                                    ↓            │
│  ┌─────────┐                    ┌─────────────────────┐ │
│  │   PLC   │                    │   Voice Interface   │ │
│  │ Sensors │                    │ (Multi-language TTS)│ │
│  └─────────┘                    └─────────────────────┘ │
└─────────────────────────────────────────────────────────┘
```

## Components

### 1. World Model (`src/model/`)
- Learns normal equipment behavior from data
- Detects anomalies by comparing current vs expected state
- Lightweight enough for edge deployment

### 2. Inference Engine (`src/inference/`)
- Runs world model predictions in real-time
- Generates diagnostic insights
- Works offline (no internet required)

### 3. Voice Interface (`src/voice/`)
- Text-to-speech for hands-free operation
- Multi-language support (Spanish, English, etc.)
- Wake word detection (future)

### 4. API Server (`src/api/`)
- REST endpoints for integration
- WebSocket for real-time updates
- Mobile app connectivity

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run with simulated data
python -m shoptalk.main --simulate

# Run with real PLC
python -m shoptalk.main --host 192.168.1.100 --port 502
```

## Tuesday Demo Goals

1. BeagleBone/RPi connected to Factory I/O via Modbus
2. World model trained on normal operation
3. Inject fault → model detects anomaly
4. Voice announces diagnosis in Spanish

## Files

- `src/model/world_model.py` - Core world model
- `src/model/trainer.py` - Training pipeline
- `src/inference/engine.py` - Real-time inference
- `src/voice/tts.py` - Text-to-speech
- `src/api/server.py` - REST API
- `config/default.yaml` - Configuration
