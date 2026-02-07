# FactoryLM — YC Pitch Deck Core Thesis

**Deadline:** Feb 9, 2026 11:59 PM EST

---

## THE ONE-LINER (80 chars)

> "Logic-first CMMS that makes 98% of maintenance requests free."

**Alt:**
> "Poka-yoke maintenance system — AI is the last resort, not the first."

---

## THE PROBLEM (What everyone else gets wrong)

**The industry is drunk on AI.**

Every maintenance software company is racing to add more LLMs, more tokens, more compute. They're building expensive, fragile, slow systems that still produce garbage because **garbage in = garbage out**.

**The real problem isn't intelligence. It's data quality.**

- Technicians enter "pump" when they mean "Grundfos CR-150"
- Work orders have no photos, no context
- 30+ years of history sits in spreadsheets no AI can read
- Every LLM call starts from zero — no memory of YOUR equipment

---

## THE INSIGHT (Our unfair advantage)

> **"You don't need more AI. You need less chaos."**

We inverted the architecture:

| Everyone Else | FactoryLM |
|---------------|-----------|
| AI-first | Logic-first |
| Expensive | 98% free |
| Fragile | Poka-yoke robust |
| Stateless | Remembers everything |
| Generic knowledge | YOUR equipment history |

---

## THE ARCHITECTURE (Layer 0-3)

```
USER INPUT
    │
    ▼
┌─────────────────────────────────────┐
│ LAYER 0: PURE LOGIC (70% of requests)
│ • Poka-yoke validation
│ • Pattern matching
│ • Direct DB queries
│ • NO LLM — instant, FREE
└─────────────────────────────────────┘
    │ only if needed
    ▼
┌─────────────────────────────────────┐
│ LAYER 1: LOCAL KNOWLEDGE (20%)
│ • Cached responses
│ • Similar past answers
│ • Rule engine
│ • Still FREE
└─────────────────────────────────────┘
    │ only if needed
    ▼
┌─────────────────────────────────────┐
│ LAYER 2: LOCAL LLM (8%)
│ • Ollama / Mistral 7B
│ • Private, air-gapped capable
│ • Still FREE
└─────────────────────────────────────┘
    │ LAST RESORT
    ▼
┌─────────────────────────────────────┐
│ LAYER 3: CLOUD LLM (2%)
│ • Complex reasoning only
│ • Vision, long context
│ • PAID — but rare
└─────────────────────────────────────┘
    │
    ▼
LEARNING LOOP: Cloud answers → become local rules
              System gets SMARTER by needing LESS AI
```

---

## THE POKA-YOKE DIFFERENCE

**Traditional CMMS:**
```
User: "Add pump"
System: ✓ Created. (garbage data)
```

**FactoryLM:**
```
User: "Add pump"
System: "What kind? I see you have Grundfos pumps — is this one too?"
User: "Yeah"
System: "What's the nameplate say for HP and GPM?"
User: [sends photo]
System: "Got it — Grundfos CR-150, 5HP, 200GPM. Setting up quarterly PM 
        based on Grundfos specs. First check: March 7."
```

**Every entry becomes GOOD data because the LLM guardian won't accept lazy input.**

---

## THE MOAT

> "LLMs are encyclopedias. Maintenance needs a diary."

No context window — not 100k, not 1M tokens — can hold:
- Complete history of all YOUR assets
- What Joe tried last time this happened
- That this VFD hates humidity
- That the vendor always lies about lead times

**Your CMMS learns this. The LLM never will.**

**Our moat:** Every cloud answer hardens into Layer 0 logic. Competitors' costs grow with usage. Ours shrink.

---

## THE MARKET

- **$50B/year** lost to unplanned downtime (US manufacturing)
- **600,000** unfilled maintenance jobs
- **Average tech age:** 55 — knowledge walking out the door
- **Pain point:** $10K-$100K/hour downtime cost

---

## THE TRACTION

- Working system: Photo → Asset → Work Order (zero manual entry)
- Integrated CMMS (Atlas) with 38 assets tracked
- PLC connectivity (Allen-Bradley Micro820)
- Edge device architecture (Raspberry Pi gateway)
- One technical founder, 30+ years maintenance experience

---

## THE ASK

**$500K to:**
1. Launch public beta with 10 pilot customers
2. Prove the Layer 0 thesis at scale
3. Build the self-improving knowledge loop

**Milestones:**
- Month 1-2: 10 paying pilots
- Month 3-4: 100 assets managed, measure Layer 0 hit rate
- Month 5-6: First customer where 90%+ requests hit Layer 0

---

## THE FOUNDER

**30+ years as a maintenance technician.** Debugged PLCs at 2 AM with paper manuals. Learned to code to solve this problem.

> "My competitors are enterprise software companies who've never touched a wrench. I'm building the tool I wished I had."

---

## ONE SLIDE SUMMARY

```
╔═══════════════════════════════════════════════════════════════╗
║                        FACTORYLM                              ║
╠═══════════════════════════════════════════════════════════════╣
║                                                               ║
║  THESIS:    You don't need more AI. You need less chaos.     ║
║                                                               ║
║  HOW:       Logic-first architecture (Layer 0-3)             ║
║             98% of requests never hit paid AI                 ║
║             Poka-yoke makes bad data impossible              ║
║                                                               ║
║  MOAT:      Every AI answer becomes a rule                   ║
║             System gets cheaper as it gets smarter           ║
║                                                               ║
║  MARKET:    $50B/year problem, 600K unfilled jobs           ║
║                                                               ║
║  FOUNDER:   30+ years maintenance tech → taught self to code  ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
```

---

## FILES

- Architecture diagram: `/docs/architecture/factorylm-user-flow-bw.d2`
- PNG export: `/tmp/FactoryLM-BW.png`
- PDF export: `/tmp/FactoryLM-BW.pdf`
