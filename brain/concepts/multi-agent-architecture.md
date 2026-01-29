# Multi-Agent Architecture

## The Concept

Instead of one AI doing everything, deploy multiple specialized AI agents that work in parallel, each optimized for specific tasks.

```
┌─────────────────────────────────────────┐
│           ORCHESTRATOR (Opus)           │
│      Strategic decisions, user IF       │
└─────────────────────────────────────────┘
         │              │              │
    ┌────┴────┐    ┌────┴────┐    ┌────┴────┐
    │ Worker  │    │ Worker  │    │ Worker  │
    │(Sonnet) │    │(Sonnet) │    │ (Haiku) │
    └─────────┘    └─────────┘    └─────────┘
```

## Why It Works

### 1. Cost Optimization
- Use expensive models (Opus) only for complex reasoning
- Use cheap models (Haiku, Groq) for routine tasks
- 10-100x cost reduction on bulk work

### 2. Parallelization
- Multiple agents working simultaneously
- No waiting for one task to finish before starting another
- 24/7 coverage without fatigue

### 3. Specialization
- Each agent develops expertise in its domain
- Better prompts, better results
- Cleaner separation of concerns

### 4. Fault Isolation
- One agent failing doesn't break others
- Can restart individual agents
- Easier debugging

## Our Implementation

| Agent | Model | Schedule | Role |
|-------|-------|----------|------|
| Jarvis Prime | Opus | Always on | Strategy, Mike interface |
| Code Agent | Sonnet | Every 30 min | PRs, debugging |
| Monitor Agent | Haiku | Every 15 min | Health checks |

## Coordination Protocol

### Shared Workspace
All agents read/write to `/root/jarvis-workspace`:
- `memory/` — Daily logs, everyone writes
- `signals/inbox/` — Task queue
- `signals/outbox/` — Completed reports
- `brain/` — Knowledge documents

### Escalation Path
```
Monitor detects issue → tries simple fix
                      → if fails, escalates to Code Agent
                      → if still fails, escalates to Prime
                      → Prime decides whether to wake Mike
```

## Scaling

| Budget | Agents | Configuration |
|--------|--------|---------------|
| $100/mo | 5-7 | 1 Opus + 2 Sonnet + 3 Haiku |
| $200/mo | 10-15 | 2 Opus + 5 Sonnet + 8 Haiku |
| $500/mo | 20-30 | Full specialized team |

## Key Insight

> "The goal isn't to have one super-intelligent AI. It's to have a team of competent AIs that together exceed what any single AI could do."

This mirrors how human organizations work — specialists coordinated by management.

---

*Concept documented: 2026-01-29*
*Related: Constitution Article IV (One-Team Principle)*
