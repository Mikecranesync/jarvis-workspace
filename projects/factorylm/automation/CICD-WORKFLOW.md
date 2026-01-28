# FactoryLM CI/CD Workflow

## The Flow (GitHub-Native)

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   BACKLOG   │ →   │ IN PROGRESS │ →   │   REVIEW    │ →   │    DONE     │
│             │     │             │     │             │     │             │
│ Issue/Task  │     │ Branch +    │     │ PR Created  │     │ Merged      │
│ Created     │     │ Code        │     │ Awaiting    │     │ Deployed    │
└─────────────┘     └─────────────┘     └─────────────┘     └─────────────┘
      ↓                   ↓                   ↓                   ↓
   @jarvis           git checkout        gh pr create         gh pr merge
   triggers          -b feature/xxx      + Card moved         + Alert sent
```

## Jarvis Workflow (Per Task)

### 1. Pick Up Task
```bash
# Move card to In Progress
# Parse task requirements from card description
```

### 2. Create Branch
```bash
cd /path/to/repo
git checkout main
git pull origin main
git checkout -b feature/trello-{card_id_short}
```

### 3. Do The Work
```bash
# Write code, create files, make changes
# Commit with meaningful messages
git add .
git commit -m "feat: {task_title}

Trello: {card_url}
- {deliverable 1}
- {deliverable 2}"
```

### 4. Push & Create PR
```bash
git push -u origin feature/trello-{card_id_short}

gh pr create \
  --title "{task_title}" \
  --body "## Task
{card_description}

## Changes
- {change 1}
- {change 2}

## Trello Card
{card_url}" \
  --base main
```

### 5. Update Trello Card
```bash
# Add comment with PR link
# Move card to Review
# Send alert to Mike
```

### 6. Await Review
- Mike reviews PR on GitHub
- Approves or requests changes
- Jarvis responds to feedback

### 7. Merge & Deploy
```bash
gh pr merge --squash
git checkout main
git pull
# Deploy if applicable
```

### 8. Complete
- Move card to Done
- Send completion alert
- Check for next task

## Alert Configuration

### Completion Alerts (Telegram)
Every completed task sends:
```
✅ TASK COMPLETED

📋 {task_title}
🔗 Trello: {card_url}
🔀 PR: {pr_url}
📊 Status: Ready for Review / Merged

Time: {duration}
```

### Failure Alerts
```
❌ TASK FAILED

📋 {task_title}
🔗 {card_url}
⚠️ Error: {error_message}

Needs manual intervention.
```

## GitHub Repos

| Repo | Purpose |
|------|---------|
| factorylm/puppeteer | AR glasses integration |
| factorylm/backend | API + AI services |
| factorylm/landing | Marketing site |
| factorylm/cmms-integration | Atlas CMMS connector |

## Branch Naming

```
feature/trello-{shortId}  - New features
fix/trello-{shortId}      - Bug fixes  
docs/trello-{shortId}     - Documentation
refactor/trello-{shortId} - Code improvements
```

## Commit Message Format

```
type: brief description

Trello: https://trello.com/c/{shortId}

- Detailed change 1
- Detailed change 2
```

Types: feat, fix, docs, refactor, test, chore
