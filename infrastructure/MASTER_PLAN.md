# RemoteMe Infrastructure - Master Plan

**Last Updated:** 2026-02-03

---

## 🎯 Goal

Make all of Mike's computers observable and controllable remotely via Telegram, with AI-powered automation.

---

## 🏗️ Architecture

```
                         ┌─────────────────────────┐
                         │       TELEGRAM          │
                         │    (User Interface)     │
                         └───────────┬─────────────┘
                                     │
                         ┌───────────▼─────────────┐
                         │    JARVIS VPS           │
                         │  factorylm-prod         │
                         │  100.68.120.99          │
                         │                         │
                         │  • Clawdbot (Telegram)  │
                         │  • Open Interpreter     │
                         │  • Jarvis Node Client   │
                         │  • Proof of Work        │
                         │  • Ground Truth         │
                         └───────────┬─────────────┘
                                     │
                    ┌────────────────┼────────────────┐
                    │ Tailscale      │                │
                    │ (Encrypted)    │                │
         ┌──────────▼──────────┐  ┌──▼────────────┐  ┌▼─────────────────┐
         │   PLC LAPTOP        │  │ TRAVEL LAPTOP │  │  RASPBERRY PI    │
         │   100.72.2.99       │  │ 100.83.251.23 │  │  (Pending)       │
         │                     │  │               │  │                  │
         │   • Jarvis Node     │  │ • Jarvis Node │  │  • Jarvis Node   │
         │   • Ollama (LLM)    │  │ • Claude Code │  │  • Camera        │
         │   • RSLogix         │  │               │  │  • Sensors       │
         │   • OBS Studio      │  │               │  │  • GPIO          │
         └─────────────────────┘  └───────────────┘  └──────────────────┘
```

---

## 📋 Components

### 1. VPS (Brain) - DONE ✅
- Ubuntu 24.04 LTS
- Clawdbot running
- Open Interpreter installed
- Docker, Git, Python, Node
- Claude Code CLI installed
- Firewall configured
- User 'mike' with sudo

### 2. Tailscale Mesh - DONE ✅
- All devices visible
- Encrypted P2P connections
- No port forwarding needed

### 3. Jarvis Node (Laptops) - PENDING ⏳
- FastAPI server on each laptop
- Endpoints: /health, /shell, /screenshot, /click, /type, /interpret
- Auto-starts as Windows service
- Connects via Tailscale

### 4. Jarvis Node (Raspberry Pi) - PENDING ⏳
- Headless Raspberry Pi
- Camera support
- GPIO control
- Sensor monitoring
- Tailscale for connectivity

### 5. Observability - PENDING ⏳
- Grafana dashboards
- OTEL metrics from Clawdbot
- System health monitoring
- Proof of Work evidence

---

## 🚀 Deployment Status

| Component | Status | Blocker |
|-----------|--------|---------|
| VPS Setup | ✅ Done | - |
| Tailscale | ✅ Done | - |
| SSH VPS→Laptops | ❌ Blocked | Key not authorized |
| Jarvis Node (PLC) | ⏳ Pending | SSH needed first |
| Jarvis Node (Travel) | ⏳ Pending | SSH needed first |
| Raspberry Pi | ⏳ Pending | Network setup |
| Grafana | ⏳ Pending | After Jarvis Nodes |
| OTEL | ⏳ Pending | Clawdbot restart |

---

## 📁 File Locations

```
/root/jarvis-workspace/
├── infrastructure/
│   ├── MASTER_PLAN.md          # This file
│   ├── scripts/
│   │   ├── setup-ssh-key.ps1   # Add VPS key to Windows
│   │   ├── install-jarvis-node.ps1
│   │   ├── setup-pi.sh         # Raspberry Pi setup
│   │   └── health-check.sh     # Check all nodes
│   ├── docs/
│   │   ├── WINDOWS_SSH_SETUP.md
│   │   ├── RASPBERRY_PI_SETUP.md
│   │   └── TROUBLESHOOTING.md
│   └── installers/
│       └── raspberry-pi/
│           ├── first-boot.sh
│           └── jarvis-node-pi.py
├── installers/
│   └── jarvis-node/
│       ├── jarvis_node.py
│       ├── install-plc-laptop.ps1
│       └── install-travel-laptop.ps1
└── MISSION.md
```
