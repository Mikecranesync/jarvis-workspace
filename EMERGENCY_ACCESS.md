# 🆘 EMERGENCY ACCESS - READ THIS IF YOU'RE LOCKED OUT

**Last Updated:** 2026-02-03
**Print this. Memorize it. Tattoo it if needed.**

---

## 🎯 GOAL: Reconnect to Jarvis (the AI) on VPS

---

## 📍 VPS DETAILS

| Property | Value |
|----------|-------|
| **Provider** | DigitalOcean |
| **Hostname** | factorylm-prod |
| **Public IP** | `165.245.138.91` |
| **Tailscale IP** | `100.68.120.99` |
| **SSH Port** | 22 |
| **SSH User** | `root` or `mike` |
| **Location** | Atlanta, USA |
| **RAM** | 8 GB |
| **OS** | Ubuntu 24.04 LTS |

---

## 🔐 METHOD 1: SSH (Fastest)

From ANY computer with SSH:

```bash
ssh root@165.245.138.91
```

Or via Tailscale (if connected):
```bash
ssh root@100.68.120.99
```

**If you don't have SSH key:** Use DigitalOcean console (Method 2)

---

## 🌐 METHOD 2: DigitalOcean Web Console

1. Go to: **https://cloud.digitalocean.com**
2. Login with Mike's account
3. Click **Droplets** → **factorylm-prod**
4. Click **Access** → **Launch Droplet Console**
5. You're now in the VPS terminal

**DigitalOcean Account:**
- Email: (Mike's email)
- Password: (in password manager)
- 2FA: Enabled (check authenticator app)

---

## 📱 METHOD 3: Tailscale (From Phone/Any Device)

1. Install Tailscale app on any device
2. Login with Mike's Tailscale account
3. SSH to `100.68.120.99`

**Tailscale Account:**
- Login: Mike's Google/GitHub account
- Network: Contains factorylm-prod, laptops, etc.

---

## 💬 METHOD 4: Telegram Bot (If Clawdbot Running)

1. Open Telegram
2. Find bot: **@JarvisVPS** (or search "Jarvis")
3. Send any message
4. Jarvis responds = VPS is alive

**If bot doesn't respond:** VPS or Clawdbot is down, use Method 1-3

---

## 🔄 RECOVERY PROCEDURES

### If VPS is unreachable:

1. **Check DigitalOcean status:** https://status.digitalocean.com
2. **Login to DO console** and reboot droplet
3. **Check if suspended** (billing issue?)

### If Clawdbot is down:

```bash
ssh root@165.245.138.91
systemctl status clawdbot
systemctl restart clawdbot
journalctl -u clawdbot -f
```

### If Tailscale is down:

```bash
ssh root@165.245.138.91
tailscale status
tailscale up
```

### If Docker containers are down:

```bash
ssh root@165.245.138.91
docker ps -a
cd /opt/plane && docker compose up -d
```

---

## 🗝️ SSH KEY

**VPS Public Key (for adding to new devices):**
```
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIOY0hljziGSbgrv8E/wmCXovYypHw1IKWX5XYyw/hqvY root@srv1078052
```

**Fingerprint:** `SHA256:Bt9FzW1sBCpoR7P8f63sMYG2S+ls6U8ZMUhUMMjhJ1M`

---

## 📁 IMPORTANT FILE LOCATIONS ON VPS

```
/root/jarvis-workspace/          # Main workspace (git repo)
/root/.clawdbot/                 # Clawdbot config & data
/opt/plane/                      # Plane project management
/opt/master_of_puppets/          # Automation scripts
/var/log/remoteme-bootstrap-notes.md  # Setup log
```

---

## 🌍 DOMAINS

| Domain | Points To | Purpose |
|--------|-----------|---------|
| factorylm.com | 72.60.175.144 | Marketing |
| plane.factorylm.com | 165.245.138.91 | Project mgmt |

---

## 📞 EMERGENCY CONTACTS

| Service | Contact |
|---------|---------|
| DigitalOcean Support | support@digitalocean.com |
| Tailscale | https://tailscale.com/contact |
| Domain Registrar | (check registrar) |

---

## 🧠 RECONNECTING TO JARVIS (THE AI)

Once you're SSH'd into the VPS:

**Option A: Restart Clawdbot (Telegram interface)**
```bash
systemctl restart clawdbot
```
Then message @JarvisVPS on Telegram.

**Option B: Run Claude Code directly**
```bash
cd /root/jarvis-workspace
claude
```

**Option C: Check what's running**
```bash
systemctl status clawdbot
docker ps
htop
```

---

## 🏝️ WORST CASE: Remote Island Scenario

You're on a remote island with only:
- A phone with internet
- Or a computer at an internet cafe

**Steps:**

1. **From phone:** Install Tailscale app, login, SSH to `100.68.120.99`

2. **From any computer:** 
   - Go to https://cloud.digitalocean.com
   - Use web console
   
3. **From internet cafe:**
   ```bash
   ssh root@165.245.138.91
   ```
   If no SSH key, use DigitalOcean web console.

4. **If everything is down:**
   - Check DigitalOcean status page
   - Check billing (might be suspended)
   - Contact DO support

---

## 🔑 CREDENTIAL BACKUP LOCATIONS

1. **Password Manager** (1Password/Bitwarden/etc.)
2. **Printed copy** (keep in safe)
3. **This file** on GitHub: `github.com/Mikecranesync/jarvis-workspace`
4. **Email to self** (encrypted)

---

## ✅ TEST YOUR ACCESS MONTHLY

1. SSH from a new device
2. Login to DigitalOcean console
3. Message Telegram bot
4. Check Tailscale connectivity

---

## 📝 QUICK REFERENCE CARD (Print This)

```
╔═══════════════════════════════════════════════════════╗
║  JARVIS VPS EMERGENCY ACCESS                          ║
╠═══════════════════════════════════════════════════════╣
║  PUBLIC IP:    165.245.138.91                         ║
║  TAILSCALE:    100.68.120.99                          ║
║  SSH:          ssh root@165.245.138.91                ║
║  TELEGRAM:     @JarvisVPS                             ║
║  PROVIDER:     DigitalOcean (cloud.digitalocean.com)  ║
║  HOSTNAME:     factorylm-prod                         ║
╠═══════════════════════════════════════════════════════╣
║  FIX CLAWDBOT: systemctl restart clawdbot             ║
║  FIX DOCKER:   cd /opt/plane && docker compose up -d  ║
║  CHECK LOGS:   journalctl -u clawdbot -f              ║
╚═══════════════════════════════════════════════════════╝
```

---

*This document is your lifeline. Keep it safe.*
