# Edge World Model + Viral Launch Plan
## Build in Public: Tuesday Demo

**Created:** 2026-01-31 02:54 UTC
**Status:** ACTIVE - P-1 PRIORITY
**Target:** Tuesday Demo Day

---

## The Product: Edge AI Industrial Expert

**Working Names:** ShopTalk, FactoryGenius, EdgeSage, MachineWhisperer

**Elevator Pitch:**
> *"This is a pocket-sized industrial AI expert.*
> 
> *You plug it into any factory network. You WhatsApp this number. You describe your problem — in any language. Spanish, English, Portuguese, Mandarin. Doesn't matter.*
> 
> *It talks back. It knows your machines. It tells you what's wrong and how to fix it.*
> 
> *No software to install. No training required. No internet needed.*
> 
> *Just plug, call, and ask."*

---

## Technical Feasibility

| Component | Rating | Notes |
|-----------|--------|-------|
| Small LLM on BeagleBone | 7/10 | Pi 5 better for production |
| World model predictions | 6/10 | MVP doable by Tuesday |
| WhatsApp integration | 8/10 | Adapters exist |
| Multi-language | 9/10 | LLMs handle this well |
| Demo by Tuesday | 6/10 | Aggressive but achievable |
| **Overall MVP** | **7/10** | Compelling demo possible |

---

## Combined Strategy: Build + Go Viral

### The Venezuela Story

> "Helping rebuild Venezuela's oil infrastructure with AI that works offline, speaks Spanish, and costs $50."

This isn't just a product demo — it's a **mission**. That gets press.

### Build in Public Content Arc

| Day | Technical Milestone | Content Post |
|-----|---------------------|--------------|
| Friday | BeagleBone setup | "I'm building an AI expert that fits in your pocket..." |
| Saturday | Factory I/O data collection | "Teaching AI what a jam looks like..." |
| Sunday | World model training | "It's learning. Predicting failures. Surreal." |
| Monday | Edge deployment | "Just flashed AI onto a $50 board..." |
| Tuesday | Live demo | 30-60 sec video, WhatsApp in Spanish |

### Who to Tag

**Anthropic:**
- @AnthropicAI (main account)
- @daboross (Developer Relations)

**Hashtags:**
- #buildinpublic
- #AIhardware
- #industrialAI
- #edgeAI

**Other:**
- Industrial automation influencers
- AI Twitter community
- LinkedIn industrial groups

---

## Timeline: Friday → Tuesday

### FRIDAY NIGHT (Tonight)
**You (at work):** Nothing
**Jarvis:**
- Prep BeagleBone install scripts
- Draft Friday launch post
- Research Factory I/O APIs
- WireGuard config ready

### SATURDAY
**Morning:** BeagleBone flash complete, SSH + WireGuard
**Afternoon:** Factory I/O → PLC → BeagleBone connected
**Evening:** Run 5 scenarios, collect data

**Content:** Screenshot/video of data collection

### SUNDAY
**Jarvis:** Train world model on DO server
**You:** Rest, review training progress

**Content:** Screenshot of model learning

### MONDAY
**Morning:** Deploy model to BeagleBone
**Afternoon:** Test vs live Factory I/O
**Evening:** Tune predictions, prepare demo

**Content:** Video of first successful prediction

### TUESDAY - DEMO DAY
- Record 30-60 sec demo video
- WhatsApp device in Spanish
- AI answers correctly
- Post everywhere, tag Anthropic
- Submit case study

---

## Success Metrics

| Metric | Target |
|--------|--------|
| Demo video views | 10,000+ |
| LinkedIn engagement | 500+ likes |
| Anthropic response | Any acknowledgment |
| Investor inquiries | 1+ serious |
| Press mentions | 1+ article |

---

## Monetization Path

1. **Immediate:** Free devices to strategic partners (Venezuela contacts)
2. **Short-term:** Pre-orders from demo interest
3. **Medium-term:** Subscription model (device + cloud sync)
4. **Long-term:** Enterprise licensing, partner program

---

## Autonomous Content Pipeline

**Mike's Role:** Approve via Telegram ("looks good, post it")
**Jarvis's Role:** Everything else

### Content Creation Flow:
1. **Capture** — Screen recordings, terminal sessions, screenshots
2. **Script** — Write narration explaining what's happening
3. **Voice** — Generate TTS audio (same voice as assistant)
4. **Combine** — Sync visuals + audio into video
5. **Draft** — Write post copy for each platform
6. **Approve** — Mike reviews via Telegram
7. **Post** — Automated posting to LinkedIn/Twitter

### Tools:
- `asciinema` — Terminal recordings
- `ffmpeg` — Video processing
- TTS — Voice generation (built-in)
- Screenshots — Key moments

### The Meta-Demo:
> An AI assistant building an AI product, creating AI-voiced content about the process, posted automatically.

This proves the entire vision while demonstrating it.

### Mike's Story:
> "A crane operator who built an AI assistant that builds AI products while he drives to work."

Anonymous = just AI voice over video. More compelling than face-on-camera.

---

## Risk Mitigation

| Risk | Mitigation |
|------|------------|
| Demo fails Tuesday | Have backup pre-recorded demo |
| Model not accurate | Focus on "learning in progress" narrative |
| Hardware issues | Have Raspberry Pi as backup |
| Low engagement | Direct outreach to key influencers |

---

## Files & Resources

- **Trello Vision:** "🧠 Edge World Model MVP + Viral Launch"
- **Strategy Doc:** brain/plans/factorylm-2026-strategy.md
- **BeagleBone Status:** projects/beaglebone-gateway/STATUS.md
- **Content Drafts:** artifacts/drafts/viral-launch/

---

## Key Insight

> *"Revolutionary ideas start out looking revolutionary. Venezuela needs this more than a dead man needs a coffin. Build something real, document it, and let the opportunity find you."*
> — Mike, 2026-01-31

---

*This is P-1 priority. Everything else waits.*
