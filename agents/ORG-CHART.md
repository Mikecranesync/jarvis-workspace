# FactoryLM Business Army - Organizational Structure

*Last Updated: 2026-02-05*

## Executive Leadership

### CEO: Mike Harpool
- Final decision authority
- Strategic direction
- External representation

### Chief of Staff: Jarvis (Main Agent)
- Orchestrates all agent activities
- Direct line to Mike
- Escalation point for all divisions

---

## Division Structure

### 🌐 WEBSITE DIVISION (NEW)
**Mission:** Rapidly build Apple-quality website for FactoryLM three-tier products

| Role | Agent | Frequency | Status |
|------|-------|-----------|--------|
| **Web Director** | Web Director | 1 hr | ✅ Active |
| **UI Designer** | UI Designer | On-demand | ✅ Defined |
| **Frontend Dev** | Frontend Developer | On-demand | ✅ Defined |
| **Copywriter** | Copywriter | On-demand | ✅ Defined |
| **QA** | QA Agent | On-demand | ✅ Defined |

**Sprint Plan:** 7 days to production website
- Day 1-2: Landing page
- Day 3: Identify page
- Day 4: Connect page
- Day 5: Predict page
- Day 6-7: Polish & Launch

---

### 🔬 RESEARCH DIVISION
**Mission:** Deep technical research to make FactoryLM the most informed industrial AI company

| Role | Agent | Frequency | Status |
|------|-------|-----------|--------|
| **IIoT Research Director** | IIoT Research | Daily | ✅ Active |
| **Protocol Specialist** | *Planned* | - | ⏳ |
| **Edge AI Researcher** | *Planned* | - | ⏳ |
| **Competitive Intel** | *Planned* | - | ⏳ |

**Current Research Queue:**
1. IO-Link protocol deep dive
2. OPC-UA Pub/Sub architecture
3. TinyML deployment options
4. Allen-Bradley AOI development
5. Industrial network security

---

### 🏭 OPERATIONS DIVISION
**Mission:** Keep infrastructure running

| Role | Agent | Frequency | Status |
|------|-------|-----------|--------|
| **Ops Director** | Monitor Agent | 15 min | ✅ Active |
| **SRE Lead** | Robot Army Status | 30 min | ✅ Active |
| **Auto-Remediation** | Auto-Fix Agent | 30 min | ✅ Active |

**Responsibilities:**
- System health monitoring
- Docker container health
- Service uptime
- Autonomous issue resolution

---

### 💻 ENGINEERING DIVISION
**Mission:** Build and maintain code

| Role | Agent | Frequency | Status |
|------|-------|-----------|--------|
| **Engineering Director** | Code Agent | 30 min | ✅ Active |
| **QA Lead** | PLC-Copilot Tester | 2 hr | ✅ Active |
| **Compliance Officer** | Compliance Agent | 6 hr | ✅ Active |

**Responsibilities:**
- GitHub issue triage
- PR creation and review
- Test automation
- Engineering standards enforcement

---

### 📊 KNOWLEDGE DIVISION
**Mission:** Capture, organize, remember everything

| Role | Agent | Frequency | Status |
|------|-------|-----------|--------|
| **Knowledge Director** | Knowledge Director | 6 hr | ✅ Active |
| **Archivist** | Telegram Ingestion | 5 min | ✅ Near-realtime |
| **Timeline Curator** | Timeline Aggregator | 1 hr | ✅ Active |
| **Researcher** | Research Agent | 4 hr | ✅ Active |

**Responsibilities:**
- Message archival (Telegram, email, etc.)
- Knowledge base maintenance
- Fact extraction and storage
- Research and intelligence

**GAP:** No real-time webhook ingestion. Currently batch cron.

---

### 📣 MARKETING DIVISION
**Mission:** Build audience and brand

| Role | Agent | Frequency | Status |
|------|-------|-----------|--------|
| **Marketing Director** | Marketing Director | Mon/Fri 2 PM | ✅ Active |
| **Email Manager** | MailerLite Manager | Weekly | ✅ Active |
| **Email Strategist** | MailerLite Strategist | Weekly | ✅ Active |
| **Content Lead** | LinkedIn Prep | Weekly | ✅ Active |

**Responsibilities:**
- Email campaigns
- Social media content
- Brand building
- Audience growth

---

### 📋 PROJECT MANAGEMENT DIVISION
**Mission:** Keep work organized and moving

| Role | Agent | Frequency | Status |
|------|-------|-----------|--------|
| **PM Director** | PM Director | Daily 2 PM | ✅ Active |
| **Scrum Master** | Agile Check | 5 min | ✅ Active |
| **Standup Lead** | Daily Standup | Daily | ✅ Active |
| **Stale Hunter** | Stale Task Check | Daily | ✅ Active |

**Responsibilities:**
- Trello board management
- Task prioritization
- Blockers identification
- Progress reporting

---

## GAPS & REMAINING NEEDS

### ✅ Recently Filled:

1. **Knowledge Director** - ✅ ACTIVE (6 hr audits)
2. **Marketing Director** - ✅ ACTIVE (Mon/Fri 2 PM)
3. **PM Director** - ✅ ACTIVE (Daily 2 PM)
4. **Near-Realtime Archival** - ✅ ACTIVE (5 min intervals)

### Infrastructure Still Needed:

1. **Agent Communication Bus** - Agents talk to each other
   - Pass tasks between divisions
   - Escalation paths

2. **Metrics Dashboard** - See army performance
   - Jobs run/failed
   - Issues fixed
   - Content produced

3. **True Webhook** - Instant message capture
   - Currently 5-min polling (good enough for now)
   - True webhook would be instant

---

## Reporting Structure

```
                    MIKE (CEO)
                        │
                    JARVIS (CoS)
                        │
        ┌───────┬───────┼───────┬───────┐
        │       │       │       │       │
      OPS    ENG    KNOWLEDGE  MKTG    PM
        │       │       │       │       │
    Monitor  Code   Archivist Email  Scrum
    SRE      QA     Timeline  Social Standup
    AutoFix  Comply Research  Content Stale
```

---

## Communication Protocols

- **Escalate to Mike:** Only true blockers, security issues, decisions requiring human judgment
- **Escalate to Jarvis:** Cross-division coordination, priority conflicts, resource needs
- **Division Internal:** Agents handle within their domain autonomously

---

*This org chart is a living document. Update as agents are added/removed.*
