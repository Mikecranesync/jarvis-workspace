# Pending Decisions — Morning Review

*Prepared: 2026-01-30 05:20 UTC*
*For: Mike Harper*
*From: Jarvis Orchestrator*

---

## Decision 1: Hetzner Migration

### The Question
Should we migrate from Hostinger VPS (4GB RAM, €12/mo) to Hetzner (16GB RAM, €12/mo)?

### Context
- Current VPS is maxed out on RAM
- Local LLM is too slow (40s for simple prompts)
- Can't run multiple agent instances in parallel
- Hetzner offers 4x RAM for same price

### Options

| Option | Pros | Cons |
|--------|------|------|
| **A: Migrate Now** | Better performance immediately | Downtime risk, migration work |
| **B: Migrate Later** | No disruption | Continue limited by RAM |
| **C: Keep Current** | Stability | Blocked on local LLM |

### My Recommendation
**Option A: Migrate Now** — The RAM limitation is blocking multiple priorities (local LLM, parallel agents). Same cost, 4x resources.

### If Approved
I can prepare migration checklist and schedule for minimal downtime.

---

## Decision 2: BeagleBone / Edge Adapter

### The Question
How do we proceed with the Edge Adapter given the BeagleBone needs a password reset?

### Context
- BeagleBone is physically at your location
- Needs SD card reflash to reset password
- P1 priority on Trello (Industrial Edge Adapter)
- Blocks real PLC data collection

### Options

| Option | Pros | Cons |
|--------|------|------|
| **A: You flash it** | Fastest path | Requires your time |
| **B: Ship to me** | I handle it | Delay, shipping cost |
| **C: Buy new device** | Fresh start | Cost (~$50-100) |
| **D: Defer project** | Focus elsewhere | Blocks vision goal |

### My Recommendation
**Option A** if you have 30 minutes — Otherwise **Option D** and revisit in 2 weeks.

### If Approved
I'll prepare the exact flash instructions for Debian/Ubuntu on BeagleBone.

---

## Decision 3: Content Publication Cadence

### The Question
How often should we publish LinkedIn content?

### Context
- I've drafted 5 LinkedIn posts ready for review
- Industry best practice: 3-5 posts/week for B2B
- You'll need to personalize and post from your account
- Goal: Build FactoryLM brand awareness

### Options

| Option | Frequency | Your Time Required |
|--------|-----------|-------------------|
| **A: Aggressive** | 5/week | ~30 min/week review |
| **B: Moderate** | 3/week | ~20 min/week review |
| **C: Light** | 1/week | ~10 min/week review |

### My Recommendation
**Option B: 3/week** — Mon/Wed/Fri rhythm. Sustainable, builds presence.

### If Approved
I'll prepare a 4-week content calendar with posts queued.

---

## Decision 4: Landing Page Priority

### The Question
Should landing page be the immediate focus, or continue with infrastructure?

### Context
- Landing page copy drafted (3 options)
- No current email capture mechanism
- Product not fully ready for customers
- But: Can start building email list now

### Options

| Option | Focus | Trade-off |
|--------|-------|-----------|
| **A: Landing page now** | Marketing first | Product gaps remain |
| **B: Product first** | Build before selling | Delays list building |
| **C: Parallel** | Both at 50% | Slower on both |

### My Recommendation
**Option A** — Even a simple landing page with email capture starts the flywheel. Product can continue in parallel.

### If Approved
I'll create a minimal factorylm.com deployment spec.

---

## Decision 5: API Keys for Full YCB Pipeline

### The Question
Which API keys should we configure for the YouTube Content Factory?

### Context
- Manim rendering: ✅ Working
- Script generation: Needs LLM API (local too slow)
- Voice generation: Needs TTS API or use free Edge TTS
- Image generation: Optional (thumbnails)

### Options

| Service | Purpose | Cost | Recommendation |
|---------|---------|------|----------------|
| **Groq** | Script LLM | Free tier | ✅ Enable |
| **Edge TTS** | Voice | Free | ✅ Enable |
| **ElevenLabs** | Better voice | ~$5/mo | Optional |
| **Anthropic** | Backup LLM | Pay-per-use | Optional |

### My Recommendation
Start with **Groq + Edge TTS** (both free). Add ElevenLabs later if quality needs improvement.

### If Approved
Share Groq API key or I'll sign up for a free account.

---

## Summary Action Required

| Decision | My Rec | Your Input Needed |
|----------|--------|-------------------|
| Hetzner | Migrate now | Approve timing |
| BeagleBone | You flash or defer | Time availability |
| Content | 3/week | Approve cadence |
| Landing page | Do now | Approve priority |
| API keys | Groq + Edge TTS | Share or approve signup |

---

*Ready when you wake up. No rush — the factory keeps running.*
