# 48-Hour Sales Automation Sprint

*Started: 2026-01-30*
*Target: Fully automated lead → email → demo pipeline*

---

## Progress Tracker

### ✅ Hour 0-4: VPS setup + Docker (DONE)
- [x] VPS already running (Hostinger)
- [x] Docker installed
- [x] Mautic deployed (port 8081)
- [x] n8n deployed (port 5678)
- [x] MariaDB deployed

### 🔄 Hour 4-8: n8n + First Workflow (IN PROGRESS)
- [ ] Build: "Manual webhook → Create Mautic contact" workflow
- [ ] Test end-to-end
- [ ] Configure Mautic SMTP (SendGrid)

### ⏳ Hour 8-16: Lead Enrichment Pipeline
- [ ] Google Sheet with 10 test leads
- [ ] n8n: Sheet trigger → Hunter.io email lookup → Mautic contact
- [ ] Verify all 10 leads appear in Mautic

### ⏳ Hour 16-24: AI Personalization
- [ ] Add n8n HTTP node → Claude API
- [ ] Generate personalized email subject + body for each lead
- [ ] Store in Mautic custom fields

### ⏳ Hour 24-36: First Campaign
- [ ] Create 3-email sequence in Mautic (Day 0, Day 2, Day 5)
- [ ] Use Claude-generated content from pipeline
- [ ] Trigger campaign for test leads

### ⏳ Hour 36-48: Notifications + Monitoring
- [ ] n8n: Mautic email opened → Telegram alert
- [ ] n8n: Reply detected → Parse with Claude → Alert Mike

---

## Access URLs

| Service | URL | Credentials |
|---------|-----|-------------|
| n8n | http://72.60.175.144:5678 | admin / factorylm2026 |
| Mautic | http://72.60.175.144:8081 | (complete setup wizard) |

---

## Key Repos to Study

| Purpose | Repo |
|---------|------|
| AI sales agent | filip-michalsky/SalesGPT |
| Cold email automation | PaulleDemon/Email-automation |
| Multi-agent patterns | Abdulbasit110/Blog-writer-multi-agent |
| n8n cold outreach | n8n.io/workflows/6089 |
| Lead qualification | n8n.io/workflows/6649 |

---

## Claude Prompts (Ready to Use)

### Cold Email Generator
```
Write a cold outreach email to {lead_name} at {company_name} in {industry}.
Known pain points: {pain_points}.
Our product: AI-powered maintenance training platform (FactoryLM).

Requirements:
- 120 words max
- Conversational, non-salesy tone
- Specific observation about their industry/company in first line
- One clear pain point addressed
- CTA: "Would a 10-minute demo be helpful?"

Output JSON: {subject: string, body: string}
```

### Lead Qualification
```
Score this lead 1-10 for industrial PLC automation training.
Company: {company_name}
Industry: {industry}
Website: {website}

Return JSON: {score: 1-10, reasoning: string, pain_points: []}
```

---

## Cost Estimate

| Component | Cost |
|-----------|------|
| VPS (Hostinger) | Already paid |
| SMTP (SendGrid) | Free tier (100/day) |
| Claude API | ~$5-15/mo |
| Hunter.io | Free tier (25/mo) |
| **Total** | **~$15-20/mo** |

---

## Next Action
Configure Mautic setup wizard, then build first n8n workflow.
