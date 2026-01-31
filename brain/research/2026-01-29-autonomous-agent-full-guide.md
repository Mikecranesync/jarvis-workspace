# Autonomous Self-Iterating Agent - Full Setup Guide

**Source:** Mike's complete Moltbot autonomous agent documentation  
**Date:** 2026-01-29

---

## Overview

A Moltbot agent that:
1. Listens for vision statements via Telegram
2. Breaks them into executable steps
3. Builds each step automatically
4. Searches web via Perplexity for context
5. Self-iterates until vision complete
6. Runs 10 judge-evaluated iterations for creative work

---

## Commands

| Command | Action |
|---------|--------|
| `BUILD: [vision]` | Start new vision, create steps, begin building |
| `STATUS` | Show current step and progress |
| `PAUSE` | Stop builder, save state |
| `RESUME` | Continue from last step |
| `SKIP [N]` | Skip step N, move to next |
| `RESEARCH [topic]` | Query Perplexity manually |
| `ITERATE [count] [step]` | Run judge loop on step |
| `NEXT STEPS` | Get Perplexity recommendations |
| `COMPLETE VISION` | Mark all done, reset |
| `HELP` | Show commands |

---

## 8 Setup Steps

### Step 1: Vision Breakdown Skill
Trigger: "BUILD: [vision]"
Creates steps.md with 5-7 executable steps

### Step 2: Autonomous Builder Workflow  
Lobster workflow that loops forever:
- Check steps.md
- Find CURRENT step
- Build/test/fix
- Mark DONE
- Move to next
- 30-second delay between iterations

### Step 3: Perplexity Context Gatherer
Before each step:
- Read vision and current step
- Ask Perplexity for best practices
- Save to context/step-N-research.md

### Step 4: Next Steps Recommender
After step completes:
- If < 3 steps remaining
- Ask Perplexity for 3 valuable additions
- Prompt user to add or complete

### Step 5: Judge Evaluation Loop (Creative)
For videos/images:
- Generate 10 iterations
- Claude evaluates each
- Pick best 3, select winner
- Save to outputs/FINAL/

### Step 6: Cron for 24/7 Operation
```bash
moltbot cron add \
  --name "autonomous-builder-loop" \
  --cron "*/2 * * * *" \
  --session isolated \
  --message "Check steps.md, resume if work exists"
```

### Step 7: Project Memory (Soul)
Create `~/.moltbot/souls/rivet-pro-builder.md` with:
- Mission
- Current vision
- Completed projects
- Architecture context
- Guidelines
- Personality

### Step 8: Command Parser
Enable all commands (BUILD, STATUS, PAUSE, etc.)

---

## Safeguards

### Approval Gates
For high-risk steps (PLC, production, financial):
1. Build code
2. Test in isolation
3. Ask for approval
4. Wait 5 min for reply
5. Only proceed on "APPROVE"

### Budget Controls
- Max 5 Perplexity calls per vision
- Max 10 iterations per creative step
- Cache context for 15 minutes

### Error Recovery
- 3 failures → PAUSE
- Send Telegram alert
- Wait for manual RESUME

---

## Expected Timeline

"AI Video Generator" vision:
- Hour 1: Research + Pipeline + Preprocessing
- Hour 2: Voiceover + 10 judge iterations
- Hour 3: UI + Testing + Deploy
- Total: ~2.5-3 hours

---

## Cost Estimates

| Item | Cost |
|------|------|
| Perplexity per vision | ~$0.50 |
| 30 visions/month | ~$15 |
| VPS compute | Minimal |

---

## Test Command

```
BUILD: Create a simple todo list app with Telegram commands. 
Features: add task, list tasks, mark done, delete task. 
Store in JSON file. Deploy to my VPS.
```

Expected: 30-45 minutes for complete working app.

---

## Environment Variables

```bash
export PERPLEXITY_API_KEY="pplx-xxxxx"
export TELEGRAM_BOT_TOKEN="your-bot-token"
```

---

*This is the complete blueprint for the autonomous agent factory.*
