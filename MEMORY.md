# MEMORY.md — Jarvis Long-Term Memory

*Last updated: 2026-01-29*

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

## Important Dates
- 2026-01-29: FactoryLM repo created, rebrand completed, Amendment I ratified, Halo glasses ordered
