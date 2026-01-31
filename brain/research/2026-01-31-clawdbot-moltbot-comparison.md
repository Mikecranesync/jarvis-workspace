# Clawdbot / Moltbot / OpenClaw Comparison & Updates
**Date:** 2026-01-31
**Purpose:** Research agentic features and controlled autonomy

---

## The Rebranding

Clawdbot has been rebranded to **OpenClaw** (open source) and **Moltbot** (commercial/viral branding).
- npm package: `openclaw`
- GitHub: `github.com/openclaw/openclaw`
- Still compatible with `clawdbot` commands (shim provided)

---

## Latest Release: 2026.1.29

### Key New Features for Agentic Interaction:

#### 1. **Multi-Agent Routing** 
Route different channels/accounts to isolated agents with separate workspaces and sessions.
```
- Per-account DM session scope
- Multi-account isolation
- Separate agents for work vs personal contexts
```

#### 2. **Memory Search Enhancements**
```
- Extra paths for memory indexing
- Better semantic search across MEMORY.md + memory/*.md
- Agents can recall context from prior conversations
```

#### 3. **Controlled Autonomy Features**
```
- Per-sender group tool policies
- Tool precedence controls
- Cron tool with full schema docs
- Compaction safeguard pruning (summarizes dropped messages)
```

#### 4. **Sub-Agent Announcements**
Sub-agent announce replies now visible in WebChat - better tracking of what autonomous agents are doing.

#### 5. **Enhanced Telegram Integration**
```
- Silent send flag (disable notifications)
- Edit sent messages
- Quote replies for inbound context
- Sticker receive/send with vision
- Caption for media sends
```

#### 6. **Browser Control via Gateway/Node**
Route browser control through gateway - enables remote browser automation.

---

## Agentic Patterns We Should Adopt

### 1. **Heartbeat-Driven Autonomy** (Already Using ✅)
- Agent checks in periodically
- Processes HEARTBEAT.md for tasks
- Proactively reaches out when needed

### 2. **Sub-Agent Spawning** (Partial ✅)
- `sessions_spawn` for background tasks
- Could improve: better announce routing

### 3. **Memory System** (Already Using ✅)
- MEMORY.md for long-term
- memory/*.md for daily logs
- `memory_search` for recall

### 4. **Tool Policies** (Could Improve)
- Define allowed tools per context
- Safety controls on dangerous operations

### 5. **Cron-Based Autonomy** (Already Using ✅)
- Scheduled tasks via cron tool
- Could improve: more autonomous scheduling

---

## GitHub Repos to Fork/Reference

### 1. **OpenClaw Core** (Already Using)
- `github.com/openclaw/openclaw`
- Latest version: 2026.1.29

### 2. **Community Skills**
- Skills system for extending capabilities
- Check `clawdhub.com` for community skills

### 3. **A2UI (Agent-to-UI)**
- Bundled assets for canvas presentations
- Enables visual agent interactions

### 4. **Control UI**
- Web interface for managing agents
- Enhanced refresh in latest release

---

## Recommendations for Our Setup

### Immediate Improvements:

1. **Update Clawdbot to 2026.1.29**
   ```bash
   npm update -g clawdbot
   # or
   npm install -g openclaw
   ```

2. **Enable Multi-Agent Routing**
   - Separate agents for ShopTalk vs personal
   - Industrial context isolated from other tasks

3. **Enhance Tool Policies**
   - Define safe operations for autonomous mode
   - Gate dangerous tools by approval

4. **Improve Memory Search**
   - Add knowledge/ folder to search paths
   - Better recall of technical context

### Controlled Autonomy Architecture:

```
┌─────────────────────────────────────────┐
│           AUTONOMOUS MODE               │
├─────────────────────────────────────────┤
│                                         │
│  ┌──────────┐    ┌──────────┐          │
│  │ HEARTBEAT│───▶│ TASK     │          │
│  │ (2 min)  │    │ QUEUE    │          │
│  └──────────┘    └────┬─────┘          │
│                       │                 │
│                       ▼                 │
│  ┌──────────────────────────────┐      │
│  │     SAFETY GATES             │      │
│  │  - Tool policies             │      │
│  │  - Approval requirements     │      │
│  │  - Commandments enforcement  │      │
│  └─────────────┬────────────────┘      │
│                │                        │
│                ▼                        │
│  ┌────────┐  ┌────────┐  ┌────────┐   │
│  │ BUILD  │  │RESEARCH│  │ REPORT │   │
│  │ CODE   │  │ & LEARN│  │ STATUS │   │
│  └────────┘  └────────┘  └────────┘   │
│                                         │
│  All outputs → Mike for approval        │
│  (Engineering Commandments)             │
│                                         │
└─────────────────────────────────────────┘
```

---

## What Moltbot Does Differently

The viral Moltbot hype emphasizes:
1. **Proactive messaging** - Agent reaches out first
2. **Real-world automation** - Email, calendar, bookings
3. **24/7 availability** - Always-on assistant
4. **Multi-channel** - Telegram, WhatsApp, Discord, etc.

**We already have all of this.** The difference is marketing, not features.

---

## Action Items

- [ ] Update to openclaw 2026.1.29
- [ ] Add knowledge/ to memory_search paths
- [ ] Implement tool policies for ShopTalk context
- [ ] Test multi-agent routing for industrial vs personal
- [ ] Document controlled autonomy patterns in AGENTS.md
