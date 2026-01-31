# AI Blog Automation — Research

*Date: 2026-01-30*
*Source: Mike's research + GitHub analysis*

---

## Current Setup

- Landing page: GitHub Pages (static HTML)
- No WordPress
- GitHub-centric workflow
- Claude + Perplexity for content

---

## Repo Options

### WordPress-Focused

| Repo | Stars | Language | Best For |
|------|-------|----------|----------|
| grumpyp/blogging-with-ai | 60 | Python | WordPress end-to-end |
| AryanVBW/AUTO-blogger | 8 | Python | WordPress + Getty + SEO |
| imgeraldalinio/AI-Generated-WordPress-Blog-Post-Automation | - | Python | Technical WordPress posts |

### Static Site / GitHub-Centric

| Repo | Stars | Language | Best For |
|------|-------|----------|----------|
| ikramhasan/AutoBlog-AI-Blog-Generator | 14 | Jupyter | Local LLMs, static sites |
| kunal00000/Blogblocks | - | - | Block-based content |
| Abdulbasit110/Blog-writer-multi-agent | 44 | Jupyter | Multi-agent quality |

---

## Recommended Architecture for FactoryLM

```
┌─────────────────────────────────────────────────────────┐
│                    BLOG AUTOMATION                      │
│                                                         │
│  ┌──────────────┐      ┌──────────────────────┐        │
│  │  Cron Job    │─────►│  Research Agent      │        │
│  │  (Daily)     │      │  (Perplexity)        │        │
│  └──────────────┘      └──────────────────────┘        │
│                                 │                       │
│                                 ▼                       │
│                        ┌──────────────────────┐        │
│                        │  Writer Agent        │        │
│                        │  (Claude)            │        │
│                        └──────────────────────┘        │
│                                 │                       │
│                                 ▼                       │
│                        ┌──────────────────────┐        │
│                        │  Editor Agent        │        │
│                        │  (Claude)            │        │
│                        └──────────────────────┘        │
│                                 │                       │
│                                 ▼                       │
│  ┌──────────────┐      ┌──────────────────────┐        │
│  │  GitHub      │◄─────│  Markdown Output     │        │
│  │  Commit      │      │  + SEO Metadata      │        │
│  └──────────────┘      └──────────────────────┘        │
│         │                                               │
│         ▼                                               │
│  ┌──────────────┐                                       │
│  │  Vercel /    │                                       │
│  │  GitHub Pages│                                       │
│  └──────────────┘                                       │
└─────────────────────────────────────────────────────────┘
```

---

## Implementation Steps

1. Fork `Blog-writer-multi-agent`
2. Replace Gemini with Claude API
3. Add Perplexity for research step
4. Output Markdown to blog repo
5. Set up GitHub Actions for deploy
6. Add cron for scheduled posts

---

## Content Strategy Integration

Topics (from ICP research):
- PLC error codes (Siemens, Allen-Bradley, ABB)
- Maintenance best practices
- Diagnostic tips
- Industry trends
- Case studies

Frequency: 2-3 posts/week

SEO targets: "Siemens error codes", "PLC troubleshooting", etc.

---

## References

- grumpyp/blogging-with-ai
- AryanVBW/AUTO-blogger
- ikramhasan/AutoBlog-AI-Blog-Generator
- Abdulbasit110/Blog-writer-multi-agent
- HowDoIUseAI.com case study (Claude + GitHub Actions)

---

*Ready to fork and adapt when Mike approves.*
