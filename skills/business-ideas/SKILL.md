# Business Ideas Capture Skill

## Purpose
Capture, organize, and track business ideas that emerge during work.

## Triggers
- User says "new business idea" or "business idea"
- User uses /newidea command
- Agent discovers monetizable pattern during work

## Capture Process

### 1. Immediate Capture
When triggered, extract:
- **Idea name** (short, memorable)
- **One-liner** (what is it?)
- **Discovery context** (what were we doing?)
- **Why it's valuable** (pain point solved)
- **Proof of concept** (did we already build it?)

### 2. Create GitHub Issue
```bash
gh issue create --repo mikecranesync/Rivet-PRO \
  --title "💡 Product Idea: [NAME]" \
  --body "[TEMPLATE]" \
  --label "enhancement"
```

### 3. Update Memory
Append to `/root/jarvis-workspace/memory/YYYY-MM-DD.md`:
```markdown
## Business Ideas Discovered Today

### [Name]
**Time:** HH:MM UTC
**Trigger:** [What were we doing]
**Core insight:** [Why this is valuable]
**Status:** [Idea | POC Working | Prototype | Product]
```

### 4. Update Ideas Index
Maintain `/root/jarvis-workspace/memory/business-ideas.md` with all ideas.

## Ideas Index Location
`/root/jarvis-workspace/memory/business-ideas.md`

## GitHub Label
Use `enhancement` label (create `business-idea` label if repo allows)

## Template for Issue Body
```markdown
## Business Idea: [NAME]

**Discovered:** [DATE] while [CONTEXT]

### What It Does
[One paragraph description]

### Market Opportunity
| Customer | Pain Point | Price Point |
|----------|------------|-------------|
| [Segment] | [Problem] | $XX |

### Competitive Advantage
- [Unique thing 1]
- [Unique thing 2]

### Status
- [ ] Idea captured
- [ ] Proof of concept
- [ ] Landing page
- [ ] MVP
- [ ] Revenue

---
*Auto-captured by Jarvis Business Idea System*
```

## Future: Repo Mining Swarm
TODO: Build agent swarm to scan all 50 GitHub repos for:
- Interesting tools built
- Problems solved
- Patterns that could be products
- Dead code that had potential

Output: Consolidated business ideas report
