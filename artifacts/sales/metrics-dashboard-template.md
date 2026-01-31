# FactoryLM — Metrics Dashboard Template

*Task: [V-PLC-9] Track Metrics & Gather Feedback*
*Use: Google Sheets or Notion*

---

## Dashboard Overview

### Key Metrics at a Glance

| Metric | Current | Target | Status |
|--------|---------|--------|--------|
| MRR | $ | $5,000 | 🔴/🟡/🟢 |
| Total Customers | | 5 | 🔴/🟡/🟢 |
| Total Users | | 25 | 🔴/🟡/🟢 |
| Churn Rate | % | <5% | 🔴/🟡/🟢 |
| NPS Score | | >40 | 🔴/🟡/🟢 |
| Diagnosis Accuracy | % | >80% | 🔴/🟡/🟢 |

---

## Pipeline Metrics

### Funnel

| Stage | Count | Conversion |
|-------|-------|------------|
| Prospects | | — |
| Contacted | | % of Prospects |
| Replied | | % of Contacted |
| Demo Booked | | % of Replied |
| Demo Completed | | % of Booked |
| Pilot Started | | % of Completed |
| Paid Customer | | % of Pilot |

### Weekly Activity

| Week | Outreach Sent | Replies | Demos | Pilots | Revenue |
|------|---------------|---------|-------|--------|---------|
| W1 | | | | | $ |
| W2 | | | | | $ |
| W3 | | | | | $ |
| W4 | | | | | $ |

---

## Customer Metrics

### Per Customer

| Customer | Start Date | Users | MRR | Diagnoses Used | Accuracy | NPS | Renewal Date |
|----------|------------|-------|-----|----------------|----------|-----|--------------|
| Company A | 2026-02-01 | 3 | $297 | 45 | 82% | 45 | 2026-03-01 |
| Company B | | | | | | | |
| Company C | | | | | | | |

### Cohort Analysis

| Cohort | Month 1 Retention | Month 2 | Month 3 |
|--------|-------------------|---------|---------|
| Jan 2026 | % | % | % |
| Feb 2026 | | | |

---

## Product Metrics

### Usage

| Metric | Daily | Weekly | Monthly |
|--------|-------|--------|---------|
| Total Diagnoses | | | |
| Active Users | | | |
| Avg Diagnoses/User | | | |

### Accuracy

| PLC Brand | Diagnoses | Correct | Accuracy |
|-----------|-----------|---------|----------|
| Siemens | | | % |
| Allen-Bradley | | | % |
| ABB | | | % |
| Schneider | | | % |
| Other | | | % |
| **Total** | | | **%** |

### Response Time

| Percentile | Time (seconds) |
|------------|----------------|
| P50 (Median) | |
| P90 | |
| P99 | |

---

## Financial Metrics

### Revenue

| Month | MRR Start | New MRR | Churned MRR | MRR End | MoM Growth |
|-------|-----------|---------|-------------|---------|------------|
| Jan | $0 | | | | |
| Feb | | | | | % |
| Mar | | | | | % |

### Unit Economics

| Metric | Value | Target |
|--------|-------|--------|
| CAC (Customer Acquisition Cost) | $ | <$1,000 |
| LTV (Lifetime Value) | $ | >$3,000 |
| LTV:CAC Ratio | | >3:1 |
| Payback Period | months | <6 months |

### Expenses

| Category | Monthly | Notes |
|----------|---------|-------|
| Marketing | $ | Ads, tools |
| Tools | $ | Lemlist, Sales Nav |
| Infrastructure | $ | VPS, APIs |
| Other | $ | |
| **Total Burn** | $ | |

---

## Marketing Metrics

### By Channel

| Channel | Spend | Leads | Customers | CAC | ROI |
|---------|-------|-------|-----------|-----|-----|
| LinkedIn | $ | | | $ | % |
| Cold Email | $ | | | $ | % |
| Reddit | $ | | | $ | % |
| YouTube | $ | | | $ | % |
| Referral | $0 | | | $0 | ∞ |

### Content Performance

| Content | Views | Clicks | Conversions |
|---------|-------|--------|-------------|
| Landing Page | | | |
| Blog Post 1 | | | |
| YouTube Video 1 | | | |

---

## Weekly Review Template

### What Went Well
- 

### What Didn't Work
- 

### Key Learnings
- 

### Next Week Priorities
1. 
2. 
3. 

---

## Monthly Review Template

### Summary
- MRR: $ → $
- Customers: → 
- Key Win:
- Biggest Challenge:

### Metrics Analysis
- Best performing channel:
- Worst performing channel:
- Accuracy trend:
- Churn risk customers:

### Action Items
1. 
2. 
3. 

---

## Google Sheets Setup

### Tabs to Create
1. **Dashboard** — Summary view with charts
2. **Prospects** — CRM tracking
3. **Customers** — Active customer details
4. **Usage** — Product usage data
5. **Revenue** — Financial tracking
6. **Weekly** — Weekly review notes

### Formulas

**MRR Calculation:**
```
=SUMIF(Customers!Status, "Active", Customers!MRR)
```

**Conversion Rate:**
```
=Demos/Contacted
```

**Churn Rate:**
```
=Churned Customers / Start of Month Customers
```

**LTV:**
```
=ARPU / Monthly Churn Rate
```

---

*Template ready. Create in Google Sheets and update weekly.*
