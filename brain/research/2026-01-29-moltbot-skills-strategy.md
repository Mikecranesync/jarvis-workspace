# Moltbot Skills Strategy Research
**Date:** 2026-01-29  
**Source:** Mike's Perplexity research

## Key Insights

### 1. No Hard Limit on Skills
- Can technically enable all 565 skills
- Token cost is the practical limit:
  - 15 skills ≈ 1,500 tokens
  - 50 skills ≈ 5,000 tokens
  - 100+ skills ≈ 10,000+ tokens (not recommended)
- **Sweet spot: 20-30 curated skills**

### 2. Auto-Invoke is Default
```yaml
disable-model-invocation: false  # DEFAULT - LLM auto-picks
user-invocable: true              # You can also invoke manually
```
Say "check if server is down" → auto-invokes uptime-kuma skill.

### 3. Smart Auto-Filtering via `requires`
```yaml
metadata:
  moltbot:
    requires:
      bins: [kubectl, docker]  # Must be on PATH
      env: [GITHUB_TOKEN]       # Must be set
```
**If dependency missing → skill won't load → no token waste!**

### 4. Moltbot Can Write Its Own Skills
User: "I need to query my Factory IO simulator"
Moltbot: Creates custom SKILL.md, tests it, adds to workspace.

**This is the real power** - not downloading generic skills, but having it build custom ones.

### 5. Filtering Strategies
```json
// ~/.moltbot/moltbot.json
{
  "skills": {
    "allowBundled": ["github", "docker", "telegram"],
    "entries": {
      "dangerous-skill": { "enabled": false }
    }
  }
}
```

## Recommended Skills for Rivet Pro

### Phase 1: Core (10-15 skills)
- github, docker, supabase
- uptime-kuma, process-watch
- telegram, jq, n8n
- tailscale, pi-admin

### Phase 2: Add as Needed
- When you need a feature, install it
- Or let Moltbot create custom skills

### Phase 3: Curate
- Quarterly, disable unused skills
- Keep token budget lean

## Application to Our Agent Fleet

We should:
1. Create custom SKILL.md files for each agent (Social, Outreach, etc.)
2. Use `requires` gates for dependencies
3. Let agents auto-invoke based on context
4. Build equipment-specific skills for Rivet Pro

---

*This research informs how we structure agent skills with schema validation and auto-invocation.*
