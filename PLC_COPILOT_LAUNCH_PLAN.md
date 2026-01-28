# PLC-Copilot Launch Plan
## From Zero to First Paying Customer in 14 Days

**Prepared by:** Jarvis AI  
**Date:** January 26, 2026  
**For:** Mike Harper, CraneSync Inc.

---

## Executive Summary

**Goal:** Launch plc-copilot.app and acquire 3 paying customers ($87 MRR)  
**Timeline:** 14 days  
**Investment Required:** ~$50 (VPS hosting) + time  
**Assets Available:** Rivet-PRO codebase (90% complete)

---

## Phase 1: Infrastructure (Days 1-3)

### Day 1: Server Setup

**Morning (2 hours)**
- [ ] Purchase VPS from DigitalOcean or Hetzner
  - Recommended: $12/mo (2GB RAM, 2 vCPU)
  - Location: NYC or nearest to target users
- [ ] Point plc-copilot.app domain to VPS IP
  - A record: @ → VPS IP
  - A record: www → VPS IP

**Afternoon (3 hours)**
- [ ] SSH into VPS, install dependencies
  - Python 3.11+
  - PostgreSQL or SQLite (start simple)
  - Redis (for rate limiting, optional)
  - Nginx (reverse proxy)
- [ ] Clone Rivet-PRO repository to server
- [ ] Set up environment variables
  - Telegram bot token
  - API keys (Groq, DeepSeek, Claude, Gemini)
  - SendGrid for transactional email

**Evening (1 hour)**
- [ ] Test bot responds to /start command
- [ ] Document any issues encountered

---

### Day 2: Bot Deployment

**Morning (3 hours)**
- [ ] Configure systemd service for bot
  - Auto-restart on crash
  - Start on boot
- [ ] Set up SSL certificate (Let's Encrypt)
- [ ] Configure webhook (faster than polling)
  - URL: https://plc-copilot.app/webhook
  - Telegram setBotWebhook API call

**Afternoon (2 hours)**
- [ ] Test photo upload pipeline end-to-end
  - Send photo of equipment nameplate
  - Verify OCR extracts text
  - Verify equipment matching works
- [ ] Test manual/KB lookup
  - Ask a troubleshooting question
  - Verify relevant response

**Evening (1 hour)**
- [ ] Set up basic logging
  - Track: user IDs, message counts, errors
- [ ] Create simple admin dashboard (or use Telegram logs)

---

### Day 3: Landing Page & Payment

**Morning (2 hours)**
- [ ] Deploy simple landing page to plc-copilot.app
  - Hero: "AI Troubleshooting for Industrial Techs"
  - Features: Photo diagnosis, Manual search, 24/7 availability
  - CTA: "Try Free on Telegram" → bot link
  - Pricing section (see below)

**Afternoon (3 hours)**
- [ ] Set up Stripe account (if not already)
- [ ] Create products in Stripe
  - Free: $0 (10 lookups/month)
  - Pro: $29/month (unlimited lookups)
  - Team: $99/month (5 users, shared KB)
- [ ] Integrate Stripe with bot OR
- [ ] Use Stripe Payment Links (simpler)
  - Generate link for Pro subscription
  - Bot sends link when user hits free limit

**Evening (1 hour)**
- [ ] Test payment flow end-to-end
  - Hit free limit → see upgrade prompt
  - Click link → Stripe checkout
  - Complete payment → bot unlocks Pro

---

## Phase 2: Seed Users (Days 4-7)

### Day 4: Reddit Reconnaissance

**Morning (2 hours)**
- [ ] Create list of target subreddits
  - r/PLC (78K members) - PRIMARY
  - r/IndustrialMaintenance
  - r/HVAC (for controls techs)
  - r/electricians (industrial subset)
  - r/AskEngineers
- [ ] Read top 20 posts in r/PLC from past month
- [ ] Identify common pain points
  - Fault code interpretation
  - Wiring diagram questions
  - "What does this error mean?"
  - Communication setup (Ethernet/IP, Modbus)

**Afternoon (2 hours)**
- [ ] Find 5 unanswered questions you can help with
- [ ] Draft helpful responses (NO selling yet)
  - Pure value, show expertise
  - Include screenshots/diagrams if relevant
- [ ] Post responses from your personal Reddit account

**Evening (1 hour)**
- [ ] Engage with any replies
- [ ] Note which topics get most engagement

---

### Day 5: Value Bombing

**Morning (2 hours)**
- [ ] Find 5 more questions to answer
- [ ] Create one "resource post"
  - Example: "Common Allen-Bradley Fault Codes Cheat Sheet"
  - Or: "How to Troubleshoot Modbus Communication Issues"
  - Pure value, builds authority

**Afternoon (2 hours)**
- [ ] Post the resource in r/PLC
- [ ] Cross-post to r/IndustrialMaintenance if relevant
- [ ] Continue answering questions

**Evening (1 hour)**
- [ ] Check bot for any organic signups
- [ ] Respond to any DMs asking about your expertise

---

### Day 6: Soft Launch Announcement

**Morning (2 hours)**
- [ ] Draft "Show r/PLC" post
  - Title: "I built a free AI assistant for troubleshooting industrial equipment"
  - Body: Problem you're solving, how it works, link to try
  - Offer: "Free for the first 50 users, looking for feedback"
  - Tone: Humble, seeking feedback, not salesy

**Afternoon (1 hour)**
- [ ] Post to r/PLC
- [ ] Monitor comments and respond to ALL of them
- [ ] Be prepared for skepticism (AI replacing jobs concerns)
  - Response: "It's a tool for techs, not a replacement"

**Evening (2 hours)**
- [ ] Handle influx of new users
- [ ] Note any bugs or UX issues
- [ ] Collect feedback (what do they like/hate?)

---

### Day 7: Facebook Groups

**Morning (2 hours)**
- [ ] Join industrial maintenance Facebook groups
  - "PLC Programming"
  - "Industrial Maintenance Technicians"
  - "Allen-Bradley PLC Users"
  - "Siemens PLC Programming"
- [ ] Observe group culture (some hate self-promotion)

**Afternoon (2 hours)**
- [ ] Answer questions in groups (no promotion)
- [ ] Build rapport with admins if possible

**Evening (1 hour)**
- [ ] Review first week metrics
  - Total users
  - Messages per user
  - Photo uploads
  - Any upgrade attempts?

---

## Phase 3: Conversion (Days 8-14)

### Day 8: User Feedback Sprint

**Morning (2 hours)**
- [ ] Message top 10 most active users
  - "Hey, thanks for trying PLC-Copilot! Quick question - what's working well and what's frustrating?"
- [ ] Compile feedback into themes

**Afternoon (3 hours)**
- [ ] Fix top 3 pain points (quick wins only)
- [ ] Improve response quality for common questions
- [ ] Add any missing equipment to KB

**Evening (1 hour)**
- [ ] Send update to users: "Based on your feedback, we fixed X, Y, Z"

---

### Day 9: Content Creation

**Morning (3 hours)**
- [ ] Record 60-second demo video
  - Show: Photo upload → instant diagnosis
  - Keep it simple, no fancy editing
  - Post to LinkedIn (your profile)

**Afternoon (2 hours)**
- [ ] Write case study from real user interaction
  - "How PLC-Copilot helped diagnose a VFD fault in 30 seconds"
  - Post to blog or LinkedIn article

**Evening (1 hour)**
- [ ] Share content in relevant communities
- [ ] Engage with comments

---

### Day 10: Upgrade Push

**Morning (2 hours)**
- [ ] Identify users approaching free limit
- [ ] Craft personalized upgrade message
  - "Hey [name], noticed you've been using PLC-Copilot a lot! You're at 8/10 free lookups this month. Want to upgrade to unlimited for $29/mo?"

**Afternoon (2 hours)**
- [ ] Send upgrade messages to qualifying users
- [ ] Offer: "Reply in next 24 hours for 50% off first month" ($14.50)

**Evening (1 hour)**
- [ ] Process any upgrades
- [ ] Thank new paying customers personally

---

### Day 11-12: Double Down on What Works

**Morning (2 hours each day)**
- [ ] Analyze which channels drove most signups
- [ ] Double down on that channel
- [ ] If Reddit worked: Post more, answer more
- [ ] If Facebook worked: Engage more in groups

**Afternoon (2 hours each day)**
- [ ] Continue user outreach
- [ ] Fix any reported bugs
- [ ] Improve KB based on queries

**Evening (1 hour each day)**
- [ ] Update metrics dashboard
- [ ] Plan next day's activities

---

### Day 13: Referral Program

**Morning (2 hours)**
- [ ] Create simple referral incentive
  - "Refer a friend, both get 1 month free"
  - Or: "Refer 3 friends, get Pro free for life"
- [ ] Message existing users about referral program

**Afternoon (2 hours)**
- [ ] Create shareable link/code for each user
- [ ] Track referrals in simple spreadsheet

**Evening (1 hour)**
- [ ] Follow up with users who said they'd refer

---

### Day 14: Review & Plan Next Sprint

**Morning (2 hours)**
- [ ] Compile all metrics
  - Total users: ___
  - Active users (used 3+ times): ___
  - Paying customers: ___
  - MRR: $___
  - Conversion rate: ___%

**Afternoon (2 hours)**
- [ ] Write retrospective
  - What worked?
  - What didn't?
  - What surprised you?
- [ ] Plan next 14-day sprint

**Evening (1 hour)**
- [ ] Celebrate wins (even small ones!)
- [ ] Rest before next sprint

---

## Success Metrics

| Metric | Target | Stretch Goal |
|--------|--------|--------------|
| Total Users | 50 | 100 |
| Active Users | 20 | 40 |
| Paying Customers | 3 | 5 |
| MRR | $87 | $145 |
| Reddit Karma Gained | 100 | 500 |

---

## Risk Mitigation

| Risk | Likelihood | Mitigation |
|------|------------|------------|
| Bot crashes under load | Medium | Start with polling, move to webhook |
| Reddit post gets removed | Medium | Follow rules, don't be salesy |
| No one converts to paid | Medium | Lower price or extend free tier |
| Negative feedback | Low | Address quickly, iterate fast |
| API costs exceed budget | Low | Start with Groq (cheap), rate limit |

---

## Budget

| Item | Cost | Notes |
|------|------|-------|
| VPS (DigitalOcean) | $12/mo | Can start with $6 droplet |
| Domain (already owned) | $0 | plc-copilot.app |
| Stripe fees | 2.9% + $0.30 | Per transaction |
| API costs (estimate) | $20/mo | Groq is cheap, Claude for complex |
| **Total** | **~$35/mo** | Covered by 2 customers |

---

## Key Resources

**Codebase:** Rivet-PRO (Agent-Factory repo)  
**Landing page:** Use factorylm-landing as template  
**Docs:** Agent-Factory/docs/ has extensive documentation  

---

## What Jarvis Will Do

While you execute, I can:
1. Monitor bot logs and alert you to issues
2. Help draft Reddit posts and responses
3. Analyze user queries to improve KB
4. Track metrics and report weekly
5. Handle customer support messages

---

## Next Action

**Tomorrow morning:** Purchase VPS and start Day 1.

Or, if you want to validate demand first before spending money:
- Post in r/PLC today: "Would you use an AI troubleshooting assistant?"
- Gauge response before building

---

*"The best time to launch was yesterday. The second best time is today."*

---

**Document Version:** 1.0  
**Last Updated:** January 26, 2026  
**Questions?** Message Jarvis on Telegram or email jarvis@cranesync.com
