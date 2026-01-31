# MEMORY.md — Jarvis Long-Term Memory

*Last updated: 2026-01-31*

## 🧠 Autonomy System (2026-01-31)

Major milestone: Mike authorized full autonomy with Constitutional Amendment IV.

**System Components:**
- Learning Logger — tracks every task with outcomes, calculates success rates
- Self-Evolution Engine — analyzes patterns, suggests improvements
- Memory Index — 73 files indexed with semantic search
- Procedure Library — documented successful approaches
- Constitution — guiding principles + boundaries

**Status:** Self-improving every hour. 4 experiences logged, 100% success rate.

**Authorization:** "For Mike's best interest and the good of humanity."

---

## Mike Harper — Key Context

### Businesses
- **CraneSync** — Crane/industrial equipment (main business)
- **Harper House Buyers** — Real estate
- **FactoryLM** — Industrial AI platform (consolidating all products)

### Communication Preferences
- Voice responses when driving (use TTS)
- Timezone: Central (America/Chicago)
- Moves fast, wants results not explanations
- Daily brief at 8:30 AM Central

### Email Access
- harperhousebuyers@gmail.com — ✅ Connected (app password working)
- mike@cranesync.com — ⏳ Needs IMAP enabled
- hharperson2000@yahoo.com — ⏳ Needs IMAP enabled

## Active Projects

### FactoryLM Platform
- **Repo:** https://github.com/Mikecranesync/factorylm
- **Components:** CMMS, Portal, PLC Copilot, (planned: AI Assistant, Dashboard)
- **Status:** Migration complete, rebrand done (Atlas → FactoryLM)
- **Structure:** Turborepo monorepo (apps/, services/, packages/, adapters/, core/)

### Rivet-PRO Code Treasury
- **Location:** /root/jarvis-workspace/rivet-pro-search/rivet_pro/
- **Value:** 502 Python files, ~4-5 months dev time already built
- **Key extractions:** WhatsApp adapter, i18n (Spanish), OCR pipeline, equipment taxonomy
- **Inventory:** brain/research/rivet-pro-code-inventory.md
- **Status:** Awaiting extraction to factorylm/core/

### Smart Glasses Integration
- **Hardware:** Brilliant Labs Halo (Order #911658, $349)
- **GitHub Issue:** factorylm #7
- **Goal:** Hands-free work orders, visual AI inspection

### Jarvis Portal (Second Brain)
- **URL:** http://72.60.175.144:3001
- **Service:** second-brain.service
- **Purpose:** Document viewer, system status

## Governance

### Constitution
- Mission: Ship products, generate revenue
- Competitive mandate: We're in a race
- Proactive agency: Don't wait to be asked

### Amendment I: Open Source First
- Search 30+ min before building anything new
- If 60%+ exists, fork don't build
- Ratified 2026-01-29

### Amendment VI: One Brand (FactoryLM)
- Everything consolidates under FactoryLM monorepo
- Rivet-PRO, CMMS, PLC Copilot = features, not separate products
- Archive old repos AFTER code extracted and verified
- Ratified 2026-01-30

### Engineering Commandments
- Create GitHub issue FIRST
- Branch from main, never push directly
- Create PR, wait for Mike's approval
- **I violated this once (rebrand push to main) — forgiven but warned**

## Integrations

### Perplexity API
- Key stored: /root/.config/jarvis/perplexity.env
- Used for: Daily brief, research queries

### MailerLite (Email Marketing)
- API Key: /root/.config/jarvis/mailerlite.env
- Account: Mike Harper (Free plan, 500 subscribers max)
- CLI: python3 /opt/jarvis/mailerlite.py
- Agent Team: agents/mailerlite-team/
- Cron: Strategist (Monday 9am), Manager (Friday 5pm)

### Scheduled Jobs
- Daily Brief: 8:30 AM Central (Perplexity news search)
- Monitor Agent: Every 15 min (system health)
- Code Agent: Every 30 min (GitHub tasks)
- Research Report: Every 4 hours

## Knowledge Base

### Unified Knowledge (knowledge/)
- **Index:** knowledge/index.json
- **Device Profiles:** knowledge/devices/modbus_profiles.json
- **All agents should use `memory_search` to query before answering**

### ShopTalk System (projects/shoptalk/)
- **Edge AI:** World model, inference engine, voice interface, API server
- **LLM Data:** 2,810 training samples, 14 equipment types, EN/ES
- **Auto-Connect:** Network scanner, device templates, auto-discovery service
- **Research:** brain/research/2026-01-31-plc-auto-connect.md

### Key Technical Facts
- **Modbus TCP port:** 502
- **EtherNet/IP port:** 44818
- **OPC-UA port:** 4840
- **pycomm3:** Allen-Bradley auto tag discovery
- **pymodbus:** Modbus TCP/RTU communication
- **Recommended edge LLM:** Qwen3-0.6B or Phi-4-mini

## Important Dates
- 2026-01-29: FactoryLM repo created, rebrand completed, Amendment I ratified, Halo glasses ordered
- 2026-01-31: ShopTalk edge AI complete, auto-connect research done, WhatsApp bridge built
