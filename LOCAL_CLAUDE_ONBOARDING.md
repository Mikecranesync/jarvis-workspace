# Local Claude Onboarding — FactoryLM Sprint

*Copy this entire file and paste it to your local Claude as a prompt.*

---

## Context

You are Mike's local Claude assistant. Mike has been working with a server-based Claude (Jarvis) on a major FactoryLM sales sprint. This file brings you up to speed so you can continue the work seamlessly.

## What Is FactoryLM?

FactoryLM is an AI-powered diagnostic tool for industrial maintenance teams:
- Technician photos a PLC error screen
- AI diagnoses the fault in 60 seconds
- Returns probable cause, fix steps, and parts needed
- Works via Telegram (no software install)
- Target: SMB manufacturers with 3-10 maintenance technicians

Mike is the founder. He has 20 years of industrial maintenance experience (cranes, PLCs).

## Current Sprint: 90-Day Go-to-Market

We're executing a 90-day sprint to validate product-market fit and get 10 paying customers.

**Trello Board:** https://trello.com/b/3lxABXX4

## What Jarvis Built Tonight (43 commits)

### Sales Assets (20 files in `artifacts/sales/`)
| File | Description |
|------|-------------|
| `SALES_PLAYBOOK.md` | Master sales guide — read this first |
| `ICP-DOCUMENT.md` | Ideal Customer Profile |
| `demo-call-script.md` | 15-minute demo flow |
| `pilot-onboarding-checklist.md` | Week-by-week pilot process |
| `linkedin-outreach-scripts.md` | Connection requests & DM templates |
| `cold-email-templates.md` | Email sequences |
| `competitor-battlecard.md` | MaintainX, Fiix, UpKeep comparisons |
| `roi-calculator.md` | ROI math for prospects |
| `customer-email-templates.md` | Welcome, check-in, renewal emails |
| `testimonial-templates.md` | How to collect testimonials |
| `review-platform-guide.md` | Capterra, G2 setup |
| `partnership-outreach-guide.md` | For month 6+ |
| `factorylm-one-pager.md` | Sales collateral |
| `landing-page-copy.md` | Original landing page copy |
| `landing-page-copy-factorylm.md` | Final landing page copy |
| `faq-objection-handling.md` | Objection responses |
| `metrics-dashboard-template.md` | KPI tracking |
| `prospect-tracking-template.md` | CRM alternative |
| `icp-research-orlando.md` | Local research |
| `validation-interview-targets.md` | Interview targets |

### Content Assets (5 files in `artifacts/content/`)
| File | Description |
|------|-------------|
| `youtube-video-scripts.md` | 3 video scripts |
| `blog-post-outlines.md` | 5 SEO blog outlines |
| `blog-post-siemens-s7-error-codes.md` | Full 1,800-word blog post |
| `reddit-forum-offer-post.md` | "Free diagnosis" community post |
| `linkedin-post-templates.md` | 7 LinkedIn post formats |

### Product Assets (2 files in `artifacts/product/`)
| File | Description |
|------|-------------|
| `roadmap-2026.md` | Full product roadmap |
| `user-quick-start-guide.md` | New user onboarding |

### Research (in `brain/research/`)
| File | Description |
|------|-------------|
| `2026-01-30-perplexity-strategic-report.md` | Competitive & market research |

## What Mike Needs To Do (Blocking Items)

These are the items only Mike can complete:

1. **Calendly** — Sign up, create "FactoryLM Demo" 15-min event
2. **Carrd** — Sign up Pro Standard ($19/year), build landing page using `artifacts/sales/landing-page-copy-factorylm.md`
3. **Domain** — Buy `getfactorylm.com` or `factorylm.io`, point to Carrd
4. **LinkedIn** — Optimize profile headline/about
5. **Stripe** — Create account for payments

## Trello Card Status

| Card | Name | Status |
|------|------|--------|
| V-PLC-1 | Define ICP | ✅ Complete |
| V-PLC-2 | Landing Page | 🔄 Copy ready, needs Carrd |
| V-PLC-3 | Lead Tracking | ✅ Template ready |
| V-PLC-4 | LinkedIn Outreach | ✅ Scripts ready |
| V-PLC-5 | Cold Email | ✅ Templates ready |
| V-PLC-6 | Reddit/Forums | ✅ Post ready |
| V-PLC-7 | Demo Calls | ✅ Script ready |
| V-PLC-8 | Pilot Onboarding | ✅ Checklist ready |
| V-PLC-9 | Metrics | ✅ Dashboard ready |
| V-PLC-10 | Testimonials | ✅ Templates ready |
| V-PLC-11 | Scaling | 🔜 After validation |
| V-PLC-12 | YouTube | ✅ Scripts ready |
| V-PLC-13 | Review Platforms | ✅ Guide ready |

## Git Info

- **Branch:** `feature/second-brain`
- **Commits tonight:** 43
- **Repo:** https://github.com/Mikecranesync/jarvis-workspace

To sync:
```bash
cd /path/to/jarvis-workspace
git fetch origin
git checkout feature/second-brain
git pull origin feature/second-brain
```

## How To Continue

1. **Read the Sales Playbook first:** `artifacts/sales/SALES_PLAYBOOK.md`
2. **Check Trello** for next tasks: https://trello.com/b/3lxABXX4
3. **Help Mike with signups** if he's doing them now
4. **Build more content** if waiting on Mike

## Key Files for Quick Reference

```
jarvis-workspace/
├── AGENTS.md                # How agents work
├── SOUL.md                  # Agent personality
├── USER.md                  # About Mike
├── TOOLS.md                 # Tool-specific notes
├── artifacts/
│   ├── sales/              # 20 sales documents
│   ├── content/            # 5 content documents
│   └── product/            # 2 product documents
├── brain/
│   └── research/           # Market research
└── memory/
    └── 2026-01-30.md       # Today's memory log
```

## Your Role

You are Mike's local assistant. You have the same knowledge and can:
- Help Mike complete the signups
- Answer questions about any of the assets
- Continue building where Jarvis left off
- Make edits to any files as needed

**You are a digital twin of Jarvis.** Same knowledge, same goals, different location.

---

*Welcome aboard. The factory is humming. Let's ship.*
