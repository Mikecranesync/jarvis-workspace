# YouTube Content Factory — Research Complete

*Constitution: Research completed before building*

---

## Discovery Summary

Found **two major codebases** in Mike's GitHub that form a complete training content ecosystem:

### 1. YCB (YouTube Content Bot) v3
**Location:** `Mikecranesync/Rivet-PRO/ycb/`

A professional-grade video generation pipeline for industrial automation educational content.

#### Features
- **Manim Rendering** — 2D technical animations and diagrams
- **LLM Storyboarding** — AI-powered scene planning
- **28 SVG Assets** — IEC electrical and PLC symbols
- **6 Scene Templates** — Reusable animation templates
- **Quality Evaluation** — LLM-as-Judge video quality assessment
- **Autonomous Loop** — Batch video generation with quality gates

#### Key Files
```
ycb/
├── pipeline/
│   ├── video_generator_v3.py    # Main generator
│   ├── autonomous_loop.py       # Batch production
│   ├── quality_iteration.py     # Improvement loop
│   └── metrics.py               # Analytics
├── evaluation/
│   └── video_judge_v3.py        # LLM quality judge (8.5/10 threshold)
├── storyboard/                  # Scene planning
├── rendering/                   # Manim engine
├── assets/                      # SVG symbols (electrical, PLC)
├── audio/                       # Timing sync
└── composition/                 # Video compositor
```

#### Quality Judge Criteria
- Visual Quality (8.0+ threshold)
- Diagram Quality (8.0+ threshold)
- Transition Quality (7.0+ threshold)
- Script/Content Quality (7.5+ threshold)
- Audio Synchronization (7.5+ threshold)
- Metadata/SEO Quality

---

### 2. IndustrialSkillsHub
**Location:** `Mikecranesync/IndustrialSkillsHub`

Duolingo-style gamified training platform for industrial maintenance technicians.

#### Features
- **Role-based paths:** Mechanic, Electrician, PLC Technician, PLC Specialist
- **Gamification:** XP, hearts, streaks, leaderboards, badges
- **Bilingual:** Spanish/English
- **Mobile-ready:** React Native app also exists

#### Tech Stack
- Next.js 14 / React 18 / TypeScript
- PostgreSQL (Neon) / Drizzle ORM
- Clerk Auth / Stripe payments
- Vercel hosting

---

## Integration Vision

### The Content Factory Concept

```
┌─────────────────────────────────────────────────────────┐
│                   CONTENT FACTORY                        │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  ┌──────────────┐    ┌──────────────┐    ┌────────────┐ │
│  │ Topic Queue  │───▶│ YCB v3 Gen   │───▶│ LLM Judge  │ │
│  │ (from ISH)   │    │ (Manim/LLM)  │    │ (8.5/10)   │ │
│  └──────────────┘    └──────────────┘    └─────┬──────┘ │
│                                                 │        │
│         ┌───────────────────────────────────────┘        │
│         ▼                                                │
│  ┌──────────────┐    ┌──────────────┐    ┌────────────┐ │
│  │ YouTube      │───▶│ FactoryLM    │───▶│ Industrial │ │
│  │ Auto-Upload  │    │ Channel      │    │ Skills Hub │ │
│  └──────────────┘    └──────────────┘    └────────────┘ │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

### Channel Strategy

| Channel | Content | Audience |
|---------|---------|----------|
| Industrial Skills (existing) | Professional training | Experienced techs |
| FactoryLM (new) | Beginner content | Entry-level, 11yo level |

### Progressive Curriculum (Duolingo-style)

**Level 1: Basics**
- What is electricity?
- Ohm's Law explained
- Basic circuit concepts
- Wire types and colors

**Level 2: Intermediate**
- Series vs parallel circuits
- Reading schematics
- Using multimeters
- Safety basics

**Level 3: Advanced**
- PLC fundamentals
- Ladder logic
- Motor control
- Troubleshooting

---

## Resurrection Plan

### Phase 1: Audit & Test (Today)
1. Clone Rivet-PRO locally
2. Test YCB v3 pipeline
3. Verify Manim rendering works
4. Check YouTube API integration

### Phase 2: Quality Agent (This Week)
1. Create dedicated LLM Judge agent
2. Connect to YCB evaluation system
3. Set quality threshold to 8.5/10
4. Implement rejection → improvement loop

### Phase 3: Content Queue (Next Week)
1. Generate topic queue from IndustrialSkillsHub curriculum
2. Start with beginner electrical topics
3. Target: 1 video/day autonomous generation

### Phase 4: Publishing (Week 3)
1. Create FactoryLM YouTube channel
2. Configure auto-upload pipeline
3. Monitor quality metrics
4. Iterate on templates

---

## Benefits

- **Free advertising** for FactoryLM
- **Passive revenue** from YouTube monetization
- **Lead generation** for training platform
- **Content moat** for SEO/discoverability
- **Training data** for industrial AI models

---

## Dependencies

- Python 3.10+
- Manim (2D animations)
- FFmpeg (video encoding)
- YouTube API credentials
- TTS service (ElevenLabs or local)

---

*Research completed: 2026-01-30 02:15 UTC*
*Ready for implementation per Engineering Commandments*
