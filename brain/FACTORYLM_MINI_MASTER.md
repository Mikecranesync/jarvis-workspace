# FactoryLM Mini - Master Knowledge Base

**Created:** 2026-02-04  
**Version:** 0.1.0  
**Status:** ACTIVE DEVELOPMENT

---

## Executive Summary

FactoryLM Mini is a low-cost, edge-first industrial AI platform that enables any machine to be monitored and analyzed by AI for ~$30 per device.

**Core Value Proposition:**
- 10-100x cheaper than enterprise alternatives
- Air-gapped capable (no cloud required)
- LLM-powered natural language interface
- Open source, no vendor lock-in

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    FACTORYLM MINI STACK                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  TIER 1: SENSOR NODES ($15-30 each)                            │
│  ├── ESP32-S3 + W5500 Ethernet                                 │
│  ├── Protocols: Modbus TCP, CAN, Analog, Digital               │
│  ├── Reports via MQTT to Edge Gateway                          │
│  └── Passive monitoring OR active data collection              │
│                                                                 │
│  TIER 2: EDGE GATEWAY ($175-400)                               │
│  ├── Raspberry Pi 4/5 OR Jetson Orin Nano                      │
│  ├── Google Coral for AI inference (optional)                  │
│  ├── Runs FactoryLM Engine + LLM                               │
│  └── Handles messaging (Telegram/WhatsApp/Signal)              │
│                                                                 │
│  TIER 3: PLANT SERVER (optional, $500-1000)                    │
│  ├── Intel NUC or industrial PC                                │
│  ├── Aggregates multiple gateways                              │
│  ├── Long-term data storage                                    │
│  └── Enterprise features                                       │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Hardware Tiers Comparison

| Tier | Device | AI Capability | Price | Use Case |
|------|--------|---------------|-------|----------|
| Sensor Node | ESP32-S3 | None | $15-30 | Data collection |
| Edge Gateway Basic | Pi 4 + Coral | 4 TOPS | $175 | Small facility |
| Edge Gateway Pro | Jetson Orin Nano | 67 TOPS | $400 | Vision AI |
| Plant Server | Intel NUC | CPU inference | $800 | Multi-line |

---

## Key Technical Specs

### ESP32 Sensor Node
- CPU: Dual-core 240MHz
- RAM: 512KB
- Flash: 8MB
- WiFi: 802.11 b/g/n
- Ethernet: W5500 (add-on or integrated)
- Power: 5V DC, <2W
- Protocols: Modbus TCP, MQTT, HTTP, CAN (with module)

### Google Coral USB Accelerator
- AI Chip: Google Edge TPU
- Performance: 4 TOPS
- Interface: USB 3.0
- Power: 2W
- Models: TensorFlow Lite (quantized)
- Use: Real-time vision, anomaly detection

### NVIDIA Jetson Orin Nano
- AI Performance: 67 TOPS
- CPU: 6-core Arm Cortex-A78AE
- GPU: 1024-core Ampere
- RAM: 8GB LPDDR5
- Price: $249
- Use: Advanced AI, local LLM inference

---

## Protocol Support Matrix

| Protocol | Node Support | Use Case |
|----------|--------------|----------|
| Modbus TCP | ✅ Native | PLCs, VFDs |
| Modbus RTU | ✅ Serial | Legacy devices |
| EtherNet/IP | 🟡 Library | Allen Bradley |
| CAN Bus | ✅ Module | Vehicles, mobile |
| OPC-UA | 🟡 Limited | Modern PLCs |
| MQTT | ✅ Native | Internal comms |
| HTTP/S | ✅ Native | APIs |
| Analog 4-20mA | ✅ ADC | Sensors |

---

## Application Domains

### 1. Manufacturing (FactoryLM)
- PLC/VFD monitoring
- Predictive maintenance
- Production analytics

### 2. Overhead Cranes (CraneSync)
- Hoist/trolley/bridge VFDs
- Load cell monitoring
- Duty cycle tracking
- Encoder position

### 3. Vehicles (Fleet)
- OBD2/CAN data
- GPS tracking
- Driver behavior
- Maintenance prediction

### 4. HVAC/Facilities
- Compressor monitoring
- Power consumption
- Environmental sensors

---

## Competitive Advantages

1. **Price**: $30/node vs $500+ competitors
2. **Air-gapped**: No cloud dependency
3. **LLM Interface**: Natural language queries
4. **Open Source**: No vendor lock-in
5. **Edge-First**: Real-time local processing
6. **Universal**: Any protocol, any machine

---

## Security Architecture

```
┌─────────────────────────────────────────────────┐
│          SECURITY BY DESIGN                     │
├─────────────────────────────────────────────────┤
│  • READ-ONLY by default (no write to PLCs)      │
│  • One-way data flow (outbound only)            │
│  • Network isolation (separate VLAN)            │
│  • TLS encryption (MQTT over TLS)               │
│  • No inbound internet connections              │
│  • Local-first processing                       │
└─────────────────────────────────────────────────┘
```

---

## Market Position

| Competitor | Focus | Price Point | Cloud Req | Our Advantage |
|------------|-------|-------------|-----------|---------------|
| Augury | Vibration | $50K+ | Yes | 100x cheaper |
| Uptake | Analytics | $100K+ | Yes | Edge-first |
| Sight Machine | Dashboards | $200K+ | Yes | LLM interface |
| MachineMetrics | CNC | $10K+ | Yes | Universal |
| TRACTIAN | LatAm | $20K+ | Yes | Air-gapped |

---

## Related Documents

- `brain/field-logs/2026-02-04-florida-natural-duplicate-cpu.md`
- `brain/field-logs/2026-02-04-cranesync-overhead-crane-architecture.md`
- `projects/FACTORYLM_SENSOR_NODE_SPECS.md`
- `projects/SIGNAL_DEVELOPMENT_STRATEGY.md`
- `projects/WHATSAPP_ADAPTER_STRATEGY.md`

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 0.1.0 | 2026-02-04 | Initial brain dump from strategy session |

