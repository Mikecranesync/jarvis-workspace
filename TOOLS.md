# TOOLS.md - Local Notes

Skills define *how* tools work. This file is for *your* specifics — the stuff that's unique to your setup.

---

## FactoryLM Website
- **Repo:** `https://github.com/Mikecranesync/factorylm-landing`
- **Local:** `/root/jarvis-workspace/landing-page/`
- **Live:** `https://factorylm.com`
- **Hosting:** Unknown server (72.60.175.144) - TODO: find deploy method
- **Skill:** `/root/jarvis-workspace/skills/factorylm-website/SKILL.md`

## Servers
- **This VPS:** factorylm-prod (DigitalOcean Atlanta, 8GB RAM)
- **PLC Laptop:** 100.72.2.99 (Tailscale), Quadro P620 GPU, runs Ollama
- **Old VPS:** Unknown (4GB RAM, 91% disk) - still sending heartbeats, needs shutdown

## Key Services
- **Master of Puppets:** `/opt/master_of_puppets/` - Celery swarm (22 agents)
- **PLC Copilot:** `/opt/plc-copilot/` - Telegram bot for photo→CMMS
- **FactoryLM Monolith:** `/opt/factorylm/` - New consolidated codebase (WIP)
- **CMMS:** Docker container `cmms-backend` on port 8080

## API Keys Location
- `/opt/master_of_puppets/.env` - Main env file for all agents
- Groq, Gemini, Perplexity, LangFuse configured

## Telegram Bots
- **Clawdbot/Jarvis:** This bot (main assistant)
- **JarvisMIO:** PLC Copilot bot (token: 7855741814)
- **JarvisVPS Heartbeat:** Uses token 8387943893

## GitHub Repos
- `mikecranesync/factorylm-landing` - Marketing website
- `mikecranesync/Rivet-PRO` - Main product repo

## Jarvis Nodes (Remote Laptop Control)
Installers: `/root/jarvis-workspace/installers/jarvis-node/`

| Node | Tailscale IP | Port | Status |
|------|-------------|------|--------|
| plc-laptop | 100.72.2.99 | 8765 | Install pending |
| travel-laptop | 100.83.251.23 | 8765 | Install pending |

### Quick commands from VPS:
```python
from workers.jarvis_node_client import plc_laptop, travel_laptop

# Screenshot
plc_laptop().screenshot(save_path="/tmp/screen.png")

# Run command
plc_laptop().shell("ollama list")

# Click
plc_laptop().click(500, 300)

# Type
plc_laptop().type_text("Hello!")
```

### Install on Windows (run as Admin):
```powershell
# PLC Laptop
scp root@100.68.120.99:/root/jarvis-workspace/installers/jarvis-node/install-plc-laptop.ps1 .
.\install-plc-laptop.ps1

# Travel Laptop
scp root@100.68.120.99:/root/jarvis-workspace/installers/jarvis-node/install-travel-laptop.ps1 .
.\install-travel-laptop.ps1
```

---

Add whatever helps you do your job. This is your cheat sheet.

## Raspberry Pi Edge Device
- **Tailscale IP:** 100.97.210.121
- **Hostname:** factorylm-edge-pi
- **OS:** balenaOS 6.10.24
- **Balena Dashboard:** https://dashboard.balena-cloud.com/devices/9cc587cafd03a9fe57d2480bc0bff931
- **SSH:** `ssh root@100.97.210.121`
- **Purpose:** Micro820 PLC gateway

### Quick Commands:
```bash
# SSH to Pi
ssh root@100.97.210.121

# Check Pi status via Balena
balena device list --fleet factorylm-edge

# Restart Pi
balena device restart 9cc587cafd03
```
