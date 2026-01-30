# TOOLS.md - Local Notes

Skills define *how* tools work. This file is for *your* specifics — the stuff that's unique to your setup.

---

## Tailscale Network

| Device | Tailscale IP | Name | Status |
|--------|--------------|------|--------|
| VPS (Jarvis) | 100.102.30.102 | srv1078052 | Always online |
| Mike's Laptop | 100.83.251.23 | miguelomaniac | Check before connecting |
| BeagleBone | TBD | TBD | Pending setup |

**To connect to Mike's laptop:**
```bash
ssh mike@100.83.251.23
```

---

## BeagleBone (Edge Adapter)

| Property | Value |
|----------|-------|
| USB IP | 192.168.7.2 |
| MAC | 64-70-60-ae-f2-07 |
| WireGuard IP | 10.100.0.10 (pending) |
| Status | Needs password reset (flash SD) |

---

## Email Accounts

| Account | Purpose | Status |
|---------|---------|--------|
| jarvis@cranesync.com | Sending (SMTP) | ⚠️ Needs re-auth |
| hharperson2000@yahoo.com | Mike's personal | ✅ App password set |
| mike@cranesync.com | Mike's business | ✅ MailerLite verified |

---

## APIs

| Service | Key Location | Notes |
|---------|--------------|-------|
| MailerLite | /root/.config/jarvis/mailerlite.env | Email marketing |
| Perplexity | /root/.config/jarvis/perplexity.env | Research/search |
| Trello | clawdbot.json env | Board automation |
| SendGrid | clawdbot.json env | Backup email send |
| Calendly | /root/.config/jarvis/calendly.env | Demo scheduling (mike@cranesync.com) |

---

## Cron Jobs Active

- Monitor Agent (15 min)
- Code Agent (30 min)
- Trello Check (5 min)
- Email Strategist (Monday 9am)
- Email Manager (Friday 5pm)
- LinkedIn Prep (Monday 9am)
- Laptop Online Check (5 min)

---

Add whatever helps you do your job. This is your cheat sheet.
