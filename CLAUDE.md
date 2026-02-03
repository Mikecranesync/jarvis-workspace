# CLAUDE.md - Emergency Reconnection Guide

**If you're reading this, you need to reconnect to Jarvis (the AI on the VPS).**

---

## 🆘 QUICK ACCESS

| Method | Command/URL |
|--------|-------------|
| **SSH** | `ssh root@165.245.138.91` |
| **Tailscale SSH** | `ssh root@100.68.120.99` |
| **DigitalOcean Console** | https://cloud.digitalocean.com → Droplets → factorylm-prod → Access |
| **Telegram** | Message @JarvisVPS |

---

## 📍 VPS INFO

- **Public IP:** `165.245.138.91`
- **Tailscale IP:** `100.68.120.99`
- **Hostname:** factorylm-prod
- **Provider:** DigitalOcean (Atlanta)
- **OS:** Ubuntu 24.04 LTS
- **Users:** root, mike

---

## 🔧 FIX COMMANDS

```bash
# Restart Jarvis/Clawdbot
systemctl restart clawdbot

# Check status
systemctl status clawdbot

# View logs
journalctl -u clawdbot -f

# Restart Tailscale
tailscale up

# Fix Docker
cd /opt/plane && docker compose up -d
```

---

## 📁 KEY PATHS

```
/root/jarvis-workspace/    # Main repo
/root/.clawdbot/           # Bot config
/opt/plane/                # Plane
/opt/master_of_puppets/    # Automation
```

---

## 🗝️ VPS SSH PUBLIC KEY

```
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIOY0hljziGSbgrv8E/wmCXovYypHw1IKWX5XYyw/hqvY root@srv1078052
```

---

**Full docs:** See `EMERGENCY_ACCESS.md` in this repo.
