# FactoryLM Sensor Node - Technical Specifications

## Overview
Low-cost network monitoring node for industrial PLC environments.

---

## Hardware: ESP32-S3 + W5500 Ethernet

### Core Module: ESP32-S3-WROOM-1
| Spec | Value |
|------|-------|
| CPU | Dual-core Xtensa LX7, 240 MHz |
| RAM | 512 KB SRAM |
| Flash | 8 MB (16 MB variants available) |
| WiFi | 802.11 b/g/n |
| Bluetooth | BLE 5.0 + Mesh |
| GPIO | 45 programmable pins |
| Cost | $8-15 |

### Ethernet Module: W5500
| Spec | Value |
|------|-------|
| Interface | SPI (80 MHz max) |
| Speed | 10/100 Mbps |
| Sockets | 8 simultaneous TCP/UDP |
| Protocols | TCP, UDP, ICMP, IPv4, ARP, IGMP, PPPoE |
| Cost | $5 |

### Recommended Board: LILYGO T-ETH-Lite
- ESP32-S3 + W5500 integrated
- **Power over Ethernet (PoE) support**
- Single cable for power + data
- Cost: ~$25

---

## Power Requirements

| Mode | Current | Power |
|------|---------|-------|
| Idle | 20 mA | 0.1 W |
| WiFi Active | 100 mA | 0.5 W |
| Ethernet + Processing | 200 mA | 1.0 W |
| Peak | 400 mA | 2.0 W |

**Input:** 5V DC via USB-C, barrel jack, or PoE

**Power Sources:**
- USB phone charger ($3)
- Industrial 5V supply
- PoE injector/switch (recommended for industrial)

---

## Communication Protocols

### Supported (with libraries)
| Protocol | Library | Use Case |
|----------|---------|----------|
| Modbus TCP | eModbus | Read PLC registers |
| Modbus RTU | eModbus | Serial devices |
| MQTT | PubSubClient | Report to gateway |
| HTTP/HTTPS | HTTPClient | REST APIs |
| EtherNet/IP | Custom | Allen Bradley native |
| OPC-UA | open62541 (limited) | Modern PLCs |
| Raw TCP | Socket | Custom protocols |

### Network Monitoring (passive)
- ARP table monitoring
- ICMP ping
- Port scanning
- MAC address tracking
- Traffic analysis (promiscuous mode limited)

---

## Deployment Modes

### Mode 1: Passive Network Sentinel
```
┌─────────────────────────────────────────────────┐
│  PASSIVE MONITORING (Zero Risk)                 │
├─────────────────────────────────────────────────┤
│  • Plugs into network switch                    │
│  • Does NOT communicate with PLCs               │
│  • Monitors ARP table for changes               │
│  • Pings devices to check online status         │
│  • Detects IP conflicts                         │
│  • Reports via MQTT to Edge Gateway             │
└─────────────────────────────────────────────────┘
```

### Mode 2: Active Modbus TCP Client
```
┌─────────────────────────────────────────────────┐
│  ACTIVE DATA COLLECTION                         │
├─────────────────────────────────────────────────┤
│  • Reads Modbus registers from PLCs             │
│  • Polls tag values (temps, counts, states)     │
│  • Reads fault/alarm registers                  │
│  • Configurable poll rate (100ms - 60s)         │
│  • Reports data via MQTT                        │
└─────────────────────────────────────────────────┘
```

### Mode 3: Protocol Gateway
```
┌─────────────────────────────────────────────────┐
│  PROTOCOL TRANSLATION                           │
├─────────────────────────────────────────────────┤
│  • Modbus RTU (serial) ↔ Modbus TCP             │
│  • Legacy device integration                    │
│  • Serial → MQTT bridge                         │
└─────────────────────────────────────────────────┘
```

---

## Programming Environment

### Option 1: Arduino IDE (Beginner-friendly)
```bash
# Install ESP32 board support
# Add to Preferences → Board Manager URLs:
https://raw.githubusercontent.com/espressif/arduino-esp32/gh-pages/package_esp32_index.json

# Install libraries via Library Manager:
# - EthernetESP32
# - PubSubClient (MQTT)
# - eModbus
# - ArduinoJson
```

### Option 2: PlatformIO (Professional)
```ini
; platformio.ini
[env:esp32-s3]
platform = espressif32
board = esp32-s3-devkitc-1
framework = arduino
lib_deps =
    knolleary/PubSubClient@^2.8
    eModbus/eModbus@^1.7
    bblanchon/ArduinoJson@^7.0
```

### Option 3: ESP-IDF (Advanced/Production)
- Native Espressif framework
- FreeRTOS based
- Maximum performance/control
- Steeper learning curve

---

## Firmware Architecture

```
┌────────────────────────────────────────────────────────┐
│                 FACTORYLM SENSOR NODE                  │
├────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
│  │   Network    │  │   Modbus     │  │    MQTT      │ │
│  │   Monitor    │  │   Client     │  │   Reporter   │ │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘ │
│         │                 │                 │         │
│         └────────────┬────┴────────────────┘         │
│                      │                                │
│              ┌───────▼───────┐                       │
│              │  Event Queue  │                       │
│              └───────┬───────┘                       │
│                      │                                │
│              ┌───────▼───────┐                       │
│              │ Config Store  │ ← OTA Updates         │
│              └───────────────┘                       │
└────────────────────────────────────────────────────────┘
```

---

## Sample Code: Network Sentinel

```cpp
#include <ETH.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>

#define MQTT_SERVER "192.168.1.100"
#define NODE_ID "sentinel-01"

WiFiClient ethClient;
PubSubClient mqtt(ethClient);

// Devices to monitor
IPAddress targets[] = {
  IPAddress(192,168,1,10),  // PLC 1
  IPAddress(192,168,1,11),  // PLC 2
  IPAddress(192,168,1,12),  // VFD
};

void setup() {
  ETH.begin();
  mqtt.setServer(MQTT_SERVER, 1883);
}

void loop() {
  for (auto& target : targets) {
    bool online = Ping.ping(target);
    
    JsonDocument doc;
    doc["node"] = NODE_ID;
    doc["target"] = target.toString();
    doc["online"] = online;
    doc["latency_ms"] = Ping.averageTime();
    
    char buffer[256];
    serializeJson(doc, buffer);
    mqtt.publish("factorylm/sentinel", buffer);
  }
  delay(5000);
}
```

---

## Bill of Materials ($25 node)

| Item | Source | Cost |
|------|--------|------|
| LILYGO T-ETH-Lite (ESP32-S3 + W5500 + PoE) | AliExpress | $22 |
| 3D printed enclosure | Local/print | $2 |
| DIN rail clip | Amazon | $1 |
| **TOTAL** | | **$25** |

### Budget Version ($15 node)

| Item | Source | Cost |
|------|--------|------|
| ESP32-S3 DevKit | AliExpress | $8 |
| W5500 Ethernet module | AliExpress | $4 |
| USB power supply | Amazon | $2 |
| Enclosure | Generic | $1 |
| **TOTAL** | | **$15** |

---

## PLC Compatibility

| PLC Brand | Protocol | Support Level |
|-----------|----------|---------------|
| Allen Bradley (Logix) | EtherNet/IP, Modbus TCP | ✅ Good |
| Siemens S7 | S7comm, Modbus TCP | ✅ Good |
| Modicon/Schneider | Modbus TCP | ✅ Native |
| Omron | FINS, Modbus TCP | ✅ Good |
| Mitsubishi | MC Protocol, Modbus | 🟡 Partial |
| Beckhoff | ADS, Modbus TCP | 🟡 Partial |

---

## Next Steps

1. [ ] Order 5x LILYGO T-ETH-Lite for prototyping
2. [ ] Create GitHub repo: `factorylm-sentinel`
3. [ ] Write base firmware with MQTT reporting
4. [ ] Add Modbus TCP client support
5. [ ] Build web-based configuration portal
6. [ ] Test with Allen Bradley CompactLogix

---

**Document Status:** DRAFT  
**Created:** 2026-02-04  
**Author:** Jarvis  
