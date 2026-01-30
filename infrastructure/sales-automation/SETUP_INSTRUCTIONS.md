# 🚀 Sales Automation Setup - Mike's Physical Actions

**Total time needed: 5-10 minutes**

---

## Step 1: Access n8n (30 seconds)

1. Open: **http://72.60.175.144:5678**
2. Login:
   - Email: `admin@factorylm.com`
   - Password: `factorylm2026`
3. If asked to create account, use those credentials

---

## Step 2: Add Credentials (3 minutes)

Go to **Settings → Credentials** and add:

### A) SendGrid SMTP
- Name: `SendGrid SMTP`
- User: `apikey`
- Password: `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`
- Host: `smtp.sendgrid.net`
- Port: `587`
- SSL/TLS: `true`

### B) Anthropic API
- Name: `Anthropic API`
- API Key: *(get from your Anthropic dashboard)*

### C) Telegram Bot (Optional - for notifications)
- Name: `Telegram Bot`
- Access Token: *(from BotFather, or I can create one)*

---

## Step 3: Import Workflow (1 minute)

1. Go to **Workflows → Import from File**
2. Upload: `/root/jarvis-workspace/infrastructure/sales-automation/workflows/complete-outreach-workflow.json`
3. Or copy-paste the JSON from that file

---

## Step 4: Activate Workflow (30 seconds)

1. Open the imported workflow
2. Click the toggle to **Activate** it
3. Copy the webhook URL (will look like `http://72.60.175.144:5678/webhook/new-lead`)

---

## Step 5: Test It (1 minute)

Run this command to send a test lead:
```bash
curl -X POST http://72.60.175.144:5678/webhook/new-lead \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Test",
    "last_name": "Lead",
    "email": "mike@cranesync.com",
    "company": "Test Company",
    "title": "Maintenance Manager",
    "industry": "Manufacturing"
  }'
```

**Expected result:**
- Claude generates personalized email
- Email sends to mike@cranesync.com (so you can see it)
- You get a Telegram notification

---

## What Happens After Setup

The system runs 24/7:
1. New leads hit the webhook
2. Claude writes personalized emails
3. SendGrid delivers them
4. You get Telegram alerts
5. Replies come to your inbox

---

## Optional: Mautic Setup (Advanced)

If you want email sequences and lead scoring, complete Mautic at:
**http://72.60.175.144:8081**

Setup wizard takes ~2 minutes:
- Database password: `mautic2026`
- Admin: your email + password

---

**Questions?** Just ask me. I'm here 24/7 too.
