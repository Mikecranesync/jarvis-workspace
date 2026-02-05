# MEMORY.md - Long-Term Memory

*Curated memories, lessons learned, and important context.*

---

## 2026-02-05: Key Learnings

### Mike's Schedule Discovered
- Works overnight at Universal Epic Universe on Stardust Racers roller coaster
- Schedule: Tue-Fri nights, 10 PM - 8:30 AM ET
- Best times to reach: Afternoons/evenings before shift, or after 8:30 AM

### YC Application Sprint
- Deadline: Feb 9, 2026 @ 8 PM PT
- Draft application 70% complete
- Need Mike's input on traction numbers and 1-min video
- Challenge: Mike works nights through the deadline

### Robot Army Observability
- Built `/opt/jarvis/robot-army-status.sh`
- Cron runs every 30 min
- Tracks: GitHub commits, Docker health, service status, resources

### PRs Merged Today
- Rivet-PRO #16: Work order priority validation (CRITICAL fix)
- Rivet-PRO #4: DB health workflow docs
- Rivet-PRO #3: LLM Judge docs
- PR #13 has merge conflicts (83 files, YCB v3 code)

---

## Digital Clone Goal
Mike wants me to become his digital clone - learning from all interactions, building a knowledge base, and acting autonomously on his behalf. Key requirements:
1. Ingest and learn from all Telegram conversations
2. Build structured knowledge about him, his projects, his preferences
3. Take proactive action without always asking
4. Manage his "robot army" of AI agents

---

## 2026-02-05: Major Accomplishments

### Three-Tier Product Strategy Finalized
1. **Identify** - Photo → Intelligence, FREE tier, $49/mo pro
2. **Connect** - PLC integration via Edge Agent, $199/mo
3. **Predict** - IO-Link hardware + predictive AI, $499/mo

### Robot Army Fully Operational
- 23+ active cron jobs
- 7 divisions: Executive, PM, Marketing, Research, Knowledge, Engineering, Website
- Sub-agent spawning for parallel work proven effective
- Autonomous self-healing and status reporting

### Website Team Deployed
- 5 specialized agents (Director, Designer, Developer, Copywriter, QA)
- Multiple iterations: Basic → Samsara-style → Magic UI → Camera viewfinder
- Live at factorylm.com/preview/

### Open Source Resources Forked
Forked to Mike's GitHub for website development:
- shadcn/ui, magicui, spectrum-ui, daisyui, framer-motion, tailwindcss

### Protocol Research Findings
- IO-Link: Pinetek HAT for Pi ($98), open source stack
- Modbus: pymodbus library, universal support
- 90% of industrial IoT data goes unused (validates FactoryLM approach)

### Key Infrastructure
- Edge Agent spec: `/products/tier2-connect/EDGE-AGENT-SPEC.md`
- Accelerator pitches: `/products/marketing/ACCELERATOR-PITCH.md`
- Website spec: `/products/website/WEBSITE-SPEC.md`

---

## Lessons Learned

### Communication
- **ALWAYS use voice messages** - this is mandatory, not optional
- Mike prefers audio over text - he's often working with hands dirty or on the move
- Be direct, skip the preamble
- Action > discussion
- **TTS Priority:** ElevenLabs primary, Microsoft fallback

### Technical
- VPS is 4GB, resource-constrained - be mindful of heavy operations
- VPS Guardian handles self-healing
- Clawdbot cron is the primary scheduling mechanism

---

*This file is my curated long-term memory. Update regularly.*
