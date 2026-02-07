# 🔥 FIRE DRILL - Emergency Recovery Procedures

**Last tested:** 2026-02-07 (VPS self-destruction incident)  
**Result:** Mike manually revived using Claude CLI from laptop ✅

---

## Architecture Overview

Three independent Jarvis instances for redundancy:

| Instance | Location | Telegram Bot | Status |
|----------|----------|--------------|--------|
| **Main Jarvis** | DigitalOcean VPS | @JarvisMainBot | Primary |
| **Travel Jarvis** | Travel Laptop | @TravelLaptop_bot | Backup |
| **PLC Jarvis** | PLC Laptop | @PLCLaptop_bot | Backup |

**Full Clawdbot on each machine** - not just bridges. Each can:
- Control its own machine (exec, files, browser)
- Receive direct messages from Mike
- Receive delegated tasks from other Jarvis instances

**Rule:** If one dies, the others still work. Mike can always reach Claude.

---

## 🚨 Scenario 1: VPS Down

**Symptoms:** Main Telegram bot not responding, VPS unreachable

**Recovery Steps:**

### Option A: Use Laptop Claude (Immediate)
```bash
# On either laptop, open terminal/PowerShell:
claude

# You're now in Claude CLI - ask it anything
```

### Option B: Restart VPS
1. Login to DigitalOcean: https://cloud.digitalocean.com
2. Find `factorylm-prod` droplet
3. Click "Power" → "Power Cycle"
4. Wait 2-3 minutes
5. SSH verify: `ssh root@100.68.120.99`

### Option C: Restart Clawdbot Service
```bash
# SSH to VPS
ssh root@100.68.120.99

# Check status
clawdbot gateway status

# Restart
clawdbot gateway restart

# Check logs
journalctl -u clawdbot -n 50 --no-pager
```

---

## 🚨 Scenario 2: Laptop Offline

**Symptoms:** Laptop bot not responding, Tailscale shows offline

**Recovery:** 
- Physical access required
- Check: Is laptop powered on? Is Tailscale running?
- Restart Tailscale: `tailscale up`

---

## 🚨 Scenario 3: Telegram Bot Token Revoked

**Symptoms:** Bot returns errors, Telegram says "bot not found"

**Recovery:**
1. Create new bot via @BotFather
2. Get new token
3. Update config:
   ```bash
   # VPS
   nano /opt/clawdbot/config.yaml
   # Update telegram.token
   clawdbot gateway restart
   ```

---

## 🚨 Scenario 4: Claude API Down

**Symptoms:** All bots respond but Claude returns errors

**Recovery:**
- Check status: https://status.anthropic.com
- Switch to local LLM on PLC laptop:
  ```bash
  ollama run llama3.2
  ```

---

## 🚨 Scenario 5: Self-Inflicted Damage (What Happened Today)

**Symptoms:** Jarvis tried to upgrade itself and broke

**Prevention:**
1. ❌ Never auto-upgrade without human approval
2. ❌ Never run `gateway update.run` or `config.apply` unprompted
3. ✅ Always ask before system changes

**Recovery:**
1. SSH to VPS
2. Check what's broken: `clawdbot gateway status`
3. Rollback if needed: `cd /opt/clawdbot && git checkout HEAD~1`
4. Restart: `clawdbot gateway restart`

---

## 📋 Regular Fire Drills (Monthly)

### Drill 1: VPS Failover
- [ ] Message laptop bot
- [ ] Confirm it responds
- [ ] Run a simple command

### Drill 2: Recovery from Backup
- [ ] Stop main VPS bot
- [ ] Use laptop bot to diagnose
- [ ] Restart main bot

### Drill 3: Cold Start
- [ ] Power cycle VPS
- [ ] Verify auto-start of all services
- [ ] Check Docker containers

---

## 🔐 Critical Credentials Location

| What | Where |
|------|-------|
| VPS SSH | `ssh root@100.68.120.99` |
| Hetzner SSH | `ssh -i ~/.ssh/hetzner_key root@178.156.173.186` |
| Telegram Bot Tokens | `/opt/clawdbot/config.yaml` |
| Claude API Key | `~/.anthropic/api_key` or env |
| DigitalOcean Dashboard | https://cloud.digitalocean.com |

---

## 🛠️ Quick Commands

```bash
# Check if Jarvis is alive
clawdbot gateway status

# Restart Jarvis
clawdbot gateway restart

# View logs
journalctl -u clawdbot -f

# Check all Docker services
docker ps

# Check disk space
df -h

# Check Tailscale connectivity
tailscale status
```

---

*Updated after every fire drill or real incident.*
