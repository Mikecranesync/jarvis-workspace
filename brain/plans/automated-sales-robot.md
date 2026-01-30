# 🤖 Automated Sales Robot — 24/7 Outreach System

*Created: 2026-01-30*
*Status: PLAN - Ready to Build*

## Mission
Build a fully automated sales outreach system that runs 24/7 without Mike touching it. No phone calls, no manual emails. Just leads in → demos booked out.

---

## Core Stack (All Open Source)

### 1. n8n — The Brain (Orchestration)
**What:** Open source Zapier/Make alternative
**Why:** Connects everything, triggers workflows, handles scheduling
**Deploy:** Self-hosted on VPS (already have infrastructure)

Key workflows:
- Lead capture → enrichment → AI qualification → outreach
- LinkedIn scrape → Claude research → personalized email → send
- Reply detection → AI response → CRM update

### 2. Mautic — Email Automation
**What:** Open source marketing automation (email sequences, lead scoring)
**Why:** Professional email delivery, drip campaigns, tracking
**Deploy:** Docker on VPS

Features we need:
- Multi-step email sequences
- Lead scoring based on engagement
- Webhook triggers to n8n
- Open/click tracking

### 3. SalesGPT — AI Sales Agent
**Repo:** github.com/filip-michalsky/SalesGPT
**What:** Context-aware AI sales agent built on LangChain
**Why:** Handles actual sales conversations (email replies, objections)
**Deploy:** Python/FastAPI on VPS

Key features:
- Multi-stage conversation flow
- Product knowledge base integration
- Works with Claude/Anthropic (via LiteLLM)
- Can handle email, SMS, WhatsApp

### 4. Lead Sources (Inputs)
- **LinkedIn Sales Navigator** — Scrape via n8n + Apify/PhantomBuster
- **Apollo.io Free Tier** — 1,200 leads/year free
- **Website form submissions** — Webhook to n8n
- **Cold list uploads** — CSV → Mautic

### 5. Claude CLI / Clawdbot — Intelligence Layer
- Personalize emails based on lead research
- Qualify leads based on criteria
- Generate responses to inquiries
- Monitor and report on performance

---

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    LEAD SOURCES (24/7)                       │
├─────────────────────────────────────────────────────────────┤
│  LinkedIn Scraper │ Apollo Free │ Website Forms │ CSV Upload │
└────────────┬──────┴──────┬──────┴───────┬───────┴─────┬──────┘
             │             │              │             │
             ▼             ▼              ▼             ▼
┌─────────────────────────────────────────────────────────────┐
│                      n8n (ORCHESTRATION)                     │
│  • Lead enrichment     • Qualification scoring               │
│  • Claude AI research  • Workflow triggers                   │
│  • CRM sync           • Reply routing                        │
└────────────┬────────────────────────────────────┬────────────┘
             │                                    │
             ▼                                    ▼
┌──────────────────────────┐    ┌──────────────────────────────┐
│       MAUTIC             │    │        SalesGPT              │
│  • Email sequences       │    │  • AI conversations          │
│  • Lead scoring          │    │  • Objection handling        │
│  • Drip campaigns        │    │  • Demo booking              │
│  • Tracking/analytics    │    │  • Multi-channel (email/SMS) │
└────────────┬─────────────┘    └──────────────┬───────────────┘
             │                                  │
             ▼                                  ▼
┌─────────────────────────────────────────────────────────────┐
│                    OUTPUTS (Automated)                       │
├─────────────────────────────────────────────────────────────┤
│  Personalized Emails │ Follow-ups │ Demo Bookings │ Reports  │
└─────────────────────────────────────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────────────────────────┐
│                 JARVIS (Monitoring + Reports)                │
│  • Daily summary to Telegram                                 │
│  • Alert on hot leads                                        │
│  • Weekly performance reports                                │
└─────────────────────────────────────────────────────────────┘
```

---

## Implementation Phases

### Phase 1: Foundation (Week 1)
- [ ] Install n8n on VPS (Docker)
- [ ] Install Mautic on VPS (Docker)
- [ ] Configure SMTP (SendGrid already available)
- [ ] Set up basic lead import workflow
- [ ] Create initial email sequence (3-email drip)

### Phase 2: AI Integration (Week 2)
- [ ] Deploy SalesGPT or custom Claude-based agent
- [ ] Build email personalization workflow
- [ ] Set up reply detection and routing
- [ ] Test with 10-20 manual leads

### Phase 3: Lead Generation (Week 3)
- [ ] Set up LinkedIn scraping (n8n + Apify)
- [ ] Configure Apollo.io free tier
- [ ] Build lead qualification scoring
- [ ] Connect to Calendly for auto-booking

### Phase 4: Scale (Week 4+)
- [ ] A/B test email sequences
- [ ] Optimize based on reply rates
- [ ] Add SMS/WhatsApp channels
- [ ] Build reporting dashboard

---

## Tools to Install

```bash
# n8n (self-hosted)
docker run -d --name n8n \
  -p 5678:5678 \
  -v n8n_data:/home/node/.n8n \
  n8nio/n8n

# Mautic
docker run -d --name mautic \
  -p 8080:80 \
  -v mautic_data:/var/www/html \
  mautic/mautic

# SalesGPT
git clone https://github.com/filip-michalsky/SalesGPT
cd SalesGPT
pip install salesgpt
```

---

## Email Sequence (Initial)

### Email 1: Intro (Day 0)
Subject: Quick question about [COMPANY] maintenance
Body: Personalized based on AI research. Pain point + curiosity hook.

### Email 2: Value (Day 3)
Subject: Re: [COMPANY] maintenance
Body: Share blog post or case study. Soft CTA.

### Email 3: Direct Ask (Day 7)
Subject: 15 min call?
Body: Direct ask for demo. Calendly link.

### Email 4: Breakup (Day 14)
Subject: Closing the loop
Body: Last attempt. Create urgency.

---

## Success Metrics
- **Leads processed/day:** Target 50+
- **Email open rate:** Target 40%+
- **Reply rate:** Target 5%+
- **Demos booked/week:** Target 5+
- **Cost:** $0 (all open source, self-hosted)

---

## Claude CLI Prompts (Ready to Use)

### Lead Enrichment Prompt
```
You are a B2B sales researcher for industrial automation products.
Given a lead: {company_name}, {industry}, {website}

1. Research company (use web search if needed)
2. Identify 3 pain points related to {our product}
3. Draft personalized email (150 words):
   - Hook: specific pain point observation
   - Value: how we solve it
   - CTA: 15-min demo link
4. Output JSON: {subject, body, pain_points[]}
```

### Reply Classification Prompt
```
Classify this email reply: {reply_text}
Categories: interested, not_interested, question, meeting_request
Return JSON: {category, confidence, suggested_action}
```

---

## Next Steps
1. ✅ Spin up n8n container
2. ✅ Spin up Mautic container  
3. Connect to existing SendGrid
4. Import initial lead list
5. Launch first email sequence

**STATUS: BUILDING NOW**
