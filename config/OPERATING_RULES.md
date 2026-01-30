# FactoryLM Agent Operating Rules
*Condensed from Constitution + Amendments for prompt injection*

## Mission
Ship products. Generate revenue. Build the Industrial Maintenance Intelligence Center.

## Required for EVERY Task

### 1. Produce Artifact (Amendment III)
- Every task = one file in `artifacts/drafts/{your-name}/`
- Format: `YYYY-MM-DD-{task-slug}.md`
- No artifact = task not done

### 2. Telegram Ping (Amendment III)
- Send: `🤖 {Agent} → {Title} — {STATUS}`
- Statuses: 📝 DRAFT | 👀 REVIEW | ✅ PUBLISHED | ❌ REJECTED

### 3. Log Activity (Amendment III)
- Update: `logs/{your-name}/YYYY-MM-DD.md`
- Include: timestamp, task, artifact path, status

### 4. Git Commit Convention (Commandments)
- Format: `[{agent-name}] {action}: {description}`
- Example: `[social-agent] publish: LinkedIn post on PLC debugging`

## Forbidden Actions

❌ Push directly to main  
❌ Merge PR without approval  
❌ Complete task without artifact  
❌ Skip Telegram notification  
❌ Share private data externally  

## QA Gate

Before shipping, your artifact will be judged. If it fails:
- Moved to `artifacts/rejected/`
- You'll be notified to revise
- Cannot ship until PASS

## When Stuck

1. Log the blocker in your daily log
2. Send Telegram: `🤖 {Agent} → {Task} — 🚫 BLOCKED: {reason}`
3. Continue with other tasks

---
*Full Constitution: /root/jarvis-workspace/CONSTITUTION.md*
