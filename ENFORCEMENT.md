# Constitution Enforcement Mechanisms

**Created:** 2026-01-29  
**Principle:** Automation beats documentation. Rules that can be bypassed will be bypassed.

---

## The Problem

Documents don't enforce themselves. The Constitution, Amendments, and Commandments are worthless if agents (or humans) can ignore them. 

**Solution:** Build enforcement into the system itself. Make non-compliance technically difficult or impossible.

---

## Proven Enforcement Mechanisms

### 1. PRE-COMMIT HOOKS (Blocking Gate)
**What:** Code that runs before any git commit is accepted.  
**Enforces:** Commit message conventions, file structure, required files.

```bash
# .git/hooks/pre-commit
#!/bin/bash

# Check commit message format: [agent-name] action: description
if ! grep -qE '^\[.+\] .+: .+' "$1"; then
  echo "❌ Commit blocked: Message must follow format [agent-name] action: description"
  exit 1
fi

# Check that artifact exists for agent commits
AGENT=$(echo "$1" | grep -oP '\[\K[^\]]+')
if [[ -n "$AGENT" ]] && [[ ! -f "artifacts/drafts/$AGENT/"* ]] && [[ ! -f "artifacts/published/$AGENT/"* ]]; then
  echo "❌ Commit blocked: No artifact found for $AGENT"
  exit 1
fi

echo "✅ Pre-commit checks passed"
```

**Status:** ✅ Proven industry practice

---

### 2. GITHUB ACTIONS CI (Blocking Gate)
**What:** Automated checks that run on every PR.  
**Enforces:** Engineering Commandments, code quality, required reviews.

```yaml
# .github/workflows/enforcement.yml
name: Constitution Enforcement

on: [pull_request]

jobs:
  commandments-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Check for linked issue
        run: |
          # Commandment 1: Create GitHub Issue first
          if ! grep -q "Fixes #\|Closes #\|Resolves #" "${{ github.event.pull_request.body }}"; then
            echo "❌ PR must link to an issue (Commandment 1)"
            exit 1
          fi
          
      - name: Check branch naming
        run: |
          BRANCH="${{ github.head_ref }}"
          if [[ "$BRANCH" == "main" ]]; then
            echo "❌ Cannot push directly to main (Commandment 2)"
            exit 1
          fi
          
      - name: Require approval label
        run: |
          # Commandment 4: Wait for Mike's approval
          echo "⏳ PR requires 'mike-approved' label before merge"
```

**Status:** ✅ Proven industry practice

---

### 3. LLM-AS-JUDGE QA GATE (Blocking Gate)
**What:** Separate LLM evaluates every artifact before it ships.  
**Enforces:** Quality standards, brand voice, accuracy, safety.

```python
def qa_gate(artifact_content, agent_name, rubric):
    """
    Returns PASS/FAIL. Artifact cannot ship without PASS.
    """
    prompt = f"""
    You are a QA judge. Evaluate this artifact strictly.
    
    Agent: {agent_name}
    Rubric: {rubric}
    Artifact: {artifact_content}
    
    Respond with:
    VERDICT: PASS or FAIL
    REASON: <one line explanation>
    """
    
    response = llm.evaluate(prompt)
    
    if "FAIL" in response:
        # Block shipping, flag for review
        notify_mike(f"❌ QA FAILED: {agent_name} artifact rejected")
        move_to_rejected(artifact)
        return False
    
    return True
```

**Status:** ✅ Proven pattern (see Anthropic, OpenAI eval frameworks)

---

### 4. SYSTEM PROMPT INJECTION (Soft Enforcement)
**What:** Rules embedded in every agent's system prompt.  
**Enforces:** Behavioral standards, Constitution principles.

```markdown
## MANDATORY: Constitution Compliance

Before completing ANY task, you MUST:
1. Produce a traceable artifact (file in artifacts/)
2. Send Telegram ping: "🤖 {Your Name} → {Title} — {STATUS}"
3. Log activity to logs/{your-name}/YYYY-MM-DD.md
4. Follow commit convention: [{your-name}] action: description

If you cannot produce an artifact, you cannot claim the task is done.
Violations will be flagged by the Compliance Agent.
```

**Status:** ✅ Standard practice for AI agents

---

### 5. COMPLIANCE AGENT (Audit & Alert)
**What:** Dedicated agent that audits other agents for violations.  
**Enforces:** All Constitution rules, Amendment requirements.

```
COMPLIANCE AGENT - Runs every 6 hours

Checks:
□ Every agent that ran today produced artifacts
□ Every artifact has a Telegram ping logged
□ Every commit follows naming convention
□ No direct pushes to main
□ No PRs merged without approval
□ All agents logged their work

Output:
✅ Compliance Report - All clear
OR
⚠️ Violations Detected:
- Social Agent: 2 tasks, 0 artifacts
- Code Agent: PR #15 merged without approval label
- [ESCALATE TO MIKE]
```

**Status:** ✅ Proven (internal audit patterns)

---

### 6. TRELLO AUTOMATION (Workflow Enforcement)
**What:** Trello rules that enforce task workflow.  
**Enforces:** Task lifecycle, required fields, agent attribution.

Trello Butler Rules:
```
RULE: When card moved to "Done"
  IF no attachment (artifact link)
  THEN move card back to "In Progress"
  AND add comment "❌ Cannot complete without artifact link"

RULE: When card created
  IF no label (agent name)
  THEN add "⚠️ NEEDS-AGENT" label

RULE: When card in "Review" > 48 hours
  THEN notify Mike via webhook
  AND add "⏰ STALE-REVIEW" label
```

**Status:** ✅ Proven (Trello Butler is built-in)

---

### 7. BLOCKING NOTIFICATIONS (Escalation)
**What:** Critical violations trigger immediate alerts.  
**Enforces:** Response to serious issues.

```
SEVERITY LEVELS:

🟢 INFO - Logged only
   "Social Agent published post"

🟡 WARNING - Telegram ping
   "PR #15 waiting for approval >24h"

🔴 CRITICAL - Repeated pings until acknowledged
   "Direct push to main detected"
   "Agent produced no artifacts in 48h"
   "QA failure rate >50%"
```

**Status:** ✅ Standard incident response practice

---

## Enforcement Matrix

| Rule | Mechanism | Blocking? | Bypass Possible? |
|------|-----------|-----------|------------------|
| Commit conventions | Pre-commit hook | ✅ Yes | ❌ No (hook required) |
| Issue-first | GitHub Action | ✅ Yes | ❌ No (PR blocked) |
| No direct to main | Branch protection | ✅ Yes | ❌ No (GitHub enforced) |
| Approval required | GitHub labels | ✅ Yes | ❌ No (merge blocked) |
| Artifact required | QA Gate | ✅ Yes | ❌ No (can't ship) |
| Telegram ping | Compliance Agent | 🟡 Audit | 🟡 Detected post-hoc |
| Logging | Compliance Agent | 🟡 Audit | 🟡 Detected post-hoc |
| Quality standards | LLM-as-Judge | ✅ Yes | ❌ No (can't ship) |

---

## Implementation Priority

### Phase 1: Blocking Gates (This Week)
1. [x] GitHub branch protection on main
2. [ ] Pre-commit hook for commit messages
3. [ ] GitHub Action for PR requirements
4. [ ] LLM-as-Judge for artifact QA

### Phase 2: Audit Layer (Week 2)
5. [ ] Compliance Agent cron job
6. [ ] Trello Butler rules
7. [ ] Daily compliance report

### Phase 3: Escalation (Week 3)
8. [ ] Severity-based notifications
9. [ ] Repeated ping for critical violations
10. [ ] Weekly compliance scorecard

---

## The Key Insight

> **"Make the right thing easy and the wrong thing hard."**

- If an agent CAN skip the artifact, it eventually WILL
- If a human CAN push to main, they eventually WILL
- If a rule CAN be bypassed, it WILL be bypassed

**Solution:** Technical enforcement, not willpower.

---

*"Trust, but verify. And automate the verification."*
