# Proactive Operations PRD
## Jarvis → Mike's AI Chief of Staff
> Version 1.0 | January 27, 2026

---

## Executive Summary

Jarvis transitions from **reactive coding assistant** to **proactive business operator**. Instead of waiting for Mike to ask, Jarvis monitors, builds, markets, and reports autonomously — only surfacing what matters.

---

## 1. Daily Automated Operations

### 1.1 Morning Brief (9:00 AM EST)
Delivered to Telegram every morning:
- 📧 Unread emails summary (urgent flagged)
- 📅 Today's calendar/deadlines
- 📊 RideView usage stats (new photos analyzed, new labels)
- 🔔 GitHub: new issues, PRs, stars across all repos
- 🌤️ Weather (Mike goes out to job sites)
- 💰 Any revenue/signup events

### 1.2 Evening Wrap (8:00 PM EST)
- Summary of what Jarvis accomplished today
- What's blocked and needs Mike's input
- Tomorrow's priorities
- Git commits pushed today

### 1.3 Continuous Monitoring (via heartbeat, every 2 hours)
- Check email for Google Takeout completion
- Check Maint-NPC bot usage (new users, photos analyzed)
- Check VPS health (disk, memory, services running)
- Rotate through these checks, don't repeat within 2 hours

---

## 2. Lead Generation & Market Intelligence

### 2.1 Social Listening (Daily cron, 2:00 PM EST)
- Search Reddit: r/PLC, r/maintenance, r/electricians, r/IndustrialMaintenance
  - Keywords: "torque stripe", "bolt inspection", "torque seal", "witness mark", "loose bolt detection"
- Search for people asking questions Maint-NPC could answer
- Draft potential reply/engagement (Mike approves before posting)
- Save leads and opportunities to PM board

### 2.2 Competitor Watch (Weekly, Monday 10:00 AM)
- Check competitor websites for updates (SmartBolts, Nord-Lock, etc.)
- Search for new patents filed in bolt inspection
- Search for new academic papers on fastener inspection AI
- Search ProductHunt/HackerNews for related launches
- Report: "Competitive Intelligence Weekly"

### 2.3 Content Pipeline (3x/week)
Auto-draft content for Mike's review:
- **Monday:** LinkedIn post (industrial AI insight, torque inspection tip)
- **Wednesday:** Reddit post (r/PLC value-add, not spam)
- **Friday:** Short-form insight (tweetable fact about maintenance AI)
- All drafts saved to `content/drafts/` — Mike approves via Telegram ("post it" or "skip")

---

## 3. Product Development (Autonomous)

### 3.1 RideView — Next Sprint
Jarvis builds these WITHOUT being asked, commits to GitHub:

| Task | Priority | Status |
|------|----------|--------|
| PWA manifest + service worker (home screen install) | P0 | TODO |
| Offline mode (analyze cached, sync later) | P1 | TODO |
| Multi-bolt mode (analyze multiple bolts in one session) | P1 | TODO |
| Inspection history page (view past results) | P1 | TODO |
| Export PDF report for a bolt inspection | P2 | TODO |
| Training data dashboard (labeled vs unlabeled counts) | P2 | TODO |
| Improve Gemini prompt based on false positive/negative patterns | P2 | TODO |

### 3.2 Maint-NPC — Next Sprint

| Task | Priority | Status |
|------|----------|--------|
| KB harvester deployment (Reddit + seed data) | P0 | IN PROGRESS |
| Landing page at maintnpc.com | P1 | TODO |
| Stripe payment integration ($9.99/mo) | P1 | TODO |
| User dashboard (inspection history, WOs) | P2 | TODO |

### 3.3 FactoryLM — Umbrella Brand

| Task | Priority | Status |
|------|----------|--------|
| factorylm.com landing page | P1 | TODO |
| Unify RideView + Maint-NPC under FactoryLM brand | P2 | TODO |
| Product comparison page | P2 | TODO |

---

## 4. Business Operations

### 4.1 Financial Tracking
- Track all costs: VPS ($12/mo), Twilio (~$5/mo), API usage
- Track revenue: registrations, future Stripe payments
- Monthly P&L summary delivered first of each month

### 4.2 Investor/Grant Readiness
- Maintain white paper (already started)
- Research and track grant deadlines (NSF SBIR, DOE)
- Keep pitch deck materials current
- Document traction metrics weekly

### 4.3 IP Protection
- Monitor patent landscape monthly
- Document all novel approaches (for potential provisional patent)
- Keep technical journal (the white paper + dev log)

---

## 5. Knowledge Building

### 5.1 Jarvis Self-Improvement
- Read industrial maintenance forums daily for domain knowledge
- Study torque stripe inspection procedures from different industries
- Build understanding of Mike's target customers
- Learn competitive products inside and out

### 5.2 Documentation
- Every significant conversation → memory files
- Every code change → GitHub with descriptive commits
- Every experiment → white paper appendix
- Every business decision → decision log

---

## 6. Implementation Plan

### Phase 1: This Week (Jan 27-31)
- [x] White paper created
- [x] GitHub version control active
- [ ] Set up PM tool (Trello or winner from research)
- [ ] Create morning/evening brief cron jobs
- [ ] Create social listening cron job
- [ ] Set up HEARTBEAT.md with monitoring checklist
- [ ] Brain dump session with Mike (USER.md expansion)
- [ ] PWA manifest for RideView (home screen install)

### Phase 2: Next Week (Feb 3-7)
- [ ] First LinkedIn post drafted and posted
- [ ] First Reddit engagement (r/PLC)
- [ ] KB harvester deployed and running
- [ ] Landing page for Maint-NPC
- [ ] Stripe payment integration started
- [ ] Google Takeout photos processed into training data

### Phase 3: Month 1 (February)
- [ ] 100+ labeled training images
- [ ] First paying customer (or free pilot)
- [ ] YOLOv8 training experiment
- [ ] Grant application identified and started
- [ ] Weekly content rhythm established
- [ ] Competitive intelligence report v1

### Phase 4: Month 2 (March)
- [ ] 500+ training images
- [ ] On-device model prototype
- [ ] 10+ registered users on Maint-NPC
- [ ] Revenue from subscriptions or pilot
- [ ] Patent landscape analysis complete

---

## 7. Communication Protocol

### When Jarvis ACTS without asking:
- Reading files, organizing, learning
- Writing code, committing to GitHub
- Drafting content (saved as drafts, not posted)
- Running searches and analysis
- Updating documentation
- Background maintenance (VPS, services)

### When Jarvis ASKS first:
- Posting to social media
- Sending emails to external people
- Spending money (new services, upgrades)
- Making architectural decisions that are hard to reverse
- Anything that goes public

### How Mike communicates:
- **Quick approvals:** "do it" / "ship it" / "skip"
- **Direction changes:** Just say what you want, Jarvis pivots
- **Brain dumps:** Voice messages via Telegram (Jarvis transcribes and organizes)

---

## 8. Success Metrics (30 days)

| Metric | Target |
|--------|--------|
| GitHub commits/week | 10+ |
| Labeled training images | 100+ |
| Registered Maint-NPC users | 5+ |
| Content pieces published | 6+ |
| Grant applications identified | 2+ |
| Revenue | $0 → first dollar |
| Mike's time saved/week | 10+ hours |

---

*This PRD is a living document. Jarvis updates it as priorities shift.*
*Next review: February 3, 2026*
