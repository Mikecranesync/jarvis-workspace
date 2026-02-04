# Signal Development Strategy for FactoryLM

## Executive Summary
Signal as a **premium/enterprise channel** for security-conscious industrial customers (defense, pharma, critical infrastructure).

## Why Signal for FactoryLM

### Target Customers
- Defense contractors (ITAR compliance)
- Pharmaceutical manufacturing (FDA 21 CFR Part 11)
- Critical infrastructure (power, water, oil & gas)
- Government facilities
- Customers with strict no-cloud policies

### Value Proposition
- **E2E encryption** — messages never readable by third parties
- **Open source** — auditable, no hidden backdoors
- **Disappearing messages** — auto-delete sensitive operational data
- **No Big Tech** — not owned by Meta/Google

## Technical Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    FACTORYLM EDGE DEVICE                    │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐     │
│  │ PLC Driver  │───▶│ FactoryLM   │───▶│  Clawdbot   │     │
│  │ (pycomm3)   │    │   Engine    │    │  Gateway    │     │
│  └─────────────┘    └─────────────┘    └──────┬──────┘     │
│                                               │             │
│                                    ┌──────────┴──────────┐  │
│                                    │                     │  │
│                              ┌─────▼─────┐        ┌──────▼──┐
│                              │ Telegram  │        │ Signal  │
│                              │  Channel  │        │ Channel │
│                              └───────────┘        └─────────┘
└─────────────────────────────────────────────────────────────┘
```

## Implementation Phases

### Phase 1: Proof of Concept (Week 1)
- [ ] Install signal-cli on VPS (Java dependency)
- [ ] Register test Signal number
- [ ] Configure Clawdbot Signal channel
- [ ] Test basic send/receive with FactoryLM

### Phase 2: Feature Parity (Week 2-3)
- [ ] Alarm notifications via Signal
- [ ] Status queries (text commands vs buttons)
- [ ] Media attachments (charts, screenshots)
- [ ] Group chat support for shift teams

### Phase 3: Enterprise Features (Week 4+)
- [ ] Disappearing messages for sensitive alerts
- [ ] Read receipts for delivery confirmation
- [ ] Multi-account (per-facility) support
- [ ] Audit logging (who received what, when)

## Signal vs Telegram Feature Map

| FactoryLM Feature      | Telegram          | Signal Equivalent      |
|------------------------|-------------------|------------------------|
| E-Stop Button          | Inline button     | Text: "ESTOP" or "1"   |
| Alarm Acknowledge      | ✅ ACK button     | Text: "ACK" or "A"     |
| Status Dashboard       | Inline graphic    | Image attachment       |
| Mode Selection         | Button menu       | Numbered menu in text  |
| Quick Actions          | Button row        | Shortcodes: S/P/A/R    |

### Text Command Mapping
```
Signal Commands (no buttons):
  S or STOP     → Emergency Stop
  A or ACK      → Acknowledge Alarm
  R or RUN      → Start/Resume
  P or PAUSE    → Pause Operation
  STATUS        → Get current status
  HELP          → Show commands
```

## Hardware Requirements (Edge Device)

For Signal support on FactoryLM Edge:
- **Additional RAM:** +256MB for JVM (signal-cli)
- **Storage:** +100MB for Java runtime
- **Recommendation:** 2GB RAM minimum (vs 1GB for Telegram-only)

## Pricing Strategy

| Tier          | Channels              | Price/month |
|---------------|-----------------------|-------------|
| Standard      | Telegram only         | $99         |
| Professional  | Telegram + WhatsApp   | $149        |
| Enterprise    | All + Signal + SLA    | $299        |

## Security Certification Angle

Signal support enables marketing to:
- SOC 2 Type II environments
- HIPAA-covered entities
- ITAR/EAR controlled facilities
- FedRAMP pathway (future)

## Next Steps

1. **Immediate:** Set up Signal test environment on VPS
2. **This Week:** Port FactoryLM commands to text-based interface
3. **Demo (Feb 10):** Show Telegram primary + Signal option
4. **Launch:** Include in FactoryLM Edge v1.0 as enterprise add-on

---
Created: 2026-02-04
Status: STRATEGY APPROVED
