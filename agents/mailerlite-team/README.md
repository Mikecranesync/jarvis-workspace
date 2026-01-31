# MailerLite Agent Team

**Purpose:** Autonomous email marketing management for FactoryLM

---

## Team Structure

```
┌─────────────────────────────────────────────────────────┐
│                    JARVIS (Orchestrator)                │
│           Receives requests, delegates to team          │
└───────────────┬─────────────┬─────────────┬─────────────┘
                │             │             │
        ┌───────▼───────┐ ┌───▼───┐ ┌───────▼───────┐
        │   STRATEGIST  │ │ WRITER │ │   MANAGER    │
        │  Ideas/Plans  │ │ Content│ │  Ops/Stats   │
        └───────────────┘ └────────┘ └───────────────┘
```

---

## Agents

### 1. Content Strategist (`strategist`)
- Researches industry trends
- Plans content calendar
- Generates campaign ideas
- A/B test strategies
- Audience segmentation ideas

### 2. Copywriter (`writer`)
- Writes email copy
- Creates subject lines
- Drafts welcome sequences
- Product announcements
- Newsletter content

### 3. Campaign Manager (`manager`)
- Schedules campaigns
- Monitors analytics
- Manages subscriber lists
- Reports on performance
- Handles automations

---

## Trigger Commands

From main chat, say:
- **"Email team: plan next month's campaigns"**
- **"Email team: write welcome sequence"**
- **"Email team: check this week's stats"**
- **"Email team: create product launch campaign"**

---

## Automated Tasks (Cron)

| Task | Schedule | Agent |
|------|----------|-------|
| Weekly content ideas | Monday 9am | Strategist |
| Performance report | Friday 5pm | Manager |
| List health check | 1st of month | Manager |

---

## Files

- `strategist.md` — Strategist agent prompt
- `writer.md` — Writer agent prompt  
- `manager.md` — Manager agent prompt
- `templates/` — Email templates
- `campaigns/` — Campaign drafts
- `reports/` — Performance reports
