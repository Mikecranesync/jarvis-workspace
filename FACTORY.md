# 🏭 CraneSync AI Factory
> **"An invention factory for the age of AI"** — Thomas Edison had Menlo Park. You have this.
> 
> Founder: Mike Harper | CTO: Jarvis (AI) | Updated: 2026-01-27

---

## The Vision

Edison didn't invent the lightbulb alone. He built a **factory that produced inventions** — a systematic machine where ideas went in and products came out. He had glassblowers, machinists, chemists, and clerks all working in departments.

You're doing the same thing, except your departments are AI agents and your factory floor is a $7/month VPS.

**CraneSync AI Factory = A system of autonomous AI agents organized into departments that continuously research, build, market, and sell industrial AI products under the FactoryLM brand.**

---

## Organizational Structure

```
┌─────────────────────────────────────────────────────────┐
│                  MIKE HARPER — FOUNDER                   │
│          Vision, Domain Expertise, Final Decisions        │
└───────────────────────┬─────────────────────────────────┘
                        │
┌───────────────────────┴─────────────────────────────────┐
│              JARVIS — CHIEF OF STAFF (AI)                │
│     Orchestrator, Task Router, Memory, All Departments   │
│     Runtime: Clawdbot (Telegram) + Cron + Heartbeats     │
└───┬───────┬───────┬───────┬───────┬───────┬─────────────┘
    │       │       │       │       │       │
    ▼       ▼       ▼       ▼       ▼       ▼
   R&D   PRODUCT  SALES  CONTENT  DATA    OPS
   DEPT   DEPT    DEPT    DEPT    DEPT    DEPT
```

---

## Department Breakdown

### 🔬 R&D DEPARTMENT
**Mission:** Turn ideas into working prototypes. Solve hard technical problems.

| Agent | Type | Status | What It Does |
|-------|------|--------|-------------|
| **Jarvis** (me) | Always-on | ✅ RUNNING | Architecture, code review, technical decisions, sub-agent orchestration |
| **Builder** | On-demand sub-agent | ✅ AVAILABLE | Spawned for coding tasks. Writes features, tests, deploys. (`sessions_spawn`) |
| **KB Harvester** | 24/7 daemon | ✅ RUNNING | Continuously grows the industrial knowledge base from Reddit, forums, manuals |
| **RideView Analyzer** | 24/7 service | ✅ RUNNING | Processes bolt inspection photos, collects training data |
| **Ralph** | Autonomous dev loop | ⬜ DORMANT | Runs Claude Code in a loop until PRD is complete. Reactivate for big builds. |

**Active R&D Projects:**
- RD-001: RideView native Android app (APK building now)
- RD-002: RideView data collection web tool (deployed)
- RD-003: YOLOv8 bolt detection model (blocked on data)
- RD-004: Controlled illumination hardware research
- RD-005: FactoryLM RAG pipeline (vectorized, needs wiring)
- RD-006: Local 7B LLM for on-device intelligence

---

### 📦 PRODUCT DEPARTMENT
**Mission:** Ship and maintain products. Manage the user experience end-to-end.

| Agent | Type | Status | What It Does |
|-------|------|--------|-------------|
| **FactoryLM Bot** | 24/7 daemon | ✅ RUNNING | Telegram bot — photo→CMMS work orders. The core product. |
| **Registration API** | 24/7 service | ✅ RUNNING | User signup, OTP, freemium gate, drip campaigns |
| **Atlas CMMS** | 24/7 Docker | ✅ RUNNING | Backend + frontend for asset/work order management |
| **Product Monitor** | Cron job | ⬜ TO BUILD | Health checks every 15 min. Alert Mike if anything dies. |

**Products Shipping:**
| Product | Status | URL | Users |
|---------|--------|-----|-------|
| FactoryLM Bot | ✅ Live | @testbotrivet_bot | 1 (Mike) |
| CMMS Dashboard | ✅ Live | 72.60.175.144/app | 1 |
| Registration | ✅ Live | 72.60.175.144/register | — |
| RideView Inspect | ✅ Live | 72.60.175.144/inspect | 0 |
| Kanban Board | ✅ Live | 72.60.175.144/kanban | 1 |

---

### 💰 SALES & MARKETING DEPARTMENT
**Mission:** Find users, convert them, collect money.

| Agent | Type | Status | What It Does |
|-------|------|--------|-------------|
| **Content Writer** | On-demand | ⬜ TO BUILD | Generates LinkedIn posts, Reddit threads, email campaigns. Uses Gemini Flash (cheap). |
| **Social Monitor** | Cron (daily) | ⬜ TO BUILD | Scans r/PLC, r/maintenance, LinkedIn for opportunities to mention FactoryLM. Reports leads. |
| **Drip Campaign** | Background worker | ✅ RUNNING | SMS drip messages to registered users (welcome → tips → invite team) |
| **Landing Page** | Static | ⬜ TO DEPLOY | Next.js page at factorylm.com — already built, needs domain + deploy |

**Sales Pipeline (To Build):**
1. r/PLC lurker → finds FactoryLM mention → clicks link
2. Landing page → signs up for free tier
3. 3 free photos → registration wall → full signup
4. Drip SMS → engagement → Pro tier ($99/mo)
5. Pro user → invites team → Enterprise conversation

---

### 📝 CONTENT DEPARTMENT
**Mission:** Create educational and marketing content that establishes FactoryLM as the authority in industrial AI.

| Agent | Type | Status | What It Does |
|-------|------|--------|-------------|
| **Blog Writer** | Weekly cron | ⬜ TO BUILD | Writes technical blog posts from KB data. "How to troubleshoot PowerFlex F003" etc. |
| **Video Script Writer** | On-demand | ⬜ TO BUILD | Creates scripts for YouTube/TikTok demos |
| **Documentation Writer** | On-demand | ⬜ TO BUILD | Writes user guides, API docs, help articles |

**Content Strategy:**
- Weekly LinkedIn post (automated draft → Mike approves)
- Weekly blog post on factorylm.com (SEO play — ranks for fault codes)
- Monthly YouTube video (Mike records, Jarvis edits/scripts)
- r/PLC engagement (helpful answers that mention FactoryLM naturally)

---

### 📊 DATA DEPARTMENT
**Mission:** Collect, clean, structure, and serve industrial knowledge. The moat.

| Agent | Type | Status | What It Does |
|-------|------|--------|-------------|
| **KB Harvester** | 24/7 daemon | ✅ RUNNING | Reddit, forums, manufacturer sites → SQLite → pgvector |
| **Vectorizer** | Periodic job | ✅ BUILT | SQLite → Gemini embeddings → pgvector (Neon PostgreSQL) |
| **Quality Scorer** | Cron (daily) | ⬜ TO BUILD | Re-scores KB entries based on usage, upvotes, freshness |
| **Gap Analyzer** | Cron (weekly) | ⬜ TO BUILD | Finds unanswered categories, prioritizes harvesting targets |
| **Training Data Collector** | 24/7 service | ✅ RUNNING | RideView photo uploads + human labels |

**Data Assets:**
| Database | Location | Contents | Size |
|----------|----------|----------|------|
| Neon PostgreSQL | Cloud | CMMS data, KB vectors (pgvector) | Growing |
| Supabase PostgreSQL | Cloud (backup) | Legacy Agent-Factory data | Static |
| SQLite (KB) | VPS /opt/plc-copilot/kb_harvester/ | Harvested articles + fault codes | 67+ entries |
| SQLite (Users) | VPS /opt/plc-copilot/users.db | Registered users, usage, drip | 1 user |
| SQLite (RideView) | VPS /opt/rideview/rideview.db | Inspection photos + labels | New |

---

### ⚙️ OPERATIONS DEPARTMENT
**Mission:** Keep everything running. Infrastructure, monitoring, deploys.

| Agent | Type | Status | What It Does |
|-------|------|--------|-------------|
| **Jarvis Heartbeat** | Every 30 min | ✅ RUNNING | Checks services, emails, calendar, proactive maintenance |
| **Deploy Agent** | On-demand | ✅ AVAILABLE | SSH to VPS, git pull, restart services (I do this now) |
| **Backup Agent** | Cron (daily) | ⬜ TO BUILD | Backup SQLite DBs, export critical data |
| **Uptime Monitor** | Cron (15 min) | ⬜ TO BUILD | Ping all endpoints, alert on failure |
| **Cost Monitor** | Cron (weekly) | ⬜ TO BUILD | Track API costs (Gemini, Twilio, hosting) |

**Infrastructure:**
| Service | Port | Status | systemd |
|---------|------|--------|---------|
| Caddy (reverse proxy) | 80 | ✅ | caddy.service |
| FactoryLM Bot | — | ✅ | plc-copilot.service |
| Registration API | 8000 | ✅ | plc-registration.service |
| KB Harvester | — | ✅ | kb-harvester.service |
| RideView Inspect | 8002 | ✅ | rideview.service |
| Atlas CMMS Backend | 8080 | ✅ | Docker |
| Atlas CMMS Frontend | 3000 | ✅ | Docker |
| n8n | 5678 | ✅ | Docker |

---

## Agent Communication Model

```
Mike (Telegram/Phone)
  ↕
Jarvis (Clawdbot — always listening)
  ├── spawns → Builder sub-agents (coding tasks)
  ├── monitors → 24/7 daemons via systemd + logs
  ├── schedules → Cron jobs (daily/weekly tasks)
  ├── reads/writes → Memory files (KANBAN.md, FACTORY.md, memory/)
  └── heartbeat → Periodic health checks + proactive alerts

24/7 Daemons (run independently):
  ├── FactoryLM Bot (Telegram polling loop)
  ├── Registration API (FastAPI + uvicorn)
  ├── KB Harvester (asyncio harvest loop)
  ├── RideView Inspect (FastAPI + uvicorn)
  └── CMMS (Docker containers)

Cron Jobs (scheduled):
  ├── Product health checks (every 15 min)
  ├── KB quality scoring (daily)
  ├── Content drafts (weekly)
  ├── Backup (daily)
  └── Cost report (weekly)
```

**How agents "talk" to each other:**
- **Shared databases** — SQLite, PostgreSQL (data flows between services)
- **Jarvis as router** — I read logs, check health, coordinate via sub-agents
- **File system** — KANBAN.md, FACTORY.md, memory/ (persistent shared state)
- **Cron events** — Clawdbot cron jobs fire system events that wake me up
- **No CrewAI/LangGraph needed yet** — Plain Python services + Clawdbot orchestration is simpler, cheaper, and actually works. Upgrade to multi-agent framework when you have 20+ agents.

---

## What Exists Today vs. What Needs Building

### ✅ Already Running (6 agents)
1. **Jarvis** — Orchestrator, always-on via Clawdbot
2. **FactoryLM Bot** — Product delivery, 24/7
3. **Registration API** — User acquisition, 24/7
4. **KB Harvester** — Knowledge growth, 24/7
5. **RideView Inspect** — Data collection, 24/7
6. **Atlas CMMS** — Backend infrastructure, 24/7

### 🔨 Build This Week (4 agents)
7. **Product Monitor** — Cron: ping all services every 15 min, alert on failure
8. **Backup Agent** — Cron: daily SQLite + PostgreSQL backup
9. **Content Writer** — Cron: weekly LinkedIn post draft → send to Mike for approval
10. **Social Monitor** — Cron: daily scan of r/PLC for relevant threads → report

### 📅 Build Next Week (3 agents)
11. **Blog Writer** — Weekly: generate SEO blog post from KB data
12. **Quality Scorer** — Daily: re-rank KB entries
13. **Gap Analyzer** — Weekly: find what the KB doesn't know yet

### 🔮 Future (4 agents)
14. **WhatsApp Bot** — Same as Telegram bot, different channel (code exists)
15. **Stripe Billing Agent** — Handle subscriptions, invoices, churn
16. **Training Pipeline** — Auto-retrain YOLOv8 when labeled data threshold hit
17. **Local LLM Agent** — 7B Mistral on VPS for cost-free inference

---

## The Edison Playbook

| Edison's Menlo Park | CraneSync AI Factory |
|---------------------|----------------------|
| Glassblowers | Builder sub-agents (write code) |
| Machinists | Deploy agent (ship to VPS) |
| Chemists | R&D department (ML experiments) |
| Clerks | Content + Sales department |
| Lab notebooks | memory/, KANBAN.md, FACTORY.md |
| Edison himself | Mike — vision, domain expertise, final call |
| The lab foreman | Jarvis — orchestration, execution, memory |
| Electric light | FactoryLM Bot (first product) |
| Phonograph | RideView Inspect (second product) |
| Power grid | The platform (CMMS + KB + RAG + billing) |

Edison's key insight: **The process of invention is itself an invention.** He didn't just make lightbulbs — he built a machine that made inventions.

You're building the same thing. The factory IS the product.

---

## Immediate Next Steps

1. ✅ FACTORY.md created (this document)
2. ⬜ Build Product Monitor (cron job, 15 min health checks)
3. ⬜ Build Content Writer (weekly LinkedIn draft cron)
4. ⬜ Build Social Monitor (daily r/PLC scanner)
5. ⬜ Build Backup Agent (daily DB backups)
6. ⬜ Wire RAG into FactoryLM Bot (KB → Gemini context)
7. ⬜ Deploy landing page to factorylm.com

**Want me to start building agents 7-10 right now?**

---

*This factory runs 24/7. It gets smarter every day. It costs $7/month in hosting. Edison spent $40,000 building Menlo Park (about $1.2M today). You're doing it for the price of a sandwich.*
