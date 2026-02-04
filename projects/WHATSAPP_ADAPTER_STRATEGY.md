# WhatsApp Adapter Strategy for FactoryLM

## URGENT: Go Live Before Morning (2026-02-04)

## Why WhatsApp

- **2 billion users** — most factory workers already have it
- **No app install** — works on any smartphone
- **Group chats** — natural fit for shift teams
- **Voice notes** — hands-free in noisy environments
- **International** — dominant in Latin America, Europe, Asia

## Architecture

```
┌──────────────────────────────────────────────────────────┐
│                     CLAWDBOT GATEWAY                     │
├──────────────────────────────────────────────────────────┤
│                                                          │
│   WhatsApp Channel (Baileys)                             │
│   ├── Web Socket to WhatsApp servers                     │
│   ├── QR code login (Linked Devices)                     │
│   └── Session persistence (creds.json)                   │
│                                                          │
│   Routing:                                               │
│   ├── DMs → Main agent session                           │
│   └── Groups → Isolated session per group                │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

## Tonight's Deployment Checklist

### Step 1: Get a Phone Number
- [ ] Option A: Use spare phone with prepaid SIM
- [ ] Option B: Use Mike's WhatsApp Business number
- [ ] Option C: eSIM on existing device

### Step 2: Configure Clawdbot
```json5
{
  channels: {
    whatsapp: {
      enabled: true,
      dmPolicy: "allowlist",
      allowFrom: ["+1MIKESNUMBER"],
      groupPolicy: "allowlist",
      groups: ["*"],
      ackReaction: {
        emoji: "👀",
        direct: true,
        group: "mentions"
      }
    }
  }
}
```

### Step 3: Login & Link
```bash
clawdbot channels login
# Scan QR code with WhatsApp → Settings → Linked Devices
```

### Step 4: Test
```bash
# From Mike's phone, send WhatsApp message to bot number
# Verify response comes back
```

### Step 5: FactoryLM Integration
- Route factory keywords to diagnosis service
- Same routing as Telegram:
  ```
  Keywords: factory, plc, motor, conveyor, production, alarm, sensor
  → POST http://localhost:8200/diagnose
  ```

## WhatsApp vs Telegram Features

| Feature              | Telegram | WhatsApp | Notes                    |
|----------------------|----------|----------|--------------------------|
| Inline Buttons       | ✅       | ❌       | Use text commands        |
| Voice Notes          | ✅       | ✅       | Native PTT support       |
| Read Receipts        | ❌       | ✅       | Blue ticks               |
| Groups               | ✅       | ✅       | @mention activation      |
| Media                | 50MB     | 50MB     | Parity                   |
| Reactions            | ✅       | ✅       | Full support             |
| Business API         | Free     | Paid*    | We use Web, not Business |

*We bypass WhatsApp Business API costs by using Baileys (Web protocol)

## Text Command Interface (No Buttons)

```
FACTORYLM WHATSAPP COMMANDS
═══════════════════════════
STATUS    → Current system status
ESTOP     → Emergency stop
ACK       → Acknowledge alarm  
RUN       → Start production
PAUSE     → Pause production
HELP      → Show this menu

Or just ask naturally:
"What's the motor temperature?"
"Show me today's production count"
```

## Go-Live Steps (Execute Now)

1. ✅ Strategy documented
2. ⬜ Mike provides phone number for WhatsApp bot
3. ⬜ Update clawdbot.json with WhatsApp config
4. ⬜ Run `clawdbot channels login`
5. ⬜ Mike scans QR from his phone
6. ⬜ Test DM conversation
7. ⬜ Test FactoryLM query routing
8. ⬜ Announce ready

## Risks & Mitigations

| Risk                        | Mitigation                           |
|-----------------------------|--------------------------------------|
| WhatsApp bans bot number    | Use dedicated number, low volume     |
| Session disconnects         | Baileys auto-reconnect configured    |
| 24h reply window (Business) | We use Web, not Business API         |
| QR code expires             | Re-scan if needed                    |

---
Created: 2026-02-04 00:40 UTC
Status: READY TO EXECUTE
Owner: Jarvis
