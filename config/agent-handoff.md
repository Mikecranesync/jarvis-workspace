# Agent Handoff System

**Created:** 2026-01-29  
**Status:** ACTIVE

## The Rule

> **Every agent, after completing ANY task, MUST:**
> 1. Commit their work (artifact to repo)
> 2. Create/update `NEXT_STEPS.md` in the artifact folder
> 3. Tag the next responsible agent
> 4. Send Telegram ping

---

## NEXT_STEPS.md Template

Every artifact folder gets a `NEXT_STEPS.md`:

```markdown
# Next Steps

**Last Updated:** {timestamp}
**Last Agent:** {agent-name}
**Artifact:** {path-to-artifact}

## Completed
- [x] {what this agent did}

## Next Actions
- [ ] {action 1} → **@{next-agent}**
- [ ] {action 2} → **@{next-agent}**

## Blocked (if any)
- {blocker} → **@mike** or **@jarvis**

## Context for Next Agent
{Brief context the next agent needs to pick this up}
```

---

## Agent Routing Rules

### Social Agent → 
| Output | Routes To |
|--------|-----------|
| Draft post | QA Judge |
| Approved post | Mike (for publish) |
| Rejected post | Social Agent (revision) |

### Outreach Agent →
| Output | Routes To |
|--------|-----------|
| Prospect list | Mike (review) |
| Draft email | QA Judge |
| Approved email | Mike (send) |

### Content Agent →
| Output | Routes To |
|--------|-----------|
| Blog draft | QA Judge |
| Approved blog | Mike (publish) |

### PR Agent →
| Output | Routes To |
|--------|-----------|
| Podcast list | Mike (review) |
| Pitch draft | QA Judge |
| Approved pitch | Mike (send) |

### QA Judge →
| Output | Routes To |
|--------|-----------|
| PASS | Original agent → Mike |
| FAIL | Original agent (revision) |

### Code Agent →
| Output | Routes To |
|--------|-----------|
| PR created | Mike (review) |
| PR merged | Monitor Agent |

---

## Handoff Flow

```
Agent A starts task
    ↓
Agent A produces artifact
    ↓
Agent A commits to repo
    ↓
Agent A creates/updates NEXT_STEPS.md
    ↓
Agent A sends Telegram ping
    ↓
Agile Agent reads NEXT_STEPS.md
    ↓
Agile Agent routes to Agent B (or Mike)
    ↓
Agent B picks up, repeats cycle
```

---

## Example: Social Agent Handoff

**Social Agent completes LinkedIn post draft:**

1. **Commits:**
```bash
git add artifacts/drafts/social-agent/2026-01-29-linkedin-cmms.md
git commit -m "[social-agent] draft: LinkedIn post on CMMS failures"
```

2. **Creates NEXT_STEPS.md:**
```markdown
# Next Steps

**Last Updated:** 2026-01-29 14:30 UTC
**Last Agent:** Social Agent
**Artifact:** artifacts/drafts/social-agent/2026-01-29-linkedin-cmms.md

## Completed
- [x] Drafted LinkedIn post: "Why CMMS Implementations Fail"
- [x] Added hashtags and CTA
- [x] Validated against schema

## Next Actions
- [ ] QA validation against rubric → **@qa-judge**
- [ ] If approved, route to Mike for publish → **@mike**

## Context for Next Agent
Post targets maintenance managers frustrated with failed CMMS rollouts.
Key angle: Implementation is harder than buying software.
CTA: "What's your biggest CMMS challenge?"
```

3. **Sends Ping:**
```
🤖 Social Agent → LinkedIn Draft: Why CMMS Fails — 📝 DRAFT → @qa-judge
```

---

## Agile Agent Responsibilities

The Agile Agent (every 5 min) must:

1. Scan all `NEXT_STEPS.md` files in artifacts/
2. Find any with pending actions
3. Check if tagged agent can pick up
4. If agent is available, trigger them
5. If blocked, escalate to Mike

---

## Future: A2A Protocol Integration

When we scale beyond simple file-based handoff:

1. Each agent gets an **Agent Card** (capability manifest)
2. Agents discover each other via A2A protocol
3. Task passing via JSON-RPC
4. Full observability and tracing
5. No LangChain licensing costs (A2A is Apache 2.0)

**For now:** File-based NEXT_STEPS.md is sufficient.

---

## Enforcement

- No artifact without NEXT_STEPS.md update
- Compliance Agent checks for orphaned tasks
- Missing handoff = violation flagged

---

*"A task without a next owner is a task that dies."*
