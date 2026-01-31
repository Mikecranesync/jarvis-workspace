# Sales Automation Stack

**Priority Zero** — 24/7 automated lead → demo pipeline

## Stack Status

| Service | URL | Status |
|---------|-----|--------|
| n8n | http://72.60.175.144:5678 | ✅ Running |
| Mautic | http://72.60.175.144:8081 | ✅ Running |
| MariaDB | internal:3306 | ✅ Running |

## Credentials

### n8n
- **URL:** http://72.60.175.144:5678
- **User:** admin
- **Pass:** factorylm2026

### Mautic
- **URL:** http://72.60.175.144:8081
- **Setup Required:** Complete wizard on first visit

## Workflow Templates

### 1. Lead Import (`workflows/lead-import-workflow.json`)
- Polls Google Sheet every 15 minutes
- Creates Mautic contacts for new leads
- Sends Telegram notification

### 2. AI Personalization (`workflows/ai-personalization-workflow.json`)
- Webhook endpoint for generating personalized emails
- Uses Claude API
- Returns JSON with subject + body

## Docker Commands

```bash
# Start all services
cd /root/jarvis-workspace/infrastructure/sales-automation
docker-compose up -d

# View logs
docker-compose logs -f n8n
docker-compose logs -f mautic

# Restart
docker-compose restart

# Stop
docker-compose down
```

## Google Sheet Template

Create a sheet with these columns:
| first_name | last_name | email | company | title | industry | processed |
|------------|-----------|-------|---------|-------|----------|-----------|
| John | Smith | john@acme.com | Acme Mfg | Maintenance Manager | Manufacturing | |

## Mautic SMTP Setup (SendGrid)

1. Go to Mautic → Settings → Email Settings
2. **Mailer Transport:** Other SMTP Server
3. **Server:** smtp.sendgrid.net
4. **Port:** 587
5. **Encryption:** TLS
6. **Username:** apikey
7. **Password:** (SendGrid API key)
8. **From Email:** mike@cranesync.com

## Email Sequences

### Cold Outreach (3-touch)
- **Day 0:** Personalized intro email
- **Day 2:** Value add (blog post / case study)
- **Day 5:** Direct ask for demo

### Warm Nurture (weekly)
- Weekly value emails for 4 weeks
- Educational content, no hard sell

### Breakup (Day 14)
- Final email
- Create urgency
- Clear opt-out

---

*Created: 2026-01-30*
*Vision: https://trello.com/c/jelnmdnB*
