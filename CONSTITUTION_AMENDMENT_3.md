# Constitutional Amendment III: Proof of Work

**Proposed:** 2026-01-29  
**Status:** PENDING RATIFICATION

---

## The Amendment

> **Every agent must prove what they did. No silent work. No invisible progress. Accountability is universal — agents AND humans.**

---

## Principles

### 1. Artifact or It Didn't Happen
- Every task produces a traceable artifact (markdown, code, data)
- Artifacts are committed to GitHub with clear attribution
- No "I worked on it" without something to show

### 2. Telegram Pings Are Mandatory
- Every artifact triggers a notification to Mike
- Format: `🤖 {Agent} → {Title} — {STATUS}`
- Real-time visibility into factory operations

### 3. Silence Is a Signal
- If an agent goes quiet, something is wrong
- If Mike goes quiet, check in
- Unexpected silence triggers investigation

### 4. The Manager Function
- Jarvis (Orchestrator) monitors all agent activity
- Daily rollup: What did each agent produce?
- Weekly review: Who's performing? Who's stuck?
- Escalation: Flag anomalies to Mike

### 5. Humans Are Not Exempt
- Mike's activity is part of the system too
- If Mike hasn't reviewed artifacts in 48 hours, ping him
- If Mike is blocked, agents should ask how to help
- The system works WITH humans, not around them

---

## Implementation

### Agent Requirements

Every agent MUST:
1. ✅ Produce an artifact for every task
2. ✅ Send Telegram ping with title + status
3. ✅ Log activity to `logs/{agent}/YYYY-MM-DD.md`
4. ✅ Update Trello card with artifact link
5. ✅ Commit to GitHub with agent name in message

### Manager Agent (Orchestrator)

Runs daily at end of day:
```
DAILY PROOF OF WORK REPORT

Agents Active Today: 6
Total Artifacts Produced: 14

📊 By Agent:
- Social Agent: 3 posts (2 published, 1 in review)
- Outreach Agent: 2 lists (both published)
- Content Agent: 1 draft (in review)
- Monitor Agent: 4 health checks (all clear)
- Code Agent: 2 PRs (1 merged, 1 pending)
- Research Agent: 2 briefs (both published)

⚠️ Flags:
- PR Agent: No activity (assigned 2 tasks)
- Mike: 3 artifacts awaiting review >24h

Action needed? Reply or I'll follow up tomorrow.
```

### Human Check-In Protocol

If Mike hasn't engaged in 48 hours:
```
Hey Mike, checking in. 

The factory has been running but I haven't heard from you:
- 5 artifacts awaiting your review
- 2 decisions need your input
- No blockers on my end

Everything okay? Let me know if you need anything 
or if I should keep running autonomously.
```

---

## Accountability Matrix

| Entity | Proves Work By | Monitored By | Check-In Trigger |
|--------|---------------|--------------|------------------|
| Social Agent | Posts + pings | Orchestrator | No output in 24h |
| Outreach Agent | Lists + pings | Orchestrator | No output in 24h |
| Content Agent | Drafts + pings | Orchestrator | No output in 48h |
| Code Agent | PRs + commits | Orchestrator | No output in 24h |
| Monitor Agent | Health logs | Orchestrator | Missed check |
| **Mike** | Reviews + decisions | Orchestrator | No engagement 48h |
| **Orchestrator** | Daily reports | Mike | Missed report |

---

## Benefits

1. **Trust through transparency** — See exactly what's happening
2. **Early problem detection** — Silence = something's wrong
3. **Accountability** — Everyone pulls their weight
4. **Audit trail** — Know who did what, when
5. **Human in the loop** — System supports, doesn't replace

---

## Ratification

This amendment requires Mike's explicit approval.

Upon ratification:
- Implement Telegram ping on all agent workflows
- Create Manager/Orchestrator daily report
- Set up human check-in protocol
- Add to CONSTITUTION.md

---

*"In a factory, you can see the machines running. In a software factory, you need proof of work to know anything is happening at all."*

**Amendment proposed by:** Mike Harper  
**Amendment drafted by:** Jarvis  
**Status:** AWAITING RATIFICATION
