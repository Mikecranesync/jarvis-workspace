# Industrial Edge Adapter — BeagleBone Gateway

**Vision:** P1 (CRITICAL)  
**Hardware:** BeagleBone Black Industrial  
**Status:** ACTIVE

---

## ⚠️ CORE PRINCIPLE: READ-ONLY PASSIVE TAP

**This device NEVER:**
- Sends queries to PLCs
- Writes registers or coils
- Modifies ladder logic
- Changes network configs
- Broadcasts on the network
- Responds to scans/pings

**This device ONLY:**
- Listens passively (promiscuous mode)
- Decodes existing network traffic
- Extracts PLC data from packets
- Forwards to technician via secure tunnel

---

## What It Does (Tech's Perspective)

1. **Plug in** → Ethernet cable to empty switch port
2. **Silent listen** → Promiscuous mode, sees all traffic
3. **Decode protocols** → Parses Modbus/OPC UA/EtherNet-IP packets
4. **Extract data** → Temps, pressures, alarms, I/O states
5. **Alert phone** → Telegram: "Motor 3 temp: 85°C, Alarm detected"
6. **AI analysis** → Claude API suggests diagnostics
7. **Zero footprint** → No trace on the network

---

## Architecture

```
┌─────────────────┐
│ PLC Network     │ (Modbus TCP, OPC UA, EtherNet/IP)
│ 192.168.1.x     │
└────────┬────────┘
         │ Ethernet
         ↓
┌────────────────────────────────────────┐
│ BeagleBone Black Industrial (Edge)     │
│ ┌──────────────┐ ┌───────────────────┐ │
│ │ PRU (200MHz) │ │ ARM Cortex-A8     │ │
│ │ Real-time    │←→│ Linux             │ │
│ │ Modbus poll  │ │ OPC UA client     │ │
│ └──────────────┘ │ MQTT pub          │ │
│                  │ WireGuard VPN     │ │
│                  └─────────┬─────────┘ │
└────────────────────────────┼───────────┘
                             │ Internet (encrypted)
                             ↓
┌─────────────────────┐
│ Your Cloud Backend  │
│ (VPS, Neon DB,      │
│  Claude API)        │
└──────────┬──────────┘
           │
           ↓
┌──────────────────┐
│ Technician Phone │
│ (Telegram bot)   │
└──────────────────┘
```

---

## Protocols

| Protocol | Library | Use Case |
|----------|---------|----------|
| **Modbus TCP** | pymodbus (Python) | Most PLCs, simple registers |
| **OPC UA** | opcua-asyncio | Allen-Bradley, Siemens, modern PLCs |
| **MQTT** | paho-mqtt + Mosquitto | Data pipeline to cloud |
| **WireGuard** | wg-quick | Secure VPN tunnel |

---

## Development Phases

| Phase | Task | Tools |
|-------|------|-------|
| 1 | Base OS + networking | Debian, SSH, WireGuard |
| 2 | Modbus TCP client | pymodbus, Factory IO simulator |
| 3 | OPC UA client | opcua-asyncio |
| 4 | Data pipeline | MQTT, JSON normalization |
| 5 | Secure tunnel | WireGuard to VPS |
| 6 | Telegram integration | python-telegram-bot |
| 7 | Edge AI | Claude API, threshold checks |
| 8 | Packaging | systemd, watchdog, enclosure |

---

## Hardware Specs

- **Board:** BeagleBone Black Industrial
- **CPU:** ARM Cortex-A8 + 2x PRU (200MHz real-time)
- **RAM:** 512MB
- **Storage:** 4GB eMMC
- **Network:** 10/100 Ethernet
- **Temp range:** Industrial (-40°C to 85°C)
- **Cost:** ~$100/unit

---

## MVP Checklist

- [ ] Flash BeagleBone with Debian
- [ ] SSH access working
- [ ] WireGuard tunnel to VPS
- [ ] Read one Modbus register from Factory IO
- [ ] Publish to MQTT
- [ ] Forward to Telegram
- [ ] Call Claude API with context

---

## Test Environment

- **PLC Simulator:** Factory IO + Modbus TCP
- **Backend:** This VPS (72.60.175.144)
- **Telegram:** Jarvis bot

---

*The missing piece between your equipment and your phone.*
