# PLC-Copilot — First Contact Workflow

## The Detective Flow 🔍

User sends a photo → Bot becomes a detective, gathering intel before proposing action.

```
┌─────────────────────────────────────────────────────────┐
│                    📸 PHOTO RECEIVED                     │
│              User sends nameplate/equipment pic           │
└──────────────────────────┬──────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────┐
│               🔍 PHASE 1: IDENTIFICATION                 │
│                                                          │
│  • OCR + Vision AI extracts:                            │
│    - Manufacturer (Siemens, AB, etc)                    │
│    - Model (KP300 Basic mono)                           │
│    - Part Number (6AV6647-0AH11-3AX0)                  │
│    - Serial Number                                       │
│    - Voltage/Power specs                                │
│    - Certifications                                      │
│                                                          │
│  Bot responds: "I identified this as a [equipment]"     │
│  Shows extracted specs in a clean card                   │
└──────────────────────────┬──────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────┐
│              📋 PHASE 2: CMMS REGISTRATION               │
│                                                          │
│  "This is new equipment! Let me add it to your system." │
│                                                          │
│  • Creates equipment record in CMMS                     │
│  • Assigns unique asset tag                              │
│  • Stores photo as reference                            │
│  • Asks: "What machine/area is this part of?"           │
│    → User replies: "Sorting Station" or "Line 3"        │
│  • Links component to parent machine                    │
│                                                          │
│  ✅ Equipment registered as standalone component         │
└──────────────────────────┬──────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────┐
│              📚 PHASE 3: KNOWLEDGE ACQUISITION           │
│                                                          │
│  "Want me to find the user manual for this?"            │
│  [📖 Yes, find manual] [⏭️ Skip for now]                │
│                                                          │
│  If YES:                                                │
│  • KB Enrichment Pipeline triggers                      │
│  • Searches Google CSE + ManualsLib                     │
│  • Downloads PDF manual                                 │
│  • Parses specs, wiring diagrams, fault codes           │
│  • Indexes into knowledge base                          │
│  • "Found the KP300 manual! 127 pages indexed."         │
│  • Stores manual linked to equipment record             │
└──────────────────────────┬──────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────┐
│              🔧 PHASE 4: DETECTIVE MODE                  │
│                                                          │
│  Bot starts asking smart questions:                     │
│                                                          │
│  "Now that I know this equipment, let me learn more:"   │
│                                                          │
│  Q1: "Is this a new install or existing equipment?"     │
│  Q2: "Is it currently operational?"                     │
│  Q3: "Any known issues or symptoms?"                    │
│  Q4: "When was it last serviced?"                       │
│  Q5: "What's it connected to?" (PLC, network, etc)     │
│                                                          │
│  Each answer enriches the equipment record              │
└──────────────────────────┬──────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────┐
│              📝 PHASE 5: WORK ORDER + PLAN               │
│                                                          │
│  Bot proposes an action plan:                           │
│                                                          │
│  "Based on what I've learned, here's my recommendation:"│
│                                                          │
│  📋 Work Order #WO-001 Created:                         │
│  ┌───────────────────────────────────────┐              │
│  │ Equipment: Siemens KP300 Basic mono   │              │
│  │ Asset Tag: HMI-001                    │              │
│  │ Location: [user specified]            │              │
│  │ Type: [Install/PM/Repair]             │              │
│  │ Priority: [based on detective answers]│              │
│  │                                        │              │
│  │ Proposed Tasks:                        │              │
│  │ □ Configure via TIA Portal             │              │
│  │ □ Set PROFINET IP address              │              │
│  │ □ Map function keys to PLC tags        │              │
│  │ □ Download config to panel             │              │
│  │ □ Test all F-keys                      │              │
│  │ □ Document in CMMS                     │              │
│  └───────────────────────────────────────┘              │
│                                                          │
│  [✅ Approve Plan] [✏️ Modify] [❌ Cancel]               │
└──────────────────────────┬──────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────┐
│           🔄 PHASE 6: ONGOING RELATIONSHIP               │
│                                                          │
│  Equipment is now in the system. Future interactions:    │
│                                                          │
│  • "Having trouble with the KP300" → pulls context      │
│  • "Show me the wiring diagram" → from indexed manual   │
│  • "What fault codes does this support?" → from KB      │
│  • "Schedule PM for next month" → creates WO            │
│  • Photo of error screen → AI diagnosis with context    │
│  • PLC bridge: live data from connected equipment       │
│                                                          │
│  Every interaction enriches the equipment history        │
└─────────────────────────────────────────────────────────┘
```

## Key Principles

1. **Detective First** — Don't assume. Ask. Gather intel before acting.
2. **One Component at a Time** — Each photo = one asset in CMMS
3. **Manual is Step 1** — Can't troubleshoot what you don't understand
4. **Propose, Don't Impose** — Show the plan, let user approve/modify
5. **Build History** — Every interaction adds to the equipment's story
6. **Smart Questions** — Based on equipment type, ask relevant questions
   - HMI → "What PLC is it connected to?"
   - Motor → "What's the rated HP? VFD controlled?"
   - Sensor → "What's it measuring? Analog or digital?"
