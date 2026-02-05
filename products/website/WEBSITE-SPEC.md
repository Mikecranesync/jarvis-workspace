# FactoryLM Website Specification

*Apple-quality design, minimal aesthetic, conversion-focused*

---

## Design Principles

1. **White space is your friend** - Let elements breathe
2. **One message per section** - Don't overwhelm
3. **Show, don't tell** - Screenshots, demos, videos
4. **Mobile-first** - Most techs will visit on phones
5. **Fast load times** - Under 2 seconds
6. **Clear CTAs** - One primary action per page

---

## Color Palette

- **Primary:** #0066CC (Trust blue)
- **Secondary:** #1A1A1A (Near black for text)
- **Accent:** #00C853 (Success green)
- **Background:** #FFFFFF (Pure white)
- **Light gray:** #F5F5F7 (Section alternation)
- **Warning:** #FF9500 (Orange for alerts)

---

## Typography

- **Headlines:** SF Pro Display or Inter, 48-72px
- **Subheads:** SF Pro Display or Inter, 24-32px
- **Body:** SF Pro Text or Inter, 16-18px
- **Captions:** SF Pro Text or Inter, 14px

---

## Page Structure

### 1. LANDING PAGE: factorylm.com

#### Hero Section
```
[Full-width, minimal]

HEADLINE: AI that speaks maintenance.
SUBHEAD: From photo identification to predictive analytics. 
         Three products. One platform. Zero complexity.

[Three product cards side by side]

IDENTIFY          CONNECT           PREDICT
Photo → Answer    PLC → Insights    Sensor → Foresight
$49/mo            $199/mo           $499/mo
[Learn More]      [Learn More]      [Learn More]
```

#### Problem Section
```
[Light gray background]

HEADLINE: Manufacturing loses $50B annually to downtime.

[Three stats in a row]
600,000          55 years         90%
unfilled jobs    avg tech age     data unused

BODY: The knowledge is walking out the door. 
      FactoryLM captures it before it's gone.
```

#### Solution Section
```
[White background]

HEADLINE: Intelligence at every level.

[Visual showing progression]

LEGACY EQUIPMENT → NETWORKED PLCs → SMART SENSORS
      ↓                  ↓               ↓
   Identify          Connect          Predict
   Photo-based       Real-time        Predictive
   identification    monitoring       maintenance
```

#### Social Proof Section
```
[Light gray background]

HEADLINE: Built by a maintenance tech. For maintenance techs.

[Photo of Mike]
"I spent 15 years debugging PLCs at 2 AM with paper manuals.
 I built the tool I wished I had."
 
 — Mike Harpool, Founder
   15 years industrial maintenance
```

#### CTA Section
```
[Blue background, white text]

HEADLINE: Start with a photo. Scale to predictive.

[Two buttons]
[Try Free - Identify]    [Request Demo - Connect/Predict]
```

---

### 2. IDENTIFY PAGE: factorylm.com/identify

#### Hero
```
HEADLINE: Snap a photo. Get answers.
SUBHEAD: Equipment identification, troubleshooting steps, 
         and parts info — no installation required.

[Phone mockup showing Telegram chat with equipment photo and AI response]

[Start Free]
```

#### How It Works
```
[Three steps, horizontal]

1. TAKE A PHOTO        2. AI IDENTIFIES         3. GET GUIDANCE
   Nameplate, wiring,     Manufacturer, model,     Troubleshooting,
   components             specs, age               parts, procedures
   
[Animated demo or video]
```

#### Features
```
- Nameplate OCR (reads worn labels)
- Component recognition (motors, VFDs, sensors)
- Cross-reference parts across manufacturers
- Maintenance history logging
- Works via Telegram (no app install)
```

#### Pricing
```
FREE              PRO               TEAM
10 queries/mo     Unlimited         5 users
Basic ID          Full history      Shared history
                  Priority support  Admin dashboard

$0                $49/mo            $99/mo
[Start Free]      [Subscribe]       [Subscribe]
```

---

### 3. CONNECT PAGE: factorylm.com/connect

#### Hero
```
HEADLINE: See what your PLCs already know.
SUBHEAD: Real-time monitoring and AI insights — 
         no sensor changes, just software.

[Dashboard mockup showing live equipment status]

[Request Demo]
```

#### Supported Protocols
```
[Grid of protocol logos with checkmarks]

✓ Modbus TCP/RTU    ✓ Ethernet/IP (Allen-Bradley)
✓ PROFINET          ✓ OPC-UA  
✓ S7 (Siemens)      ✓ BACnet

Don't see yours? We're adding more monthly.
```

#### Architecture
```
[Clean diagram]

Your PLCs → Edge Agent (software) → FactoryLM Cloud → Your Team
           (runs on any Linux/Windows)

- No inbound ports required
- Read-only by default
- TLS 1.3 encryption
- Offline buffering
```

#### Features
```
- Auto-discover PLCs on network
- Real-time fault code interpretation
- Process value trending
- AI-powered root cause analysis
- Photo + data correlation
- Alert notifications (SMS, email, Telegram)
```

#### Pricing
```
BASE                          ENTERPRISE
$199/mo per facility          Custom pricing
10 PLC connections included   Unlimited connections
Additional PLCs: $19/mo       Multi-site dashboard
                              Dedicated support

[Request Demo]                [Contact Sales]
```

---

### 4. PREDICT PAGE: factorylm.com/predict

#### Hero
```
HEADLINE: Know what will fail. Before it does.
SUBHEAD: Component-level monitoring with predictive AI.
         The future of maintenance is here.

[Edge gateway hardware photo + dashboard showing predictions]

[Contact Sales]
```

#### Hardware
```
FACTORYLM EDGE GATEWAY

- 2x IO-Link master ports
- Connects to any smart sensor
- Industrial enclosure (DIN rail)
- Pre-configured, plug and play

$499 one-time
```

#### Capabilities
```
[Visual timeline showing]

TRADITIONAL: Equipment fails → Tech responds → 4 hours downtime

FACTORYLM PREDICT: 
  Day 1: Sensor installed
  Day 14: Baseline established
  Day 45: Anomaly detected → "Bearing degradation, 72hr to failure"
  Day 46: Scheduled replacement → Zero downtime
```

#### Features
```
- IO-Link smart sensor integration
- Vibration analysis
- Temperature trending
- Predictive failure algorithms
- Automatic parts ordering (coming soon)
- Digital twin visualization (roadmap)
```

#### Pricing
```
HARDWARE                SERVICE
$499 one-time           $499/mo per facility
Edge gateway            Unlimited sensors
                        Full predictive suite
                        Quarterly reviews

[Contact Sales]
```

---

## Technical Notes

### Hosting
- Vercel or Netlify for static hosting
- Edge CDN for global performance

### Framework
- Next.js or Astro for static generation
- TailwindCSS for styling
- Framer Motion for animations

### Analytics
- Plausible or Fathom (privacy-friendly)
- Conversion tracking on CTAs

### Forms
- Signup: Connect to Stripe for payments
- Demo requests: Send to CRM/email
- Free tier: Link to Telegram bot

---

## Implementation Priority

1. **Landing page** - Most important, drives everything
2. **Identify page** - Active product, can convert now
3. **Connect page** - Coming soon messaging acceptable
4. **Predict page** - Roadmap positioning acceptable

---

*Document Owner: Marketing Director*
*Last Updated: 2026-02-05*
