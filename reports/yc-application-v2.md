# Y Combinator X26 Application — FactoryLM (v2)

**Deadline:** February 9, 2026 @ 11:59 PM EST

---

## COMPANY

### Company Name
**FactoryLM**

### One-liner (80 chars)
> Logic-first CMMS that makes 98% of maintenance requests free.

---

### What does your company do? (250 words max)

FactoryLM is a maintenance management system built backwards from everyone else.

The industry is racing to add more AI to maintenance software. We're doing the opposite — building a system where AI is the last resort, not the first.

Here's our architecture:
- **Layer 0 (70% of requests):** Pure logic. Pattern matching, validation, direct database queries. Instant. Free.
- **Layer 1 (20%):** Local knowledge base. Cached answers, similar past responses. Still free.
- **Layer 2 (8%):** Local LLM (Ollama). Runs on-site, air-gapped capable. Still free.
- **Layer 3 (2%):** Cloud AI. Only for complex reasoning. The only paid layer.

The secret: Every cloud AI answer gets converted into local rules. The system gets smarter by needing less intelligence.

We also built "poka-yoke" data entry — the system won't accept garbage. Send a photo of equipment and say "add pump"? It asks follow-up questions, reads the nameplate, and creates a complete asset record automatically. No more "garbage in, garbage out."

Why this matters: No LLM context window can hold 30+ years of YOUR equipment history. Generic AI knows how pumps work. Only YOUR system knows how YOUR Pump 3 works — its quirks, its history, what Joe tried last time it broke.

We're building the diary. AI is just the pen.

---

### Why did you pick this idea?

I was a maintenance technician for 30+ years before I learned to code.

I've watched the enterprise software industry spend billions building "AI-powered" maintenance tools that don't work. They fail because they put AI first and data quality last. You can't get good answers from bad data.

The insight came from my own experience: 90% of maintenance questions don't need AI at all. "When was this last serviced?" "What's the part number?" "Who worked on this before?" These are database queries, not LLM prompts.

I built FactoryLM to prove that maintenance software needs less AI, not more. The hard part isn't the intelligence — it's the organization, the data quality, the poka-yoke systems that prevent bad input in the first place.

My competitors are enterprise software companies who've never touched a wrench. They're building top-down platforms that cost $500K. I'm building bottom-up tools that work on day one because I know what actually happens at 2 AM when a machine breaks.

---

### Progress / Traction

- Working prototype: Photo → AI identification → Asset creation → Work order
- Integrated CMMS (Atlas) with 38 assets tracked
- PLC connectivity (Allen-Bradley Micro820)
- Edge device architecture (Raspberry Pi gateway running BalenaOS)
- Telegram bot interface (zero-friction for technicians)
- Full system running on cloud infrastructure
- One technical founder, built in 6 months

---

### How do you know people want this?

Three signals:

1. **Personal pain:** 30+ years watching technicians struggle with the same problems — wrong manuals, missing history, garbage data in CMMS systems that cost millions.

2. **Industry crisis:** 600,000 unfilled maintenance jobs. Average tech is 55. Companies are desperate for tools that let junior techs perform like veterans. The knowledge is walking out the door.

3. **Economic pressure:** $50B/year lost to unplanned downtime. Plants pay $10K-$100K per hour when a line goes down. Even small efficiency gains justify significant spend.

The first maintenance manager who saw the demo said: "This would have saved us $40K last month." Six hours of downtime because the tech couldn't find the right manual.

---

### Business Model

SaaS subscription per site:

- **Starter ($199/mo):** Up to 50 assets, Telegram bot, basic reporting
- **Pro ($499/mo):** Unlimited assets, CMMS integration, AI diagnostics
- **Enterprise (Custom):** On-prem deployment, PLC integration, custom training

Land with Telegram bot (zero friction), expand to full CMMS replacement.

---

### What's your long-term vision?

Phase 1: Best maintenance assistant (current)
Phase 2: Self-building CMMS (photo → complete asset record)
Phase 3: Predictive system (knows what will break before it does)
Phase 4: Autonomous maintenance scheduling (AI runs the PM program)

The moat deepens at each phase: Layer 0 accumulates more rules, Layer 1 builds more knowledge, cloud AI becomes increasingly unnecessary.

End state: A maintenance system that gets cheaper and smarter every month, while competitors' costs grow with usage.

---

### Why now?

1. **LLMs crossed the usefulness threshold** — but only as a component, not a product
2. **Edge AI is viable** — Ollama runs 7B models on commodity hardware
3. **Manufacturing is desperate** — labor shortage forces technology adoption
4. **Cloud costs are dropping** — makes the "logic-first" architecture even more compelling

---

### Competition

| Competitor | Approach | Problem |
|------------|----------|---------|
| Fiix, UpKeep | Traditional CMMS | Garbage in, garbage out. No AI. |
| Augury, Samsara | Sensors + AI | Expensive hardware. Top-down sales. |
| Generic AI (ChatGPT) | Pure LLM | No context. No memory. No YOUR data. |

**Our advantage:** Logic-first architecture. 98% free. System improves over time.

---

### 30-second pitch

"FactoryLM is maintenance software built backwards.

Everyone else is racing to add more AI. We built a system where 98% of requests never touch AI at all — they hit pure logic, local knowledge, and on-prem models. Only 2% reach the cloud.

The secret: every AI answer becomes a rule. The system gets smarter by needing less intelligence.

I was a maintenance tech for 30+ years. I'm building the tool I wish I had — and the moat gets deeper every day."
