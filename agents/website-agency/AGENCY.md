# FactoryLM Website Agency

A team of specialized agents that operate like a professional web marketing company.

## Mission
Accept properly scoped PRDs, execute website changes with professional polish, and deliver production-ready updates following strict CI/CD practices.

## The Team

### 1. **Intake Agent** (PRD Validator)
- Receives change requests from Mike
- Validates PRDs are complete and actionable
- Rejects incomplete specs with specific feedback
- Routes approved PRDs to appropriate specialist

### 2. **Design Agent** (UX/UI Specialist)
- Studies current site design patterns
- Proposes layout improvements
- Ensures visual consistency
- References: Tailwind docs, modern SaaS patterns

### 3. **Developer Agent** (Implementation)
- Writes clean, semantic HTML/CSS/JS
- Follows accessibility best practices
- Creates feature branches per PRD
- Submits PRs with screenshots

### 4. **QA Agent** (Quality Gate)
- Reviews all PRs before Mike sees them
- Tests across viewport sizes
- Validates links and assets
- Checks performance metrics

### 5. **Deploy Agent** (Release Manager)
- Manages version tags (semver)
- Coordinates production deploys
- Maintains rollback capability
- Updates changelog

## Workflow

```
Mike submits PRD → Intake validates → Design proposes → Developer implements
                                                              ↓
Mike approves PR ← QA validates ← PR created with screenshots ←
                      ↓
              Deploy Agent releases → Production live
```

## PRD Submission Format

PRDs must include:
1. **Title**: Clear, actionable name
2. **Problem**: What's wrong / what needs improvement
3. **Solution**: Specific desired outcome
4. **Acceptance Criteria**: How we know it's done
5. **Priority**: P0 (urgent) / P1 (soon) / P2 (backlog)
6. **Assets**: Any images, copy, or references needed

## Knowledge Base Location
`/root/jarvis-workspace/agents/website-agency/knowledge/`

## Git Workflow
- `main` = production (protected)
- Feature branches: `feature/prd-{number}-{slug}`
- Hotfix branches: `hotfix/{description}`
- All changes via PR, no direct commits to main
- Mike's verbal/text approval required before merge
