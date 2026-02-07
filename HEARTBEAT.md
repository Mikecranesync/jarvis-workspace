# HEARTBEAT.md

## 🚨 PRIORITY ZERO: YC APPLICATION
**Deadline: February 9, 2026 @ 8:00 PM PT (5 DAYS)**

Every heartbeat, check YC sprint progress FIRST:
1. Check `agents/accelerator-sprint/deliverables/` for new files
2. Check sub-agent sessions for completion
3. If blockers, ping Mike immediately
4. Log progress to `brain/accelerators/yc-sprint-log.md`

## Periodic Checks (rotate through these)

### Network Health (Every heartbeat)
- Run: `/root/jarvis-workspace/scripts/network-health-check.sh`
- **CHECK signals/alerts/*.txt for ANY undelivered alerts**
- If alerts found, SEND them to Mike via Telegram immediately (use message tool)
- Don't just log - actually DELIVER the alert

### System Health (2x daily)
- Check Docker containers: `docker ps --format '{{.Names}}: {{.Status}}'`
- Check disk space: `df -h /`
- Check memory: `free -h`

### YC Sprint Status (Every 2 hours)
- Check deliverables folder for completed drafts
- Spawn sub-agents on TODO items
- Send progress update to Mike
