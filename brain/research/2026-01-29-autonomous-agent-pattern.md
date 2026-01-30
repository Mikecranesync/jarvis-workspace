# Autonomous Self-Iterating Agent Pattern

**Source:** Mike's Moltbot setup guide  
**Date:** 2026-01-29

---

## The Pattern

```
Vision Statement
    ↓
Break into 5-7 executable steps (Phase 1)
    ↓
┌─────────────────────────────────────────┐
│           SELF-ITERATING LOOP           │
│                                         │
│  1. Check steps.md for CURRENT task     │
│  2. Gather context via Perplexity       │
│  3. Build/implement the step            │
│  4. Test and fix errors                 │
│  5. Mark step DONE                      │
│  6. Move CURRENT to next step           │
│  7. Check if all done                   │
│  8. If not done → loop back to 1        │
│                                         │
└─────────────────────────────────────────┘
    ↓
All steps complete → Send summary
```

---

## Component Skills

### 1. Vision Breakdown Skill
**Trigger:** "BUILD: [vision description]"

**Output:** steps.md file
```markdown
# Vision: [Description]

## Step 1: ✓ CURRENT
- [First task]

## Step 2:
- [Second task]

...

Status: Ready to start Step 1
```

### 2. Autonomous Builder Workflow
**Type:** Lobster workflow (loops forever)

**Steps:**
- A: Check steps.md
- B: Find ✓ CURRENT line
- C: Extract task description
- D: Build/implement
- E: Test and fix
- F: Mark DONE, move CURRENT
- G: Check if all done
- H: If done → Telegram summary
- I: If not done → loop

**Delay:** 30 seconds between iterations

### 3. Perplexity Context Gatherer
**Runs:** Before each new step

**Query Template:**
```
VISION: [from steps.md]
CURRENT STEP: [current step description]
CONTEXT NEEDED: Best practices, libraries, patterns

Question for Perplexity: "I'm building [vision]. For the step '[step]', 
what are the top implementation patterns and libraries I should use?"

Return research points with sources.
```

**Output:** `context/step-[N]-research.md`

---

## For Creative Work (Videos/Images)

Run **10 judge-evaluated iterations** automatically:
1. Generate version 1
2. Judge evaluates against rubric
3. Generate version 2 based on feedback
4. Repeat until v10 or PASS

---

## Application to Our Agents

| Agent | How to Apply |
|-------|--------------|
| Social Agent | Vision: "LinkedIn content for industrial AI" → 3 posts auto-generated |
| Content Agent | Vision: "Blog about CMMS ROI" → Research → Write → Edit → Publish |
| Home Lab Factory | Vision: "PLC tutorial video" → Script → Record → Edit → Upload |

---

## Implementation Notes

- Use `steps.md` file as state management
- 30-second delay prevents overwhelming
- Log to `logs/build-progress.log`
- Perplexity provides real research context
- Judge iterations ensure quality

---

*This is the pattern for turning visions into shipped products autonomously.*
