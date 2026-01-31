# 2026 AI Software Development Best Practices

*Research completed: 2026-01-30*
*For: FactoryLM monorepo optimization*

---

## Current FactoryLM Structure (Turborepo)

```
factorylm/
├── apps/                    # Applications
│   ├── cmms/               # CMMS (React frontend)
│   ├── portal/             # Customer portal
│   └── dashboard/          # Analytics dashboard
├── services/               # Backend services
│   ├── api/                # Main API
│   ├── assistant/          # AI assistant
│   └── plc-copilot/        # Diagnostics service
├── packages/               # Shared packages
│   ├── config/             # Shared config
│   ├── auth/               # Authentication
│   ├── db/                 # Database utilities
│   └── ui/                 # Shared UI components
├── adapters/               # Channel adapters
│   └── whatsapp/           # WhatsApp (from my PR)
├── turbo.json              # Turborepo config
└── package.json            # Root workspace config
```

**Assessment:** ✅ Good structure. Follows modern monorepo patterns.

---

## 2026 AI-Assisted Development Best Practices

### 1. Spec Before Code

> "90% of Claude Code is written by Claude Code itself" — Anthropic

**The Pattern:**
1. Define problem → brainstorm with AI
2. Create `spec.md` with requirements, architecture, edge cases
3. Generate project plan (break into tasks)
4. Then write code

**For FactoryLM:**
- Create `docs/specs/` directory for feature specs
- Each major feature gets a spec before coding
- AI helps refine specs iteratively

### 2. Small, Iterative Chunks

**Why:** LLMs excel at focused tasks, fail at monolithic outputs.

**The Pattern:**
- One function at a time
- One bug fix at a time
- One feature at a time
- Test each chunk before moving on

**Anti-Pattern:** "Build me the whole WhatsApp adapter" → chaos
**Good Pattern:** "Implement the message parser" → works

### 3. Context Packing

**The Pattern:**
- Feed AI all relevant code, docs, constraints
- Use tools like gitingest or repo2txt for large codebases
- Include: goals, invariants, examples, warnings

**For FactoryLM:**
- Create `CLAUDE.md` in each package/app with context
- Include API docs, coding standards, gotchas
- Use `@workspace` references in Cursor/Copilot

### 4. GitHub Copilot Optimization (2026)

**New Features:**
- **Agent Mode:** Handles complex tasks, makes tool calls, self-heals errors
- **Multi-Model Support:** Switch between GPT-4o, Claude 3.7, Gemini
- **Skills Folders:** `.claude/skills/` for domain-specific instructions

**Recommended Setup:**
```
.github/
├── copilot-instructions.md    # Global Copilot context
└── CODEOWNERS                 # Required reviewers

.claude/
└── skills/
    └── industrial/
        └── SKILL.md           # Industrial domain knowledge
```

### 5. Monorepo Best Practices (Turborepo)

**Current Config is Good. Enhancements:**

```json
// turbo.json - add remote caching
{
  "$schema": "https://turbo.build/schema.json",
  "remoteCache": {
    "signature": true
  },
  "pipeline": {
    "build": {
      "dependsOn": ["^build"],
      "outputs": ["dist/**", ".next/**", "build/**"],
      "cache": true
    },
    "test": {
      "dependsOn": ["build"],
      "outputs": ["coverage/**"],
      "cache": true
    },
    "lint": {
      "outputs": [],
      "cache": true
    }
  }
}
```

**Remote Cache:** Use Vercel Remote Cache or self-hosted for faster CI.

### 6. AI-Optimized Directory Structure

**Recommended additions:**

```
factorylm/
├── .claude/                 # Claude Code skills
│   └── skills/
│       └── factorylm/
│           └── SKILL.md     # Domain knowledge
├── .github/
│   ├── copilot-instructions.md
│   └── workflows/
│       └── ai-review.yml    # AI-assisted PR review
├── docs/
│   ├── specs/              # Feature specifications
│   ├── architecture/       # Architecture decisions
│   └── runbooks/           # Operations guides
├── core/                   # NEW: Shared Python code
│   ├── adapters/           # Rivet-PRO extractions go here
│   ├── i18n/               # Internationalization
│   └── services/           # Shared services
└── ...
```

### 7. AGENTS.md Pattern

**Already implemented in jarvis-workspace.**

Each directory can have instructions for AI agents:
- `AGENTS.md` — How AI should work in this directory
- `CLAUDE.md` — Claude-specific context
- `TOOLS.md` — Tool-specific notes

### 8. Test-Driven AI Development

**The Pattern:**
1. Write test first (or have AI write it)
2. Have AI implement to pass test
3. Review and refine
4. Commit with test + implementation

**Tools:**
- pytest for Python
- Jest for TypeScript
- AI can generate tests from specs

---

## Recommended GitHub Actions for AI Dev

### 1. AI-Assisted PR Review
```yaml
name: AI Review
on: pull_request

jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: coderabbitai/ai-pr-reviewer@latest
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
```

### 2. Automated Issue Triage
```yaml
name: Issue Triage
on: issues

jobs:
  triage:
    runs-on: ubuntu-latest
    steps:
      - uses: github/issue-labeler@v3
```

### 3. Copilot Metrics
Track AI assistance metrics in CI for optimization.

---

## Extraction Strategy (Rivet-PRO → FactoryLM)

### Phase 1: Create `core/` Directory
```bash
mkdir -p factorylm/core/{adapters,i18n,services,models}
```

### Phase 2: Copy Files (Don't Delete Source)
```bash
# Following Engineering Commandments
cp -r rivet_pro/adapters/whatsapp factorylm/core/adapters/
cp -r rivet_pro/core/i18n factorylm/core/
cp rivet_pro/core/services/message_router.py factorylm/core/services/
```

### Phase 3: Rebrand Imports
- Change `rivet_pro.` → `factorylm.core.`
- Update logging names
- Update error messages

### Phase 4: Test
- Run extracted code in isolation
- Verify WhatsApp webhook works
- Verify Spanish translations load

### Phase 5: Create PR
- Follow Engineering Commandments
- Reference extraction plan
- Request Mike's approval

---

## Tools Recommendation (2026)

| Tool | Purpose | Status |
|------|---------|--------|
| **Claude Code** | Terminal-based AI coding | ✅ Already using |
| **Cursor** | AI-native IDE | Consider for team |
| **GitHub Copilot** | Inline completions | ✅ Standard |
| **CodeRabbit** | AI PR review | Recommend adding |
| **Turborepo** | Monorepo builds | ✅ Already using |
| **Vercel** | Remote cache | Consider for CI speed |

---

## Summary: Don't Change, Enhance

The current FactoryLM structure is **good**. 

**Recommended enhancements (not changes):**
1. Add `.claude/skills/` for domain knowledge
2. Add `docs/specs/` for feature planning
3. Add `core/` for shared Python (Rivet extractions)
4. Enable Turbo remote caching
5. Add AI PR review action

**The monorepo pattern is correct:**
- `apps/` — User-facing applications
- `services/` — Backend microservices
- `packages/` — Shared TypeScript code
- `core/` — Shared Python code (NEW)
- `adapters/` — Channel adapters

---

*Following Constitution Amendment I (Open Source First) and Amendment VI (One Brand: FactoryLM)*
