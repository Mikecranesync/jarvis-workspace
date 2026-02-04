# JARVIS Architecture - Digital Twin Blueprint

**Created:** 2026-02-04  
**Purpose:** Complete documentation of the Jarvis AI assistant configuration, enabling recreation on any server.  
**Status:** LIVING DOCUMENT - Update when configuration changes

---

## Overview

Jarvis is an AI assistant built on **Clawdbot**, an open-source framework for creating personal AI agents. This document captures everything needed to recreate Jarvis from scratch.

```
┌─────────────────────────────────────────────────────────────────┐
│                        JARVIS STACK                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   ┌─────────────────┐    ┌─────────────────┐                   │
│   │    Telegram     │    │   Other Channels │                   │
│   │    @JarvisBot   │    │   (future)       │                   │
│   └────────┬────────┘    └────────┬─────────┘                   │
│            │                      │                             │
│            └──────────┬───────────┘                             │
│                       ▼                                         │
│   ┌─────────────────────────────────────────┐                  │
│   │           CLAWDBOT GATEWAY              │                  │
│   │   - Message routing                     │                  │
│   │   - Tool execution                      │                  │
│   │   - Session management                  │                  │
│   │   - Cron jobs                           │                  │
│   └────────────────────┬────────────────────┘                  │
│                        │                                        │
│            ┌───────────┼───────────┐                           │
│            ▼           ▼           ▼                           │
│   ┌─────────────┐ ┌─────────┐ ┌─────────────┐                 │
│   │   Claude    │ │ Gemini  │ │   Ollama    │                 │
│   │   (primary) │ │ (image) │ │   (local)   │                 │
│   └─────────────┘ └─────────┘ └─────────────┘                 │
│                                                                 │
│   ┌─────────────────────────────────────────┐                  │
│   │           WORKSPACE                      │                  │
│   │   /root/jarvis-workspace                 │                  │
│   │   - AGENTS.md (behavior rules)           │                  │
│   │   - SOUL.md (personality)                │                  │
│   │   - memory/ (daily logs)                 │                  │
│   │   - brain/ (knowledge base)              │                  │
│   └─────────────────────────────────────────┘                  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 1. Infrastructure Requirements

### 1.1 Server Specifications

| Component | Current Setup | Minimum |
|-----------|---------------|---------|
| OS | Ubuntu 24.04 LTS | Ubuntu 22.04+ |
| CPU | 1 vCPU | 1 vCPU |
| RAM | 4 GB | 2 GB |
| Disk | 50 GB | 20 GB |
| Network | Static IP, ports 80/443 | Outbound internet |

### 1.2 Required Software

```bash
# System packages
apt update && apt install -y \
  curl \
  git \
  jq \
  python3 \
  python3-pip \
  docker.io \
  docker-compose

# Node.js (v22+)
curl -fsSL https://deb.nodesource.com/setup_22.x | bash -
apt install -y nodejs

# Clawdbot
npm install -g clawdbot

# Tailscale (for secure networking)
curl -fsSL https://tailscale.com/install.sh | sh
```

### 1.3 Version Information

| Software | Version |
|----------|---------|
| Clawdbot | 2026.1.24-3 |
| Node.js | v22.22.0 |
| Ubuntu | 24.04 LTS |

---

## 2. Clawdbot Configuration

### 2.1 Config File Location

```
/root/.clawdbot/clawdbot.json
```

### 2.2 Config Structure (Template)

```json
{
  "meta": {
    "lastTouchedVersion": "2026.1.24-3"
  },
  "env": {
    "GEMINI_API_KEY": "<your-gemini-key>",
    "GOOGLE_API_KEY": "<your-google-key>",
    "SENDGRID_API_KEY": "<your-sendgrid-key>",
    "TRELLO_API_KEY": "<your-trello-key>",
    "TRELLO_TOKEN": "<your-trello-token>",
    "BRAVE_API_KEY": "<your-brave-key>"
  },
  "models": {
    "providers": {
      "ollama": {
        "baseUrl": "http://127.0.0.1:11434/v1",
        "apiKey": "ollama-local",
        "api": "openai-completions",
        "models": [
          {
            "id": "qwen2.5:0.5b",
            "name": "Qwen 2.5 0.5B"
          }
        ]
      }
    }
  },
  "agents": {
    "defaults": {
      "model": {
        "primary": "anthropic/claude-opus-4-5",
        "fallbacks": ["anthropic/claude-sonnet-4-20250514", "google/gemini-2.5-flash"]
      },
      "imageModel": {
        "primary": "google/gemini-2.5-flash"
      },
      "workspace": "/root/jarvis-workspace"
    }
  },
  "channels": {
    "telegram": {
      "enabled": true,
      "token": "<your-telegram-bot-token>",
      "adminChatIds": ["8445149012"],
      "allowedChatIds": ["8445149012"]
    }
  }
}
```

### 2.3 API Keys Required

| Service | Purpose | How to Get |
|---------|---------|------------|
| Anthropic | Claude AI (primary) | console.anthropic.com |
| Google | Gemini (images, fallback) | aistudio.google.com |
| Telegram | Messaging | @BotFather |
| Trello | Task management | trello.com/app-key |
| Brave | Web search | brave.com/search/api |
| SendGrid | Email sending | sendgrid.com |

---

## 3. Workspace Structure

### 3.1 Location

```
/root/jarvis-workspace/
```

### 3.2 Core Files (MUST HAVE)

| File | Purpose | Critical? |
|------|---------|-----------|
| `AGENTS.md` | Behavior rules, how I operate | ✅ YES |
| `SOUL.md` | Personality, values, boundaries | ✅ YES |
| `USER.md` | Information about Mike | ✅ YES |
| `TOOLS.md` | Local tool notes, API details | ✅ YES |
| `MEMORY.md` | Long-term curated memory | ✅ YES |
| `HEARTBEAT.md` | Periodic check tasks | Optional |
| `ENGINEERING_COMMANDMENTS.md` | Code review rules | ✅ YES |

### 3.3 Directory Structure

```
jarvis-workspace/
├── AGENTS.md                 # Core behavior rules
├── SOUL.md                   # Personality
├── USER.md                   # User profile
├── TOOLS.md                  # Tool notes
├── MEMORY.md                 # Long-term memory
├── ENGINEERING_COMMANDMENTS.md
├── HEARTBEAT.md              # Periodic checks
│
├── memory/                   # Daily memory files
│   ├── 2026-02-04.md
│   ├── 2026-02-03.md
│   └── heartbeat-state.json
│
├── brain/                    # Knowledge base
│   ├── FACTORYLM_MINI_MASTER.md
│   ├── FACTORYLM_UNIVERSAL_FAULT_SCHEMA.md
│   ├── AUTOMATED_TESTING_FACTORYLM.md
│   ├── specs/               # Specification documents
│   ├── field-logs/          # Real-world experiences
│   ├── research/            # Research reports
│   └── decisions/           # Decision logs
│
├── projects/                 # Active project docs
├── signals/                  # Inter-process communication
│   ├── inbox/
│   ├── outbox/
│   └── alerts/
│
└── skills/                   # Custom skills (future)
```

### 3.4 Key File Contents Summary

**AGENTS.md** - Tells me:
- How to wake up each session (read SOUL, USER, memory)
- When to use memory files vs MEMORY.md
- Safety rules (no exfiltration, ask before external actions)
- Group chat etiquette
- Heartbeat behavior
- Vision-to-Trello workflow
- Zero-drift infrastructure rule

**SOUL.md** - Tells me:
- Be genuinely helpful, not performatively
- Have opinions
- Be resourceful before asking
- Earn trust through competence
- Keep private things private
- Be concise but thorough

**USER.md** - Contains:
- Mike's name, timezone, preferences
- Business context (CraneSync, FactoryLM)
- Email accounts
- Working style notes

---

## 4. Cron Jobs (Clawdbot Internal)

Clawdbot manages cron jobs internally. Current active jobs:

| Job | Schedule | Purpose |
|-----|----------|---------|
| Monitor Agent | Every 15 min | System health checks |
| Code Agent | Every 30 min | Check for coding tasks |
| Trello Check | Every 5 min | Look for @jarvis tasks |
| Laptop Check | Every 5 min | Tailscale status monitoring |
| Research Report | Periodic | Generate insights |

These are configured via the Clawdbot cron system, not system crontab.

---

## 5. Integrations

### 5.1 Telegram Bot

- **Bot Name:** Jarvis
- **Admin Chat ID:** 8445149012 (Mike)
- **Features:** Voice messages, inline buttons, reactions

### 5.2 GitHub

- **Auth:** `gh` CLI authenticated
- **Repos:** mikecranesync/* (private repos)
- **Workflow:** Issue → Branch → PR → Review → Merge

### 5.3 Trello

- **Board:** FactoryLM: Path to $1M ARR
- **Board:** Beginning with the End in Mind
- **Usage:** Task tracking, vision cards

### 5.4 Email (Himalaya)

- **Config:** `/root/.config/himalaya/config.toml`
- **Accounts:** harperhousebuyers@gmail.com, hharperson2000@yahoo.com
- **Pending:** mike@cranesync.com

### 5.5 Tailscale

- **VPS IP:** 100.102.30.102
- **Connected devices:** See TOOLS.md

---

## 6. Memory System

### 6.1 Three-Layer Memory

1. **Daily Files** (`memory/YYYY-MM-DD.md`)
   - Raw session logs
   - What happened today
   - Ephemeral, detailed

2. **MEMORY.md** (root)
   - Curated long-term memory
   - Key insights, preferences, lessons
   - Distilled from daily files
   - Only loaded in main sessions (security)

3. **Brain Folder** (`brain/`)
   - Structured knowledge documents
   - Project specs, schemas, plans
   - Permanent reference material

### 6.2 Memory Maintenance

Periodically (during heartbeats):
1. Review recent daily files
2. Extract significant learnings
3. Update MEMORY.md
4. Archive old daily files if needed

---

## 7. Skills

### 7.1 Built-in Skills

Located in `/usr/lib/node_modules/clawdbot/skills/`:
- github
- trello
- weather
- notion
- tmux
- coding-agent

### 7.2 Custom Skills (Planned)

To be created in `jarvis-workspace/skills/`:
- factorylm (in spec phase)

---

## 8. Recreation Procedure

### Step 1: Provision Server
```bash
# Ubuntu 24.04 VPS with 4GB RAM, 50GB disk
```

### Step 2: Install Dependencies
```bash
apt update && apt upgrade -y
apt install -y curl git jq python3 python3-pip docker.io

# Node.js
curl -fsSL https://deb.nodesource.com/setup_22.x | bash -
apt install -y nodejs

# Clawdbot
npm install -g clawdbot

# Tailscale
curl -fsSL https://tailscale.com/install.sh | sh
tailscale up
```

### Step 3: Clone Workspace
```bash
cd /root
git clone git@github.com:mikecranesync/jarvis-workspace.git
```

### Step 4: Configure Clawdbot
```bash
mkdir -p /root/.clawdbot
# Copy clawdbot.json template and fill in API keys
```

### Step 5: Start Clawdbot
```bash
clawdbot gateway start
systemctl enable clawdbot
```

### Step 6: Verify
- Send test message via Telegram
- Check logs: `journalctl -u clawdbot -f`

---

## 9. Backup Strategy

### 9.1 What to Backup

| Item | Location | Method |
|------|----------|--------|
| Workspace | /root/jarvis-workspace | Git (GitHub) |
| Config | /root/.clawdbot | Manual backup |
| Memory | workspace/memory/ | Git |
| Brain | workspace/brain/ | Git |

### 9.2 Backup Commands

```bash
# Push workspace to GitHub
cd /root/jarvis-workspace
git add -A
git commit -m "Backup $(date +%Y-%m-%d)"
git push

# Backup config (manual)
cp /root/.clawdbot/clawdbot.json /secure/location/
```

---

## 10. Troubleshooting

### Common Issues

| Problem | Solution |
|---------|----------|
| Clawdbot not responding | `systemctl restart clawdbot` |
| Telegram not connected | Check bot token in config |
| API errors | Check API key validity |
| Disk full | Run cleanup (see VPS optimization) |
| Memory not persisting | Check git push, workspace permissions |

### Health Check Command

```bash
# Quick health check
clawdbot status
systemctl status clawdbot
df -h /
free -h
```

---

## 11. Security Notes

### 11.1 Secrets Management

- API keys stored in `clawdbot.json` (not in git)
- Never commit secrets to workspace repo
- Use environment variables when possible

### 11.2 Access Control

- Telegram restricted to admin chat IDs
- GitHub via SSH key
- Tailscale for secure remote access

### 11.3 What Jarvis Should Never Do

- Exfiltrate private data
- Run destructive commands without asking
- Send external communications without approval
- Share memory contents in group chats

---

## 12. Version History

| Date | Change |
|------|--------|
| 2026-02-04 | Initial architecture document created |

---

## 13. Contact

If this document is being used to recreate Jarvis after a failure:
- Owner: Mike Harper
- Email: mike@cranesync.com
- Telegram: @MikeHarper (8445149012)

---

*This document is the complete blueprint for Jarvis. Keep it updated whenever configuration changes.*
