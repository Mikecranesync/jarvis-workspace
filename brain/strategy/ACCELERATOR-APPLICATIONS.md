# Accelerator Application Package
*FactoryLM - Industrial AI for Maintenance Teams*

**Created:** 2026-02-05
**Status:** IN PROGRESS

---

## Target Accelerators

### Tier 1 - Apply Immediately

| Accelerator | Deadline | Investment | Focus | Status |
|-------------|----------|------------|-------|--------|
| Y Combinator | Rolling (W26) | $500k | General tech | ⏳ |
| Techstars | Spring 2026 open | $120k | Industry-specific | ⏳ |
| 500 Global | Rolling | $150k | AI-native, Agentic | ⏳ |

### Tier 2 - Strong Alternatives

| Accelerator | Focus | Fit |
|-------------|-------|-----|
| Plug and Play | Manufacturing/IoT | Strong - edge devices |
| MassChallenge | General (no equity) | Good backup |
| Alchemist | Enterprise B2B | Strong - CMMS angle |
| HAX | Hardware + AI | Good - Pi/BeagleBone angle |
| Antler | AI-first companies | Strong fit |

---

## Application Package Components

### 1. Master Narrative (All Platforms)

**The Problem (30 seconds)**
Industrial maintenance is broken. $222B/year lost to unplanned downtime. Maintenance techs work with paper manuals and tribal knowledge. When equipment fails, they're Googling solutions on their phones.

**The Solution (30 seconds)**
FactoryLM: Take a photo of any equipment, get instant AI identification, troubleshooting guidance, and CMMS entry creation. Voice-guided, hands-free, works from any phone.

**The Moat (30 seconds)**
Every photo trains our industrial equipment LLM. Free users aren't freeloaders - they're contributors. We're building the maintenance knowledge base for the world.

**The Team (30 seconds)**
Mike Harp: 15 years industrial maintenance experience. Built this entire platform in 4 months using AI agents as his engineering team. That's not a limitation - it's proof of concept.

**The Ask**
Funding to scale user acquisition and build the specialized industrial LLM.

---

### 2. Demo Video Script (60 seconds)

```
[0:00-0:10] HOOK
"What if any maintenance tech could identify any equipment instantly?"
[Show phone camera pointed at motor]

[0:10-0:25] THE MAGIC
Phone captures photo → AI processes → Voice speaks: "This is a Baldor 5HP motor..."
[Screen shows equipment card appearing]

[0:25-0:40] THE SYSTEM
"Every photo builds our knowledge base. Every user makes the AI smarter."
[Quick cuts: Telegram bot, CMMS entry, PLC dashboard]

[0:40-0:55] THE VISION
"We're building the maintenance LLM for the world. Starting with photos."
[Show map of users worldwide]

[0:55-0:60] CTA
"FactoryLM. Industrial AI that works."
[Logo + URL]
```

---

### 3. Metrics Sheet

| Metric | Value | Notes |
|--------|-------|-------|
| Development Time | 4 months | Solo founder with AI agents |
| Lines of Code | ~50,000+ | Across all services |
| Tech Stack | FastAPI, React, Gemini, Telegram | Production-ready |
| Cost to Build | ~$500 | API costs only |
| Current Users | TBD | Need beta launch |
| Target Market | $8B CMMS market | Growing 10%/year |

---

### 4. Founder Bio

**Mike Harp**
- 15 years industrial maintenance experience
- PLC programming, CMMS implementation, team leadership
- Built FactoryLM entirely using AI agents (Jarvis/Claude)
- Domain expert turned tech founder

*"I've spent 15 years being the guy who gets called at 2am when the line goes down. I built FactoryLM because I know exactly what maintenance techs need - and it's not another enterprise software suite."*

---

### 5. Technical Architecture (One-Pager)

```
┌─────────────────────────────────────────────────┐
│                  USER LAYER                      │
│   Phone Camera → Telegram Bot → Web App          │
└─────────────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────┐
│                  AI LAYER                        │
│   LLM Cascade: DeepSeek → Gemini → Claude       │
│   Quality Judge: Auto-escalation                 │
│   Voice: ElevenLabs TTS                         │
└─────────────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────┐
│               INTEGRATION LAYER                  │
│   CMMS API → PLC Control → Alert Routing        │
└─────────────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────┐
│                 DATA LAYER                       │
│   Equipment Photos → Training Data → LLM        │
│   (The flywheel)                                │
└─────────────────────────────────────────────────┘
```

---

## Platform-Specific Formatting

### Y Combinator
- Application form (text fields)
- 1-minute video (required)
- Founder video (talking to camera)
- Metrics: revenue, users, growth rate

### Techstars
- Longer application (5-10 pages)
- Team focus
- Market analysis required
- Mentor fit important

### 500 Global
- Pitch deck (10-15 slides)
- Demo video
- Traction metrics emphasized
- Global market potential

---

## Wellfound (AngelList) Profile

**Company Name:** FactoryLM
**Tagline:** Industrial AI for maintenance teams
**Stage:** Pre-seed
**Industry:** Industrial Tech, AI/ML, SaaS
**Location:** Atlanta, GA (remote-first)

**Description:**
FactoryLM turns any smartphone into an industrial AI assistant. Maintenance techs take a photo of equipment, get instant identification, troubleshooting guidance, and CMMS integration. Built by a 15-year maintenance veteran using AI agents. Every user makes the system smarter.

**What We're Looking For:**
- Pre-seed funding ($500k-$1M)
- Industrial tech advisors
- Beta users at manufacturing facilities

---

## Next Steps

1. [ ] Finalize demo video script
2. [ ] Record demo footage (PLC + simulation)
3. [ ] Create Wellfound profile
4. [ ] Submit YC application
5. [ ] Submit Techstars application
6. [ ] Submit 500 Global application
7. [ ] Draft pitch deck for backup accelerators
