# The Ten Engineering Commandments

*Standard practices for all Jarvis instances when working on code.*

---

## I. Thou Shalt Create an Issue First

Before touching any code, **create a GitHub issue** describing:
- What is broken or what needs to be built
- Why it matters
- Acceptance criteria (how do we know it's done?)

```bash
gh issue create --title "Bug: description" --body "..."
```

---

## II. Thou Shalt Branch from Main

Always create a feature branch from an up-to-date `main`:
```bash
git checkout main && git pull origin main
git checkout -b fix/issue-number-short-description
```

Branch naming:
- `fix/` — Bug fixes
- `feature/` — New features
- `chore/` — Maintenance tasks
- `docs/` — Documentation

---

## III. Thou Shalt Not Push Directly to Main

All changes go through Pull Requests. No exceptions.

---

## IV. Thou Shalt Link PRs to Issues

Every PR must reference its issue:
```
Fixes #123
```

---

## V. Thou Shalt Not Merge Without Approval

**WAIT for Mike's verbal approval** before merging any PR.

Even if CI passes, even if it looks perfect — wait for the green light.

---

## VI. Thou Shalt Not Deploy Without Approval

Production deployments require explicit approval.

If a hotfix is urgent, document it and get retroactive approval immediately.

---

## VII. Thou Shalt Write Meaningful Commits

Commit messages must explain:
- What changed
- Why it changed

Format: `type: short description`
```
fix: Validate work order priority to prevent CMMS API errors
feat: Add mobile-responsive tabs to MultipleTabsLayout
```

---

## VIII. Thou Shalt Test Before Pushing

Verify changes work locally/in dev before pushing:
- Run the code
- Check for errors
- Test the happy path AND edge cases

---

## IX. Thou Shalt Document Thy Changes

Every significant change needs:
- PR description explaining the change
- Updated docs if behavior changes
- Trello card for tracking

---

## X. Thou Shalt Learn from Failures

When something breaks:
1. Fix it properly (not just a band-aid)
2. Document what happened
3. Add safeguards to prevent recurrence
4. Share learnings in memory files

---

## The Workflow (TL;DR)

```
1. Create GitHub Issue
2. Create feature branch
3. Make changes
4. Push & create PR (link to issue)
5. Wait for Mike's approval
6. Merge after approval
7. Deploy after approval
8. Update Trello
```

---

*These commandments apply to all Jarvis instances. No shortcuts.*
