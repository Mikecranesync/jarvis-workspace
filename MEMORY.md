# MEMORY.md - Long-Term Memory

## CRITICAL DIRECTIVE: KNOWLEDGE BASE CAPTURE
**Everything I do is being traced via LangSmith/Flowise/n8n.**
- All interactions → knowledge base
- Every troubleshooting session = learning atoms
- I must actively capture lessons, not just work through problems
- Tracing infrastructure: Flowise :3001, n8n :5678

## Mike Harp (My Human)
- Industrial AI / PLC automation expert
- Building FactoryLM - autonomous industrial maintenance platform
- Wants AI agents that work while he sleeps
- Values: Visual/observable systems, spec-based engineering, 5-second verification
- Hates: "We don't need that yet" responses, walls of text, JSON output

## The Spec (TATTOOED)
Every workflow MUST:
1. Be mapped in Flowise/n8n OR callable via API
2. Be proven end-to-end with REAL WORLD results
3. Be testable in 5 seconds with simple prompt
4. Pass the 11-year-old test
5. Be observable - Mike must SEE what's happening

---

## Hardware & Network

### Laptops
| Device | Tailscale IP | Role |
|--------|--------------|------|
| PLC Laptop (LAPTOP-0KA3C70H) | 100.72.2.99 | Factory I/O, TIA Portal, RSLinx |
| Travel Laptop (miguelomaniac) | 100.83.251.23 | Mobile work |

### BeagleBone Setup - LESSONS LEARNED
**USB Drivers on Windows are BROKEN:**
- Official BONE_D64.exe fails on Win10/11
- RNDIS (USB network) won't install
- USB Serial (COM3) won't install
- Device Manager "update driver" says "no update needed" but doesn't work

**Working Path: Ethernet**
- Direct cable from laptop to BeagleBone
- Laptop static IP: 192.168.1.50 / 255.255.255.0
- Command: `netsh interface ip set address "Ethernet" static 192.168.1.50 255.255.255.0`

**Power Requirements:**
- Use 5V 2A+ barrel jack (USB power is flaky)
- KITT heartbeat LEDs = booted successfully

**Custom Image:**
- Mike and I built a custom SD card image
- IP: 192.168.1.100
- SSH may not be enabled by default!
- Need serial console or re-flash to enable SSH

### Network Map
```
192.168.1.50  = PLC Laptop (Ethernet)
192.168.1.100 = BeagleBone OR Micro 820 PLC
192.168.4.x   = Home WiFi network
100.x.x.x     = Tailscale VPN
```

---

## Key Repos

### factorylm (monorepo)
- `services/plc-modbus/` - Modbus TCP communication
- `services/plc-modbus/factorylm-edge/` - BeagleBone edge device
- `services/plc-copilot/` - PLC assistant

### Edge Device Config
```json
{
  "server": {"host": "0.0.0.0", "port": 502},
  "inputs": [{"coil": 0, "gpio": 17, "name": "Start_Button"}],
  "outputs": [{"coil": 10, "gpio": 5, "name": "LED_Green"}]
}
```

---

## VPS Architecture

### Master of Puppets (Celery Workers)
- The Monkey: Polls Jira, routes tasks
- The Conductor: Orchestrates automatons
- Manual Hunter: Searches manuals
- The Weaver: Generates reports
- The Watchman: Monitors systems
- The Cartographer: Maps code dependencies

### Integrations
- Syncthing: File sync between VPS/laptops/phones
- Laptop Agent: Remote Claude Code execution via SSH
- Jira: Task management
- Telegram: Alerts and chat

---

## Lessons Learned

### 2026-02-01
- BeagleBone USB drivers are nightmare on Windows - USE ETHERNET
- Always have serial console backup (USB-to-TTL adapter)
- Custom images need SSH enabled before deployment
- Document EVERYTHING - I forget between sessions
