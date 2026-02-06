# Jarvis Remote Access Architecture
*Immutable. Set once, never touch again.*

## Overview

Jarvis (VPS) can remotely control Windows laptops via SSH. This is the PRIMARY method for:
- Running Claude CLI on laptops
- Taking screenshots
- Executing commands
- Controlling Factory I/O
- Any remote operation

## Network Topology

```
┌─────────────────────────────────────────────────────────────────┐
│                        TAILSCALE MESH                           │
│                                                                 │
│  ┌──────────────┐     ┌──────────────┐     ┌──────────────┐    │
│  │  VPS (Jarvis)│────▶│ Travel Laptop│     │  PLC Laptop  │    │
│  │ 100.68.120.99│     │100.83.251.23 │     │ 100.72.2.99  │    │
│  │              │────▶│              │     │              │    │
│  └──────────────┘     └──────────────┘     └──────────────┘    │
│         │                    │                    │             │
│         │              SSH (Port 22)        SSH (Port 22)       │
│         │                    │                    │             │
│         └────────────────────┴────────────────────┘             │
│                                                                 │
│  ┌──────────────┐     ┌──────────────┐                         │
│  │   Hetzner    │     │  Pixel 9a    │                         │
│  │100.67.25.53  │     │100.73.197.64 │                         │
│  └──────────────┘     └──────────────┘                         │
└─────────────────────────────────────────────────────────────────┘
```

## Authentication

**SSH Key:** `/root/.ssh/jarvis_laptop_key`
**Public Key:**
```
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAILEvc+FEGGSG0yswWMPGYxh1NA5FdRAdfAkTVR1pfxwY jarvis-remote-access
```

## Laptop Configuration (One-Time Setup)

Each Windows laptop needs:
1. OpenSSH Server enabled
2. Jarvis public key in authorized_keys
3. Claude CLI installed
4. Startup script to ensure services run

## Usage

From VPS, run:
```bash
# Travel laptop
ssh -i ~/.ssh/jarvis_laptop_key mike@100.83.251.23 "command"

# PLC laptop  
ssh -i ~/.ssh/jarvis_laptop_key mike@100.72.2.99 "command"
```

## Wrapper Functions

See `/opt/jarvis/remote-laptop.sh` for helper functions:
- `laptop_exec <laptop> <command>` - Run command
- `laptop_claude <laptop> <prompt>` - Run Claude CLI
- `laptop_screenshot <laptop>` - Take screenshot
- `laptop_status` - Check all laptops

## Fallback Methods

If SSH fails:
1. Jarvis Node (WebSocket) - Port 8765
2. FastAPI webhook - Port 8000
3. Manual intervention

## Troubleshooting

**SSH connection refused:**
- Check Windows OpenSSH Server is running
- Check Windows Firewall allows port 22
- Run `services.msc` → OpenSSH SSH Server → Start

**Permission denied:**
- Verify public key in `C:\Users\mike\.ssh\authorized_keys`
- Check file permissions (Windows ACL)

---
*Last updated: 2026-02-06*
