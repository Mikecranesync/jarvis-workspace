# BeagleBone Edge World Model - Complete Project Scope
## Industrial AI Brain - "ShopTalk" / "FactoryGenius"

**Priority:** P-1 (First project using The Automaton)
**Status:** Flash in progress, full build by Tuesday
**Target:** Demo Day - Tuesday 2026-02-04

---

## The Vision

> *"A pocket-sized industrial AI expert. Plug it into any factory network. WhatsApp it. Ask what's wrong in any language. It answers. No internet required."*

**The Venezuela Story:**
> "Helping rebuild Venezuela's oil infrastructure with AI that works offline, speaks Spanish, and costs $50."

---

## Product Capabilities

| Feature | Description |
|---------|-------------|
| **Protocol Bridge** | Modbus, S7, EtherNet/IP, OPC-UA |
| **Local AI** | Small LLM for diagnostics (1-7B params) |
| **World Model** | Predicts equipment behavior |
| **Multi-language** | Spanish, English, Portuguese, etc. |
| **Air-gapped** | Works with zero internet |
| **WhatsApp Interface** | Just text/call a phone number |

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    BEAGLEBONE EDGE                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────────────────────────────────────────────────┐  │
│  │                   AI LAYER                            │  │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐   │  │
│  │  │ Small LLM   │  │ World Model │  │ Translator  │   │  │
│  │  │ (Phi-3/Qwen)│  │ (PyTorch)   │  │ (Multi-lang)│   │  │
│  │  └─────────────┘  └─────────────┘  └─────────────┘   │  │
│  └──────────────────────────────────────────────────────┘  │
│                           │                                 │
│  ┌──────────────────────────────────────────────────────┐  │
│  │                 PROTOCOL LAYER                        │  │
│  │  ┌────────┐  ┌────────┐  ┌────────┐  ┌────────┐     │  │
│  │  │ Modbus │  │  S7    │  │ EIP    │  │ OPC-UA │     │  │
│  │  └────────┘  └────────┘  └────────┘  └────────┘     │  │
│  └──────────────────────────────────────────────────────┘  │
│                           │                                 │
│  ┌──────────────────────────────────────────────────────┐  │
│  │               COMMUNICATION LAYER                     │  │
│  │  ┌────────────┐  ┌────────────┐  ┌────────────┐     │  │
│  │  │  WhatsApp  │  │    VPN     │  │   Local    │     │  │
│  │  │  (Twilio)  │  │ (WireGuard)│  │   Web UI   │     │  │
│  │  └────────────┘  └────────────┘  └────────────┘     │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                             │
└─────────────────────────────────────────────────────────────┘
         │                    │                    │
    ┌────▼────┐          ┌────▼────┐          ┌────▼────┐
    │   PLC   │          │  Cloud  │          │  Phone  │
    │ Network │          │ (opt.)  │          │ WhatsApp│
    └─────────┘          └─────────┘          └─────────┘
```

---

## Hardware

| Component | Spec | Cost |
|-----------|------|------|
| BeagleBone Black | AM335x 1GHz, 512MB RAM | ~$55 |
| MicroSD Card | 32GB Class 10 | ~$10 |
| Enclosure | Aluminum case (future) | ~$15 |
| Power | 5V 2A USB or barrel | included |
| **Total** | | **~$80** |

**Alternative:** Raspberry Pi 5 (more power, more cost)

---

## Software Stack

| Layer | Technology |
|-------|------------|
| OS | Debian 12 (Bookworm) |
| Runtime | Python 3.11 |
| AI Inference | ONNX Runtime / llama.cpp |
| World Model | PyTorch (trained on server, deployed here) |
| Protocols | pymodbus, python-snap7, opcua |
| VPN | WireGuard |
| Web UI | FastAPI + HTMX |

---

## Implementation Phases

### Phase 1: Infrastructure (Friday Night → Saturday AM)
- [x] Flash Debian to eMMC (in progress)
- [ ] SSH access working
- [ ] WireGuard VPN connected
- [ ] Jarvis remote access confirmed
- [ ] Basic system packages installed

**Deliverables:**
- BeagleBone accessible via `ssh debian@192.168.7.2`
- WireGuard tunnel to VPS at 10.100.0.10
- Jarvis can SSH in remotely

### Phase 2: Data Pipeline (Saturday)
- [ ] Factory I/O connected to PLC
- [ ] PLC connected to BeagleBone (Modbus/Ethernet)
- [ ] Data logger capturing PLC states
- [ ] 5 scenarios run and captured

**Scenarios:**
| # | Scenario | Duration | Purpose |
|---|----------|----------|---------|
| 1 | Normal operation | 30 min | Baseline behavior |
| 2 | Speed 80% | 15 min | Under-speed patterns |
| 3 | Speed 120% | 15 min | Over-speed patterns |
| 4 | Speed 140% | 15 min | Stress patterns |
| 5 | Sensor delay | 15 min | Degradation patterns |
| 6 | Jam condition | 10 min | Failure signatures |
| 7 | Overload | 10 min | Limit behaviors |

**Deliverables:**
- `data/raw/` folder with timestamped CSVs
- Minimum 100 hours equivalent simulation data
- Labeled scenarios (normal, warning, failure)

### Phase 3: World Model Training (Sunday)
- [ ] Data preprocessed (normalization, windowing)
- [ ] State-space model architecture defined
- [ ] Training on DigitalOcean (GPU if available)
- [ ] Model validated on held-out data
- [ ] Model exported to ONNX

**Model Architecture:**
```
Input: [state(t-N), ..., state(t-1), state(t)]
       ↓
LSTM/Transformer encoder (small)
       ↓
Dense prediction heads
       ↓
Output: [state(t+1), anomaly_score, failure_prob]
```

**Training Targets:**
| Metric | Target |
|--------|--------|
| Validation loss | < 0.1 |
| Anomaly detection AUC | > 0.85 |
| Failure prediction | > 80% recall |

**Deliverables:**
- `models/world_model_v1.onnx` (< 50MB)
- Training logs and metrics
- Validation report

### Phase 4: Edge Deployment (Monday)
- [ ] Model copied to BeagleBone
- [ ] ONNX Runtime installed
- [ ] Inference service running
- [ ] Real-time predictions tested
- [ ] Performance optimized

**Performance Targets:**
| Metric | Target |
|--------|--------|
| Inference latency | < 100ms |
| Memory usage | < 256MB |
| CPU usage | < 50% |

**Deliverables:**
- Running inference service
- Real-time predictions against Factory I/O
- Performance benchmarks

### Phase 5: Demo Day (Tuesday)
- [ ] Full demo recorded
- [ ] WhatsApp query in Spanish
- [ ] AI response with diagnosis
- [ ] Content posted everywhere
- [ ] Anthropic tagged

**Demo Script:**
1. Show BeagleBone connected to Factory I/O
2. Factory I/O running normally
3. WhatsApp message in Spanish: "¿Cómo está la máquina?"
4. AI responds: "Todo funciona normal. Motor a 85% capacidad."
5. Introduce fault in Factory I/O
6. AI alerts: "Advertencia: Patrón de falla detectado. Revise el sensor #3."
7. End with: "Built in 4 days. $50 hardware. Works offline."

---

## Connection Details

| Property | Value |
|----------|-------|
| USB IP | 192.168.7.2 |
| MAC | 64-70-60-ae-f2-07 |
| SSH User | debian |
| SSH Pass | temppwd (change after setup) |
| WireGuard IP | 10.100.0.10 (planned) |
| VPS WireGuard | factorylm-prod (165.245.138.91) |

---

## World Model Specification

### Input Features
| Feature | Type | Source | Range |
|---------|------|--------|-------|
| Motor current | float | PLC analog | 0-10A |
| Motor speed | float | PLC analog | 0-1800 RPM |
| Conveyor speed | float | PLC analog | 0-100% |
| Sensor 1-8 | bool | PLC digital | 0/1 |
| Valve 1-4 | bool | PLC digital | 0/1 |
| Timestamp | float | System | Unix ms |

### Output Predictions
| Prediction | Type | Description |
|------------|------|-------------|
| next_state | vector | Predicted next sensor/motor values |
| anomaly_score | float 0-1 | How unusual is current state |
| failure_prob | float 0-1 | Probability of failure in next 60s |
| failure_type | string | Most likely failure mode |
| recommended_action | string | What to do about it |

### Model Size Variants
| Variant | Params | Size | Latency | Use Case |
|---------|--------|------|---------|----------|
| Tiny | 100K | 5 MB | < 10ms | Always-on monitoring |
| Small | 500K | 20 MB | < 50ms | Predictions |
| Medium | 2M | 50 MB | < 100ms | Complex diagnostics |

---

## Directory Structure

```
projects/beaglebone-gateway/
├── README.md           # Original protocol gateway docs
├── SCOPE.md            # This file - complete project scope
├── STATUS.md           # Current progress tracking
├── requirements.txt    # Python dependencies
├── config/
│   ├── gateway.yaml    # Main gateway config
│   ├── wireguard/      # VPN configs
│   └── factory_io.yaml # Factory I/O specific config
├── scripts/
│   ├── install.sh      # Initial BeagleBone setup
│   ├── collect.py      # Data collection from PLC
│   ├── train.py        # Model training (run on server)
│   └── deploy.sh       # Deploy model to BeagleBone
├── src/
│   ├── core/
│   │   ├── config.py
│   │   └── logger.py
│   ├── adapters/
│   │   ├── modbus.py
│   │   ├── s7.py
│   │   └── opcua.py
│   ├── inference/
│   │   ├── world_model.py  # Model inference
│   │   └── llm.py          # Language model interface
│   ├── api/
│   │   ├── server.py       # REST API
│   │   └── whatsapp.py     # WhatsApp webhook
│   └── web/
│       └── app.py          # Web UI
├── models/
│   └── (trained models go here)
├── data/
│   ├── raw/            # Raw collected data
│   ├── processed/      # Training-ready data
│   └── scenarios/      # Labeled scenario data
├── tests/
└── docs/
    ├── setup.md
    ├── training.md
    └── deployment.md
```

---

## Content Capture Points (For Automaton)

| Milestone | Capture Type | Content Angle |
|-----------|--------------|---------------|
| First SSH | Terminal recording | "It's alive!" |
| WireGuard connected | Screenshot | "Remote access from anywhere" |
| Data flowing | Terminal + graph | "Teaching AI what normal looks like" |
| Training progress | Graph animation | "Watching AI learn" |
| First prediction | Terminal + Factory I/O | "It predicted the future" |
| Spanish demo | Screen recording | "The money shot" |

---

## Risk Mitigation

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| BeagleBone underpowered | Medium | High | Have RPi5 as backup |
| Training data insufficient | Medium | Medium | Extend scenario runs |
| Model not accurate | Medium | High | Focus on "learning" narrative |
| WhatsApp integration issues | Low | Medium | Demo with Telegram instead |
| Time overrun | Medium | Medium | Scope to MVP features |

---

## Success Criteria

| Criteria | Target | Stretch |
|----------|--------|---------|
| Prediction accuracy | > 80% | > 90% |
| Inference latency | < 100ms | < 50ms |
| Languages | EN + ES | + PT |
| Demo video views | 10,000+ | 100,000+ |
| Investor interest | 1 inquiry | Term sheet |

---

## Dependencies

### External
- Factory I/O license (Mike has)
- Allen-Bradley Micro 820 (Mike has)
- DigitalOcean GPU (if needed for training)
- Twilio/WhatsApp Business API (for production)

### Internal
- The Automaton (for content creation)
- WireGuard server config (ready on VPS)
- BeagleBone flash complete (in progress)

---

## Appendix: Factory I/O Scenarios

### Scenario 1: Sorting Station
- 2 conveyors
- 3 sensors
- 1 pusher
- Good for jam detection

### Scenario 2: Palletizer
- Multiple axes
- Timing-critical
- Good for sequence learning

### Scenario 3: Warehouse
- Multiple zones
- Traffic management
- Good for anomaly detection

---

*This scope document serves as the complete specification for the Tuesday Demo build.*
