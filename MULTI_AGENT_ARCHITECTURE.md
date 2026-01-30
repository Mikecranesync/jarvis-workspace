# Multi-Agent Architecture

*How Jarvis instances coordinate as a team of digital employees.*
*Updated: 2026-01-30 — Integrated Agent Cards + Handoff Protocol*

---

## Overview

We run multiple specialized AI agents, each optimized for specific tasks. They share a common workspace and coordinate through the NEXT_STEPS.md handoff protocol and signals directory.

```
┌─────────────────────────────────────────────────────────────────┐
│                    SHARED WORKSPACE                              │
│                 /root/jarvis-workspace                           │
│                                                                  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐           │
│  │ NEXT_STEPS   │  │   signals/   │  │   memory/    │           │
│  │    .md       │  │   inbox/     │  │  YYYY-MM-DD  │           │
│  │  (handoffs)  │  │   outbox/    │  │   (logs)     │           │
│  └──────────────┘  └──────────────┘  └──────────────┘           │
└─────────────────────────────────────────────────────────────────┘
        ▲              ▲              ▲              ▲
        │              │              │              │
   ┌────┴────┐    ┌────┴────┐    ┌────┴────┐    ┌────┴────┐
   │  ORCH-  │    │  CODE   │    │ MONITOR │    │ RESEARCH│
   │ ESTRATOR│    │  AGENT  │    │  AGENT  │    │  AGENT  │
   │         │    │         │    │         │    │         │
   │Main Jrvs│    │ GitHub  │    │ Health  │    │ Intel   │
   │ (Opus)  │    │(Sonnet) │    │ (Haiku) │    │(Sonnet) │
   └─────────┘    └─────────┘    └─────────┘    └─────────┘
```

---

## Agent Cards

Each agent has a capability declaration in `agents/cards/`:

| Agent | Card File | Trigger | Skills |
|-------|-----------|---------|--------|
| Orchestrator | `orchestrator.json` | Direct message, heartbeat | 7 |
| Monitor | `monitor.json` | 15-min cron | 5 |
| Code Agent | `code-agent.json` | 30-min cron, signals | 5 |
| Agile Agent | `agile-agent.json` | 5-min cron | 5 |
| Research Agent | `research-agent.json` | 4-hour cron, on-demand | 6 |

See `agents/cards/README.md` for full documentation.

---

## Active Agents

### Orchestrator (Jarvis Prime) — ACTIVE

| Property | Value |
|----------|-------|
| **Model** | Claude Opus 4 |
| **Channel** | Telegram |
| **Role** | Strategic orchestrator, Mike's primary interface |
| **Heartbeat** | 5-minute eternal monitor |
| **Card** | `agents/cards/orchestrator.json` |

**Capabilities:**
- Direct communication with Mike
- Task delegation to other agents
- Complex reasoning and planning
- File operations and code generation
- Web research and browser control
- Knowledge base queries (Neon RAG)

### Monitor Agent — ACTIVE (via cron)

| Property | Value |
|----------|-------|
| **Model** | Claude (via Orchestrator) |
| **Trigger** | 15-minute cron |
| **Role** | System health monitoring |
| **Card** | `agents/cards/monitor.json` |

**Checks:**
- `systemctl status plc-copilot`
- `docker ps | grep cmms`
- Error log tails
- Memory/disk usage

### Code Agent — ACTIVE (via cron)

| Property | Value |
|----------|-------|
| **Model** | Claude (via Orchestrator) |
| **Trigger** | 30-minute cron |
| **Role** | GitHub issue/PR management |
| **Card** | `agents/cards/code-agent.json` |

**Workflow:**
1. Check `signals/inbox/` for tasks
2. Check `gh issue list --label 'code-agent'`
3. Check `gh pr list --state open`
4. Process and report to `signals/outbox/`

### Agile Agent — ACTIVE (via cron)

| Property | Value |
|----------|-------|
| **Model** | Claude (via Orchestrator) |
| **Trigger** | 5-minute cron |
| **Role** | Trello backlog management |
| **Card** | `agents/cards/agile-agent.json` |

**Workflow:**
1. Check Trello for @jarvis tasks
2. Move cards through workflow
3. Update NEXT_STEPS.md

### Research Agent — ON-DEMAND

| Property | Value |
|----------|-------|
| **Model** | Claude (via Orchestrator) |
| **Trigger** | On-demand or 4-hour cron |
| **Role** | Web research and intelligence |
| **Card** | `agents/cards/research-agent.json` |

**Workflow:**
1. Receive research topic
2. Web search (30+ min per Amendment I)
3. Fetch and analyze sources
4. Document in `brain/research/`
5. Ingest to Neon via `neon_ingest.py`

---

## Coordination Protocol

### 1. NEXT_STEPS.md Handoff

The primary coordination mechanism. See `HANDOFF_PROTOCOL.md`.

```markdown
## 🔴 In Progress
| Task | Started | ETA | Notes |

## 🟡 Queued
- [ ] Task with autonomy level

## 🟢 Completed Today
- [x] Task — outcome *(timestamp)*

## ⚫ Blocked
| Task | Blocker | Waiting On |
```

**Rules:**
1. Update on transition (before ending work)
2. Read on start (before beginning work)
3. Claim before working (prevent collisions)
4. Complete explicitly (with outcome)
5. Block explicitly (with what's needed)

### 2. Signals Directory

For async agent communication:

```
signals/
├── inbox/          # Tasks for agents to pick up
│   └── code-agent-001.json
├── outbox/         # Completed task reports
│   └── code-agent-001-done.json
└── alerts/         # Urgent notifications
    └── 2026-01-30-disk-critical.md
```

### 3. Memory Synchronization

Daily logs in `memory/YYYY-MM-DD.md`:

```markdown
# Memory Log — January 30, 2026

## Session Summary
[What happened today]

### Completed
1. Task — details

### System Status
- Stats and metrics

### Open Questions
- Items needing resolution
```

### 4. Knowledge Base Integration

All research and learnings → Neon vector database:

```bash
python3 -m tools.neon_ingest --source research
python3 -m tools.neon_ingest --file path/to/doc.md
```

---

## Escalation Path

```
Level 1: Agent handles autonomously
    ↓ (if blocked)
Level 2: Escalate to Orchestrator
    ↓ (if needs human input)
Level 3: Alert Mike via Telegram
    ↓ (if critical)
Level 4: Emergency procedures
```

---

## Resource Allocation

### Current VPS (4GB RAM)

| Service | RAM | Status |
|---------|-----|--------|
| CMMS Backend | ~400MB | ✅ Running |
| CMMS Frontend | ~100MB | ✅ Running |
| PLC Copilot | ~100MB | ✅ Running |
| Ollama (idle) | ~500MB | ✅ Available |
| Clawdbot | ~200MB | ✅ Running |
| System | ~1.5GB | Buffer |

**Note:** All agents currently run through single Clawdbot instance via cron jobs, not separate processes. This is efficient but limits parallelism.

### Future: Dedicated Agent Instances

When we scale to Hetzner (16GB+):
- Separate Clawdbot instances per agent
- True parallel processing
- Dedicated models per agent (Opus for orchestrator, Haiku for monitor)

---

## Cron Configuration

Current cron jobs in Clawdbot config:

| Job | Schedule | Agent | Purpose |
|-----|----------|-------|---------|
| Trello Check | */5 * * * * | Agile | @jarvis tasks |
| Laptop Check | */5 * * * * | Monitor | Tailscale status |
| Monitor | */15 * * * * | Monitor | System health |
| Code Agent | */30 * * * * | Code | GitHub tasks |

---

## Future: A2A Protocol

When implementing full A2A:

1. **Agent Cards become discoverable** at well-known URLs
2. **Task lifecycle** replaces signals files
3. **External agents** can collaborate
4. **Standardized messages** replace ad-hoc formats

See `brain/research/2026-01-30-a2a-protocol-research.md`.

---

## Constitutional Compliance

All agents operate under:
- **Constitution** — Core principles
- **Amendment I** — Open source first
- **Amendment II** — No drift (24/7 factory)
- **Amendment III** — Proof of work
- **Amendment IV** — Proactive next steps
- **Engineering Commandments** — Code standards

---

## Deployment Checklist

- [x] Create agent cards
- [x] Set up NEXT_STEPS.md handoff protocol
- [x] Configure cron jobs
- [x] Create signals directory structure
- [x] Document in this file
- [ ] Set up cost tracking
- [ ] Deploy to Hetzner for more resources
- [ ] Enable parallel agent instances

---

*Architecture maintained by Jarvis Orchestrator*
*Last updated: 2026-01-30 05:15 UTC*
