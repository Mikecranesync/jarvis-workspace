# FactoryLM — Product Roadmap 2026

*Living document — Updated 2026-01-30*

---

## Vision

**FactoryLM is the AI brain for industrial maintenance.**

Every maintenance team, from solo contractors to enterprise plants, has instant access to diagnostic intelligence that makes them faster, smarter, and more reliable.

---

## Current State (January 2026)

### What's Built ✅
- **FactoryLM Diagnostics Bot** — Telegram-based photo diagnosis
- **Knowledge Base** — 226 atoms of industrial troubleshooting data
- **Multi-brand support** — Siemens, Allen-Bradley, ABB, Schneider, Mitsubishi
- **CMMS Backend** — Work order management (Java/Spring Boot)

### Key Metrics
- Accuracy: ~80-85%
- Response time: <90 seconds
- Customers: 0 (pre-launch)

---

## Q1 2026: Foundation (Jan-Mar)

### Focus: First Paying Customers

**Goals:**
- 3-5 paying pilot customers
- $1,500+ MRR
- 80%+ pilot retention

**Deliverables:**

| Feature | Priority | Status | Notes |
|---------|----------|--------|-------|
| Landing page | P0 | 🔄 In Progress | Carrd + Calendly |
| Telegram bot polish | P0 | ✅ Done | Error handling, speed |
| Stripe integration | P0 | 🔜 Planned | Payment processing |
| Customer onboarding flow | P1 | ✅ Done | Documented |
| Basic analytics | P1 | 🔜 Planned | Usage tracking |
| Knowledge base expansion | P2 | 🔄 Ongoing | 500+ atoms target |

**What We're NOT Building:**
- Mobile app (Telegram is enough for now)
- Web dashboard (later)
- Integrations (later)

---

## Q2 2026: Product-Market Fit (Apr-Jun)

### Focus: Validate and Scale

**Goals:**
- 15-25 paying customers
- $5,000+ MRR
- <5% monthly churn
- Clear PMF signals

**Deliverables:**

| Feature | Priority | Notes |
|---------|----------|-------|
| Web dashboard | P1 | Usage stats, history |
| Team management | P1 | Add/remove users |
| Custom knowledge base | P1 | Customer-specific data |
| Reporting | P2 | Monthly summaries |
| API (beta) | P2 | For integrations |
| WhatsApp channel | P3 | Alternative to Telegram |

---

## Q3 2026: Expansion (Jul-Sep)

### Focus: Growth Engine

**Goals:**
- 50+ paying customers
- $15,000+ MRR
- Inbound lead flow

**Deliverables:**

| Feature | Priority | Notes |
|---------|----------|-------|
| CMMS integrations | P1 | MaintainX, UpKeep, Fiix |
| Mobile app | P2 | iOS + Android |
| Predictive alerts | P2 | "This error often leads to..." |
| Multi-site support | P2 | Enterprise feature |
| White-label option | P3 | For OEMs |

---

## Q4 2026: Enterprise (Oct-Dec)

### Focus: Larger Customers

**Goals:**
- 100+ paying customers
- $30,000+ MRR
- First enterprise deal ($5K+/month)

**Deliverables:**

| Feature | Priority | Notes |
|---------|----------|-------|
| Enterprise security | P1 | SSO, audit logs |
| Advanced analytics | P1 | Trends, predictions |
| Custom training | P2 | Train on customer data |
| On-premise option | P3 | For regulated industries |
| Partner program | P2 | Reseller enablement |

---

## 2027+ Vision

### The Full FactoryLM Platform

```
                    ┌──────────────────────┐
                    │     FactoryLM        │
                    │    Intelligence      │
                    │        Hub           │
                    └──────────┬───────────┘
                               │
        ┌──────────────────────┼──────────────────────┐
        │                      │                      │
        ▼                      ▼                      ▼
┌───────────────┐    ┌───────────────┐    ┌───────────────┐
│   Diagnostics │    │  Maintenance  │    │   Knowledge   │
│  (Photo → Fix)│    │ (Work Orders) │    │   (Training)  │
└───────────────┘    └───────────────┘    └───────────────┘
        │                      │                      │
        └──────────────────────┼──────────────────────┘
                               │
                    ┌──────────▼───────────┐
                    │     Integrations     │
                    │  (CMMS, ERP, SCADA)  │
                    └──────────────────────┘
```

**Key Capabilities:**
1. **Diagnostics** — Instant troubleshooting via photo/text
2. **Maintenance** — Full CMMS functionality
3. **Knowledge** — Training, documentation, tribal knowledge capture
4. **Intelligence** — Predictive maintenance, trend analysis
5. **Integration** — Connect to existing systems

---

## Feature Prioritization Framework

### P0 (Must Have)
- Required for first customers
- Blocks revenue
- Security/reliability critical

### P1 (Should Have)
- Strongly requested by multiple prospects
- Competitive necessity
- Clear ROI

### P2 (Nice to Have)
- Single customer request
- Future-proofing
- Nice differentiator

### P3 (Later)
- Speculative
- Long-term vision
- Low demand

---

## Technical Debt & Infrastructure

### Q1 Priorities
- [ ] Migrate to Hetzner (more RAM)
- [ ] Set up proper CI/CD
- [ ] Improve error handling
- [ ] Add monitoring/alerting

### Q2 Priorities
- [ ] Scale architecture for 100+ users
- [ ] Implement proper logging
- [ ] Set up staging environment

---

## Competitive Response

### If MaintainX adds photo diagnostics
→ Emphasize PLC-specific accuracy, 20 years domain expertise

### If Fiix gets more aggressive
→ Position as vendor-neutral alternative

### If new AI startup enters
→ First-mover advantage, customer relationships, domain expertise

---

## Success Metrics by Quarter

| Metric | Q1 | Q2 | Q3 | Q4 |
|--------|----|----|----|----|
| Customers | 5 | 25 | 50 | 100 |
| MRR | $1,500 | $5,000 | $15,000 | $30,000 |
| Accuracy | 82% | 85% | 88% | 90% |
| NPS | 40+ | 45+ | 50+ | 55+ |
| Churn | <10% | <8% | <5% | <5% |

---

*Roadmap reviewed monthly. Adjust based on customer feedback.*
