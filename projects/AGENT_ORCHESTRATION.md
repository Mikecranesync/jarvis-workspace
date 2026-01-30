# Agent Orchestration Architecture

**Created:** 2026-01-29  
**Status:** ARCHITECTURE PROPOSAL

---

## The Challenge

With dozens of agents running 24/7, we need:
1. **Artifact trails** — Every action produces a traceable file
2. **QA gates** — LLM-as-Judge validates before shipping
3. **Coordination** — No conflicts, no duplicate work
4. **Observability** — Know what's happening at all times

---

## Research Findings: Current Best Practices

### Multi-Agent Frameworks (2025/2026)

| Framework | Best For | Our Use |
|-----------|----------|---------|
| **LangGraph** | Stateful workflows, complex branching | Orchestration layer |
| **CrewAI** | Role-based agents, collaboration | Agent definitions |
| **AutoGen** | Async conversations, tool execution | Individual agents |
| **Langfuse** | Observability, tracing, logging | Monitoring |

**Recommendation:** Hybrid approach
- Use **Clawdbot cron** as the scheduler (already working)
- Implement **LLM-as-Judge** for QA gates
- Store all artifacts in **GitHub** (issues, PRs, markdown files)
- Log everything to **Trello** under agent names

### LLM-as-Judge Pattern

From research:
- Use a separate LLM to evaluate agent outputs
- Chain-of-thought reasoning for transparent decisions
- Rubrics for consistent scoring
- Pass/fail gates before artifacts are "shipped"

---

## Proposed Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     JARVIS ORCHESTRATION LAYER                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐     │
│  │ Scheduler│   │  Router  │   │   QA     │   │ Artifact │     │
│  │ (Cron)   │──▶│          │──▶│ (Judge)  │──▶│ Manager  │     │
│  └──────────┘   └──────────┘   └──────────┘   └──────────┘     │
│       │              │              │              │            │
│       ▼              ▼              ▼              ▼            │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                    AGENT FLEET                          │   │
│  │  ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐           │   │
│  │  │Social  │ │Outreach│ │Content │ │  PR    │ ...       │   │
│  │  │Agent   │ │Agent   │ │Agent   │ │ Agent  │           │   │
│  │  └────────┘ └────────┘ └────────┘ └────────┘           │   │
│  └─────────────────────────────────────────────────────────┘   │
│       │              │              │              │            │
│       ▼              ▼              ▼              ▼            │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                    OUTPUT LAYER                         │   │
│  │  ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐           │   │
│  │  │ Trello │ │ GitHub │ │Markdown│ │  Logs  │           │   │
│  │  │ Cards  │ │Issues  │ │ Files  │ │        │           │   │
│  │  └────────┘ └────────┘ └────────┘ └────────┘           │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Agent Workflow Standard

Every agent follows this workflow:

```
1. TRIGGER (cron/event)
       │
       ▼
2. WORK (agent executes task)
       │
       ▼
3. PRODUCE DRAFT ARTIFACT
   └── Save to: artifacts/drafts/{agent}/{date}-{task}.md
       │
       ▼
4. QA GATE (LLM-as-Judge)
   ├── PASS → Continue
   └── FAIL → Flag for human review
       │
       ▼
5. COMMIT ARTIFACT
   ├── Move to: artifacts/published/{agent}/
   ├── Create GitHub commit
   └── Log to Trello (agent's name)
       │
       ▼
6. TELEGRAM PING (required)
   └── Send one-liner to Mike: "{Agent} → {Title} — {STATUS}"
       │
       ▼
7. REPORT
   └── Update agent log: logs/{agent}/YYYY-MM-DD.md
```

---

## Telegram Notification Format

Every artifact produces a Telegram ping:

```
🤖 {AGENT} → {Artifact Title} — {STATUS}
```

### Status Types
| Status | Emoji | Meaning |
|--------|-------|---------|
| `DRAFT` | 📝 | Work in progress |
| `REVIEW` | 👀 | Ready for Mike's review |
| `PUBLISHED` | ✅ | Shipped/committed |
| `REJECTED` | ❌ | Failed QA, needs revision |
| `BLOCKED` | 🚫 | Needs human input |

### Examples
```
🤖 Social Agent → LinkedIn Post: PLC Debugging with AI — 👀 REVIEW
🤖 Outreach Agent → Prospect List (+15 contacts) — ✅ PUBLISHED  
🤖 Content Agent → Blog Draft: CMMS ROI Calculator — 📝 DRAFT
🤖 QA Judge → Social Post rejected: needs CTA — ❌ REJECTED
```

This gives Mike real-time factory visibility without checking Trello.

---

## Artifact Structure

```
jarvis-workspace/
├── artifacts/
│   ├── drafts/                    # Pre-QA outputs
│   │   ├── social-agent/
│   │   ├── outreach-agent/
│   │   ├── content-agent/
│   │   └── pr-agent/
│   │
│   ├── published/                 # Post-QA, committed
│   │   ├── social-agent/
│   │   │   └── 2026-01-29-linkedin-post-1.md
│   │   ├── outreach-agent/
│   │   │   └── 2026-01-29-prospect-list.md
│   │   └── ...
│   │
│   └── rejected/                  # Failed QA
│       └── {agent}/{date}-{task}.md
│
├── logs/
│   ├── orchestrator/              # Master coordination log
│   │   └── 2026-01-29.md
│   ├── social-agent/
│   │   └── 2026-01-29.md
│   └── ...
│
└── config/
    ├── agents.yaml                # Agent definitions
    ├── qa-rubrics.yaml            # QA criteria per agent
    └── routing.yaml               # Task routing rules
```

---

## QA Gate: LLM-as-Judge

### Judge Prompt Template

```
You are a QA judge for the {agent_name} agent.

## Task Completed
{task_description}

## Artifact Produced
{artifact_content}

## Evaluation Criteria
{rubric}

## Your Job
1. Evaluate the artifact against the criteria
2. Provide chain-of-thought reasoning
3. Give a PASS or FAIL verdict
4. If FAIL, explain what needs improvement

## Output Format
REASONING: <your analysis>
VERDICT: PASS or FAIL
FEEDBACK: <specific improvement suggestions if FAIL>
```

### Rubrics by Agent Type

**Social Agent:**
- [ ] Content is relevant to industrial AI/maintenance
- [ ] Professional tone appropriate for LinkedIn
- [ ] Includes call-to-action or engagement hook
- [ ] No confidential information exposed
- [ ] Correct spelling/grammar

**Outreach Agent:**
- [ ] Personalized to recipient (not generic)
- [ ] Clear value proposition
- [ ] Professional but human tone
- [ ] Appropriate length (not too long)
- [ ] Clear next step/CTA

**Content Agent:**
- [ ] Accurate technical information
- [ ] Well-structured with clear sections
- [ ] Actionable insights included
- [ ] Appropriate for target audience
- [ ] Properly cited sources

---

## Trello Integration

### Agent Naming Convention
Each Trello card created by an agent includes:
- **Card Title:** `[AGENT-NAME] Task Description`
- **Labels:** Agent name label + status label
- **Description:** Link to artifact in GitHub
- **Checklist:** Task breakdown + completion status

### Example Card
```
Title: [SOCIAL-AGENT] LinkedIn Post: PLC Debugging with AI
Labels: social-agent, content, published
Description: 
  Artifact: github.com/mikecranesync/factorylm/artifacts/published/social-agent/2026-01-29-linkedin-post-1.md
  QA Status: PASSED
  Published: 2026-01-29 14:30 UTC
```

---

## GitHub Integration

### Commit Convention
```
[{agent-name}] {action}: {description}

Examples:
[social-agent] publish: LinkedIn post on PLC debugging
[outreach-agent] update: Prospect list +15 contacts
[content-agent] draft: Blog post on CMMS ROI
[qa-judge] reject: Social post - needs revision
```

### Branch Strategy
- `main` — Human-approved, production content
- `agent/{agent-name}` — Agent work branches
- PRs required for anything going to main

---

## Coordination: Preventing Conflicts

### Task Locking
Before an agent starts a task:
1. Check `locks/{task-id}.lock` file
2. If exists, skip (another agent working)
3. If not, create lock file with agent name + timestamp
4. On completion, remove lock

### Deduplication
- Each task has unique ID based on: `{type}-{target}-{date}`
- Check `completed/{date}.json` before starting
- Log completed tasks to prevent re-work

---

## Implementation Plan

### Phase 1: Foundation (This Week)
1. [ ] Create artifact directory structure
2. [ ] Create log file templates
3. [ ] Implement QA judge prompt
4. [ ] Test with Social Agent

### Phase 2: Rollout (Week 2)
5. [ ] Apply pattern to Outreach Agent
6. [ ] Apply pattern to Content Agent
7. [ ] Apply pattern to PR Agent
8. [ ] Create orchestrator dashboard

### Phase 3: Scale (Week 3+)
9. [ ] Automated conflict resolution
10. [ ] Performance metrics dashboard
11. [ ] Self-healing capabilities
12. [ ] Consider LangGraph for complex workflows

---

## Open Source Tools to Consider

| Tool | Purpose | GitHub |
|------|---------|--------|
| **Langfuse** | LLM observability & tracing | github.com/langfuse/langfuse |
| **LangGraph** | Stateful agent workflows | github.com/langchain-ai/langgraph |
| **CrewAI** | Role-based agent teams | github.com/crewai/crewai |
| **Instructor** | Structured LLM outputs | github.com/jxnl/instructor |
| **Pydantic AI** | Type-safe agent outputs | github.com/pydantic/pydantic-ai |

---

## Can Jarvis Coordinate This?

**Honest answer:** Yes, with structure.

Current Clawdbot + cron jobs can handle this IF:
1. Clear artifact conventions (defined above)
2. QA gates prevent bad outputs
3. Everything logged to files + GitHub
4. Trello provides human visibility

**Scaling concerns:**
- At 10+ agents, may need dedicated orchestrator
- LangGraph could help with complex dependencies
- Langfuse for observability as volume increases

**For now:** Start simple, add complexity as needed. The artifact trail and QA gates are the critical foundation.

---

*"The goal is not to build the most sophisticated orchestration system. It's to ship products while maintaining quality and traceability."*
