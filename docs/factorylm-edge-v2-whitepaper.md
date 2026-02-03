# FactoryLM Edge v2.0 - Technical White Paper

## Adaptive Network Bridge for Industrial Edge Computing

**Version:** 2.0.0  
**Date:** 2026-02-03  
**Authors:** Mike Harper (Human Systems Engineer), Jarvis (AI Development Assistant)

---

## Abstract

FactoryLM Edge v2.0 is an adaptive network bridge that eliminates manual IP configuration when connecting industrial devices. The system autonomously detects the network topology of any connected device and reconfigures itself to establish communication—achieving true plug-and-play connectivity for previously incompatible network segments.

---

## Problem Statement

Industrial networks typically require manual IP configuration when connecting new devices. A technician must:
1. Determine the target device's IP subnet
2. Manually configure the gateway's network interface
3. Verify connectivity
4. Repeat for each network change

This process creates deployment friction, requires trained personnel, and introduces human error.

---

## Solution Architecture

### Hardware Platform
- Raspberry Pi 4 (4GB RAM)
- Dual network interfaces (WiFi + Ethernet)
- balenaOS containerized deployment

### Software Components

```
┌─────────────────────────────────────────────────────┐
│              FactoryLM Edge Gateway                 │
├─────────────────────────────────────────────────────┤
│  ┌─────────────────┐    ┌──────────────────────┐   │
│  │ Network Detect  │───▶│   IP Keepalive       │   │
│  │   (Python)      │    │   (Bash daemon)      │   │
│  └────────┬────────┘    └──────────────────────┘   │
│           │                                         │
│           ▼                                         │
│  ┌─────────────────┐    ┌──────────────────────┐   │
│  │ Auto-Configure  │    │  Fallback DHCP       │   │
│  │   eth0 IP       │    │  (dnsmasq)           │   │
│  └─────────────────┘    └──────────────────────┘   │
├─────────────────────────────────────────────────────┤
│                   Tailscale VPN                     │
│              (Remote Management Layer)              │
└─────────────────────────────────────────────────────┘
```

---

## Detection Algorithm

### Phase 1: Link Detection
```
Monitor eth0 carrier signal
Wait for physical link establishment (cable connected)
Timeout: 30 seconds → fallback to DHCP server mode
```

### Phase 2: Neighbor Discovery
```
Methods (executed in parallel):
1. ARP table inspection for existing entries
2. ARP probe of common gateway IPs:
   - 192.168.137.1 (Windows ICS)
   - 192.168.1.1   (Consumer routers)
   - 192.168.0.1   (Alternative default)
   - 10.0.0.1      (Enterprise networks)
3. ICMP echo to discovered addresses
```

### Phase 3: Subnet Calculation
```
Given detected neighbor IP: X.X.X.N
Calculate gateway IP: X.X.X.{1 or 2}
  - If neighbor ends in .1 → use .2
  - Otherwise → use .1
Apply /24 subnet mask (255.255.255.0)
```

### Phase 4: Configuration & Verification
```
1. Flush existing eth0 IPv4 addresses
2. Assign calculated IP to eth0
3. Verify connectivity via ICMP
4. Start IP keepalive daemon
```

---

## IP Persistence Mechanism

The keepalive daemon runs as a background process, polling every 5 seconds:

```bash
while true; do
    if [current_ip != expected_ip]; then
        ip addr add $expected_ip dev eth0
    fi
    sleep 5
done
```

This overcomes OS-level network reconfiguration that may occur due to:
- Container networking events
- DHCP client interference
- NetworkManager policies

---

## Fallback Behavior

When no device is detected within the timeout period:

1. Gateway assumes **DHCP server role**
2. Configures eth0 as `192.168.1.1/24`
3. Starts dnsmasq with range `192.168.1.100-200`
4. Any device connecting will receive automatic IP assignment

---

## Performance Metrics

| Metric | Value |
|--------|-------|
| Boot to network ready | ~50 seconds |
| Detection time | 5-20 seconds |
| Ping latency (local) | 0.3-0.8 ms |
| IP recovery time | ≤5 seconds |

---

## Test Results

### Validation Test (2026-02-03 15:18 UTC)

| Phase | Timestamp | Result |
|-------|-----------|--------|
| Power off | 15:18:41 | — |
| Power on | 15:19:31 | Boot: 50s |
| Detection | 15:19:45 | Found 192.168.137.1 |
| Configuration | 15:19:45 | Set 192.168.137.2/24 |
| Verification | 15:19:56 | 3/3 packets, 0% loss |

---

## Human-AI Collaboration Model

This system was developed through real-time collaboration between:

- **Human (Mike Harper):** Requirements specification, hardware setup, physical testing, architectural decisions
- **AI (Jarvis/Claude):** Code generation, deployment automation, remote monitoring, documentation

Communication occurred via Telegram messaging. The AI had direct access to:
- VPS infrastructure (SSH)
- balenaCloud deployment platform
- Raspberry Pi via Tailscale VPN
- GitHub repository

The development cycle—from concept to validated deployment—completed in approximately 2 hours.

---

## Future Work (v3.0)

- PLC protocol integration (EtherNet/IP, Modbus TCP)
- Tag read/write via REST API
- MQTT telemetry publishing
- Multi-device subnet bridging

---

## Repository

**Source:** https://github.com/Mikecranesync/jarvis-workspace  
**Release:** https://github.com/Mikecranesync/jarvis-workspace/releases/tag/v2.0.0

---

*© 2026 FactoryLM. Developed in Atlanta, GA.*
