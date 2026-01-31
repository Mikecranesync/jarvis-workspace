# FactoryLM Blog Automation

Multi-agent AI blog generation system for FactoryLM.

## Architecture

```
Perplexity (Research)
    ↓
Claude (Write)
    ↓
Claude (Edit)
    ↓
GitHub (Publish)
```

## Setup

1. Add secrets to GitHub repo:
   - `PERPLEXITY_API_KEY`
   - `ANTHROPIC_API_KEY`

2. Enable GitHub Actions

3. Posts auto-generate Mon/Thu at 9 AM UTC

## Manual Generation

```bash
export PERPLEXITY_API_KEY=your_key
export ANTHROPIC_API_KEY=your_key
python generate_post.py "Your Topic Here"
```

## Topic Ideas

See `TOPIC_IDEAS` in `generate_post.py`

## Integration

Posts output as Markdown with frontmatter.
Deploy to any static site generator (Jekyll, Hugo, Next.js, Astro).

---

*Part of the FactoryLM content factory.*
