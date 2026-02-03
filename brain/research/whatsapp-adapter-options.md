# WhatsApp Adapter Research — FactoryLM

*Research completed: 2026-01-30*
*Priority: P0 (Critical for Venezuela market)*

---

## Why WhatsApp is Critical

- **WhatsApp dominates Latin America** — 90%+ penetration in Venezuela
- Technicians in the field use WhatsApp, not Telegram
- Voice notes are common for describing equipment issues
- Group chats for maintenance teams already exist on WhatsApp

## Options Evaluated

### Option 1: WhatsApp Cloud API (Direct Meta)

**Pros:**
- Lower per-message cost (~$0.005-0.08 depending on country/type)
- Direct integration, no middleman
- Full feature access
- Better for high volume

**Cons:**
- Requires Facebook Business verification (takes days/weeks)
- More complex webhook setup
- Need to handle infrastructure yourself

**Pricing (Venezuela):**
- Marketing: ~$0.0513/message
- Utility: ~$0.0200/message
- Service (24hr window): Free
- Authentication: ~$0.0308/message

### Option 2: Twilio WhatsApp API

**Pros:**
- Easier setup, sandbox available immediately
- Excellent Node.js SDK
- Good documentation
- Reliable infrastructure

**Cons:**
- Higher per-message cost (~$0.005 base + carrier fees)
- Another vendor to manage
- Markup on top of Meta fees

**Pricing:**
- ~$0.005/message (Twilio) + Meta conversation fees
- Phone number: $1/month

### Option 3: 360dialog

**Pros:**
- Direct WhatsApp access
- Good for high volume
- Lower cost than Twilio

**Cons:**
- Less documentation
- Smaller community
- EU-based (GDPR focus)

### Option 4: MessageBird

**Pros:**
- Multi-channel support
- Good API
- Global presence

**Cons:**
- Higher cost
- More complex than needed

---

## Recommendation

### Phase 1: Twilio (MVP)
- Use Twilio WhatsApp Sandbox for development
- Fast to set up, can test immediately
- Good for pilot with 10-20 technicians

### Phase 2: Cloud API (Production)
- Apply for WhatsApp Business verification
- Migrate to direct Cloud API for cost savings
- Required for high-volume production use

---

## Technical Architecture

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│  WhatsApp User  │────▶│  Twilio Webhook  │────▶│   FactoryLM     │
│  (Technician)   │     │  /whatsapp/hook  │     │  WhatsApp Plugin│
└─────────────────┘     └──────────────────┘     └────────┬────────┘
                                                          │
                                                          ▼
                                                 ┌─────────────────┐
                                                 │  Clawdbot Core  │
                                                 │  (AI Processing)│
                                                 └────────┬────────┘
                                                          │
                                                          ▼
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│  WhatsApp User  │◀────│  Twilio API      │◀────│  Response       │
│  (Response)     │     │  Send Message    │     │  Generator      │
└─────────────────┘     └──────────────────┘     └─────────────────┘
```

---

## Implementation Plan

### Week 1: Setup
1. Create Twilio account
2. Set up WhatsApp Sandbox
3. Scaffold plugin structure following Clawdbot patterns

### Week 2: Core Functionality
1. Webhook handler for incoming messages
2. Text message parsing and response
3. Basic error handling

### Week 3: Media & Polish
1. Image attachment handling (equipment photos)
2. Voice note handling (technician descriptions)
3. Spanish language testing
4. Rate limiting

### Week 4: Testing & Documentation
1. End-to-end testing with real devices
2. Documentation
3. PR and review

---

## Code Skeleton

```javascript
// whatsapp-adapter/index.js
const twilio = require('twilio');

class WhatsAppAdapter {
  constructor(config) {
    this.client = twilio(config.accountSid, config.authToken);
    this.fromNumber = config.whatsappNumber;
  }

  // Handle incoming webhook
  async handleIncoming(req) {
    const { Body, From, MediaUrl0, MediaContentType0 } = req.body;
    
    return {
      text: Body,
      from: From.replace('whatsapp:', ''),
      media: MediaUrl0 ? { url: MediaUrl0, type: MediaContentType0 } : null
    };
  }

  // Send response
  async send(to, message) {
    return this.client.messages.create({
      body: message,
      from: `whatsapp:${this.fromNumber}`,
      to: `whatsapp:${to}`
    });
  }

  // Send media
  async sendMedia(to, message, mediaUrl) {
    return this.client.messages.create({
      body: message,
      from: `whatsapp:${this.fromNumber}`,
      to: `whatsapp:${to}`,
      mediaUrl: [mediaUrl]
    });
  }
}

module.exports = WhatsAppAdapter;
```

---

## Environment Variables

```env
TWILIO_ACCOUNT_SID=ACxxxxx
TWILIO_AUTH_TOKEN=xxxxx
TWILIO_WHATSAPP_NUMBER=+14155238886  # Sandbox number
WHATSAPP_WEBHOOK_PATH=/whatsapp/hook
```

---

## WhatsApp Message Templates

For proactive messaging (outside 24hr window), need approved templates:

### Template 1: Maintenance Alert
```
Alerta de Mantenimiento - {{1}}

Equipo: {{2}}
Estado: {{3}}
Acción requerida: {{4}}

Responda para más detalles.
```

### Template 2: Diagnostic Result
```
Resultado de Diagnóstico

Su consulta sobre {{1}} ha sido analizada.

Causa probable: {{2}}
Recomendación: {{3}}

¿Necesita ayuda adicional?
```

---

## Cost Estimate (Venezuela Pilot)

**Assumptions:**
- 20 technicians
- 50 messages/day average
- 30-day pilot

**Calculation:**
- Messages: 20 × 50 × 30 = 30,000 messages
- Cost @ $0.02/msg (service conversations): ~$600/month

**Note:** Most messages will be within 24hr service window (free conversations after first message). Actual cost likely $100-200/month for pilot.

---

## Next Steps

1. ✅ GitHub Issue created: #10
2. ⏳ Set up Twilio account
3. ⏳ Request WhatsApp Sandbox access
4. ⏳ Create branch: `feat/whatsapp-adapter`
5. ⏳ Build MVP
6. ⏳ Create PR for review

---

*Following Engineering Commandments: Research → Issue → Branch → PR → Approval*
