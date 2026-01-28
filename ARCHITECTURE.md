# CraneSync AI Architecture
*Jarvis Orchestrator + Tiered Sub-Agents*

---

## 🎯 Approved Decisions

| # | Decision | Your Choice |
|---|----------|-------------|
| 1 | Primary platform | ✅ Telegram + WhatsApp (Twilio) |
| 2 | First market | ✅ Venezuela + Mexico (Spanish) |
| 3 | Languages | ✅ Spanish first, English always available (user picks) |
| 4 | Infrastructure | ✅ Single Clawdbot orchestrator on Hostinger VPS |
| 5 | Time | ✅ As much as you can give |
| 6 | Pricing | ✅ $9/mo LatAm, $29/mo USA |
| 7 | WhatsApp provider | ✅ Twilio |

---

## 🏗️ Proposed Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    HOSTINGER VPS (Your Server)                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │              JARVIS (Main Orchestrator)                  │   │
│  │              Clawdbot + Claude Opus                      │   │
│  │                                                          │   │
│  │  • Strategic decisions                                   │   │
│  │  • Complex problem solving                               │   │
│  │  • Subagent coordination                                 │   │
│  │  • Your direct conversations                             │   │
│  └─────────────────────────────────────────────────────────┘   │
│                              │                                  │
│              ┌───────────────┼───────────────┐                  │
│              │               │               │                  │
│              ▼               ▼               ▼                  │
│  ┌───────────────┐  ┌───────────────┐  ┌───────────────┐       │
│  │   RALPH       │  │  MINI-JARVIS  │  │  RIVET-PRO    │       │
│  │  (Claude Code)│  │ (Sonnet/Haiku)│  │  (PLC Bot)    │       │
│  │               │  │               │  │               │       │
│  │ • Coding tasks│  │ • Routine Q&A │  │ • Photo OCR   │       │
│  │ • Build PRs   │  │ • Simple tasks│  │ • Troubleshoot│       │
│  │ • Deploy code │  │ • Translations│  │ • KB lookup   │       │
│  └───────────────┘  └───────────────┘  └───────────────┘       │
│                                                                 │
├─────────────────────────────────────────────────────────────────┤
│                        MESSAGING LAYER                          │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐                │
│  │  Telegram  │  │  WhatsApp  │  │   Email    │                │
│  │    Bot     │  │  (Twilio)  │  │ (SendGrid) │                │
│  └────────────┘  └────────────┘  └────────────┘                │
├─────────────────────────────────────────────────────────────────┤
│                        DATA LAYER                               │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐                │
│  │ PostgreSQL │  │   Redis    │  │   Files    │                │
│  │ (Users/KB) │  │  (Cache)   │  │ (Logs/Mem) │                │
│  └────────────┘  └────────────┘  └────────────┘                │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    TWILIO KANBAN DASHBOARD                      │
│                                                                 │
│  • Agent health status (green/yellow/red)                       │
│  • Active tasks by agent                                        │
│  • API endpoint status                                          │
│  • Cost tracking (tokens used)                                  │
│  • Message queue depth                                          │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🤖 The Agent Hierarchy

### Tier 1: JARVIS (You're talking to me now)
- **Model:** Claude Opus (expensive but smart)
- **Role:** Orchestrator, strategist, complex decisions
- **When to use:** Important decisions, multi-step planning, talking to Mike
- **Cost:** ~$15/1M input, $75/1M output tokens

### Tier 2: MINI-JARVIS (New - to build)
- **Model:** Claude Sonnet or Haiku (cheap and fast)
- **Role:** Routine tasks, simple Q&A, translations
- **When to use:** Repetitive tasks, customer support overflow
- **Cost:** ~$3/1M input, $15/1M output (Sonnet) or $0.25/$1.25 (Haiku)

### Tier 3: RALPH (Your My-Ralph repo)
- **Model:** Claude Code CLI
- **Role:** Autonomous coding, building features, PRs
- **When to use:** "Build X feature" → runs for hours, comes back with code
- **Cost:** Uses your Claude API credits (careful!)

### Tier 4: RIVET-PRO (Customer-facing bot)
- **Model:** Groq (cheap) → Claude (complex fallback)
- **Role:** PLC troubleshooting, photo analysis, KB lookup
- **When to use:** All customer interactions
- **Cost:** ~$0.05 per conversation (Groq-heavy)

---

## 💡 Can We Run Multiple Clawdbot Instances?

**Short answer:** Yes, but with caveats.

**Option A: Single Clawdbot with Subagents (Recommended)**
- One Clawdbot instance (Jarvis)
- Use `sessions_spawn` to create isolated subagent sessions
- Each subagent can have different model (Opus vs Sonnet vs Haiku)
- ✅ Built-in feature, no extra setup
- ✅ Shared memory and context
- ✅ Lower resource usage

**Option B: Multiple Clawdbot Instances**
- Separate Clawdbot processes on different ports
- Each with its own config, model, workspace
- Communicate via API calls
- ⚠️ More complex setup
- ⚠️ Higher resource usage (each needs ~500MB-1GB RAM)
- ⚠️ No shared context unless you build it

**Option C: Hybrid (Clawdbot + Ralph)**
- Clawdbot for orchestration and messaging
- Ralph process for autonomous coding
- Jarvis calls Ralph via API when coding tasks come in
- ✅ Best of both worlds
- ✅ Ralph is purpose-built for long coding sessions

**🟢 MY RECOMMENDATION:** Option C (Hybrid)

```
Jarvis (Clawdbot)
├── handles: messaging, decisions, subagents
├── spawns: Mini-Jarvis (Sonnet) for routine tasks
└── calls: Ralph API for coding tasks

Ralph (My-Ralph)
├── handles: long-running code tasks
├── uses: Claude Code CLI
└── reports back: to Jarvis when done
```

---

## 📊 Twilio Kanban Dashboard

For monitoring agent health, we have options:

### Option 1: Twilio + Custom Dashboard
- Twilio handles messaging (WhatsApp/SMS)
- Build custom dashboard (Next.js or use existing factorylm-landing)
- WebSocket for real-time status
- **Effort:** Medium (1-2 weekends)

### Option 2: BetterUptime / UptimeRobot + Grafana
- BetterUptime monitors API endpoints ($20/mo or free tier)
- Grafana for dashboards (self-hosted, free)
- **Effort:** Low (few hours)

### Option 3: n8n + Notion/Airtable
- n8n workflows check agent health
- Push to Notion/Airtable as dashboard
- **Effort:** Low (you already forked n8n-docs)

### Option 4: Custom Slack/Discord Bot
- Agents post status to channel
- You check channel for updates
- **Effort:** Very low

**🟢 MY RECOMMENDATION:** Start with Option 4 (Slack/Discord channel for status), upgrade to Option 2 later.

---

## 📋 What I Need From You

### 1. Hostinger VPS Specs
Find your VPS details (look in Hostinger dashboard):
- RAM: ___GB
- CPU: ___ cores
- Storage: ___GB
- IP address: ___
- SSH access details

### 2. Clone My-Ralph Locally
```bash
cd C:\Users\hharp\clawd\projects
git clone https://github.com/Mikecranesync/My-Ralph.git
```

Then I can analyze it and integrate.

### 3. Your Wife's Help
For Spanish translation/validation:
- Can she join a Telegram group with me?
- Or review Spanish content I generate?

---

## 🚀 Implementation Order

### Phase 1: Foundation (This Weekend)
1. Get VPS specs
2. Deploy Clawdbot to VPS
3. Test Telegram works from VPS

### Phase 2: WhatsApp (Next Weekend)
1. Set up Twilio account
2. Apply for WhatsApp Business API
3. Integrate with Clawdbot

### Phase 3: Ralph Integration (Week 3)
1. Clone My-Ralph
2. Set up Ralph API endpoint
3. Jarvis can call Ralph for coding tasks

### Phase 4: Dashboard (Week 4)
1. Simple status channel (Discord/Slack)
2. Agent health pings
3. Cost tracking

---

## 💰 Estimated Monthly Costs (Updated)

| Component | Cost | Notes |
|-----------|------|-------|
| Hostinger VPS | ~$10-20 | (you already have this) |
| Claude API (Opus for Jarvis) | $50-100 | Strategic tasks |
| Claude API (Sonnet for Mini-Jarvis) | $20-30 | Routine tasks |
| Claude Code CLI (Ralph) | $20-50 | Coding tasks (careful!) |
| Groq API (Rivet-PRO) | $5-10 | Customer bot |
| Twilio (WhatsApp) | $20-50 | Based on volume |
| SendGrid | $0 | Free tier |
| Uptime monitoring | $0-20 | Free tier or BetterUptime |
| **Total** | **$125-280/mo** | |

**Break-even:** 5-10 customers at $29/mo (USA) or 14-31 at $9/mo (LatAm)

---

*Architecture v1.0 - January 26, 2026*
