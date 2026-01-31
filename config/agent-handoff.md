# Agent Handoff Protocol

**Status:** IMPLEMENTED
**Created:** 2026-01-30
**Updated:** 2026-01-30

---

## Overview

This protocol ensures continuity when one agent completes a task and another needs to pick it up. Every task ends with a clear handoff document.

---

## The Handoff Document: NEXT_STEPS.md

After completing any significant task, agents create/update a `NEXT_STEPS.md` file with:

```markdown
# Next Steps for [Task/Project Name]

## Status
- **Last Action:** [What was just done]
- **Completed By:** [Agent name/type]
- **Timestamp:** [ISO 8601]
- **Trello Card:** [Card ID if applicable]

## Handoff To
**Next Agent:** [Agent type or @mike for human]
**Priority:** [P0/P1/P2]
**Deadline:** [If applicable]

## Context
[2-3 sentences of essential context for the next agent]

## Immediate Next Actions
1. [First thing to do]
2. [Second thing to do]
3. [Third thing to do]

## Blockers
- [Any blockers or dependencies]

## Files Modified
- `path/to/file1.md`
- `path/to/file2.py`

## Notes for Next Agent
[Any gotchas, warnings, or tips]
```

---

## Agent Types

| Agent | Responsibilities | Typical Handoffs |
|-------|-----------------|------------------|
| **Jarvis (Main)** | Orchestration, user communication | Any agent |
| **Content Agent** | Blog posts, LinkedIn, documentation | QA Judge → Mike |
| **Outreach Agent** | Cold emails, prospect lists | Mike (for approval) |
| **PR Agent** | Podcasts, press, partnerships | Mike (for outreach) |
| **Code Agent** | Development, PRs, debugging | QA Judge → Mike |
| **Research Agent** | Web research, analysis | Requesting agent |
| **QA Judge** | Review drafts, check quality | Mike or original agent |

---

## Handoff Rules

### Rule 1: Every Task Gets a Handoff
Even if you think you're done, create the handoff. Future you (or another agent) will thank you.

### Rule 2: Be Specific
"Do more research" is bad. "Search for 3 competitor pricing pages and summarize in a table" is good.

### Rule 3: Include Files
Always list which files were created or modified. Agents can't read minds.

### Rule 4: Tag the Next Agent
Use clear tagging:
- `@mike` - Needs human action
- `@content-agent` - Content creation
- `@code-agent` - Development task
- `@qa-judge` - Needs review
- `@anyone` - Any available agent can pick up

### Rule 5: Escalate Blockers
If something is blocked, say so clearly and tag Mike.

---

## Example Handoffs

### Example 1: Content to QA

```markdown
# Next Steps for LinkedIn Post #1

## Status
- **Last Action:** Drafted LinkedIn post on CMMS failures
- **Completed By:** Content Agent
- **Timestamp:** 2026-01-30T17:21:00Z
- **Trello Card:** 697b6d236e067fdd5074978a

## Handoff To
**Next Agent:** @qa-judge
**Priority:** P1
**Deadline:** Before Mike's review

## Context
First of 3 LinkedIn posts. 207 words, professional tone, backed by research.
Topic: Why 50%+ of CMMS implementations fail.

## Immediate Next Actions
1. Review for tone consistency
2. Check statistics are accurate
3. Verify CTA is engaging

## Blockers
- None

## Files Modified
- `artifacts/drafts/social-agent/linkedin-post-1-cmms-failures.md`

## Notes for Next Agent
I used 3 sources (cited in the file). The 50% failure stat comes from tractian.com.
```

### Example 2: Code to Mike

```markdown
# Next Steps for Trello Webhook

## Status
- **Last Action:** Created PR #47 with webhook implementation
- **Completed By:** Code Agent
- **Timestamp:** 2026-01-30T15:00:00Z
- **Trello Card:** N/A

## Handoff To
**Next Agent:** @mike
**Priority:** P0
**Deadline:** Before deployment

## Context
Webhook receives Trello card moves and triggers agent actions.
PR is ready for review. CI passes.

## Immediate Next Actions
1. Review PR #47
2. Test webhook locally
3. Approve and merge
4. Deploy to production

## Blockers
- Needs Mike's approval per Commandment V

## Files Modified
- `projects/trello_webhook/server.py`
- `projects/trello_webhook/requirements.txt`
- `README.md`

## Notes for Next Agent
Webhook secret is in .env file. Test URL: http://localhost:8000/trello-webhook
```

---

## Where to Store Handoffs

**Project-specific:**
- `projects/[project-name]/NEXT_STEPS.md`

**Agent-specific:**
- `agents/[agent-name]/NEXT_STEPS.md`

**Global (cross-project):**
- `/root/jarvis-workspace/NEXT_STEPS.md`

---

## Automation

The cron jobs should:
1. Check for `NEXT_STEPS.md` files
2. Route to appropriate agent based on `Handoff To` field
3. Update Trello card status
4. Clear handoff after pickup

### Cron Check (Every 5 min)

```bash
# Pseudo-logic for handoff processing
for file in $(find . -name "NEXT_STEPS.md"); do
  next_agent=$(grep "Next Agent:" "$file" | cut -d: -f2)
  if [ "$next_agent" == "@self" ]; then
    # Pick up and execute
    process_handoff "$file"
  fi
done
```

---

## Templates

### Quick Handoff (Simple Tasks)

```markdown
# Next Steps

**Done:** [What you did]
**Next:** @[agent] — [What they should do]
**Files:** [List of files]
```

### Full Handoff (Complex Tasks)

Use the full template above.

---

## Commit Protocol

After completing a task:

1. Create/update NEXT_STEPS.md
2. `git add .`
3. `git commit -m "[agent]: Complete [task] - handoff to @[next]"`
4. `git push`

This ensures continuity survives restarts.

---

**Implementation Complete**
