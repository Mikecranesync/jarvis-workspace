# Mike's GitHub Inventory
Generated: 2026-01-26

## Summary
- **Total repos:** 42
- **Active projects:** 12 (updated in last 30 days)
- **Reusable components:** 15+
- **Dead/abandoned:** ~10
- **Forked/reference:** 8

## Quick Stats by Category

| Category | Count | Status |
|----------|-------|--------|
| Industrial AI / FactoryLM | 5 | 🟢 Active |
| Personal AI / Jarvis | 6 | 🟡 Mixed |
| Mobile Apps | 3 | 🟡 Partial |
| Agent/Automation | 6 | 🟢 Active |
| Utilities/Tools | 6 | 🟡 Mixed |
| Dead/Abandoned | ~10 | ⚫ Archive |
| Forked/Reference | 6 | 📚 Reference |

---

## By Category

### 🏭 Industrial AI / FactoryLM

| Repo | Status | Key Components | Last Updated |
|------|--------|----------------|--------------|
| **factorylm-plc-client** | ✅ Working | Modbus TCP, Mock PLC, LLM4PLC, ST Code Gen | 2026-01-25 |
| **factorylm-core** | ✅ Working | Multi-LLM abstraction (GROQ/DeepSeek/Claude), cost tracking | 2026-01-23 |
| **factorylm-landing** | ✅ Working | Next.js landing page for factorylm.com | 2026-01-26 |
| **pi-gateway** | ✅ Working | IoT gateway, OPC UA, Modbus, S7, EtherNet/IP, FastAPI | 2026-01-25 |
| **RideView** | 🟢 Active | Torque stripe CV detection, Kivy mobile, Flask web | 2026-01-26 |

### 🤖 Personal AI / Jarvis

| Repo | Status | Key Components | Last Updated |
|------|--------|----------------|--------------|
| **jarvis-workspace** | ✅ Current | This workspace - Clawdbot config | 2026-01-26 |
| **jarvis-unified** | 🟡 Partial | PAI + Gmail/Calendar/Tasks, Tauri app, 70% test coverage | 2025-11-23 |
| **jarvis-core** | ⚠️ Deprecated | Next.js monorepo, SDK pattern → moved to Agent-Factory | 2025-12-21 |
| **jarvis-for-gmail** | 🟡 Partial | Tauri + LangGraph email agent, 3-tier categorization | 2025-11-16 |
| **jarvis-android-voice-proto** | 🟡 Partial | React Native voice email app | 2025-12-21 |
| **pai-config-windows** | 📚 Reference | Claude Code PAI config patterns | 2025-11-10 |

### 📱 Mobile Apps

| Repo | Status | Key Components | Last Updated |
|------|--------|----------------|--------------|
| **IndustrialSkillsHub** | ✅ Working | Next.js, Duolingo-style gamification, bilingual | 2026-01-23 |
| **IndustrialSkillsHub-native** | 🟡 Partial | React Native version | 2026-01-22 |
| **RideView** | ✅ Working | Kivy cross-platform, Android buildable | 2026-01-26 |

### 🤖 Agent/Automation Frameworks

| Repo | Status | Key Components | Last Updated |
|------|--------|----------------|--------------|
| **Agent-Factory** | ✅ Active | 18 agents, RIVET, PLC Tutor, YouTube content pipeline | 2026-01-10 |
| **Rivet-PRO** | ✅ Active | Industrial maintenance KB, Telegram bot | 2026-01-23 |
| **ralph** | 📚 Forked | Amp-based autonomous dev loop (original snarktank) | 2026-01-07 |
| **My-Ralph** | 🟡 Partial | Claude Code version of Ralph pattern | 2026-01-23 |
| **CodeBang** | ⚠️ Deprecated | DevCTO agent → merged to Agent-Factory | 2025-12-21 |
| **clawdbot** | 📚 Forked | Personal AI assistant CLI | 2026-01-26 |

### 🛠️ Utilities / Tools

| Repo | Status | Key Components | Last Updated |
|------|--------|----------------|--------------|
| **cmms** | 📚 Forked | Atlas CMMS - full maintenance management (Java/React) | 2026-01-16 |
| **Backlog.md** | 📚 Forked | AI-agent task management | 2025-12-17 |
| **Thefuture** | 📚 Forked | PAI (Personal AI Infrastructure) reference | 2025-12-20 |
| **n8n-docs** | 📚 Forked | n8n automation docs | 2026-01-06 |
| **Archon** | 📚 Forked | Knowledge/task management for AI | 2025-08-15 |
| **langchain-crash-course** | 📚 Reference | LangChain learning | 2024-08-20 |

### ⚫ Dead/Abandoned Projects

| Repo | Status | Notes |
|------|--------|-------|
| **Friday** / **Friday-2** / **FRIDAYNEW** | ⚫ Dead | AI Studio experiments |
| **Chucky** / **chucky_project** | ⚫ Dead | Early AI app experiments |
| **claudegen-coach** | ⚫ Dead | No description |
| **Nexus** / **Nexus1** / **nexus-cmms-recovery-point-2** | ⚫ Dead | CMMS experiments |
| **Nexus-backend** / **ProjectNexus** | ⚫ Dead | More CMMS iterations |
| **TechMeterAI** / **AISmartMeterApp** | ⚫ Dead | AI meter apps |
| **VibeBuddy** | ⚫ Dead | Unknown |
| **ScoutPathApp** | ⚫ Dead | Unknown |
| **Einstein** | ⚫ Dead | App |
| **questify-kid-learn** | ⚫ Dead | Kids learning app |
| **your-assistant-app** | ⚫ Dead | Generic assistant |

---

## Detailed Analysis

---

### Repo: factorylm-plc-client
**Purpose:** Python library for PLC communication with Factory I/O simulation + Allen-Bradley Micro 820 via Modbus TCP. Includes LLM4PLC for AI-generated Structured Text code.

**Stack:** Python, pymodbus, FastAPI backend

**Status:** ✅ Working - Production Ready

**Key Files:**
- `src/factorylm_plc/` - Core library
  - `factory_io.py` - Factory I/O integration
  - `micro820.py` - Allen-Bradley Micro 820 client
  - `mock_plc.py` - Full simulation without hardware
  - `llm4plc.py` - IEC 61131-3 ST code generation
  - `models.py` - FactoryState dataclass with `to_llm_context()`
- `backend/` - FastAPI web interface
  - `routes/plc.py` - PLC API endpoints
  - `routes/websocket.py` - Real-time WebSocket
  - `services/plc_connection.py` - Connection management
- `examples/` - Usage demos
- `recovery/` - PLC recovery tools for lost network config

**Reusable Components:**
- **MockPLC** - Full PLC simulation for testing without hardware
- **LLM4PLC** - ST code generation templates (conveyor, motor_safety, sorting_station)
- **to_llm_context()** - State formatting for AI prompts
- **Connection Manager** - Retry logic, reconnection handling

**Missing/Broken:** None - well documented

**Dependencies:** Standalone

---

### Repo: factorylm-core
**Purpose:** LLM abstraction layer for industrial applications. Unified interface for GROQ, DeepSeek, Claude with cost tracking.

**Stack:** Python, LangChain compatible

**Status:** ✅ Working

**Key Files:**
- `src/factorylm/llm/` - Provider implementations
  - `groq_client.py` - GROQ (Mixtral)
  - `deepseek_client.py` - DeepSeek
  - `claude_client.py` - Anthropic Claude
  - `flm_client.py` - Future FactoryLM model
  - `base.py` - Abstract base class
- `src/factorylm/config.py` - Configuration management
- `tests/` - Full test suite

**Reusable Components:**
- **LLM Router** - Switch providers with env var
- **Cost Tracker** - Built-in API cost estimation
- **analyze_machine_state()** - Industrial-focused method for PLC data analysis
- **Standardized LLMResponse** - Consistent format across providers

**Dependencies:** Used by factorylm-plc-client

---

### Repo: Agent-Factory
**Purpose:** Massive orchestration engine powering PLC Tutor (YouTube content) and RIVET (industrial maintenance KB). 18 autonomous agents for content production.

**Stack:** Python, LangGraph, Supabase, PostgreSQL, FFmpeg, ElevenLabs

**Status:** ✅ Active - Complex but Working

**Key Files:**
- `agent_factory/` - Core framework
  - `core/` - AgentFactory, Orchestrator, Settings
  - `rivet_pro/` - RIVET maintenance system
  - `workflows/` - LangGraph pipelines
  - `platform/` - Telegram adapter, state management
  - `observability/` - Slack supervisor, instrumentation
- `plc/` - PLC Tutor content
  - `content/CONTENT_ROADMAP_AtoZ.md` - 100+ video topics
- `rivet/` - RIVET deployment configs
- `docs/` - Extensive documentation (142KB+)

**Reusable Components:**
- **18 Agent System** - Research, Scriptwriter, VideoAssembly, YouTube Uploader, etc.
- **LangGraph Ingestion Pipeline** - 7-stage KB ingestion
- **Hybrid Search** - pgvector + Supabase
- **Cost-Optimized LLM Router** - Ollama (free) / GPT-4o-mini / Claude
- **Telegram Bot Framework** - Complete bot with inline keyboards
- **Perplexity-Style Citations** - Attribution system for KB atoms

**Dependencies:** Uses factorylm-core patterns

---

### Repo: pi-gateway
**Purpose:** Industrial IoT gateway - eWON replacement for Raspberry Pi. VPN remote access, multi-protocol PLC data collection.

**Stack:** Python, FastAPI, React, WireGuard, asyncio

**Status:** ✅ Working

**Key Files:**
- `src/api/` - FastAPI application
- `src/plc/` - Protocol clients
  - OPC UA (asyncua)
  - Modbus TCP/RTU (pymodbus)
  - Siemens S7 (python-snap7)
  - EtherNet/IP (pycomm3)
- `src/data/` - Database & MQTT
- `src/alerts/` - Multi-channel alerting (Email, SMS, Telegram, Webhook)
- `src/vpn/` - WireGuard management
- `web/` - React dashboard
- `config/default.yaml` - Device configuration

**Reusable Components:**
- **Multi-Protocol PLC Clients** - Connect to any industrial PLC
- **Alert Engine** - Telegram, Email, SMS, Webhook
- **VPN Manager** - WireGuard tunnel setup
- **Device Config Schema** - YAML-based tag configuration

**Dependencies:** Standalone

---

### Repo: RideView
**Purpose:** Real-time torque stripe detection for industrial bolt verification. CV-based PASS/WARNING/FAIL classification.

**Stack:** Python, OpenCV, Kivy (mobile), Flask (web), uv

**Status:** ✅ Working

**Key Files:**
- `src/rideview/core/` - Detection pipeline
  - `detector.py` - Main TorqueStripeDetector
  - `config.py` - Configuration management
- `src/rideview/detection/` - Pipeline components
  - `preprocessor.py`, `color_segmenter.py`, `line_analyzer.py`, `stripe_validator.py`
- `src/rideview/mobile/` - Kivy cross-platform app
- `src/rideview/web/` - Flask MJPEG streaming
- `buildozer.spec` - Android build config

**Reusable Components:**
- **CV Detection Pipeline** - Modular frame processing
- **Kivy Camera Provider** - Cross-platform camera abstraction
- **MJPEG Streaming** - Flask-based video streaming

**Dependencies:** Standalone

---

### Repo: IndustrialSkillsHub
**Purpose:** Duolingo-style gamified training for industrial maintenance technicians. Bilingual Spanish/English.

**Stack:** Next.js 14, React 18, TypeScript, PostgreSQL (Neon), Drizzle ORM, Clerk, Stripe

**Status:** ✅ Working

**Key Files:**
- `app/` - Next.js app router
  - `(main)/` - Learn, courses, leaderboard
  - `lesson/` - Challenge pages
  - `onboarding/` - Role selection
  - `admin/` - Admin dashboard
- `db/schema.ts` - Drizzle schema (courses, lessons, challenges, progress)
- `store/use-language.ts` - Zustand bilingual toggle
- `scripts/seed-industrial.ts` - Industrial content seeder

**Reusable Components:**
- **Gamification System** - XP, hearts, streaks, leaderboards, badges
- **Bilingual System** - Instant language switch, localStorage persistence
- **Role-Based Learning Paths** - Mechanic, Electrician, PLC Technician tracks
- **Drizzle ORM Schema** - Complete learning platform data model

**Dependencies:** Standalone

---

### Repo: jarvis-unified
**Purpose:** PAI-powered personal AI operating system. Combines PAI orchestration with specialized sub-apps (Gmail, Calendar, Tasks).

**Stack:** Bun, Tauri, React, SQLite, LangGraph

**Status:** 🟡 Partial - Good foundation, needs completion

**Key Files:**
- `.claude/skills/jarvis-gmail/` - PAI skill with workflows
- `apps/jarvis-hub/` - Command center (React + Vite)
- `apps/jarvis-gmail/tauri-app/` - Email assistant
  - `src/agent/` - LangGraph AI categorization
  - `src/api/` - Gmail/Outlook/Yahoo providers
  - `src/db/` - SQLite database
- `docs/ARCHITECTURE.md` - System design

**Reusable Components:**
- **PAI Skills System** - Progressive disclosure, 92.5% token reduction
- **3-Tier Email Categorization** - Tier 1 (auto), Tier 2 (draft), Tier 3 (escalate)
- **Multi-Account Email Provider** - Gmail, Outlook, Yahoo abstraction
- **Hybrid AI Cost Optimization** - $30/mo → $7.50/mo for 30K emails

**Dependencies:** PAI patterns

---

### Repo: jarvis-for-gmail
**Purpose:** Autonomous agentic email assistant that handles 70% of emails automatically.

**Stack:** Tauri, Bun, LangGraph, SQLite

**Status:** 🟡 Partial - Foundation built, Phase 1 in progress

**Key Files:**
- `tauri-app/src/agent/` - LangGraph agent logic
- `tauri-app/src/gmail/` - Gmail API integration
- `tauri-app/src/style/` - Writing style learning
- `tauri-app/src/voice/` - Voice control integration

**Reusable Components:**
- **Writing Style Replication** - Few-shot prompting from sent emails
- **Multi-Model Cost Optimization** - Gemini FREE tier + Claude for quality
- **3-Tier Decision Hierarchy** - Auto-handle, Draft, Escalate

**Dependencies:** Can merge into jarvis-unified

---

### Repo: ralph / My-Ralph
**Purpose:** Autonomous AI development loop that runs Claude Code repeatedly until all PRD items complete.

**Stack:** Bash, Claude Code CLI

**Status:** 📚 Reference (ralph is fork from snarktank), 🟡 My-Ralph is adaptation

**Key Files:**
- `ralph.sh` - Main loop script
- `prompt.md` - Instructions for each iteration
- `prd.json` - User stories with pass/fail status
- `skills/` - PRD generation, Ralph conversion

**Reusable Components:**
- **Autonomous Dev Loop Pattern** - Fresh context per iteration
- **PRD → JSON Conversion** - Structured task management
- **Exit Detection** - Dual-condition completion check
- **Circuit Breaker** - Prevents runaway loops

**Dependencies:** Claude Code CLI

---

### Repo: cmms (Fork of Atlas CMMS)
**Purpose:** Self-hosted CMMS - Computerized Maintenance Management System

**Stack:** Java Spring Boot (API), React (Web), React Native (Mobile), PostgreSQL

**Status:** 📚 Reference - Fork for learning/customization

**Key Files:**
- `api/` - Java Spring Boot backend
- `frontend/` - React web app
- `mobile/` - React Native app
- `docker-compose.yml` - Full deployment

**Reusable Components:**
- **Complete CMMS Data Model** - Work orders, assets, inventory, locations
- **Multi-language Support** - 14 languages
- **Mobile + Web Architecture** - Shared backend pattern
- **Docker Deployment** - PostgreSQL + MinIO + App

**Dependencies:** Standalone

---

## Consolidation Recommendations

### Already Consolidated
- `jarvis-core` → `Agent-Factory` ✅
- `CodeBang` → `Agent-Factory` ✅

### Should Consolidate
1. **jarvis-for-gmail** → **jarvis-unified** (same purpose, unified is more complete)
2. **jarvis-android-voice-proto** → Consider for jarvis-unified mobile expansion
3. **IndustrialSkillsHub-native** → Could merge with main IndustrialSkillsHub

### Archive Candidates
All repos in "Dead/Abandoned" section can be archived:
- Friday variants, Chucky variants, Nexus variants, early experiments

### Keep as Reference
- `ralph` - Original pattern reference
- `cmms` - CMMS domain knowledge
- `Backlog.md` - Task management patterns
- `Thefuture` - PAI reference implementation

---

## Reusable Asset Inventory

### Production-Ready Libraries
| Asset | Repo | Description |
|-------|------|-------------|
| MockPLC | factorylm-plc-client | Full PLC simulation without hardware |
| LLM4PLC | factorylm-plc-client | IEC 61131-3 code generation |
| LLM Router | factorylm-core | Multi-provider LLM abstraction |
| Cost Tracker | factorylm-core | API cost estimation |
| Multi-Protocol PLC | pi-gateway | OPC UA, Modbus, S7, EtherNet/IP |
| CV Detection Pipeline | RideView | Frame → Analysis → Result |

### Frameworks/Patterns
| Pattern | Repo | Description |
|---------|------|-------------|
| 18 Agent System | Agent-Factory | Complete content production pipeline |
| PAI Skills | jarvis-unified | Progressive disclosure orchestration |
| Gamification | IndustrialSkillsHub | XP, hearts, streaks, leaderboards |
| 3-Tier Email | jarvis-* | Auto/Draft/Escalate classification |
| Ralph Loop | ralph/My-Ralph | Autonomous dev cycle pattern |

### Integrations
| Integration | Repo | Description |
|-------------|------|-------------|
| Telegram Bot | Agent-Factory | Complete bot with inline keyboards |
| Gmail API | jarvis-for-gmail | OAuth + Pub/Sub webhooks |
| YouTube API | Agent-Factory | Upload, metadata, analytics |
| Stripe | IndustrialSkillsHub | Payment integration |
| Clerk | IndustrialSkillsHub | Auth provider |

### Database Schemas
| Schema | Repo | Description |
|--------|------|-------------|
| Learning Platform | IndustrialSkillsHub | Courses, lessons, challenges, progress |
| CMMS | cmms | Work orders, assets, inventory |
| KB Atoms | Agent-Factory | Knowledge base with embeddings |
| Email State | jarvis-unified | Email categorization & drafts |

---

## Repository Health Dashboard

### Active Development (Last 7 days)
- ✅ RideView
- ✅ jarvis-workspace
- ✅ factorylm-landing
- ✅ clawdbot (fork)

### Active Development (Last 30 days)
- ✅ factorylm-plc-client
- ✅ pi-gateway
- ✅ IndustrialSkillsHub
- ✅ Rivet-PRO
- ✅ My-Ralph
- ✅ factorylm-core
- ✅ Agent-Factory

### Maintenance Mode (>30 days)
- 🟡 jarvis-unified (Nov 2025)
- 🟡 jarvis-for-gmail (Nov 2025)
- 🟡 IndustrialSkillsHub-native (Jan 2026)

### Archive Candidates
- All Nexus variants
- All Friday variants
- All Chucky variants
- Early AI experiments

---

## Next Steps

1. **Archive dead repos** - Move to private or add archive flags
2. **Consolidate Jarvis repos** - jarvis-for-gmail → jarvis-unified
3. **Document factorylm-* integration** - How PLC client + core work together
4. **Extract reusable components** - Create npm/pip packages from common code
5. **Create project dependency map** - Visual graph of how repos relate

---

*Generated by Jarvis subagent for @Mikecranesync GitHub inventory*
