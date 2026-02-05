# FactoryLM Three-Tier Product Plan

*Master Document - Created 2026-02-05*
*For: YC Application, All Accelerators, Go-to-Market Strategy*

---

## Product Overview

FactoryLM is an AI-powered maintenance intelligence platform with three distinct products serving different customer segments and technology levels.

---

## TIER 1: FactoryLM Identify

### Target Customer
- Facilities with legacy equipment (pre-networking era)
- Small/medium manufacturers without IT resources
- Maintenance teams wanting quick wins with zero infrastructure

### Value Proposition
"Take a photo, get answers. No installation, no IT, no hardware."

### Features
- Photo-based equipment identification
- Nameplate OCR and component recognition
- Manufacturer/model lookup
- Common failure modes and troubleshooting steps
- Parts cross-reference
- Maintenance history logging (optional)

### Technical Requirements
- Telegram bot (already built: Rivet-PRO)
- Cloud AI (vision + LLM)
- No customer infrastructure required

### Pricing
- **Free Tier:** 10 queries/month
- **Pro:** $49/month unlimited queries
- **Team:** $99/month, 5 users, shared history

### Development Status
- ✅ Core bot functional (Rivet-PRO)
- ✅ Photo processing pipeline
- ⚠️ Needs: expanded equipment database, improved prompts

---

## TIER 2: FactoryLM Connect

### Target Customer
- Facilities with networked PLCs
- Plants wanting real-time monitoring
- Companies with existing SCADA/MES but poor maintenance tools

### Value Proposition
"See what your PLCs already know. No sensor changes, just software."

### Features
- Everything in Identify, plus:
- PLC auto-discovery on network
- Real-time tag reading (Modbus, Ethernet/IP, PROFINET, OPC-UA)
- Fault code interpretation
- Process value correlation with equipment photos
- Historical trending
- Alert notifications

### Technical Requirements
- Edge agent software (Linux/Windows)
- Protocol libraries (pymodbus, cpppo, python-snap7, opcua)
- Secure tunnel to cloud (HTTPS/WebSocket)
- No PLC programming changes required

### Supported Protocols (Priority Order)
1. Modbus TCP - widest compatibility
2. Ethernet/IP - Allen-Bradley
3. PROFINET - Siemens
4. OPC-UA - modern unified standard
5. Modbus RTU (via serial adapter)

### Pricing
- **Base:** $199/month per facility
- **Includes:** 10 PLC connections, unlimited queries
- **Additional PLCs:** $19/month each
- **Enterprise:** Custom pricing for 10+ facilities

### Development Status
- ⚠️ Edge agent: needs development
- ⚠️ Protocol connectors: research phase
- ✅ Cloud infrastructure: ready

---

## TIER 3: FactoryLM Predict

### Target Customer
- New installations / facility upgrades
- Companies committed to predictive maintenance
- High-value equipment requiring component-level monitoring

### Value Proposition
"Know which sensor will fail before it does. Component-level intelligence."

### Features
- Everything in Connect, plus:
- IO-Link smart sensor integration
- Component-level diagnostics
- Predictive failure algorithms
- Sensor health monitoring
- Automatic parts ordering integration
- Digital twin visualization (roadmap)

### Technical Requirements
- FactoryLM Edge Gateway (hardware)
  - Raspberry Pi 4 + Pinetek IOL HAT
  - Or commercial gateway (Advantech, Moxa)
- IO-Link master software
- Predictive ML models

### Pricing
- **Edge Gateway:** $499 one-time (hardware)
- **Service:** $499/month per facility
- **Includes:** Unlimited sensors, full predictive suite
- **White-glove setup:** $2,000 (optional)

### Development Status
- ⚠️ Edge gateway: design phase
- ⚠️ IO-Link integration: research complete
- ⚠️ Predictive models: needs development
- ✅ Cloud infrastructure: ready

---

## Go-to-Market Strategy

### Phase 1: Identify (Now - Q1 2026)
- Launch free tier widely
- Build equipment database
- Collect user feedback
- Generate case studies

### Phase 2: Connect (Q2 2026)
- Beta with select customers
- Develop protocol connectors
- Partner with system integrators

### Phase 3: Predict (Q3 2026)
- Hardware production
- Enterprise pilots
- Predictive model training

---

## Revenue Model

| Tier | Price | Target Customers | Year 1 Goal |
|------|-------|------------------|-------------|
| Identify Free | $0 | 1,000 | Funnel |
| Identify Pro | $49/mo | 100 | $58,800 |
| Connect | $199/mo | 20 | $47,760 |
| Predict | $499/mo | 5 | $29,940 |
| **Total ARR** | | | **$136,500** |

---

## Competitive Differentiation

1. **No infrastructure requirement** for Tier 1 - competitors require installation
2. **Protocol-agnostic** - works with any PLC brand
3. **Photo-first interface** - natural for field technicians
4. **Land and expand** pricing - easy entry, grows with customer
5. **Open source hardware options** - reduces customer lock-in concerns

---

## Accelerator Messaging

### YC Angle
"FactoryLM is GitHub Copilot for maintenance technicians. $50B in manufacturing downtime, 600K unfilled jobs, and we're the AI that makes junior techs perform like veterans."

### NVIDIA Inception Angle
"We're building the industrial AI stack - computer vision for equipment identification, LLMs for troubleshooting, edge computing for real-time monitoring. NVIDIA hardware at every layer."

### Alchemist Angle
"Enterprise B2B SaaS for manufacturing. Three-tier land-and-expand model. Proven founder-market fit with 15 years of maintenance experience."

---

## Robot Army Assignments

| Division | Owner | Responsibility |
|----------|-------|----------------|
| Product/Code | Code Agent | Build edge agent, protocol connectors |
| Research | IIoT Research Director | Protocol specs, hardware options |
| Marketing | Marketing Director | Product pages, pitch decks |
| PM | PM Director | Trello tracking, deadlines |
| Compliance | Compliance Agent | Audit all work |

---

## Engineering Commandments (Apply to All Work)

1. Create GitHub Issue before touching code
2. Branch from main - never commit directly
3. Create PR linked to issue
4. WAIT for Mike's approval before merging
5. No production deploys without verbal OK
6. Document everything
7. Test before shipping
8. Security first - no credentials in code
9. Voice messages to Mike for updates
10. Proof of work in artifacts folder

---

*This document is the source of truth for FactoryLM product strategy.*
*Last updated: 2026-02-05 11:18 UTC*
