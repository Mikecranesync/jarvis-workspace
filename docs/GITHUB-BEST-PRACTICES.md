# GitHub Best Practices for FactoryLM
*User Intent → Agent Management*

**Philosophy:** Mike speaks his vision. Jarvis manages GitHub.

---

## The Flow

```
Mike's Idea (voice/text)
        ↓
    Spec Watcher extracts requirements
        ↓
    Jarvis creates GitHub Issue
        ↓
    Jarvis creates branch (issue-XX-description)
        ↓
    Jarvis writes code & commits
        ↓
    Jarvis creates PR
        ↓
    Jarvis pings Mike for approval
        ↓
    Mike approves → Jarvis merges
        ↓
    Main branch updated
```

---

## Repo Structure (Target)

### factorylm (Product Monorepo)
```
factorylm/
├── api/                    # FastAPI backend
│   ├── routes/
│   ├── services/
│   ├── models/
│   └── tests/
├── web/                    # Landing page & marketing
│   ├── public/
│   ├── src/
│   └── package.json
├── dashboard/              # React CMMS dashboard
│   ├── src/
│   └── package.json
├── edge/                   # Edge device code
│   ├── plc-gateway/
│   ├── network-detect/
│   └── modbus-client/
├── bot/                    # Telegram bot
│   ├── handlers/
│   ├── workflows/
│   └── integrations/
├── lib/                    # Shared libraries
│   ├── llm-cascade/
│   ├── equipment-service/
│   └── knowledge-base/
├── docs/                   # Documentation
├── tests/                  # Integration tests
├── .github/
│   └── workflows/          # CI/CD
└── README.md
```

### jarvis-workspace (AI Operations)
```
jarvis-workspace/
├── agents/                 # Agent definitions
├── brain/                  # Knowledge & specs
│   ├── specs/             # Extracted specs
│   ├── strategy/          # Strategy docs
│   └── research/          # Research findings
├── memory/                # Daily logs
├── skills/                # Clawdbot skills
├── scripts/               # Automation
├── tests/                 # Test suites
└── docs/                  # Internal docs
```

---

## Branch Naming Convention

```
main                        # Production - PROTECTED
develop                     # Integration branch (optional)
issue-XX-short-description  # Feature branches
hotfix-XX-description       # Emergency fixes
demo-YYYY-MM-description    # Demo branches (like yc-demo-keyboard-robot)
```

---

## Commit Message Format

```
type(scope): description

Types:
- feat: New feature
- fix: Bug fix
- docs: Documentation
- refactor: Code refactoring
- test: Adding tests
- chore: Maintenance

Examples:
feat(api): add LLM cascade with quality judge
fix(bot): handle empty photo uploads gracefully
docs(readme): update installation instructions
```

---

## Pull Request Template

```markdown
## Summary
Brief description of changes

## Related Issue
Closes #XX

## Changes
- [ ] Change 1
- [ ] Change 2

## Testing
- [ ] Tests pass
- [ ] Manual testing done

## Checklist
- [ ] Code follows project style
- [ ] Documentation updated
- [ ] No secrets committed
```

---

## Protection Rules

### Main Branch
- Require PR before merging
- Require approval (Mike or designated reviewer)
- Require status checks to pass
- No direct pushes

### Tags
- Use semantic versioning: vX.Y.Z
- Tag major milestones
- Protect release tags

---

## Automated Workflows (GitHub Actions)

### On Every Push
1. Run linters
2. Run tests
3. Check for secrets
4. Post summary to Telegram

### On PR Created
1. Run full test suite
2. Generate change summary
3. Notify Mike for review

### On Merge to Main
1. Deploy to staging
2. Run integration tests
3. Create release notes
4. Notify Mike of deployment

---

## Agent Responsibilities

### Spec Watcher
- Monitor conversations
- Extract requirements
- Create issues automatically

### Code Agent
- Pick up issues
- Create branches
- Write code
- Create PRs

### Review Agent
- Check PR quality
- Run tests
- Flag issues
- Request human review when needed

### Deploy Agent (future)
- Handle deployments
- Monitor health
- Rollback if needed

---

## Mike's Commands (Intent-Based)

Mike says → Jarvis does:

"I want X feature" → Create issue + start work
"Fix the Y bug" → Create issue, investigate, fix
"Show me what changed" → Summarize recent commits/PRs
"What's the status?" → Report on open issues/PRs
"Approve the PR" → Merge the pending PR
"Roll back" → Revert last merge
"Tag this as release" → Create version tag

---

## Recovery Procedures

### Lost Work
1. Check git reflog
2. Find lost commit
3. Cherry-pick or restore

### Broken Main
1. Revert problematic commit
2. Create hotfix branch
3. Fix issue properly
4. Merge with proper review

### Diverged Branches
1. Identify divergence point
2. Rebase or merge carefully
3. Resolve conflicts
4. Test thoroughly

---

*This document is the source of truth for GitHub management. Jarvis follows these practices on every operation.*
