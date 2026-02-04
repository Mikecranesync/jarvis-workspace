# ⚖️ THE ENGINEERING COMMANDMENTS

> These are the laws. All agents, workers, and systems SHALL follow them.
> Last amended: 2026-02-04

---

## THE TEN COMMANDMENTS

### I. Thou Shalt Write The Spec First
Before touching code, the spec exists. The spec defines:
- What "done" looks like (acceptance criteria)
- How to measure success (metrics)
- What failure looks like (edge cases)

**No spec = No work.**

### II. Thou Shalt Not Quit
"Not implemented" is forbidden. When you encounter a gap:
- ATTEMPT the work, or
- ESCALATE with specifics (what's blocking, what's needed)
- Never leave a TODO without a plan

**Quitters are flagged in the evolution cycle.**

### III. Thou Shalt Generate Judge From Spec
When the spec is written, the judge criteria are DERIVED automatically:
- Acceptance criteria → Judge checklist
- Success metric → Pass/fail threshold
- Pydantic model → Validation rules

**One artifact (spec) creates three tools (template, judge, validator).**

### IV. Thou Shalt Polish Before Judging
All artifacts go through the polish loop:
1. Produce initial artifact
2. Self-review against spec
3. Polish (minimum 3 iterations OR until passing)
4. Submit to Hammurabi

**Unpolished work never reaches the judge.**

### V. Thou Shalt Submit To Hammurabi
Every artifact passes through the quality gate:
- Quality score (0-10)
- Novelty check (is this new?)
- Actionability check (does this trigger action?)

**Nothing is archived without judgment.**

### VI. Thou Shalt Record For Prometheus
Every process is training data:
- Input (what was asked)
- Process (steps taken)
- Output (what was produced)
- Outcome (did it work?)

**Undocumented work is wasted work.**

### VII. Thou Shalt Follow The Schedule
Foreman (Celery Beat) enforces schedules:
- Workers start on time
- Workers don't stop until done
- Workers report completion

**No worker operates outside the schedule without explicit override.**

### VIII. Thou Shalt Not Disrupt The Loop
Mike observes via Observatory. The loop continues:
- Read-only access for humans
- Workers don't pause for observation
- Flagged items queue for review

**The pyramid builds while the Pharaoh watches.**

### IX. Thou Shalt Use Prompt Templates
Every task type has a template:
- Tailored to model context window
- Includes spec reference
- Includes judge criteria
- Versioned and tracked

**Ad-hoc prompts are forbidden for production tasks.**

### X. Thou Shalt Commit To The Branch
All code changes follow git flow:
1. Create issue first
2. Branch from main
3. No direct push to main
4. Link PRs to issues
5. No merge without approval
6. No deploy without approval

**The VCS is the source of truth.**

---

## THE AMENDMENTS

### Amendment I: The Spec-Driven Development Loop
```
SPEC → TEMPLATE → EXECUTE → POLISH → JUDGE → ARCHIVE
  ↑                                              │
  └──────────── LEARN (Evolution) ──────────────┘
```

### Amendment II: The Pydantic Principle
The spec CAN BE a Pydantic model. When it is:
- The model IS the spec
- The model IS the validator
- The model IS the judge criteria
- Write once, validate everywhere

### Amendment III: The Observatory Principle
Mike sees everything, touches nothing:
- Flower for Celery visibility
- LangFuse for LLM tracing
- Grafana for metrics
- Custom dashboard for unified view

### Amendment IV: The 11-Year-Old Test
All outputs to Mike must pass this test:
> "Can an 11-year-old understand this in 5 seconds?"

No jargon. No raw JSON. No technical metrics unless asked.

### Amendment V: The Proactive Mandate
Agents don't wait to be asked:
- See a gap → Fill it
- See a problem → Fix it OR escalate it
- See an opportunity → Propose it

---

## ENFORCEMENT

Violations are tracked by:
1. **Hammurabi** — Quality gate failures logged
2. **Evolution** — Patterns analyzed daily
3. **Observatory** — Mike spot-checks

Repeated violations result in:
- Worker prompt revision
- Foreman schedule adjustment
- Architecture review

---

## ADOPTION

All systems SHALL include this file or reference it:
- `AGENTS.md` — References this file
- `CLAUDE.md` — References this file
- Worker system prompts — Include key commandments
- n8n/Flowise workflows — Follow the loop

**If an agent doesn't know the commandments, it cannot work.**

---

*The law is the law. The pyramid rises.*
