# HEARTBEAT.md

## Periodic Checks (rotate through these)

### Network Health (Every heartbeat)
- Run: `/root/jarvis-workspace/scripts/network-health-check.sh`
- If alerts in `signals/alerts/network-down.txt`, notify Mike

### System Health (2x daily)
- Check Docker containers: `docker ps --format '{{.Names}}: {{.Status}}'`
- Check disk space: `df -h /`
- Check memory: `free -h`
