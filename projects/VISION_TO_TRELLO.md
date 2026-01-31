# Vision-to-Trello Autonomous Agent System

**Status:** IMPLEMENTING  
**Date:** 2026-01-29

---

## Overview

Trello becomes the central hub for the autonomous self-iterating agent pattern:
- **Visions** = Purple-labeled cards in "🎯 Visions" list
- **Steps** = Sky-labeled cards that flow through Backlog → In Progress → Done
- **Progress** = Visual via card positions and checklists

---

## Board Structure

```
🎯 Visions          📥 Inbox    🔬 Research    📋 Backlog    🏗️ In Progress    👀 Review    ✅ Done    📦 Shipped
┌─────────────┐                                ┌──────────┐   ┌──────────┐
│ [VISION]    │                                │ Step 1   │   │ Step 3   │
│ AI Video    │ ────────────────────────────▶  │ Research │   │ Pipeline │
│ Generator   │      (Steps created here)      │ APIs     │   │          │
│             │                                └──────────┘   └──────────┘
│ Steps: 7    │                                ┌──────────┐
│ Done: 2/7   │                                │ Step 2   │
└─────────────┘                                │ Preproc  │
                                               └──────────┘
```

---

## Card Formats

### Vision Card (Purple Label)
```markdown
Title: [VISION] AI Video Generator for Equipment Diagnostics

Description:
## Status
🔄 IN PROGRESS | Steps: 7 | Completed: 2/7

## Vision
Create an AI-powered video generator that takes equipment photos and creates 
diagnostic videos with AI voiceover explaining what's wrong.

## Steps
- [x] Step 1: Research video generation APIs
- [x] Step 2: Create video synthesis pipeline
- [ ] Step 3: Build photo preprocessing (CURRENT)
- [ ] Step 4: Add AI voiceover
- [ ] Step 5: Create approval UI
- [ ] Step 6: End-to-end testing
- [ ] Step 7: Deploy and document

## Context (Perplexity Research)
- Best APIs: ElevenLabs for voice, Synthesia for video
- Key libraries: ffmpeg, moviepy, PIL
- Cost estimate: $0.15 per video generated

## Linked Step Cards
- Step 1: [card-id-1]
- Step 2: [card-id-2]
- ...
```

### Step Card (Sky Label)
```markdown
Title: [Step 3/7] Build photo preprocessing module

Description:
## Parent Vision
AI Video Generator | Vision Card: [link]

## Step Details
- Step: 3 of 7
- Status: 🏗️ IN PROGRESS
- Estimated: 30 minutes

## Perplexity Context
Best practices for image preprocessing in video generation:
1. Resize to target resolution (1080p)
2. Normalize brightness/contrast
3. Remove background if needed
4. Add padding for consistent framing

## Completion Criteria
- [ ] Accept equipment photo input
- [ ] Resize to 1920x1080
- [ ] Auto-enhance image quality
- [ ] Output preprocessed frame
- [ ] Unit tests passing

## Progress Log
- 15:30 UTC: Started implementation
- 15:45 UTC: Resize function complete
- 16:00 UTC: Enhancement added
```

---

## Commands

### BUILD: [vision]
**Trigger:** Mike sends "BUILD: [description]"

**Actions:**
1. Create Vision card in "🎯 Visions" list (purple label)
2. Break into 5-7 steps
3. Create Step cards in "📋 Backlog" (sky label)
4. Link steps to vision card
5. Move Step 1 to "🏗️ In Progress"
6. Report to Telegram

### STATUS
**Actions:**
1. Find active Vision card
2. Count completed vs total steps
3. Find current step (in "In Progress")
4. Return summary

### PAUSE
**Actions:**
1. Move current step back to Backlog
2. Add "PAUSED" comment to Vision card
3. Stop cron polling

### RESUME
**Actions:**
1. Find paused Vision
2. Move next incomplete step to In Progress
3. Continue building

### SKIP [N]
**Actions:**
1. Move Step N card to "✅ Done"
2. Add "SKIPPED" label
3. Move Step N+1 to In Progress

### COMPLETE VISION
**Actions:**
1. Move all remaining steps to Done
2. Move Vision card to "📦 Shipped"
3. Add completion summary comment

---

## Workflow Implementation

### Jarvis Autonomous Loop (Every 5 minutes via cron/heartbeat)

```python
# Pseudocode - FULL SELF-ITERATING LOOP
def autonomous_build_loop():
    while True:
        # 1. Get active vision (highest priority not shipped)
        vision = get_active_vision()
        if not vision:
            return "All visions complete!"
        
        # 2. Find current step (in "In Progress" list)
        current_step = get_step_in_progress(vision)
        if not current_step:
            # Move next backlog step to In Progress
            current_step = promote_next_step(vision)
            if not current_step:
                # All steps done - but check for more work!
                next_steps = perplexity_next_steps(vision)
                if next_steps and should_continue(next_steps):
                    # Add new steps and continue
                    add_steps_to_backlog(vision, next_steps)
                    continue
                else:
                    # Vision truly complete
                    ship_vision(vision)
                    # Move to next priority vision
                    continue
        
        # 3. Execute current step
        context = get_perplexity_context(vision, current_step)
        result = execute_step(current_step, context)
        
        # 4. Check completion
        if step_complete(result):
            move_to_done(current_step)
            update_vision_progress(vision)
        
        # 5. Rate limit (don't burn tokens)
        sleep(30)  # 30 second delay between iterations
```

### Perplexity Next-Steps Query

After all steps complete, ask Perplexity:

```
VISION: [vision name]
COMPLETED STEPS: [list of completed steps]
CURRENT STATE: [what's been built]

Based on what's been built, what are the 3 most valuable next steps 
to improve quality or completeness? 

If the vision is fully realized, respond with "VISION COMPLETE".
Otherwise, list 3 actionable improvements.
```

### Restart Logic

The loop RESTARTS if:
- New steps were added from Perplexity suggestions
- There are still uncompleted steps in Backlog
- Current step needs more work

The loop ADVANCES TO NEXT VISION if:
- All steps complete
- Perplexity says "VISION COMPLETE"
- Quality threshold met

### Budget Controls

To avoid burning Claude/Perplexity credits:
- Max 5 Perplexity calls per vision
- 30-second delay between step executions
- Cache research results in `context/` folder
- Skip Perplexity if same query in last 15 minutes

---

## Global Restart Loop Protocol

When a vision completes OR hits an approval gate:

```
1. ANNOUNCE to Telegram:
   "🔄 Vision [N] [status]. 
    Tokens used: ~[X]K
    Starting Vision [N+1]: [name]"

2. If approval needed:
   - Move blocked step to Review list
   - Continue with next priority vision
   - Return to blocked vision when approved

3. If vision complete:
   - Move vision card to Shipped
   - Start next priority vision automatically

4. RESTART LOOP:
   - Check config/vision-ids.json for next queued vision
   - Create step cards if not exist
   - Begin autonomous execution
```

### Example Announcement
```
🔄 VISION STATUS UPDATE

Vision 1 (Landing Pages): ⏸️ AWAITING APPROVAL
- Progress: 5/7 steps
- Blocked: Step 6 (Deploy) needs Mike's OK
- Tokens: ~50K context

→ Starting Vision 2: LinkedIn Content Engine
```

This ensures continuous progress across multiple visions.

---

## Trello API Integration

### IDs Reference
```json
{
  "lists": {
    "🎯 Visions": "697b7de0ef5fdd2d4e402384",
    "📋 Backlog": "697929460bc411801260b8f3",
    "🏗️ In Progress": "697929459d88b2e1f87aceeb",
    "✅ Done": "6979294563c650cad02d8f08",
    "📦 Shipped": "697929455129a02ee8f3483c"
  },
  "labels": {
    "Vision": "697b7de7b4c785ee1968e2cb",
    "Step": "697b7de7a8685f7e58ecef1b"
  }
}
```

### API Calls

**Create Vision Card:**
```bash
curl -X POST "https://api.trello.com/1/cards" \
  -d "idList=697b7de0ef5fdd2d4e402384" \
  -d "name=[VISION] AI Video Generator" \
  -d "desc=..." \
  -d "idLabels=697b7de7b4c785ee1968e2cb"
```

**Create Step Card:**
```bash
curl -X POST "https://api.trello.com/1/cards" \
  -d "idList=697929460bc411801260b8f3" \
  -d "name=[Step 1/7] Research APIs" \
  -d "desc=..." \
  -d "idLabels=697b7de7a8685f7e58ecef1b"
```

**Add Checklist to Step:**
```bash
curl -X POST "https://api.trello.com/1/cards/{cardId}/checklists" \
  -d "name=Completion Criteria"
```

**Move Card:**
```bash
curl -X PUT "https://api.trello.com/1/cards/{cardId}" \
  -d "idList={newListId}"
```

---

## Safeguards

### Approval Required For:
- Production deployments
- Financial operations
- PLC/equipment control
- External API integrations
- Data migrations

**Implementation:** Before executing these steps, Jarvis:
1. Creates card in "👀 Review / Testing"
2. Sends Telegram: "Step requires approval: [description]"
3. Waits for Mike to move card to "In Progress"
4. Only then executes

### Budget Controls:
- Max 5 Perplexity calls per vision (cache results)
- Max 3 retries per step before PAUSE
- 5-minute delay between step executions

---

## Example: First Vision

**Mike sends:**
```
BUILD: Create LinkedIn content calendar for Q1 2026. 
Generate 12 posts (1/week) about industrial AI, CMMS, and PLC diagnostics.
Schedule them automatically.
```

**Jarvis creates:**

**Vision Card:**
- [VISION] LinkedIn Content Calendar Q1 2026
- Steps: 6
- Status: Starting

**Step Cards (in Backlog):**
1. Research top-performing industrial AI content
2. Generate 12 post drafts with themes
3. Review and edit posts (REQUIRES APPROVAL)
4. Create posting schedule
5. Set up automated posting (REQUIRES APPROVAL)
6. Monitor engagement and report

---

## Implementation Status

- [x] Created "🎯 Visions" list
- [x] Created "Vision" label (purple)
- [x] Created "Step" label (sky)
- [x] Updated trello_board.json
- [ ] Implement BUILD command
- [ ] Implement STATUS command
- [ ] Implement autonomous loop
- [ ] Test with first vision
- [ ] Set up cron job

---

*Trello + Autonomous Agent = Visual progress on autopilot.*
