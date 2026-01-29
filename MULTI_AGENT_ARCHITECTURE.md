# Multi-Agent Architecture

*How Jarvis instances coordinate as a team of digital employees.*

---

## Overview

We run multiple specialized AI agents, each optimized for specific tasks. They share a common workspace and coordinate through files and Trello.

```
┌─────────────────────────────────────────────────────────┐
│                  SHARED WORKSPACE                        │
│              /root/jarvis-workspace                      │
│   (Memory files, projects, Trello board, GitHub)         │
└─────────────────────────────────────────────────────────┘
        ▲              ▲              ▲
        │              │              │
   ┌────┴────┐    ┌────┴────┐    ┌────┴────┐
   │ JARVIS  │    │  CODE   │    │ MONITOR │
   │  PRIME  │    │  AGENT  │    │  AGENT  │
   │ (Opus)  │    │(Sonnet) │    │ (Haiku) │
   │         │    │         │    │         │
   │ Strategy│    │ PRs,    │    │ Logs,   │
   │ Mike IF │    │ Debug   │    │ Alerts  │
   └─────────┘    └─────────┘    └─────────┘
```

---

## Active Agents

### Jarvis Prime (This Instance)

| Property | Value |
|----------|-------|
| **Model** | Claude Opus 4 |
| **Channel** | Telegram |
| **Role** | Strategic orchestrator, Mike's primary interface |
| **Config** | `/root/.clawdbot/clawdbot.json` |
| **Workspace** | `/root/jarvis-workspace` |
| **Cost** | ~$50-100/month |

**Responsibilities:**
- Direct communication with Mike
- Strategic decisions and planning
- Orchestrating other agents
- Complex reasoning tasks
- Approving recommendations from other agents

### Code Agent (Planned)

| Property | Value |
|----------|-------|
| **Model** | Claude Sonnet 4 |
| **Channel** | Cron/Background |
| **Role** | Code review, PR creation, debugging |
| **Config** | `/root/.clawdbot/code-agent.json` |
| **Workspace** | `/root/jarvis-workspace` (shared) |
| **Cost** | ~$20-30/month |

**Responsibilities:**
- Check GitHub for assigned issues
- Create feature branches and PRs
- Run tests and report results
- Code review on open PRs
- Update Trello when work completes

### Monitor Agent (Planned)

| Property | Value |
|----------|-------|
| **Model** | Claude Haiku 3.5 or Groq |
| **Channel** | Cron (every 15 min) |
| **Role** | System health, log monitoring, alerts |
| **Config** | `/root/.clawdbot/monitor-agent.json` |
| **Workspace** | `/root/jarvis-workspace` (shared) |
| **Cost** | ~$5-10/month |

**Responsibilities:**
- Check service health (CMMS, bots, APIs)
- Scan logs for errors
- Alert Mike via Telegram on critical issues
- Track resource usage
- Update status dashboard

---

## Coordination Protocol

### 1. Shared Workspace

All agents read/write to `/root/jarvis-workspace`:

```
jarvis-workspace/
├── AGENTS.md           # Who we are
├── CONSTITUTION.md     # Our principles
├── ENGINEERING_COMMANDMENTS.md
├── memory/
│   └── YYYY-MM-DD.md   # Daily logs (all agents write)
├── signals/
│   ├── inbox/          # Tasks for agents to pick up
│   ├── outbox/         # Completed task reports
│   └── alerts/         # Urgent notifications
└── projects/
    └── [project files]
```

### 2. Task Handoff via Signals

When Jarvis Prime wants Code Agent to do something:

```bash
# Jarvis Prime writes:
echo '{"task": "review_pr", "pr": 16, "repo": "Rivet-PRO"}' > signals/inbox/code-agent-001.json

# Code Agent picks up, processes, then writes:
echo '{"task": "review_pr", "status": "complete", "notes": "LGTM"}' > signals/outbox/code-agent-001.json
```

### 3. Memory Synchronization

All agents append to the same daily memory file:
```markdown
## 2026-01-29

### Jarvis Prime (06:30)
- Discussed multi-agent architecture with Mike
- Created issue #1 for implementation

### Code Agent (07:00)
- Picked up PR #16 review
- Added comments, approved

### Monitor Agent (07:15)
- All services healthy
- No errors in last hour
```

### 4. Escalation Path

```
Monitor detects issue → Creates alert signal
                      → Code Agent attempts fix
                      → If unresolved, escalate to Jarvis Prime
                      → Jarvis Prime notifies Mike if critical
```

---

## Resource Allocation

### Current VPS (4GB RAM)

| Service | RAM | Priority |
|---------|-----|----------|
| CMMS (Java) | 400MB | High |
| Jarvis Prime | 430MB | High |
| PLC Copilot | 100MB | High |
| Registration API | 60MB | Medium |
| Twilio Webhook | 65MB | Medium |
| **Reserved for new agents** | **500MB** | - |
| System/Buffer | 1.5GB | - |

### Agent Memory Footprint

| Agent Type | Expected RAM |
|------------|--------------|
| Clawdbot (Node.js) | ~150-200MB each |
| Lightweight Python bot | ~50-100MB each |

**Conclusion:** Can add 2-3 agents on current VPS.

---

## Configuration Templates

### Code Agent Config

```json
{
  "agent": {
    "name": "Code Agent",
    "model": "anthropic/claude-sonnet-4",
    "workspace": "/root/jarvis-workspace"
  },
  "channels": [],
  "cron": {
    "enabled": true,
    "schedule": "*/30 * * * *",
    "prompt": "Check signals/inbox for tasks. Check GitHub issues assigned to @code-agent. Process and report."
  }
}
```

### Monitor Agent Config

```json
{
  "agent": {
    "name": "Monitor Agent",
    "model": "anthropic/claude-haiku-3.5",
    "workspace": "/root/jarvis-workspace"
  },
  "channels": [],
  "cron": {
    "enabled": true,
    "schedule": "*/15 * * * *",
    "prompt": "Check service health: CMMS, PLC Copilot, APIs. Scan logs for errors. Report issues to signals/alerts."
  }
}
```

---

## Deployment Checklist

- [ ] Create config files for each agent
- [ ] Set up systemd services
- [ ] Create signals directory structure
- [ ] Test agent communication
- [ ] Set up cost monitoring
- [ ] Document runbooks
- [ ] Get Mike's approval
- [ ] Deploy incrementally (one agent at a time)

---

## Cost Tracking

Track monthly costs in `memory/costs/YYYY-MM.md`:

```markdown
# January 2026 AI Costs

| Agent | Tokens In | Tokens Out | Cost |
|-------|-----------|------------|------|
| Jarvis Prime | 2.1M | 180K | $45.00 |
| Code Agent | 500K | 50K | $8.50 |
| Monitor Agent | 200K | 20K | $1.20 |
| **Total** | | | **$54.70** |
```

---

*Architecture designed by Jarvis Prime — Ready for review*
