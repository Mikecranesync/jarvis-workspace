# Autonomous Build Pipeline — Trello × Jarvis

## The Vision

Trello becomes the **task queue**. VPS Jarvis is the **worker**. Sub-agents are the **builders**.

```
┌─────────────────────────────────────────────────────────────────────┐
│                         TRELLO BOARD                                │
│  ┌──────────┐  ┌────────────┐  ┌──────────┐  ┌──────────┐          │
│  │ Backlog  │→ │ In Progress│→ │  Review  │→ │   Done   │          │
│  │          │  │            │  │          │  │          │          │
│  │ @jarvis  │  │ [working]  │  │ [check]  │  │ [shipped]│          │
│  └──────────┘  └────────────┘  └──────────┘  └──────────┘          │
└────────┬────────────────────────────────────────────────────────────┘
         │ Webhook
         ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      VPS JARVIS (24/7)                              │
│                                                                     │
│  1. Receive webhook (card with @jarvis)                             │
│  2. Parse task from card title + description                        │
│  3. Spawn sub-agent with task                                       │
│  4. Sub-agent does work                                             │
│  5. Post results as card comment                                    │
│  6. Move card to "Review"                                           │
│  7. Notify Mike                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

## Card Format (Task Definition)

```markdown
**Card Title:** [TASK TYPE] Brief description

**Card Description:**
## Objective
What needs to be done

## Context  
Background info, links, prior decisions

## Deliverables
- [ ] Specific output 1
- [ ] Specific output 2

## Constraints
- Time limit, tech restrictions, etc.

@jarvis
```

### Task Types
| Type | Sub-agent Model | Typical Time |
|------|-----------------|--------------|
| `[CODE]` | Claude Sonnet | 10-30 min |
| `[RESEARCH]` | Gemini Flash | 5-15 min |
| `[CONTENT]` | Claude Sonnet | 10-20 min |
| `[REVIEW]` | Claude Opus | 5-10 min |
| `[DESIGN]` | Claude Sonnet | 15-30 min |

## Webhook Handler (Upgraded)

```python
# /opt/trello-webhook/trello_webhook.py (v2)

async def handle_jarvis_task(card_id, card_name, card_desc, card_url):
    """Process a @jarvis task from Trello."""
    
    # 1. Move card to "In Progress"
    move_card_to_list(card_id, IN_PROGRESS_LIST_ID)
    add_comment(card_id, "🤖 Jarvis picked up this task...")
    
    # 2. Parse task type
    task_type = extract_task_type(card_name)  # [CODE], [RESEARCH], etc.
    
    # 3. Build prompt for sub-agent
    prompt = f"""
    Task: {card_name}
    
    {card_desc}
    
    When complete, provide:
    1. Summary of what was done
    2. Any files created/modified
    3. Next steps or blockers
    """
    
    # 4. Spawn sub-agent (via Clawdbot sessions API)
    result = await spawn_subagent(
        task=prompt,
        label=f"trello-{card_id}",
        model="anthropic/claude-sonnet-4-20250514" if task_type == "CODE" else "google/gemini-2.5-flash",
        timeout=1800  # 30 min max
    )
    
    # 5. Post results to card
    add_comment(card_id, f"## ✅ Completed\n\n{result.summary}\n\n### Files\n{result.files}\n\n### Next Steps\n{result.next_steps}")
    
    # 6. Move to Review
    move_card_to_list(card_id, REVIEW_LIST_ID)
    
    # 7. Notify Mike
    send_telegram(f"🤖 Task completed: {card_name}\n{card_url}")
```

## Butler Automations (Trello Pro)

### Rule 1: Auto-assign due dates
```
Trigger: When a card is added to "In Progress"
Action: Set due date to 24 hours from now
```

### Rule 2: Daily standup
```
Trigger: Every day at 3:00 PM EST (Mike's morning)
Action: Create card in "Backlog" with title "[REPORT] Daily Standup"
        Description: "@jarvis Summarize yesterday's completed tasks and today's priorities"
```

### Rule 3: Stale task alert
```
Trigger: When a card in "In Progress" is due
Action: Add comment "@jarvis Status update needed"
        Move to "Backlog"
```

### Rule 4: Completion chain
```
Trigger: When all checklist items are checked
Action: Move card to "Review"
        Add comment "All items complete. Ready for human review."
```

### Rule 5: Weekly polish sprint
```
Trigger: Every Sunday at 6:00 PM EST
Action: Create card "[CODE] Weekly codebase polish"
        Description: "@jarvis Review all FactoryLM repos. Fix any linting issues, 
                     update documentation, improve error handling. 
                     Commit improvements with clear messages."
```

## Continuous Improvement Tasks (Auto-Generated)

Cards that get created automatically to keep Jarvis busy:

### Daily
- `[REVIEW] Check VPS services health`
- `[RESEARCH] Industrial news scan` (find relevant articles)

### Weekly  
- `[CODE] Dependency updates + security patches`
- `[CODE] Test coverage improvement`
- `[CONTENT] Blog post draft on industrial AI`
- `[REVIEW] Documentation freshness check`

### Monthly
- `[DESIGN] Architecture review`
- `[RESEARCH] Competitor analysis update`
- `[CODE] Performance profiling + optimization`

## List IDs (To Configure)

```python
# Get these from Trello API
BOARD_ID = "68f2bfd5d622c72fdc3c9f1e"
BACKLOG_LIST_ID = "???"
IN_PROGRESS_LIST_ID = "???"
REVIEW_LIST_ID = "???"
DONE_LIST_ID = "???"
```

## Security Considerations

1. **Rate limiting**: Max 5 concurrent sub-agents
2. **Timeout**: 30 min max per task
3. **Scope**: Sub-agents can only write to approved directories
4. **Review gate**: Human must approve before "Done"
5. **Cost tracking**: Log API costs per task

## Implementation Checklist

- [ ] Get list IDs from Trello
- [ ] Upgrade webhook handler to v2
- [ ] Add Clawdbot sessions API integration
- [ ] Set up Butler rules in Trello Pro
- [ ] Create first batch of seed tasks
- [ ] Test end-to-end flow
- [ ] Monitor for 48 hours
- [ ] Iterate based on results

---

*This turns Trello into an AI-powered autonomous development system.*
