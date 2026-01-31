# LinkedIn Posting Workflow

**Schedule:** Every Tuesday, 9:00 AM Central  
**Posts Ready:** 12 (Q1 2026)

---

## Semi-Automated Workflow

Since LinkedIn doesn't have easy API posting, here's the workflow:

### Every Monday (Day Before)
1. Cron job reminds Jarvis to prepare next post
2. Jarvis reviews/polishes the scheduled post
3. Jarvis sends post to Mike via Telegram for approval
4. Mike replies "approved" or with edits

### Every Tuesday 9 AM
1. Cron reminds Mike: "Post ready - check Telegram"
2. Mike copies post to LinkedIn
3. Jarvis tracks: "LinkedIn post [week] published"

---

## Post Storage

All posts in: `artifacts/drafts/linkedin-content/posts/`
- `week-01-cmms-failures.md`
- `week-02-plc-diagnostics.md`
- etc.

---

## Alternative: Buffer Integration

If Mike sets up Buffer (free tier):
1. I can prepare posts in advance
2. Schedule via Buffer API
3. Auto-posts to LinkedIn

**Buffer setup:**
1. buffer.com → Create account
2. Connect LinkedIn profile
3. Give me API token
4. I schedule all 12 posts in one go

---

## Tracking

| Week | Post | Scheduled | Posted | Engagement |
|------|------|-----------|--------|------------|
| 1 | CMMS Failures | Feb 4 | ⏳ | — |
| 2 | PLC Diagnostics | Feb 11 | ⏳ | — |
| ... | ... | ... | ... | ... |
