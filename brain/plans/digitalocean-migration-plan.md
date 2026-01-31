# DigitalOcean Migration Plan

*Created: 2026-01-30*
*Following: Constitution + Engineering Commandments*
*Status: READY TO EXECUTE*

---

## Mission

Migrate Jarvis infrastructure from Hostinger VPS to DigitalOcean Droplet with zero downtime and full data preservation.

---

## Current State (Hostinger)

```
Server:     srv1078052.hstgr.cloud
IP:         [current Hostinger IP]
OS:         Ubuntu (Linux 6.8.0-87-generic)
CPU:        1 vCPU (AMD EPYC 9354P)
RAM:        3.8 GB (66% used)
Disk:       48 GB (88% used — CRITICAL)
Tailscale:  100.102.30.102 (srv1078052)
```

### Services Running
- Clawdbot (Jarvis AI assistant)
- Docker (CMMS containers)
- Tailscale VPN
- Various cron jobs

### Data to Migrate (~42 GB)
```
/root/jarvis-workspace/     # Main workspace (~1 GB)
/root/.config/              # Configs, API keys
/var/lib/docker/            # Docker volumes
/opt/                       # Service installations
/etc/systemd/system/        # Custom services
Cron jobs                   # All scheduled tasks
SSH keys                    # Authentication
Tailscale auth              # VPN membership
```

---

## Target State (DigitalOcean)

```
Provider:   DigitalOcean
Region:     NYC1 or SFO3 (Mike's choice)
OS:         Ubuntu 22.04 LTS
CPU:        [Mike chooses — recommend 4+ vCPU]
RAM:        [Mike chooses — recommend 8+ GB]
Disk:       [Mike chooses — recommend 160+ GB]
```

---

## Phase 1: Pre-Migration (Before Droplet Ready)

### 1.1 Inventory Current System
```bash
# Document all running services
systemctl list-units --type=service --state=running

# Document all cron jobs
crontab -l
cat /etc/cron.d/*

# Document Docker containers
docker ps -a
docker images

# Document installed packages
dpkg --get-selections > /tmp/packages.txt

# Document Tailscale config
tailscale status
```

### 1.2 Create Backup Archive
```bash
# Full backup of critical data
tar -czvf /tmp/jarvis-backup-$(date +%Y%m%d).tar.gz \
  /root/jarvis-workspace \
  /root/.config \
  /root/.ssh \
  /etc/systemd/system/clawdbot.service \
  /etc/systemd/system/second-brain.service \
  /etc/systemd/system/plc-copilot.service
```

### 1.3 Document Environment Variables
```bash
# Capture all env vars
env > /tmp/env-backup.txt

# Capture Clawdbot config (redact secrets)
cat /root/.config/clawdbot/clawdbot.json | head -50
```

---

## Phase 2: Droplet Setup (Mike Does This)

### 2.1 Create Droplet
1. Go to digitalocean.com
2. Create → Droplets
3. Choose:
   - **Region:** NYC1 (or SFO3)
   - **Image:** Ubuntu 22.04 (LTS) x64
   - **Size:** Basic → Regular → $24/mo (4 GB) or $48/mo (8 GB)
   - **Auth:** SSH key (add new or use existing)
   - **Hostname:** `jarvis-do` or `factorylm-prod`
4. Create Droplet
5. **Send Jarvis the IP address**

### 2.2 Enable Backups (Recommended)
- DigitalOcean Backups: +20% of Droplet cost
- Weekly automated snapshots
- One-click restore

### 2.3 Enable Monitoring
- Free built-in monitoring
- CPU, memory, disk, bandwidth graphs

---

## Phase 3: Initial Server Setup (Jarvis Executes)

### 3.1 First Connection
```bash
# SSH to new Droplet
ssh root@[NEW_IP]

# Update system
apt update && apt upgrade -y

# Install essentials
apt install -y curl wget git htop tmux unzip jq
```

### 3.2 Install Node.js 22
```bash
curl -fsSL https://deb.nodesource.com/setup_22.x | bash -
apt install -y nodejs
node --version  # Should show v22.x
```

### 3.3 Install Docker
```bash
curl -fsSL https://get.docker.com | sh
systemctl enable docker
docker --version
```

### 3.4 Install Tailscale
```bash
curl -fsSL https://tailscale.com/install.sh | sh
tailscale up --authkey=[AUTH_KEY]
tailscale status
```

### 3.5 Install Clawdbot
```bash
npm install -g clawdbot
clawdbot --version
```

---

## Phase 4: Data Migration (Jarvis Executes)

### 4.1 Transfer Workspace
```bash
# From OLD server to NEW server
rsync -avz --progress \
  /root/jarvis-workspace/ \
  root@[NEW_IP]:/root/jarvis-workspace/
```

### 4.2 Transfer Configs
```bash
rsync -avz --progress \
  /root/.config/ \
  root@[NEW_IP]:/root/.config/

rsync -avz --progress \
  /root/.ssh/ \
  root@[NEW_IP]:/root/.ssh/
```

### 4.3 Transfer Docker Volumes
```bash
# Export Docker volumes
docker run --rm -v [volume_name]:/data -v /tmp:/backup \
  alpine tar czf /backup/[volume_name].tar.gz /data

# Transfer to new server
scp /tmp/*.tar.gz root@[NEW_IP]:/tmp/

# Import on new server
docker run --rm -v [volume_name]:/data -v /tmp:/backup \
  alpine tar xzf /backup/[volume_name].tar.gz -C /
```

### 4.4 Transfer Systemd Services
```bash
rsync -avz \
  /etc/systemd/system/clawdbot.service \
  /etc/systemd/system/second-brain.service \
  /etc/systemd/system/plc-copilot.service \
  root@[NEW_IP]:/etc/systemd/system/
```

### 4.5 Transfer Cron Jobs
```bash
crontab -l > /tmp/crontab-backup.txt
scp /tmp/crontab-backup.txt root@[NEW_IP]:/tmp/
# On new server: crontab /tmp/crontab-backup.txt
```

---

## Phase 5: Service Activation (Jarvis Executes)

### 5.1 Start Clawdbot
```bash
# Reload systemd
systemctl daemon-reload

# Enable and start Clawdbot
systemctl enable clawdbot
systemctl start clawdbot
systemctl status clawdbot
```

### 5.2 Start Docker Services
```bash
# Start CMMS if applicable
docker-compose -f /path/to/docker-compose.yml up -d
```

### 5.3 Restore Cron Jobs
```bash
crontab /tmp/crontab-backup.txt
crontab -l  # Verify
```

### 5.4 Verify Tailscale
```bash
tailscale status
# Should show new hostname in network
```

---

## Phase 6: Verification (Jarvis Executes)

### 6.1 Service Health Checks
```bash
# Check all services
systemctl status clawdbot
systemctl status docker

# Check Clawdbot responds
clawdbot status

# Check API endpoints
curl http://localhost:3001  # Second brain portal
```

### 6.2 Data Integrity Checks
```bash
# Verify workspace
ls -la /root/jarvis-workspace/
cat /root/jarvis-workspace/SOUL.md  # Should exist

# Verify configs
ls -la /root/.config/clawdbot/
```

### 6.3 Connectivity Checks
```bash
# Tailscale connectivity
tailscale ping 100.83.251.23  # Mike's laptop

# External connectivity
curl -I https://api.telegram.org
curl -I https://api.anthropic.com
```

---

## Phase 7: Cutover (Coordinated)

### 7.1 Final Sync
```bash
# One last rsync to catch recent changes
rsync -avz --progress --delete \
  /root/jarvis-workspace/ \
  root@[NEW_IP]:/root/jarvis-workspace/
```

### 7.2 Stop Old Server Services
```bash
# On OLD Hostinger server
systemctl stop clawdbot
```

### 7.3 Verify New Server Active
```bash
# On NEW DigitalOcean server
systemctl status clawdbot  # Should be running
```

### 7.4 Update DNS (If Applicable)
- Update any A records pointing to old IP
- TTL should be lowered to 300 before cutover

### 7.5 Update Tailscale References
- Note new Tailscale hostname
- Update any scripts referencing old hostname

---

## Phase 8: Post-Migration (Week 1)

### 8.1 Monitor New Server
- Watch CPU, RAM, disk usage
- Check Clawdbot logs for errors
- Verify all cron jobs fire correctly

### 8.2 Keep Old Server Running (7 days)
- Rollback insurance
- Don't cancel Hostinger yet

### 8.3 Final Verification
- [ ] Telegram messages work
- [ ] All cron jobs execute
- [ ] Docker containers healthy
- [ ] Tailscale accessible
- [ ] Disk usage reasonable
- [ ] No errors in logs

---

## Phase 9: Decommission Hostinger

### 9.1 Confirm Migration Success
- 7 days of stable operation
- No rollback needed

### 9.2 Final Backup from Old Server
```bash
# One last backup for archive
tar -czvf hostinger-final-backup.tar.gz /root/
```

### 9.3 Cancel Hostinger
- Log into Hostinger (if possible!)
- Cancel VPS subscription
- Download any invoices for records

---

## Rollback Plan

If migration fails:

1. **Stop new server Clawdbot**
   ```bash
   systemctl stop clawdbot  # On DigitalOcean
   ```

2. **Restart old server Clawdbot**
   ```bash
   systemctl start clawdbot  # On Hostinger
   ```

3. **Investigate and retry**
   - Check logs on both servers
   - Identify what failed
   - Fix and retry migration

---

## Timeline

| Phase | Duration | Who |
|-------|----------|-----|
| Phase 1: Pre-Migration | 30 min | Jarvis |
| Phase 2: Droplet Setup | 10 min | Mike |
| Phase 3: Server Setup | 30 min | Jarvis |
| Phase 4: Data Migration | 1-2 hours | Jarvis |
| Phase 5: Service Activation | 30 min | Jarvis |
| Phase 6: Verification | 30 min | Jarvis |
| Phase 7: Cutover | 15 min | Both |
| Phase 8: Monitoring | 7 days | Jarvis |
| Phase 9: Decommission | 10 min | Mike |

**Total Active Time:** ~4-5 hours
**Total Calendar Time:** ~8 days (including monitoring period)

---

## Success Criteria

- [ ] All services running on DigitalOcean
- [ ] Telegram bot responsive
- [ ] Tailscale connected
- [ ] Disk usage < 50%
- [ ] No data loss
- [ ] Zero downtime during cutover

---

*Following Constitution: Ship products, generate revenue.*
*Following Commandments: Document everything, don't delete until verified.*
