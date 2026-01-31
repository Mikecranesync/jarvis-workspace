# The Automaton
## Autonomous Content Creation System

**Priority:** P-0 (META - System that builds systems)
**Status:** In Development
**Created:** 2026-01-31

---

## Purpose

The Automaton is an autonomous content creation pipeline that:
1. Captures work being done (screen recordings, terminal sessions, screenshots)
2. Generates narration via TTS
3. Assembles videos
4. Drafts social media posts
5. Sends for approval via Telegram
6. Posts automatically on approval

**Mike's role:** Approve with "post it" via Telegram
**Jarvis's role:** Everything else

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     THE AUTOMATON                           │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐              │
│  │ CAPTURE  │───▶│ NARRATE  │───▶│ ASSEMBLE │              │
│  │          │    │          │    │          │              │
│  │ Terminal │    │ Script   │    │ FFmpeg   │              │
│  │ Screen   │    │ TTS      │    │ Video    │              │
│  │ Photos   │    │ Audio    │    │ Output   │              │
│  └──────────┘    └──────────┘    └──────────┘              │
│                                        │                    │
│                                        ▼                    │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐              │
│  │  POST    │◀───│ APPROVE  │◀───│  DRAFT   │              │
│  │          │    │          │    │          │              │
│  │ LinkedIn │    │ Telegram │    │ Copy     │              │
│  │ Twitter  │    │ Mike OK  │    │ Hashtags │              │
│  │ YouTube  │    │          │    │ Format   │              │
│  └──────────┘    └──────────┘    └──────────┘              │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Components

### 1. Capture System
**Location:** `src/capture/`

| Tool | Purpose | Format |
|------|---------|--------|
| asciinema | Terminal recordings | .cast → .gif/.mp4 |
| scrot | Screenshots | .png |
| ffmpeg | Screen recording | .mp4 |

**Auto-capture triggers:**
- Start of major task
- Completion milestones
- Error/debug moments
- Before/after comparisons

### 2. Narration System
**Location:** `src/narrate/`

| Component | Purpose |
|-----------|---------|
| Script Generator | Write narration from context |
| TTS Engine | Convert to audio (built-in) |
| Timing Sync | Match audio to visuals |

### 3. Assembly System
**Location:** `src/assemble/`

| Tool | Purpose |
|------|---------|
| FFmpeg | Combine video + audio |
| ImageMagick | Text overlays, thumbnails |
| Templates | Intro/outro, branding |

### 4. Distribution System
**Location:** `src/distribute/`

| Platform | Method |
|----------|--------|
| LinkedIn | API (need setup) |
| Twitter/X | API (need setup) |
| YouTube | API (future) |
| Telegram | Preview + approval |

### 5. Approval Flow
**Location:** `src/approve/`

```
1. Content ready → Preview sent to Telegram
2. Mike reviews (voice note or text)
3. "post it" → Auto-publish
4. "change X" → Edit and re-preview
5. "skip" → Archive, move on
```

---

## Directory Structure

```
projects/automaton/
├── README.md           # This file
├── config/
│   ├── platforms.yaml  # API keys, settings
│   └── templates.yaml  # Content templates
├── src/
│   ├── capture/
│   │   ├── terminal.py
│   │   ├── screenshot.py
│   │   └── screen.py
│   ├── narrate/
│   │   ├── script.py
│   │   └── tts.py
│   ├── assemble/
│   │   ├── video.py
│   │   └── thumbnail.py
│   ├── distribute/
│   │   ├── linkedin.py
│   │   ├── twitter.py
│   │   └── telegram.py
│   └── approve/
│       └── flow.py
├── templates/
│   ├── intro.mp4
│   ├── outro.mp4
│   └── overlays/
├── queue/              # Content waiting for approval
├── published/          # Archive of posted content
└── logs/
```

---

## Workflows

### Workflow 1: Terminal Demo
```
Trigger: Interesting terminal session
1. Start asciinema recording
2. Do the work
3. Stop recording
4. Generate script describing what happened
5. Create TTS narration
6. Convert to video with audio
7. Draft post copy
8. Send to Telegram for approval
9. Post on approval
```

### Workflow 2: Screenshot Story
```
Trigger: Visual milestone
1. Take before screenshot
2. Do the work
3. Take after screenshot
4. Generate comparison + narration
5. Create short video/carousel
6. Draft post
7. Approve + post
```

### Workflow 3: Daily Recap
```
Trigger: End of day (via cron)
1. Gather day's captures
2. Generate summary script
3. Create TTS recap
4. Compile highlights video
5. Draft post
6. Approve + post
```

---

## Integration Points

### With BeagleBone Project:
- Capture terminal sessions during setup
- Screenshot Factory I/O data collection
- Record model training progress
- Demo video of final product

### With Heartbeat:
- Check queue for pending approvals
- Generate daily recap if milestones hit
- Alert on viral post performance

---

## Implementation Phases

### Phase 1: Core Capture (Tonight)
- [ ] Install asciinema
- [ ] Install ffmpeg (if not present)
- [ ] Create capture scripts
- [ ] Test terminal recording

### Phase 2: Narration Pipeline (Tonight)
- [ ] Script generation templates
- [ ] TTS integration (already have)
- [ ] Audio file management

### Phase 3: Video Assembly (Saturday)
- [ ] FFmpeg pipeline
- [ ] Basic templates
- [ ] Thumbnail generation

### Phase 4: Distribution (Saturday)
- [ ] Telegram preview flow
- [ ] LinkedIn API setup
- [ ] Twitter API setup

### Phase 5: Approval Flow (Sunday)
- [ ] Telegram command handling
- [ ] Edit loop
- [ ] Auto-publish

---

## Success Metrics

| Metric | Target |
|--------|--------|
| Capture → Post time | < 30 min |
| Mike approval time | < 5 min |
| Posts per day | 1-3 |
| Content quality | Viral-worthy |

---

## Notes

- Anonymous posting (AI voice, no face)
- Mike only approves, never creates
- Everything automated except final OK
- This powers ALL other projects

---

*The system that builds the system.*
