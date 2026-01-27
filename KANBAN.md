# FactoryLM — Strategic Kanban Board
> **Franklin Covey "7 Habits" Style** — Begin With The End In Mind
> *Updated: 2026-01-27*

---

## 🎯 THE END IN MIND (Habit 2)
**FactoryLM is the NotebookLM of industrial maintenance.**
- Techs snap photos → instant AI diagnosis + CMMS work orders
- Knowledge base that knows more than any single engineer
- Self-improving: every interaction makes it smarter
- Revenue: freemium → paid tiers → enterprise

---

## 🔥 QUADRANT 1: URGENT + IMPORTANT (Do First)
*Things that are on fire or blocking revenue*

| # | Task | Status | Owner | Blockers |
|---|------|--------|-------|----------|
| 1.1 | ✅ Bot deployed & working (photo→CMMS) | DONE | Jarvis | — |
| 1.2 | ✅ Registration + OTP system | DONE | Jarvis | — |
| 1.3 | ✅ Freemium gate (3 free → register) | DONE | Jarvis | — |
| 1.4 | ✅ Rebrand to FactoryLM | DONE | Jarvis | — |
| 1.5 | 🔄 KB Harvester deployment | IN PROGRESS | Jarvis | sub-agent deploying |
| 1.6 | ⬜ Fix Twilio phone number for SMS | TODO | Mike | Need Twilio number ($1/mo) to send drip SMS |
| 1.7 | ⬜ Point factorylm.com → VPS | TODO | Mike | Domain access needed |
| 1.8 | ⬜ Wire RAG into bot (KB → Gemini context) | TODO | Jarvis | Needs 1.5 done first |

---

## ⭐ QUADRANT 2: NOT URGENT + IMPORTANT (Schedule — This Is Where You Win)
*Strategic work that compounds. Covey says spend most time here.*

### 🧠 Knowledge Base (The Moat)
| # | Task | Status | Notes |
|---|------|--------|-------|
| 2.1 | ⬜ Vectorize seed data → pgvector | TODO | 500+ entries ready, needs pgvector on Neon |
| 2.2 | ⬜ Reddit harvester running 24/7 | TODO | Follows 1.5 |
| 2.3 | ⬜ Manufacturer fault code expansion | TODO | Need 500+ codes per major brand |
| 2.4 | ⬜ PDF manual download + parse pipeline | TODO | ManualsLib, OEM sites |
| 2.5 | ⬜ Knowledge gap tracking | TODO | Log unanswered questions → harvest targets |
| 2.6 | ⬜ PLCTalk / MrPLC forum harvesting | TODO | Rich troubleshooting data |
| 2.7 | ⬜ 7B Mistral local LLM on VPS | FUTURE | Next intelligence boost |
| 2.8 | ⬜ Train/fine-tune on industrial data | FUTURE | After enough KB data collected |

### 💰 Revenue Path
| # | Task | Status | Notes |
|---|------|--------|-------|
| 2.9 | ⬜ Stripe integration (paid tiers) | TODO | Free/Pro/Enterprise |
| 2.10 | ⬜ Landing page at factorylm.com | TODO | Next.js page exists in `plc-copilot-landing/` |
| 2.11 | ⬜ WhatsApp channel (Twilio) | TODO | Code exists in rivet-pro (56 tests passing) |
| 2.12 | ⬜ Soft launch on r/PLC | TODO | After KB has 1000+ entries |
| 2.13 | ⬜ Spanish localization live | TODO | Code exists (25 tests), needs deployment |
| 2.14 | ⬜ Team/org management | TODO | Multi-user, shared assets |

### 🏗️ Platform Maturity
| # | Task | Status | Notes |
|---|------|--------|-------|
| 2.15 | ⬜ Database failover (Neon + Supabase) | TODO | Schema exists, MultiDatabaseManager partially built |
| 2.16 | ⬜ CI/CD pipeline active | TODO | GitHub Actions workflows exist, need activation |
| 2.17 | ⬜ Monitoring + alerting | TODO | Health endpoints exist |
| 2.18 | ⬜ HTTPS via Let's Encrypt | TODO | After domain pointed |
| 2.19 | ⬜ Rate limiting + abuse protection | TODO | Basic rate limit exists |

---

## 📋 QUADRANT 3: URGENT + NOT IMPORTANT (Delegate/Minimize)
*Busywork that feels urgent but doesn't move the needle*

| # | Task | Status | Notes |
|---|------|--------|-------|
| 3.1 | MUI DataGrid license watermark | DONE (workaround) | JS injection hides it |
| 3.2 | git credential-manager warnings | LOW | Cosmetic, doesn't affect function |
| 3.3 | Old n8n workflows (15 active, 24 inactive) | DEFER | Working but may not be needed anymore |

---

## 🚫 QUADRANT 4: NOT URGENT + NOT IMPORTANT (Eliminate)
*Stuff to kill or permanently shelf*

| # | Project | Decision | Reason |
|---|---------|----------|--------|
| 4.1 | pi-gateway | SHELF | 2% complete, IoT gateway — no near-term revenue |
| 4.2 | IndustrialSkillsHub | SHELF | 15% complete, training app — defer until after launch |
| 4.3 | CodeBang | KILL | No clear path to revenue |
| 4.4 | jarvis-android-voice-proto | KILL | Prototype, superseded by Clawdbot |
| 4.5 | jarvis-for-gmail | SHELF | Email AI — low priority vs FactoryLM |
| 4.6 | SCAFFOLD SaaS (Agent-Factory) | SHELF | Ambitious ($1M plan) but FactoryLM ships faster |
| 4.7 | RideView | SHELF | Algorithm works but needs hardware (borescope) |

---

## 🗺️ PRE-BUILT ASSET INVENTORY
*Stuff that already exists and can be wired in*

### Ready to Deploy (Code Exists + Tests Pass)
| Asset | Location | Tests | What It Does |
|-------|----------|-------|-------------|
| KB Enrichment Pipeline | rivet-pro/rivet_pro/core/services/kb_* | 234 | 6-phase: search→download→parse→store→embed→metrics |
| Spanish Localization | rivet-pro/rivet/i18n/ | 25 | Auto-detect language, translate responses |
| WhatsApp/Twilio Integration | rivet-pro (MessageRouter) | 56 | Shared router for Telegram + WhatsApp |
| E2E Smoke Tests | rivet-pro/tests/e2e/ | 81 | Full flow testing |
| CI/CD Workflows | rivet-pro/.github/workflows/ | — | Test on push, nightly regression |
| Landing Page | plc-copilot-landing/ | 27 files | Next.js + Tailwind, dark industrial theme |
| Troubleshooting Navigator | rivet-pro/rivet_pro/core/ (Phase 2) | — | Mermaid diagram → interactive Telegram flow |
| Equipment Matcher | rivet-pro/rivet/atlas/equipment_matcher.py | — | OCR → equipment identification |
| LLM Router | Agent-Factory/agent_factory/llm/ | — | Multi-model routing, 73% cost reduction |
| Backlog.md CLI tool | _inventory/Backlog.md/ | — | CLI backlog management |

### Partially Built (Needs Integration)
| Asset | Location | Status | Gap |
|-------|----------|--------|-----|
| Database Failover | rivet-pro (MultiDatabaseManager) | 40% | Needs Turso/Supabase sync |
| PLC Tutor | Agent-Factory/products/plc-tutor/ | 20% | Spec + backlog exists |
| Ralph Autonomous System | VPS /root/ralph/ | 50% | 7 scripts, needs reconnection |
| Photo Bot V2 (n8n) | VPS n8n workflows | Working | Superseded by current bot |
| FactoryLM Core | factorylm-core/ | 85% | LLM abstraction layer |
| FactoryLM PLC Client | factorylm-plc-client/ | 90% | Web dashboard + PLC comms |

---

## 🏃 CURRENT SPRINT (This Week: Jan 27-31)
*Put First Things First (Habit 3)*

### Monday (Today)
- [x] Bot deployed + working
- [x] Registration + OTP
- [x] Freemium gate
- [x] FactoryLM rebrand
- [x] KB Harvester built
- [ ] KB Harvester deployed + seeding
- [ ] Wire RAG into bot responses

### Tuesday-Wednesday
- [ ] Twilio phone number for SMS drip
- [ ] factorylm.com → VPS (if Mike gets domain access)
- [ ] Landing page deployed at factorylm.com
- [ ] HTTPS (Let's Encrypt via Caddy)
- [ ] Reddit harvester running, verify quality

### Thursday-Friday
- [ ] WhatsApp integration deployed
- [ ] Spanish localization activated
- [ ] 1000+ KB entries target
- [ ] Stripe payment links (Pro tier)
- [ ] Soft launch prep (r/PLC post draft)

---

## 📊 KEY METRICS TO TRACK

| Metric | Current | Week Target | Month Target |
|--------|---------|-------------|-------------|
| KB entries | ~67 (SQLite) | 1,000+ | 5,000+ |
| Registered users | 1 (Mike) | 5 | 50 |
| Daily photo analyses | ~40 (test) | 10 real | 100 |
| Revenue | $0 | $0 | First paying user |
| Channels | Telegram | +WhatsApp | +Web |
| Bot response time | ~8s | <5s | <3s |

---

## 💡 COVEY PRINCIPLES APPLIED

1. **Be Proactive** — Don't wait for users to find bugs. Harvest knowledge, monitor, improve.
2. **Begin With The End In Mind** — FactoryLM = NotebookLM for factories. Every task serves that vision.
3. **Put First Things First** — Q2 work (KB, revenue path) over Q3/Q4 busywork.
4. **Think Win-Win** — Free tier is generous enough to hook users. Paid tier is worth it.
5. **Seek First to Understand** — Listen to r/PLC, r/electricians. Build what techs actually need.
6. **Synergize** — Pre-built assets combine: KB + RAG + Bot + CMMS + WhatsApp = platform.
7. **Sharpen the Saw** — Knowledge base grows 24/7. Bot gets smarter every day.

---

*This board is the single source of truth. Update it, not scattered status files.*
