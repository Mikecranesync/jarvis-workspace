# FactoryLM Conversion Funnel Architecture
*From Random Photo to PLC Integration*

**Created:** 2026-02-05
**Status:** SPEC DRAFT - Awaiting Mike's approval

---

## The Psychology Stack

### 1. Nir Eyal's Hooked Model
```
TRIGGER → ACTION → VARIABLE REWARD → INVESTMENT
   ↑                                      │
   └──────────────────────────────────────┘
```

- **Trigger:** Equipment problem (internal) or ad/search (external)
- **Action:** Take a photo (low friction)
- **Variable Reward:** Different/useful info each time
- **Investment:** Answer questions, build asset profile

### 2. IKEA Effect
Users value things 5x more when they help create them.
- Don't GIVE them a CMMS entry
- Make them BUILD it with you through questions
- By the end, they OWN it psychologically

### 3. Commitment Escalation
Each small action makes the next one easier:
1. Take photo (tiny commitment)
2. Confirm equipment type (small)
3. Name the equipment (medium)
4. Add location (medium)
5. Enter email to save (feels natural now)

### 4. Endowment Effect
Once they have something, they don't want to lose it:
- Show them the beautiful asset card they built
- Then: "Enter email to save this forever"
- Not a gate - a VALUE PROTECTION moment

---

## The Complete User Journey

### Stage 0: Discovery
**User:** Random maintenance tech in Philippines finds site via Google/ad

**Touchpoint:** Landing page with camera CTA
- No signup required
- "Take a photo. See what we find." 
- Immediate value promise

### Stage 1: First Photo (The Hook)

**Action:** User takes photo

**UI Experience:**
```
┌─────────────────────────────────────┐
│         [Camera Viewfinder]         │
│                                     │
│            ┌─────────┐              │
│            │    ⊕    │              │
│            └─────────┘              │
│                                     │
│         [📷 CAPTURE]                │
└─────────────────────────────────────┘
```

**After capture - ROBOT CONFIRMATION:**
```
┌─────────────────────────────────────┐
│                                     │
│  🤖 "I'm analyzing your equipment.  │
│      Here's what I can do:"         │
│                                     │
│  □ Identify manufacturer & model    │
│  □ Find maintenance manuals         │
│  □ Suggest common failure modes     │
│  □ Create an asset profile          │
│                                     │
│  ⏳ Searching equipment databases...│
│  ⏳ Cross-referencing nameplates... │
│  ⏳ Loading troubleshooting guides..│
│                                     │
└─────────────────────────────────────┘
```

**INTENTIONAL LATENCY:** 3-5 seconds builds anticipation
(Backend is actually done in 1-2s, but we add dramatic pause)

### Stage 2: Initial Reveal (Variable Reward)

**Voice + Visual:**
> "This is a Baldor 5-horsepower AC motor, model EM3615T."

**NEVER repeat the full model number again** - it's annoying in voice.

**Visual Card (teaser):**
```
┌─────────────────────────────────────┐
│  [EQUIPMENT IDENTIFIED]             │
│                                     │
│  🔧 Baldor 5HP Motor                │
│     Model: EM3615T                  │
│                                     │
│  ─────────────────────────          │
│  💡 I can tell you more.            │
│     Want to unlock the full         │
│     maintenance profile?            │
│                                     │
│  [YES, TELL ME MORE] [JUST THE ID]  │
└─────────────────────────────────────┘
```

### Stage 3: Progressive Profiling (Building Investment)

**The Game Theory Questions:**

Each question serves 2 purposes:
1. Gets data to improve results
2. Increases user investment (IKEA Effect)

**Question Flow (State Machine):**

```
STATE_INITIAL
    │
    ▼
Q1: "What do you call this motor?" (local name)
    │ User: "Pump 7 motor"
    ▼
STATE_NAMED
    │
    ▼
Q2: "Where does it live?" (location building)
    │ User: "Building C, Line 2"
    ▼
STATE_LOCATED  
    │
    ▼
Q3: "How old is it, roughly?" (age context)
    │ User: "About 5 years"
    ▼
STATE_AGED
    │
    ▼
Q4: "Having any issues right now?" (troubleshooting trigger)
    │ User: "Yeah, it's making a grinding noise"
    ▼
STATE_TROUBLESHOOTING (branch to troubleshooting tree)
    │
    ▼
[Continue troubleshooting flow...]
```

**Voice Personality:**
- Casual but competent
- Like a senior tech, not a robot
- "Yeah, those Baldors are workhorses. Grinding noise usually means bearings."
- Different response variations (not repetitive)

### Stage 4: The CMMS Entry Reveal

After 3-5 questions, show them what they built:

```
┌─────────────────────────────────────┐
│  🏆 ASSET PROFILE CREATED           │
│                                     │
│  ┌─────────────────────────────┐    │
│  │ Pump 7 Motor                │    │
│  │ Baldor EM3615T              │    │
│  │ Building C, Line 2          │    │
│  │ Installed: ~2021            │    │
│  │ Status: ⚠️ Needs attention  │    │
│  │                             │    │
│  │ MAINTENANCE NOTES:          │    │
│  │ • Grinding noise reported   │    │
│  │ • Check bearings first      │    │
│  │ • Cooling fan 2nd priority  │    │
│  │                             │    │
│  │ SUGGESTED PARTS:            │    │
│  │ • 6205-2RS Bearing ($12)    │    │
│  │ • Cooling fan shroud ($45)  │    │
│  │                             │    │
│  │ 📄 Manual: [Available]      │    │
│  └─────────────────────────────┘    │
│                                     │
│  [This block is READ-ONLY]          │
│  They can't edit, just admire       │
│                                     │
└─────────────────────────────────────┘
```

### Stage 5: Email Gate (Value Protection)

**The Pivot:**
> "You just built a complete asset profile from one photo. 
> Want to save it? Drop your email and it's yours forever.
> Plus I'll email you when I find relevant manuals."

**Psychology:** Not a paywall - they're PROTECTING what they created.

```
┌─────────────────────────────────────┐
│                                     │
│  📧 Save Your Asset Profile         │
│                                     │
│  ┌──────────────────────────────┐   │
│  │ your@email.com               │   │
│  └──────────────────────────────┘   │
│                                     │
│  [SAVE & SEND ME THE PROFILE]       │
│                                     │
│  ───────────────────────────────    │
│  ✓ Free forever                     │
│  ✓ No credit card                   │
│  ✓ I'll find manuals for this motor │
│                                     │
└─────────────────────────────────────┘
```

### Stage 6: Post-Email Nurture

**Immediate Email:**
- PDF of their asset profile
- QR code to stick on equipment
- "Reply to this email if you want to add more equipment"

**Day 3 Email:**
- "I found 2 more assets similar to your Baldor motor being discussed..."
- Community hook

**Day 7 Email:**
- "Want to see all your equipment on one dashboard? Try CMMS Free."

### Stage 7: Freemium → Paid Conversion

**Free Tier (after email):**
- 3 photos/month
- Basic asset cards
- Manual lookup

**Pro Tier ($49/mo):**
- Unlimited photos
- Full CMMS entry creation
- Team sharing
- Troubleshooting trees

**Connect Tier ($199/mo):**
- Everything in Pro
- PLC Edge Agent integration
- Real-time monitoring
- Alert routing

**Predict Tier ($499/mo):**
- Everything in Connect
- Predictive maintenance AI
- IO-Link sensor integration
- Anomaly detection

---

## Technical Architecture: State Machine

### Why Not Pure LLM?
- LLMs are expensive
- LLMs are unpredictable
- LLMs don't remember state efficiently
- Users hate repeating themselves

### The Hybrid Approach

```
┌─────────────────────────────────────────────┐
│           STATE MACHINE (Deterministic)     │
│  ┌──────────────────────────────────────┐   │
│  │ conversation_state = {              │   │
│  │   "session_id": "abc123",           │   │
│  │   "current_node": "Q3_LOCATION",    │   │
│  │   "equipment": {                    │   │
│  │     "manufacturer": "Baldor",       │   │
│  │     "model": "EM3615T",             │   │
│  │     "local_name": "Pump 7 motor",   │   │
│  │     "location": null                │   │
│  │   },                                │   │
│  │   "history": [Q1, A1, Q2, A2...]    │   │
│  │ }                                   │   │
│  └──────────────────────────────────────┘   │
│                                             │
│  Transitions:                               │
│  - User says location → STATE_LOCATED       │
│  - User asks question → BRANCH_TO_QA        │
│  - User says "skip" → NEXT_OPTIONAL         │
│                                             │
└─────────────────────────────────────────────┘
              │
              │ (only when needed)
              ▼
┌─────────────────────────────────────────────┐
│              LLM LAYER (Expensive)          │
│                                             │
│  Used for:                                  │
│  - Initial photo analysis                   │
│  - Free-form troubleshooting                │
│  - Edge cases state machine can't handle    │
│  - Response variation (personality)         │
│                                             │
│  NOT used for:                              │
│  - Remembering state (that's the machine)   │
│  - Predictable questions                    │
│  - Routing decisions                        │
│                                             │
└─────────────────────────────────────────────┘
```

### State Persistence

```python
# Redis for fast state lookup
state = await redis.get(f"conv:{session_id}")

# PostgreSQL for permanent history
await db.execute("""
    INSERT INTO conversations (session_id, state_json, updated_at)
    VALUES ($1, $2, NOW())
    ON CONFLICT (session_id) DO UPDATE SET state_json = $2
""")
```

### Response Templates (Not Ad-Hoc LLM)

```python
RESPONSE_TEMPLATES = {
    "Q1_EQUIPMENT_NAME": [
        "What do you call this {equipment_type}?",
        "Does this {equipment_type} have a name? Like 'Pump 7' or 'Line 3 motor'?",
        "Your team probably calls this something. What is it?"
    ],
    "Q2_LOCATION": [
        "Where does {local_name} live?",
        "What building or area is {local_name} in?",
        "Help me find {local_name} - where is it?"
    ],
    # ...
}

# Pick randomly for variation, but CONTROLLED variation
response = random.choice(RESPONSE_TEMPLATES[state.current_node])
```

---

## Troubleshooting Trees

### Maintenance Manual → Decision Tree

Every troubleshooting session follows a FLOWCHART, not freeform chat.

```
GRINDING_NOISE_MOTOR
    │
    ├─ Q: "Is it constant or intermittent?"
    │   ├─ Constant → BEARING_FAILURE_PATH
    │   └─ Intermittent → LOAD_ISSUE_PATH
    │
BEARING_FAILURE_PATH
    │
    ├─ Q: "Is it louder at startup or during running?"
    │   ├─ Startup → SUGGEST: "Check bearing lubrication"
    │   └─ Running → SUGGEST: "Bearing replacement needed"
```

**State codes for backend:**
```
path_code = "MOTOR_GRIND_BEARING_RUN_1"
# This is a SAVE POINT
# User can leave, come back, resume exactly here
```

---

## Metrics to Track

### Funnel Metrics
| Stage | Metric | Target |
|-------|--------|--------|
| Photo taken | Count | Baseline |
| Initial ID shown | Completion % | 95% |
| Q1 answered | Engagement % | 70% |
| Q3+ answered | Deep engagement | 40% |
| Email captured | Conversion | 25% |
| Day 7 active | Retention | 15% |
| Paid conversion | Revenue | 5% |

### Quality Metrics
| Metric | Target |
|--------|--------|
| Correct equipment ID | 85%+ |
| User satisfaction | 4.2/5 |
| Session abandonment | <30% |

---

## Implementation Priority

### Phase 1: MVP (Week 1-2)
1. State machine skeleton (5 states)
2. Photo → LLM → Basic response
3. Email capture at end
4. Simple Postgres storage

### Phase 2: Polish (Week 3-4)
1. Voice output via TTS
2. Response variation
3. Mobile-optimized UI
4. Basic troubleshooting tree (1 equipment type)

### Phase 3: Scale (Month 2)
1. Full troubleshooting trees
2. CMMS integration
3. Team features
4. Analytics dashboard

---

## Open Questions for Mike

1. **Voice persona:** Male or female? American or neutral accent?
2. **First equipment focus:** Motors? PLCs? Pumps? Pick one to nail first.
3. **Troubleshooting trees:** Do you have existing flowcharts from manuals?
4. **Pricing validation:** Is $49/$199/$499 right for target market?
5. **Geographic focus:** US first, or global from day 1?

---

*"The goal isn't to build a chatbot. It's to build a salesperson that never sleeps."*
