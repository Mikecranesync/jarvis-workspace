# CLAUDE.md — Onboarding for AI Instances

*Last updated: 2026-01-30*

This file helps any Claude instance (or AI coding assistant) get up to speed quickly on this workspace.

---

## 🏠 What Is This?

This is **Jarvis Workspace** — the operational hub for Mike Harper's industrial AI company **FactoryLM**.

**Mission:** Build the Industrial Maintenance Intelligence Center — AI that helps maintenance technicians diagnose equipment faults faster.

**Products:**
- **FactoryLM** — AI-powered maintenance diagnostics (photo error → get fix)
- **PLC Copilot** — AI assistant for PLC troubleshooting
- **RideView** — Torque stripe inspection for safety-critical bolts
- **BeagleBone Gateway** — Sub-$500 industrial protocol adapter

---

## 📋 First Steps When Starting a Session

1. **Read SOUL.md** — Your identity and personality
2. **Read USER.md** — About Mike (your human)
3. **Read `memory/YYYY-MM-DD.md`** — Today's and yesterday's context
4. **If direct chat with Mike:** Also read MEMORY.md (long-term memory)

---

## 🏛️ Foundational Documents

| Document | Purpose |
|----------|---------|
| `CONSTITUTION.md` | Operating principles, boundaries, mission |
| `ENGINEERING_COMMANDMENTS.md` | Code quality rules (GitHub Issues → Branch → PR → Approval) |
| `AGENTS.md` | How to operate in this workspace |
| `SOUL.md` | Your personality and identity |
| `USER.md` | About Mike Harper |

**Read these before making significant decisions.**

---

## 🚧 Current Projects (as of 2026-01-30)

### P0: BeagleBone Industrial Gateway
- **Location:** `projects/beaglebone-gateway/`
- **Status:** Software complete, awaiting hardware deployment
- **What:** Universal protocol adapter (Modbus, S7, EtherNet/IP, MELSEC, OPC UA)
- **Goal:** Sub-$500 competitor to $2,000+ commercial gateways

### Sales Automation System
- **Location:** `infrastructure/sales-automation/`
- **Status:** n8n + Mautic deployed, workflows ready
- **What:** 24/7 automated lead outreach robot
- **Services:** 
  - n8n: http://72.60.175.144:5678
  - Mautic: http://72.60.175.144:8081

### FactoryLM Landing Page
- **Location:** `landing-page/`
- **Status:** Live at https://mikecranesync.github.io/factorylm-landing/
- **Blog:** 10 posts published

---

## 🔧 Key Infrastructure

| Service | URL | Purpose |
|---------|-----|---------|
| VPS | 72.60.175.144 | Main server |
| n8n | :5678 | Workflow automation |
| Mautic | :8081 | Email marketing |
| CMMS Demo | :8080 | Atlas CMMS |
| Landing Page | GitHub Pages | Marketing site |

---

## 📁 Directory Structure

```
jarvis-workspace/
├── CONSTITUTION.md          # Operating principles
├── ENGINEERING_COMMANDMENTS.md  # Code rules
├── AGENTS.md                # Workspace behavior
├── SOUL.md                  # AI identity
├── USER.md                  # About Mike
├── MEMORY.md                # Long-term memories
├── CLAUDE.md                # This file
├── memory/                  # Daily logs
├── brain/
│   ├── plans/              # Strategic plans
│   └── research/           # Research notes
├── projects/
│   ├── beaglebone-gateway/ # Industrial gateway
│   ├── cmms/               # Maintenance system
│   └── factorylm-core/     # Core platform
├── infrastructure/
│   └── sales-automation/   # n8n + Mautic
├── landing-page/           # GitHub Pages site
├── artifacts/              # Generated content
└── signals/                # Inter-agent messaging
```

---

## 🎯 Trello Board

All work is tracked on Trello: https://trello.com/b/3lxABXX4

**Vision-to-Trello Pattern:**
1. Vision card in "🎯 Visions" list
2. Step cards broken from vision (5-7 tasks)
3. Steps flow: Backlog → In Progress → Done → Shipped

---

## ⚡ Quick Commands

```bash
# Check Trello status
# (API creds in clawdbot config)

# Git workflow (per Commandments)
git checkout -b feature/your-feature
# Make changes
git add .
git commit -m "descriptive message"
git push origin feature/your-feature
# Create PR, wait for Mike's approval

# Docker services
docker ps  # See running containers
docker-compose -f infrastructure/sales-automation/docker-compose.yml up -d
```

---

## 🚨 Important Rules

1. **Never merge PRs without Mike's verbal approval**
2. **Never deploy to production without approval**
3. **Always create GitHub issues before code changes**
4. **Always send voice + text messages to Mike (Amendment V)**
5. **Follow the Constitution and Commandments**

---

## 📞 Contact

- **Mike Harper** (human): Telegram, via Clawdbot
- **Jarvis** (this AI): Multiple instances, shared workspace

---

*This file should be updated whenever major changes occur to help future AI instances onboard quickly.*
