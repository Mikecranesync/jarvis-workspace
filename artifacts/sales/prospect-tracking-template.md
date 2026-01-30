# FactoryLM — Prospect Tracking Template

*Task: [V-PLC-3] Set Up Tracking & CRM*
*Use: Google Sheets or copy to your CRM*

---

## Spreadsheet Structure

### Sheet 1: Prospects

| Column | Description | Example |
|--------|-------------|---------|
| **A: Date Added** | When prospect entered pipeline | 2026-01-30 |
| **B: Company** | Company name | Correct Craft |
| **C: Contact Name** | Decision maker | John Smith |
| **D: Title** | Job title | Maintenance Manager |
| **E: Email** | Contact email | john@correctcraft.com |
| **F: LinkedIn** | Profile URL | linkedin.com/in/johnsmith |
| **G: Phone** | If available | 407-555-1234 |
| **H: Source** | How we found them | LinkedIn Search |
| **I: Status** | Pipeline stage | Lead/Contacted/Demo/Pilot/Customer |
| **J: Last Contact** | Date of last touch | 2026-01-30 |
| **K: Next Action** | What to do next | Follow-up DM |
| **L: Next Action Date** | When to do it | 2026-02-02 |
| **M: Notes** | Conversation details | Interested, asked about Siemens support |
| **N: Deal Value** | Potential MRR | $297 (3 users × $99) |

### Sheet 2: Activity Log

| Column | Description |
|--------|-------------|
| **A: Date** | Activity date |
| **B: Company** | Company name |
| **C: Activity Type** | Email/Call/Demo/Follow-up |
| **D: Notes** | What happened |
| **E: Outcome** | Result (Positive/Neutral/Negative) |
| **F: Next Step** | What's next |

### Sheet 3: Metrics Dashboard

| Metric | Formula | Target |
|--------|---------|--------|
| Total Prospects | COUNT(Prospects!A:A) | 100+ |
| Contacted | COUNTIF(Status, "Contacted") | 50+ |
| Demos Booked | COUNTIF(Status, "Demo") | 15-20 |
| Pilots | COUNTIF(Status, "Pilot") | 3-5 |
| Customers | COUNTIF(Status, "Customer") | 3-5 |
| Conversion Rate | Customers/Contacted | >5% |

---

## Pipeline Stages

| Stage | Definition | Action |
|-------|------------|--------|
| **Lead** | Identified, not contacted | Research + first outreach |
| **Contacted** | First message sent | Wait 3 days, then follow up |
| **Replied** | They responded | Book demo call |
| **Demo** | Demo scheduled or completed | Present FactoryLM |
| **Pilot** | Signed up for trial | Onboard + weekly check-ins |
| **Customer** | Paying | Retain + upsell |
| **Lost** | Said no or ghosted | Note reason, move on |

---

## Google Sheets Setup

1. Create new Google Sheet
2. Name it "FactoryLM Prospects"
3. Create 3 tabs: Prospects, Activity Log, Dashboard
4. Copy column headers from above
5. Add data validation for Status column
6. Set up conditional formatting (green = Customer, red = Lost)
7. Share with Mike only (keep private)

---

## Daily Workflow

**Morning (10 min):**
1. Check "Next Action Date" for today's tasks
2. Prioritize follow-ups

**During Outreach:**
1. Log every contact in Activity Log
2. Update Status immediately
3. Set Next Action and Date

**End of Day (5 min):**
1. Review metrics dashboard
2. Plan tomorrow's actions

---

*Template ready. Create Google Sheet and start tracking.*
