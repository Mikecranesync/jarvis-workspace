# HEARTBEAT.md

## Periodic Checks (rotate through these)

### Network Health (Every heartbeat)
- Run: `/root/jarvis-workspace/scripts/network-health-check.sh`
- If alerts in `signals/alerts/network-down.txt`, notify Mike

### Laptop Status (Every heartbeat)
- Run: `tailscale status | grep miguelomaniac`
- Track state in `signals/alerts/network-down.txt`
- Only alert on state CHANGE (offline → online)

### System Health (2x daily)
- Check Docker containers: `docker ps --format '{{.Names}}: {{.Status}}'`
- Check disk space: `df -h /`
- Check memory: `free -h`

### Trello Check (2x daily, morning/afternoon)
- Check for @jarvis tasks on Command Center board
- Only do quick tasks; flag large ones for Mike

## NOT in heartbeat (separate crons)
- Heavy research (isolated sessions)
- Status reports (30min cron)
- Telegram ingestion (15min cron)
