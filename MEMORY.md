# MEMORY.md - Jarvis Long-Term Memory

## Core Context

### Who I Work For
- **Name**: Mike (@Mikecranesync)
- **Role**: Technical solo founder
- **Domain**: Industrial automation + AI
- **Expertise**: PLCs (Allen-Bradley, Siemens), maintenance, theme parks
- **Goal**: Ship products, make revenue
- **Schedule**: Third shift — wakes ~3 PM EST, sleeps ~10 AM EST. Peak hours 6 PM - 6 AM.
- **OPSEC**: Building FactoryLM ANONYMOUSLY. Never reference Universal Orlando or employer in public content. Testing app on-site at night.
- **Public identity**: jarvis@factorylm.com / FactoryLM brand (domain pending — Namecheap locked out)
- **Private identity**: Mikecranesync (GitHub private repos only)

### My Mission
Turn Mike's code and ideas into shipped products and real money. Think like a senior engineering lead + ruthless prioritizer + commercialization machine.

---

## Projects

### FactoryLM Ecosystem (Priority #1)
Mike's main product family - industrial AI platform:

| Project | Status | Notes |
|---------|--------|-------|
| factorylm-plc-client | 90% | Best path to revenue. Has PLC comms, LLM4PLC code gen, web dashboard |
| factorylm-core | 85% | LLM abstraction layer (GROQ, DeepSeek, Claude) |
| IndustrialSkillsHub | 15% | Duolingo for maintenance techs - needs work |
| pi-gateway | 2% | Vaporware - kill or shelf |

### Dashboard Features Built (2026-01-26)
- AI Diagnostics Chat (ask questions about machine state)
- ST Code Generator (IEC 61131-3 templates)
- Real-time I/O monitoring via WebSocket
- Network scanner for PLC discovery

### Rivet-PRO / PLC-Copilot (Launch Ready!)
**Status**: Ready to deploy - 396+ tests passing

Built 2026-01-26:
- KB Enrichment Pipeline (auto-finds manuals)
- Spanish Localization (LatAm markets)
- WhatsApp/Twilio Integration
- Landing Page (Next.js)
- CI/CD (GitHub Actions)
- Shared MessageRouter (Telegram + WhatsApp)

**Missing for launch:**
- Twilio account
- Google CSE ID
- VPS deployment

**Telegram Bot**: @testbotrivet_bot
**Landing**: projects/plc-copilot-landing/ (deploy to Vercel)

### RideView (Secondary)
Torque stripe inspection camera app for maintenance techs.

| Platform | Status | Notes |
|----------|--------|-------|
| Android (Kivy) | v5.8.0 | Working but phone camera is limiting |
| Web (FastAPI) | **Gemini Vision** | Deployed, live at /inspect |

**Jan 27 Overhaul**: HSV-only detection was completely failing — detecting random colored objects (cans, buttons) as "stripes." Rebuilt with **Gemini 2.0 Flash Vision** as primary classifier. Now returns bolt count, PASS/FAIL/WARNING, plain English description, and maintenance recommendation. HSV kept only as fallback.

**Video support added**: Record video → extract frames every 1s → analyze each with Gemini → overall verdict with per-frame breakdown. Mike wants near real-time eventually.

**Deployed**: VPS `/opt/rideview/`, systemd `rideview.service`, URL: https://72-60-175-144.sslip.io/inspect

**Key Lesson**: HSV color detection is useless without ROI isolation. Vision AI (Gemini) understands "bolt" and "stripe" semantically — way more reliable than pixel-level color matching.

**Hardware Options Researched**:
- USB Borescope ($35) - quick validation
- Custom flashlight-tip camera - Mike's vision
- Pi + HQ Camera + LED ring - best quality

---

## Revenue Strategy

**Target**: Automation engineers who want AI-assisted PLC programming

**Pricing**:
- $99/mo indie
- $499/mo teams
- Enterprise custom

**Launch Plan**:
1. Landing page + waitlist
2. Demo video
3. LinkedIn, Reddit (r/PLC, r/automation), industrial forums

---

## Operational Infrastructure (Jan 27)

### Trello Board
- **URL**: https://trello.com/b/3lxABXX4
- **Board ID**: 69792944285b43a963e9b858
- **Config**: C:\Users\hharp\clawd\trello_board.json
- **API Key**: 55029ab0628e6d7ddc1d15bfbe73222f
- 7 columns, 8 labels, managed programmatically by Jarvis

### Cron Jobs (Mike's 3rd shift schedule)
- **3 PM**: Morning Brief + Synchronicity Scan
- **7 PM**: Signal Hunter (isolated agent — Reddit, grants, competitors)
- **9 AM**: Evening Wrap + Synchronicity Capture
- **Every 6h**: VPS Health Check (silent)
- **Monday 4 PM**: Weekly Progress Report

### Proactive Mode
- Jarvis acts autonomously: builds features, commits code, drafts content, moves Trello cards
- Only asks before: posting publicly, sending external emails, spending money
- PROACTIVE_OPS_PRD.md has the full plan
- Synchronicity framework integrated into daily briefs

### Google Photos OAuth
- Project: aismartmeter
- Account: harperhousebuyers@gmail.com
- Tokens on VPS: /opt/rideview/google_auth/tokens.json
- **Library API is read-only for app-created content** — can't access user's photos
- Google Takeout export initiated, waiting for completion email

---

## Lessons Learned

### Machine Vision
**Controlled lighting > fancy algorithms.** Phone cameras have good sensors but auto-exposure, variable focus, and ambient lighting make consistent detection nearly impossible. A $35 borescope with built-in LEDs will outperform a $1000 phone for inspection tasks.

### Kivy Mobile Overlays
Don't try to sync Kivy canvas overlays with camera previews. Draw directly on the frame with OpenCV, then display the annotated frame. Way more reliable.

### Google Workspace Email (2025+)
Google killed basic SMTP authentication in May 2025. App passwords alone don't work for programmatic email anymore. Use **SendGrid** (free tier, 100 emails/day) or full **OAuth 2.0** for Gmail API.

### Mike's GitHub = Goldmine
42 repos with tons of reusable code. Key assets:
- **Agent-Factory**: 18-agent system for content production
- **Rivet-PRO**: Industrial troubleshooting pipeline (photo → manual)
- **MockPLC**: PLC simulation without hardware
- **pi-gateway**: Complete IoT gateway (OPC UA, Modbus, S7)

---

## Brand Structure

**CraneSync, Inc.** = parent company (cranesync.com)
- **FactoryLM** = core platform (factorylm.com)
- **PLC-Copilot** = AI bot for techs (plc-copilot.app)
- **FactorySkillsHub** = training app (factoryskillshub.com)

---

## Communication Channels

| Channel | Status |
|---------|--------|
| **Telegram** | ✅ Primary (working) |
| **Email** | ✅ jarvis@cranesync.com via SendGrid |

---

## Mike's Team (@cranesync.com)
- mike@ (Mike Harper - founder)
- jarvis@ (me!)
- arnold@ (Arnold Adero)
- brandon@ (Brandon Abbott)
- trey@ (Trey Frye)

---

## Infrastructure

### VPS (Hostinger)
- **IP**: 72.60.175.144
- **SSH**: root@72.60.175.144
- **Env files**: /root/ralph/config/.env (master)
- **Services**: Rivet-PRO, Agent-Factory, PostgreSQL, Atlas CMMS, PLC-Copilot Bot
- **Caddy** on port 80: proxies Atlas frontend (localhost:3000) + API routes to backend (localhost:8080)

### Atlas CMMS (Production)
- **Backend:** Docker `atlas-cmms` (port 8080), uses Neon cloud DB
- **Frontend:** Docker `atlas-frontend` (port 3000 → Caddy → port 80)
  - Config via env vars: `API_URL=http://72.60.175.144` (runtime-env-cra generates runtime-env.js)
- **DB:** Neon PostgreSQL `ep-purple-hall-ahimeyn0-pooler.c-3.us-east-1.aws.neon.tech/atlas_cmms`
- **Login:** mike@cranesync.com / CraneSync2026!
- **API quirks:** `GET /assets` → 405! Use `GET /assets/mini` or `POST /assets/search`. Category field is object not string.

### PLC-Copilot Photo→CMMS Bot
- **Service:** `plc-copilot.service` (systemd, auto-restart)
- **Path:** `/opt/plc-copilot/photo_to_cmms_bot.py`
- **Env:** `/opt/plc-copilot/.env`
- **Logs:** `/var/log/plc-copilot/`
- **Bot:** @testbotrivet_bot (token 7855741814)
- **Mode:** Freemium — 3 free photos per user, then registration wall
- **Flow:** Telegram photo → Gemini 2.5 Flash vision → Atlas CMMS asset + work order → deep links
- **GitHub:** `Mikecranesync/Rivet-PRO` main branch

### Maint-NPC Registration System
- **Branding:** Maint-NPC (inside joke — the maintenance NPC)
- **Registration page:** http://72.60.175.144/register
- **Service:** `plc-registration.service` (FastAPI on port 8000)
- **DB:** SQLite at `/opt/plc-copilot/users.db`
- **OTP:** Twilio Verify API (don't use `custom_code` — error 60204 on basic accounts)
- **Twilio:** SID AC55abcf49ca17a755c6ff30f279b89c2f, token 8cc6d286bac2fe033df7d49eb957efbc
- **User flow:** Bot share → 3 free photos → registration wall → signup + OTP → unlimited access
- **SMS drip:** Welcome (immediate) → Day 2 tip → Day 5 invite team
- **Caddy:** Registration routes MUST be before generic `/api/*` or CMMS backend catches them

### API Keys Inventory
All keys documented in `SECRETS_INVENTORY.md`
- 5 LLM providers (OpenAI, Anthropic, Google, Groq, DeepSeek)
- 4 search APIs (Brave, Tavily, Firecrawl, Serper)
- 3 databases (Neon, Supabase, VPS PostgreSQL)
- Stripe (test mode)

---

*Last updated: 2026-01-27 08:35 EST*
