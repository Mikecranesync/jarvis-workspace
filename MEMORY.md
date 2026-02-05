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

---

## FactoryLM Edge v2.0 - TRUE PLUG-AND-PLAY (2026-02-03)

### What It Does
Raspberry Pi that auto-detects ANY connected device's network and joins it.
No manual IP configuration - just plug in ethernet cable.

### How It Works
1. network_detect.py scans via ARP/ping probing
2. Detects connected device's IP (e.g., 192.168.137.1)
3. Auto-configures Pi to same subnet (e.g., 192.168.137.2)
4. IP keepalive daemon maintains config every 5 seconds
5. Falls back to DHCP server if no device detected

### Key Insight
The Pi adapts to the DEVICE's network, not the other way around.
This is how industrial gateways work - they join existing networks.

### Micro820 PLC Notes
- pycomm3 has PARTIAL Micro820 support (finicky)
- Modbus TCP is PRIMARY protocol for Micro820
- Micro820 defaults to DHCP - need BOOTP/CCW for static IP first
- Test both port 502 (Modbus) and 44818 (EtherNet/IP)

### Files
- `/infrastructure/balena/plc-gateway/` - Container code
- `/docs/factorylm-edge-v2-whitepaper.md` - Technical paper
- GitHub: https://github.com/Mikecranesync/jarvis-workspace/releases/tag/v2.0.0

### Validated
- 50 second boot time
- 0.37-0.54ms ping latency
- 0% packet loss
- Survives power cycles

---

## 2026-02-05 Sprint Learnings

### Product Strategy Insight
Photo identification is the HOOK, not the product. The moat is:
- Workflow integration (CMMS, work orders)
- Organizational memory (equipment history across team)
- Artifact delivery (QR codes, checklists, voice walkthroughs)
- Upsell path to Connect/Predict tiers

### LLM Cascade Architecture
Mike's preferred cascade: Grok → DeepSeek → cheap model (until own LLM trained)
Infrastructure exists in Rivet-PRO's llm_manager.py (Claude → GPT-4 → Cache)

### Rivet-PRO is Production Code
48+ service files including photo_service.py, stripe_service.py, llm_manager.py
Knowledge base services, equipment services - monetizable infrastructure

### Voice Output = The Crack Moment
Instead of text results, speak to the user. "This is a Baldor 5HP motor..."
Hands-free while working on equipment. Nobody else does this.

### Three-Tier Product Strategy
1. Identify - Photo only, FREE tier, $49/mo pro
2. Connect - PLC integration via Edge Agent, $199/mo
3. Predict - IO-Link hardware + predictive AI, $499/mo
