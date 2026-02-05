# FactoryLM Edge Agent Specification

*Technical Specification for Tier 2: Connect*

---

## Overview

The FactoryLM Edge Agent is software that runs on customer premises to connect their PLCs to the FactoryLM cloud. It provides real-time data acquisition without requiring PLC programming changes.

---

## Supported Platforms

- **Linux:** Ubuntu 20.04+, Debian 10+, Raspberry Pi OS
- **Windows:** Windows 10/11, Windows Server 2019+
- **Docker:** Official container image available

---

## Supported Protocols

### Priority 1 (Launch)
| Protocol | Library | Status |
|----------|---------|--------|
| Modbus TCP | pymodbus | Ready |
| Modbus RTU | pymodbus | Ready |
| Ethernet/IP | cpppo, pycomm3 | Available |

### Priority 2 (Q2)
| Protocol | Library | Status |
|----------|---------|--------|
| OPC-UA | opcua-asyncio | Available |
| PROFINET | python-snap7 | Available |
| S7 (Siemens) | python-snap7 | Available |

### Priority 3 (Q3)
| Protocol | Library | Status |
|----------|---------|--------|
| BACnet | bacpypes | Available |
| MQTT | paho-mqtt | Ready |
| DNP3 | pydnp3 | Research |

---

## Architecture

```
┌─────────────────────────────────────────┐
│           Customer Network              │
│                                         │
│  ┌─────┐  ┌─────┐  ┌─────┐            │
│  │ PLC │  │ PLC │  │ PLC │            │
│  └──┬──┘  └──┬──┘  └──┬──┘            │
│     │        │        │                │
│     └────────┼────────┘                │
│              │                         │
│     ┌────────┴────────┐                │
│     │  Edge Agent     │                │
│     │  ┌───────────┐  │                │
│     │  │ Discovery │  │                │
│     │  ├───────────┤  │                │
│     │  │ Connectors│  │                │
│     │  ├───────────┤  │                │
│     │  │ Buffer    │  │                │
│     │  ├───────────┤  │                │
│     │  │ Uplink    │  │                │
│     │  └───────────┘  │                │
│     └────────┬────────┘                │
│              │                         │
└──────────────┼─────────────────────────┘
               │ HTTPS/WSS
               ▼
        ┌──────────────┐
        │ FactoryLM    │
        │ Cloud        │
        └──────────────┘
```

---

## Components

### 1. Discovery Module
- Auto-detect PLCs on local network
- Scan common ports (502, 44818, 102)
- Identify protocol and device type
- Report available tags/registers

### 2. Protocol Connectors
- Pluggable architecture for each protocol
- Connection pooling and retry logic
- Tag browsing and subscription
- Read-only by default (safety)

### 3. Data Buffer
- Local SQLite for offline operation
- Configurable retention (default 24h)
- Compression for bandwidth efficiency

### 4. Cloud Uplink
- HTTPS REST for configuration
- WebSocket for real-time data
- TLS 1.3 encryption required
- Auto-reconnect on failure

---

## Configuration

```yaml
# factorylm-agent.yaml
agent:
  id: auto-generated
  name: "Plant Floor 1"
  
cloud:
  endpoint: https://api.factorylm.com
  token: ${FACTORYLM_TOKEN}
  
connections:
  - name: "Main PLC"
    protocol: modbus-tcp
    host: 192.168.1.100
    port: 502
    poll_interval: 1000ms
    tags:
      - name: "Motor1_Speed"
        address: 40001
        type: int16
      - name: "Temp_Sensor1"
        address: 40010
        type: float32
        
  - name: "Safety PLC"
    protocol: ethernet-ip
    host: 192.168.1.101
    tags:
      - name: "EStop_Status"
        address: "Safety:I.Data[0]"
```

---

## Security

- **Authentication:** Token-based, rotated weekly
- **Encryption:** TLS 1.3 for all cloud communication
- **Network:** Outbound only, no inbound ports required
- **Isolation:** Recommend running on isolated VLAN
- **Permissions:** Read-only by default, write requires explicit flag

---

## Installation

### Linux (One-liner)
```bash
curl -sSL https://install.factorylm.com | bash
```

### Docker
```bash
docker run -d --name factorylm-agent \
  -e FACTORYLM_TOKEN=your-token \
  -v /path/to/config:/config \
  factorylm/edge-agent:latest
```

### Windows
Download installer from dashboard after signup.

---

## Development Roadmap

### Phase 1 (Week 1-2)
- [ ] Core agent framework
- [ ] Modbus TCP connector
- [ ] Cloud uplink (HTTPS)
- [ ] Basic CLI

### Phase 2 (Week 3-4)
- [ ] Ethernet/IP connector
- [ ] WebSocket streaming
- [ ] Auto-discovery
- [ ] Web dashboard for config

### Phase 3 (Week 5-6)
- [ ] OPC-UA connector
- [ ] S7/PROFINET connector
- [ ] Docker packaging
- [ ] Windows installer

---

## Success Metrics

- **Setup Time:** < 30 minutes from download to first data
- **Reliability:** 99.9% uptime for data collection
- **Latency:** < 1 second from PLC to cloud
- **Resource Usage:** < 100MB RAM, < 1% CPU on Raspberry Pi

---

*Document Owner: Code Agent*
*Last Updated: 2026-02-05*
