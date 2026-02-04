# Field Log: CraneSync Overhead Crane Monitoring Architecture

**Date:** 2026-02-04  
**Project:** CraneSync (cranesync.com)  
**Application:** Overhead crane VFD monitoring with FactoryLM  
**Author:** Mike Harper / Jarvis

---

## Use Case

Modern overhead cranes with:
- 3 VFDs (hoist, trolley, bridge motion)
- Encoder feedback for positioning
- Load cells for weight measurement
- Photo-eyes for limit detection
- No existing plant network connection

**Goal:** Wireless data collection to factory floor HMI showing real-time crane status, load data, and predictive analytics.

---

## Myth Busting: "VFD Data is Hard to Get"

**FALSE.** Modern VFDs (Yaskawa, ABB, Siemens, etc.) expose all data via standard protocols:

| Data Point | Availability | Protocol |
|------------|--------------|----------|
| Motor current | ✅ Standard register | Modbus TCP |
| Motor voltage | ✅ Standard register | Modbus TCP |
| Speed/frequency | ✅ Standard register | Modbus TCP |
| Encoder position | ✅ Feedback register | Modbus TCP |
| Torque estimate | ✅ Calculated register | Modbus TCP |
| Fault codes | ✅ Status register | Modbus TCP |
| Run hours | ✅ Counter register | Modbus TCP |
| Thermal model | ✅ Available on most | Modbus TCP |
| Analog inputs (load cell) | ✅ AI register | Modbus TCP |

**Yaskawa Reference:** SIEPC73060091 (Modbus TCP/IP Technical Manual)

---

## Architecture: CraneSync with FactoryLM

```
┌─────────────────────────────────────────────────────────────────┐
│                        OVERHEAD CRANE                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────┐    ┌─────────┐    ┌─────────┐                     │
│  │  HOIST  │    │ TROLLEY │    │ BRIDGE  │                     │
│  │   VFD   │    │   VFD   │    │   VFD   │                     │
│  │ Yaskawa │    │ Yaskawa │    │ Yaskawa │                     │
│  └────┬────┘    └────┬────┘    └────┬────┘                     │
│       │              │              │                           │
│       └──────────────┼──────────────┘                           │
│                      │ Ethernet (local)                         │
│               ┌──────▼──────┐                                   │
│               │   ESP32     │ ← Mounted on crane                │
│               │ SENSOR NODE │                                   │
│               └──────┬──────┘                                   │
│                      │ WiFi / Industrial Radio                  │
└──────────────────────┼──────────────────────────────────────────┘
                       │
                       │ Wireless
                       │
┌──────────────────────▼──────────────────────────────────────────┐
│                      FACTORY FLOOR                              │
├─────────────────────────────────────────────────────────────────┤
│  ┌────────────────┐     ┌────────────────┐                     │
│  │  EDGE GATEWAY  │────►│   FACTORYLM    │                     │
│  │  (Pi/Jetson)   │     │    ENGINE      │                     │
│  └────────────────┘     └───────┬────────┘                     │
│                                 │                               │
│                    ┌────────────┼────────────┐                  │
│                    │            │            │                  │
│               ┌────▼────┐ ┌─────▼─────┐ ┌───▼───┐              │
│               │ Web HMI │ │ Telegram  │ │ Alerts│              │
│               │ Display │ │ WhatsApp  │ │ Email │              │
│               └─────────┘ └───────────┘ └───────┘              │
└─────────────────────────────────────────────────────────────────┘
```

---

## Data Points to Collect (per crane)

### Real-Time (100ms - 1s polling)
| Parameter | Source | Use |
|-----------|--------|-----|
| Hoist position | Encoder via VFD | Height tracking |
| Load weight | Load cell via VFD AI | Overload protection |
| Motor currents (x3) | VFD registers | Health monitoring |
| Speed (x3) | VFD registers | Motion tracking |
| Fault status (x3) | VFD registers | Immediate alerts |
| Brake state (x3) | VFD digital inputs | Safety verification |

### Trend Data (1-minute aggregates)
| Parameter | Calculation | Use |
|-----------|-------------|-----|
| Lifts per hour | Count hoist up→down cycles | Utilization |
| Average load | Mean of load cell | Planning |
| Peak load | Max of load cell | Abuse detection |
| Duty cycle % | Runtime / hour | Maintenance scheduling |
| Motor temperature trend | Thermal model | Predictive |

### Predictive Analytics
- Motor current trending up → Bearing wear
- Brake engagement time increasing → Brake pad wear
- Encoder position drift → Mechanical slack
- Load cell calibration drift → Needs recalibration

---

## Wireless Options

### Option 1: Standard WiFi ($0 additional)
- ESP32 built-in WiFi
- Range: 50-100m line of sight
- Works for most indoor cranes
- Potential interference in metal-heavy environments

### Option 2: Industrial WiFi Radio (~$200/pair)
- Moxa AWK series or similar
- Hardened for industrial environments
- Better range and reliability
- Recommended for critical applications

### Option 3: LoRa (Long Range, Low Power) (~$20/pair)
- ESP32 with LoRa module
- Range: 1-2 km
- Lower bandwidth (fine for periodic data)
- Good for large outdoor yards

### Option 4: Cellular (~$50 + monthly)
- ESP32 with 4G module
- No local infrastructure needed
- Good for remote sites
- Requires data plan

---

## Bill of Materials: Single Crane

| Item | Cost |
|------|------|
| ESP32 with Ethernet (T-ETH-Lite) | $25 |
| Industrial enclosure (IP65) | $15 |
| WiFi antenna (external) | $5 |
| Ethernet cables (to VFDs) | $20 |
| Power supply (24V to 5V) | $10 |
| Mounting hardware | $5 |
| **TOTAL per crane** | **$80** |

### Edge Gateway (one per facility)
| Item | Cost |
|------|------|
| Raspberry Pi 4 (4GB) | $55 |
| Coral USB Accelerator | $60 |
| Industrial enclosure | $30 |
| Power supply | $15 |
| SD card (64GB) | $15 |
| **TOTAL gateway** | **$175** |

### Full System: 5 Cranes
- 5x Crane nodes: $400
- 1x Edge gateway: $175
- Software (FactoryLM): Subscription
- **Hardware total: $575**

---

## Competitive Landscape

| Company | Product | Price | Cloud Req |
|---------|---------|-------|-----------|
| CraneWerks | Intelli-Connect | ~$10K+ | Yes |
| VerveTronics | Crane Monitor | ~$15K+ | Yes |
| Konecranes | TRUCONNECT | ~$20K+ | Yes |
| **CraneSync** | FactoryLM Edge | **<$1K** | **No** |

**CraneSync Differentiators:**
1. 10-20x lower hardware cost
2. No cloud dependency (air-gapped capable)
3. Open protocols (customer owns their data)
4. LLM-powered natural language queries
5. Self-installable by maintenance staff

---

## Patent Considerations

**Mike's Provisional Patent Focus Areas:**
- Wireless crane data aggregation architecture
- LLM-based crane diagnostics ("What's wrong with crane 3?")
- Predictive maintenance algorithms specific to crane duty cycles
- Integration method for legacy cranes (retrofit approach)

**Standard (not patentable):**
- Reading Modbus registers from VFDs
- Basic data collection and display
- WiFi transmission

---

## Next Steps

1. [ ] Spec out Yaskawa A1000 register map for crane application
2. [ ] Build ESP32 firmware for 3-drive crane monitoring
3. [ ] Design crane-specific FactoryLM dashboard
4. [ ] Create CraneSync product page / demo
5. [ ] Test on a real crane (Mike's contacts?)

---

**Field Log Status:** CAPTURED  
**Knowledge Base:** Ready for ingestion  
**Project:** CraneSync / FactoryLM  
