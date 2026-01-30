# FactoryLM — ROI Calculator

*Use: Discovery calls and proposals*

---

## Quick ROI Calculator

### Input Variables

| Variable | Your Value | Default |
|----------|------------|---------|
| **A.** Downtime cost per hour | $ | $500 |
| **B.** Average diagnostic time (hours) | | 2.5 |
| **C.** Diagnostic incidents per month | | 8 |
| **D.** Number of technicians | | 4 |
| **E.** FactoryLM price/user/month | $99 | $99 |

### Calculations

**Current Monthly Diagnostic Cost:**
```
= A × B × C
= $500 × 2.5 × 8
= $10,000/month
```

**With FactoryLM (70% time reduction):**
```
= A × (B × 0.30) × C
= $500 × 0.75 × 8
= $3,000/month
```

**Monthly Savings:**
```
= Current - With FactoryLM
= $10,000 - $3,000
= $7,000/month
```

**FactoryLM Cost:**
```
= D × E
= 4 × $99
= $396/month
```

**Net Monthly Savings:**
```
= Monthly Savings - FactoryLM Cost
= $7,000 - $396
= $6,604/month
```

**ROI:**
```
= (Net Savings / Cost) × 100
= ($6,604 / $396) × 100
= 1,667% ROI
```

---

## Discovery Questions to Get Numbers

### Downtime Cost
```
"Roughly, what does an hour of unplanned downtime cost your operation?
Think about lost production, labor, expedited shipping..."
```

**If they don't know:** Use $500/hour as conservative estimate

### Diagnostic Time
```
"When a tech hits an unfamiliar fault code, how long does it typically 
take to diagnose? From 'I see an error' to 'I know what to do'?"
```

**If they don't know:** Use 2-3 hours average

### Frequency
```
"How often does that happen? Roughly how many times per month does 
someone get stuck on diagnostic issues?"
```

**If they don't know:** Estimate based on team size:
- 1-2 techs: 4-6/month
- 3-5 techs: 8-12/month
- 6-10 techs: 15-20/month

---

## ROI Scenarios

### Conservative Estimate
| Input | Value |
|-------|-------|
| Downtime cost | $300/hour |
| Diagnostic time | 2 hours |
| Incidents/month | 4 |
| Technicians | 3 |

**Result:** $492 savings/month, 165% ROI

### Moderate Estimate
| Input | Value |
|-------|-------|
| Downtime cost | $500/hour |
| Diagnostic time | 2.5 hours |
| Incidents/month | 8 |
| Technicians | 4 |

**Result:** $6,604 savings/month, 1,667% ROI

### Aggressive Estimate
| Input | Value |
|-------|-------|
| Downtime cost | $1,000/hour |
| Diagnostic time | 3 hours |
| Incidents/month | 12 |
| Technicians | 6 |

**Result:** $24,606 savings/month, 4,142% ROI

---

## Presenting ROI

### The Formula (Simple)
```
"Based on what you told me:
- $[X] per hour of downtime
- [Y] hours average diagnostic time
- [Z] incidents per month

That's $[total] in diagnostic-related downtime every month.

FactoryLM cuts that diagnostic time by 70% on average. 
That's $[savings] back in your pocket.

At $99 per user for [N] techs, you're paying $[cost] to save $[savings].

Does that math make sense?"
```

### The Story (Emotional)
```
"Imagine: Next time a tech is standing in front of a downed machine 
with an error code they don't recognize...

Instead of spending 2-3 hours digging through manuals, calling vendors, 
or waiting for someone who knows...

They snap a photo, and 60 seconds later they know exactly what to do.

That's not just saving money. That's reducing stress for your team 
and getting production back faster."
```

---

## ROI in Proposals

### Sample Proposal Section

**Investment:**
- FactoryLM Professional: $99/user/month
- 4 technicians: $396/month
- Annual: $4,752

**Expected Return:**
- Current diagnostic cost: $10,000/month
- With FactoryLM: $3,000/month
- Monthly savings: $7,000
- Annual savings: $84,000

**ROI Summary:**
- Payback period: < 1 month
- First year net savings: $79,248
- ROI: 1,667%

---

## Common Pushback

### "Those numbers seem high"
```
"Let's use your numbers. What would you estimate for downtime cost 
and diagnostic frequency? [Recalculate with their inputs]"
```

### "We don't track diagnostic time"
```
"That's common. Here's a quick way to estimate: How many times in 
the past month did a tech get stuck on something they needed help with?

Even if it's just 4 incidents at $500/hour, that's $5,000 in opportunity."
```

### "Not all downtime is diagnostic delays"
```
"Absolutely right. FactoryLM only addresses the diagnostic portion — 
the time from 'I see an error' to 'I know what to do.'

But that's often 30-50% of the total repair time. Even a partial 
improvement adds up fast."
```

---

*Use in discovery calls and proposals to quantify value.*
