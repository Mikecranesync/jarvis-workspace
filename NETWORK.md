# FactoryLM Network Registry

> **Last Updated:** 2026-02-03
> **Managed By:** Jarvis (Clawdbot)

## 🌐 Tailscale Network

| Device | Tailscale IP | Hostname | Role | Location |
|--------|-------------|----------|------|----------|
| **VPS Jarvis** | 100.68.120.99 | factorylm-prod | Gateway, Brain | DigitalOcean Atlanta |
| **Pi Edge** | 100.97.210.121 | factorylm-edge-pi | Edge Controller | Mike's Home |
| **PLC Laptop** | 100.72.2.99 | laptop-0ka3c70h | Factory I/O, Dev | Mike's Home |
| **Travel Laptop** | 100.83.251.23 | miguelomaniac | Mobile Dev | Mobile |
| **srv1078052** | 100.102.30.102 | srv1078052 | ❓ Review for decommission | Unknown |

## 🔧 Device Details

### VPS Jarvis (100.68.120.99)
- **OS:** Ubuntu Linux
- **Services:** Clawdbot, Docker (17 containers), n8n, Flowise, CMMS
- **Access:** SSH root@100.68.120.99

### Pi Edge (100.97.210.121)
- **OS:** balenaOS 6.10.24
- **Hardware:** Raspberry Pi 4, 4GB RAM
- **Balena UUID:** 9cc587cafd03a9fe57d2480bc0bff931
- **Dashboard:** https://dashboard.balena-cloud.com/devices/9cc587cafd03a9fe57d2480bc0bff931
- **Access:** SSH root@100.97.210.121
- **Purpose:** Micro820 PLC gateway via Ethernet/IP
- **PLC Gateway API:** http://100.97.210.121:5000
- **API Endpoints:**
  - `GET /` - Status
  - `GET /health` - Health check
  - `GET /plc/info` - PLC device info
  - `GET /plc/read/<tag>` - Read tag
  - `POST /plc/write` - Write tag
  - `GET /plc/tags` - List tags
- **PLC Config:** Expecting Micro820 at 192.168.1.10

### PLC Laptop (100.72.2.99)
- **OS:** Windows
- **Software:** Factory I/O, Jarvis Node (planned)
- **Connected Hardware:** Micro820 PLC (Ethernet)
- **⚠️ NEVER SET STATIC IP** - Caused outage 2026-02-03

### Travel Laptop (100.83.251.23)
- **OS:** Windows
- **Software:** Claude Code CLI, Dev environment
- **Purpose:** Mobile development

## 🚨 Lessons Learned

### 2026-02-03: Static IP Broke PLC Laptop
- **Symptom:** "No Internet, secured" on WiFi
- **Cause:** Static IP 192.168.10.1 set on WiFi adapter
- **Fix:** Changed to "Obtain IP automatically" (DHCP)
- **Prevention:** ALWAYS use DHCP. Document any exceptions here.

## 📋 Network Rules

1. **All devices use DHCP** - No static IPs without documentation
2. **Tailscale must auto-start** on all devices
3. **Device names must be descriptive** in Tailscale admin
4. **New devices** get added to this registry immediately

## 🔌 Physical Connections

```
[Eero Router] ─── WiFi ───┬─── [Pi Edge]
                          ├─── [PLC Laptop] ─── Ethernet ─── [Micro820 PLC]
                          └─── [Travel Laptop] (when home)
```

## 📡 Monitoring

Jarvis checks every 30 minutes:
- Ping all Tailscale devices
- Alert if any device offline > 10 min
- Log connectivity to memory/network-health.log
