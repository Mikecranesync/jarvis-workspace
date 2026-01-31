# Research: Skill-Based Agent Architecture
**Agent:** Research Agent  
**Timestamp:** 2026-01-29 14:09 UTC  
**Source:** Mike's Clawdbot/Moltbot research document

## Key Finding

Clawdbot Skills (SKILL.md) provide a **contract-based approach** to controlling LLM output. This directly solves our Amendment III (Proof of Work) enforcement problem.

## How It Works

```
User Request
    ↓
Gateway (routes to skill)
    ↓
Skill Matcher (finds SKILL.md)
    ↓
Agent reads skill instructions
    ↓
Agent produces output
    ↓
Output Validator (schema check)
    ├─ Valid → Ship to user + ping
    └─ Invalid → Repair prompt → Retry
```

## Application to Our Agent Fleet

### Social Agent Skill Example
```yaml
---
name: social-post
description: Create LinkedIn post with guaranteed structure
metadata:
  output_schema:
    title: { type: string, maxLength: 100 }
    body: { type: string, minLength: 50, maxLength: 1500 }
    hashtags: { type: array, minItems: 2, maxItems: 5 }
    cta: { type: string }
    qa_passed: { type: boolean }
---
```

### Outreach Agent Skill Example
```yaml
---
name: cold-outreach
description: Generate personalized outreach with validation
metadata:
  output_schema:
    recipient_name: { type: string }
    company: { type: string }
    personalization: { type: string, minLength: 20 }
    value_prop: { type: string }
    cta: { type: string }
    word_count: { type: number, max: 150 }
---
```

## Integration Plan

1. **Convert our QA Rubrics to JSON Schemas**
   - Already have rubrics in `config/qa-rubrics.yaml`
   - Convert to JSON Schema format for validation

2. **Create SKILL.md for each agent**
   - Social Agent
   - Outreach Agent
   - Content Agent
   - PR Agent

3. **Use Lobster Pipelines for multi-step workflows**
   - Draft → QA → Approve/Reject → Publish → Ping
   - Built-in approval gates for critical content

4. **Schema validation before ping**
   - If output doesn't match schema, auto-retry
   - Only ping Mike when valid artifact produced

## Benefits

- **Guaranteed structure** — No more malformed outputs
- **Automatic retry** — Bad output triggers repair, not failure
- **Audit trail** — Schema validation logged
- **Human gates** — Critical decisions require approval

## Next Steps

1. [ ] Create SKILL.md for Social Agent
2. [ ] Test schema validation on first post
3. [ ] Roll out to other agents
4. [ ] Create Lobster pipeline for GTM workflow

---
*This research directly supports Amendment III (Proof of Work) enforcement*
