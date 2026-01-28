# FactoryLM Strategy — January 2026

## The Stack

| Layer | Solution | Cost |
|-------|----------|------|
| 🥽 Hardware | Brilliant Frame glasses | $349/unit |
| 🤖 AI | Claude multimodal (OCR, troubleshooting) | API costs |
| 📊 Interface | Google Sheets + Claude formulas | ~$20/mo |
| 🔧 CMMS | Atlas CMMS (self-hosted) | Free |
| 🌍 Support | Global expert network | $100/hr (36% margin) |

---

## Phase 1: Claude + Sheets MVP (NOW)

Skip frontend entirely. Use spreadsheets as the interface.

```
Column A: Equipment ID
Column B: Equipment Name  
Column C: Current Temperature
Column D: Pressure (PSI)
Column E: Last Maintenance (days ago)
Column F: =CLAUDE("diagnose based on temp, pressure, maintenance history")
Column G: =CLAUDE("what should we do about status in column F?")
Column H: =CLAUDE("estimate repair cost")
Column I: =CLAUDE("create work order based on recommendation")
```

Flow:
1. Zapier syncs equipment data → Google Sheet every 15 min
2. Claude formulas auto-execute on all rows
3. Results sync back → Atlas creates work orders
4. Technicians see everything on mobile

**Time to build: 2 hours**

---

## Phase 2: AR Glasses Integration (Weeks 1-8)

### Hardware
- Brilliant Frame glasses ($349)
- 2 pairs ordered for dev/pilot ($698 total)
- Arrives: Early March (4-6 weeks from Jan 28)

### Development (While Waiting)
- Clone Frame SDK GitHub
- Build mock version with Telegram bot + Claude backend
- Polish existing backend (20% remaining)
- By glasses arrival = working code ready

### Distributor Partnership
- Email hello@brilliant.xyz
- Subject: "FactoryLM AR Platform - Distributor Interest"
- Goal: 20-30% discount to resell

---

## Phase 3: Global Expert Network

### Model
- Customer pays: $100/hour
- Expert gets: $64/hour (64%)
- FactoryLM keeps: $36/hour (36%)
- Expert earns: 8-16x local wage (ethical positioning)

### Recruitment Priority
1. Philippines (best English, PLC skills)
2. India
3. Eastern Europe
4. Latin America

### Target
- 5 experts by end of Week 3
- 100+ experts by end of Q2

---

## Phase 4: Pilot & Launch

### Pilot Customer (Weeks 5-8)
- Use friendly contractor contact
- Deploy 2-3 Frame glasses
- Test "puppet master" remote support workflow
- Record video proof of concept

### Market Launch (Month 3)
- Free tier + $99/month Pro tier
- Support: $100/hour with global experts
- Target: 5-10 pilot customers by end of Q1

---

## Competitive Advantages

1. **Hardware arbitrage**: $349 vs $3-4K competitors
2. **Talent arbitrage**: $64/hour for world-class experts
3. **Speed**: 90 days to MVP vs 18+ months competitors
4. **Open platform**: Attract developers, build moat early
5. **Domain focus**: Industrial/HVAC, not generic enterprise
6. **Ethical narrative**: Paying global talent 10x market rate

---

## The Moat (KEEP SECRET)

**Proprietary (don't open source):**
- Diagnostic prompts
- Equipment knowledge base
- Cost models
- PLC integration code
- Torque stripe algorithm

**Use open source:**
- Atlas CMMS (foundation)
- Google Sheets (interface)
- Claude API (intelligence)
- Frame SDK (hardware)

**Value = integration layer + domain expertise**

---

## Pricing

| Tier | Price | Includes |
|------|-------|----------|
| Free | $0 | Basic diagnostics, 50 queries/mo |
| Pro | $99/mo | Unlimited diagnostics, CMMS sync |
| Enterprise | Custom | AR glasses, expert support, SLA |
| Expert Support | $100/hr | Live remote troubleshooting |

**Your margin on sheets MVP: 80%+ ($75-150/mo profit per customer)**

---

## Market Size

- Target: Developing world SMBs first, then US, then enterprise
- Opportunity: $500M+ if executed right

---

## 48-Hour Checklist

- [ ] Order 2x Frame glasses ($698) — https://brilliant.xyz/products/frame
- [ ] Join Brilliant Labs Discord
- [ ] Clone frame-codebase GitHub
- [ ] Email hello@brilliant.xyz (distributor inquiry)
- [ ] Identify 5 warm leads (contractors you know)
- [ ] Post job ad for 5 Philippines PLC technicians
- [ ] Start building mock Frame integration
- [ ] Document vision (1-page pitch)
- [ ] Build Google Sheets MVP (2 hours)

---

*Last updated: 2026-01-28*
