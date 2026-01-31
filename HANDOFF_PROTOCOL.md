# Agent Handoff Protocol

*Version 1.0 — 2026-01-30*
*GitHub Issue: #14*

---

## Purpose

Defines how Jarvis instances (and future agents) transfer context and tasks between each other. Based on A2A Protocol patterns but simplified for our current architecture.

---

## The Problem

When a session ends, context is lost. The next Jarvis instance starts fresh and must:
1. Read MEMORY.md, SOUL.md, USER.md
2. Guess what was in progress
3. Hope nothing was missed

This is fragile. We need explicit handoffs.

---

## The Solution: NEXT_STEPS.md

A living document at workspace root that captures:
- What's in progress
- What needs to happen next
- Blockers and dependencies
- Priority order

### File Location
`/root/jarvis-workspace/NEXT_STEPS.md`

### Template

```markdown
# NEXT_STEPS.md

*Last Updated: YYYY-MM-DD HH:MM UTC*
*Updated By: [Agent/Session]*

---

## 🔴 In Progress (Do Not Interrupt)

| Task | Started | ETA | Notes |
|------|---------|-----|-------|
| [Task Name] | HH:MM | +Xmin | [Context] |

---

## 🟡 Queued (Ready to Start)

### Priority 1 (Do First)
- [ ] **[Task]** — [Brief description]
  - Depends on: [None / Task X]
  - Autonomy: 🤖/✅/🔐
  - Est: X min

### Priority 2
- [ ] **[Task]** — [Brief description]
  - Est: X min

---

## 🟢 Completed Today

- [x] **[Task]** — [Outcome] *(HH:MM)*

---

## ⚫ Blocked

| Task | Blocker | Waiting On |
|------|---------|------------|
| [Task] | [What's blocking] | [Mike / External / Resource] |

---

## Context for Next Agent

[Free-form notes: What the next instance needs to know that isn't captured above]
```

---

## Protocol Rules

### 1. Update on Transition
Before ending any significant work session, update NEXT_STEPS.md with current state.

### 2. Read on Start
New sessions/agents should read NEXT_STEPS.md before starting work.

### 3. Claim Before Working
If taking a queued task, move it to "In Progress" first to prevent collisions.

### 4. Complete Explicitly
When done, move to "Completed" with timestamp and outcome.

### 5. Block Explicitly
If stuck, move to "Blocked" with clear description of what's needed.

---

## Integration with Constitution

- **Amendment III (Proof of Work)** — NEXT_STEPS.md IS proof of work
- **Amendment IV (Proactive Next Steps)** — This is WHERE next steps live
- **Article IV (One-Team)** — Enables coordination across instances

---

## Cron Integration

Heartbeat checks should include:
1. Read NEXT_STEPS.md
2. Work queued items if autonomy allows
3. Update status before ending

---

## Future: A2A Integration

When we implement full A2A Protocol:
- NEXT_STEPS.md becomes the local task queue
- A2A endpoints can push/pull tasks
- Agent Cards describe capabilities
- Handoffs become formal API calls

For now, the file-based approach works for our single-orchestrator model.

---

*"Explicit handoffs prevent dropped balls."*
