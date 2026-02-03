# 🔐 KEYMASTER - Credentials Registry

**Master list of all credentials, API keys, and access methods.**

Last Updated: 2026-02-03 02:20 UTC

---

## 🎯 Quick Reference

| Service | Type | Location |
|---------|------|----------|
| SSH to VPS | Key | `/root/.ssh/id_ed25519` |
| Anthropic | API Key | Clawdbot config |
| Groq | API Key | `/opt/master_of_puppets/.env` |
| Gemini | API Key | `/opt/master_of_puppets/.env` |
| Perplexity | API Key | `/root/.config/jarvis/perplexity.env` |
| GitHub | OAuth | `gh auth` (Mikecranesync) |
| Telegram | Bot Token | Clawdbot config |
| Plane | User/Pass | mike@factorylm.com / plane123 |
| MailerLite | API Key | `/root/.config/jarvis/mailerlite.env` |
| Calendly | API Key | `/root/.config/jarvis/calendly.env` |
| Email | SMTP | `/root/.config/jarvis/email.env` |

---

## 🖥️ SSH Access

### VPS Public Key (For Authorizing on Other Machines)
```
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIOY0hljziGSbgrv8E/wmCXovYypHw1IKWX5XYyw/hqvY root@srv1078052
```
**Fingerprint:** `SHA256:Bt9FzW1sBCpoR7P8f63sMYG2S+ls6U8ZMUhUMMjhJ1M`

### SSH Targets
| Target | User | IP | Key Authorized |
|--------|------|-----|----------------|
| VPS | root | 100.68.120.99 | ✅ (self) |
| VPS | mike | 100.68.120.99 | ✅ |
| PLC Laptop | mike | 100.72.2.99 | ❌ |
| Travel Laptop | mike | 100.83.251.23 | ❌ |
| Raspberry Pi | pi | TBD | ⏳ |

---

## 🤖 AI/LLM APIs

### Anthropic (Claude)
- **Used by:** Clawdbot
- **Location:** Clawdbot config (`clawdbot config get`)
- **Format:** `sk-ant-api03-...`

### Groq
- **Used by:** Master of Puppets
- **Location:** `/opt/master_of_puppets/.env`
- **Variable:** `GROQ_API_KEY`
- **Format:** `gsk_...`

### Google Gemini
- **Used by:** Master of Puppets
- **Location:** `/opt/master_of_puppets/.env`
- **Variable:** `GEMINI_API_KEY`

### Perplexity
- **Used by:** Research/Search tasks
- **Location:** `/root/.config/jarvis/perplexity.env`
- **Variable:** `PERPLEXITY_API_KEY`
- **Format:** `pplx-...`

### Flowise
- **Used by:** Master of Puppets
- **Location:** `/opt/master_of_puppets/.env`
- **Variables:** `FLOWISE_URL`, `FLOWISE_API_KEY`

---

## 📱 Telegram Bots

| Bot | Purpose | Token Location |
|-----|---------|----------------|
| JarvisVPS (Clawdbot) | Main assistant | Clawdbot config |
| JarvisMIO | PLC Copilot | `7855741814:...` |
| JarvisVPS Heartbeat | Monitoring | `8387943893:...` |

**Mike's Telegram ID:** `8445149012`

---

## 📊 Databases & Services

### Master of Puppets Stack
**Location:** `/opt/master_of_puppets/.env`

| Service | Variable | Default |
|---------|----------|---------|
| PostgreSQL Host | `POSTGRES_HOST` | localhost |
| PostgreSQL Port | `POSTGRES_PORT` | 5432 |
| PostgreSQL DB | `POSTGRES_DB` | jarvis |
| PostgreSQL User | `POSTGRES_USER` | jarvis |
| PostgreSQL Pass | `POSTGRES_PASSWORD` | (in .env) |
| Redis | `REDIS_URL` | redis://localhost:6379 |
| InfluxDB URL | `INFLUXDB_URL` | (in .env) |
| InfluxDB Token | `INFLUXDB_TOKEN` | (in .env) |

### Plane Stack
**Location:** `/opt/plane/.env`

| Service | Value |
|---------|-------|
| Web URL | http://plane.factorylm.com |
| API URL | http://plane.factorylm.com/api |
| User | mike@factorylm.com |
| Password | plane123 |
| Postgres User | plane |
| Postgres DB | plane |

---

## 🌐 GitHub

**Authenticated as:** `Mikecranesync`
**Auth method:** OAuth via `gh` CLI
**Token location:** `/root/.config/gh/hosts.yml`

### Repos with Access
- mikecranesync/factorylm-landing
- mikecranesync/Rivet-PRO
- (All repos under Mikecranesync account)

---

## 📧 Email/Marketing

### MailerLite
**Location:** `/root/.config/jarvis/mailerlite.env`

### Calendly
**Location:** `/root/.config/jarvis/calendly.env`

### SMTP/Email
**Location:** `/root/.config/jarvis/email.env`

---

## 🌍 Domains

| Domain | Purpose | Registrar |
|--------|---------|-----------|
| factorylm.com | Main site | Unknown |
| plane.factorylm.com | Project mgmt | (DNS only) |

---

## 🐳 Docker

### Plane Containers (Running)
```
plane-api-1
plane-live-1
plane-space-1
plane-admin-1
plane-web-1
plane-beat-worker-1
plane-worker-1
plane-plane-redis-1
plane-plane-minio-1
plane-plane-db-1
```

---

## 📁 Credential File Locations

```
/root/
├── .ssh/
│   ├── id_ed25519           # VPS private key
│   ├── id_ed25519.pub       # VPS public key
│   └── authorized_keys      # Keys that can SSH to VPS
├── .config/
│   ├── gh/hosts.yml         # GitHub OAuth token
│   └── jarvis/
│       ├── perplexity.env   # Perplexity API
│       ├── mailerlite.env   # MailerLite API
│       ├── calendly.env     # Calendly API
│       └── email.env        # SMTP credentials
└── ...

/opt/
├── master_of_puppets/
│   └── .env                 # Main env (Groq, Gemini, Postgres, etc)
├── plane/
│   └── .env                 # Plane docker env
└── ...
```

---

## 🔄 How to Add New Credentials

1. Add the credential to the appropriate `.env` file
2. Update this file (KEYMASTER.md)
3. Update NETWORK_MAP.md if it's a connection
4. Commit changes: `git add -A && git commit -m "Add [credential name]"`

---

## ⚠️ Security Notes

- Never commit actual secrets to git
- Use `.env` files in `.gitignore`
- This file documents WHAT exists and WHERE, not the actual values
- Rotate keys if exposed
- Use least-privilege access

---

*This file is the credential registry. Keep it updated.*

---

## 🌊 Flowise (Added 2026-02-03)

| Property | Value |
|----------|-------|
| URL (internal) | http://localhost:3001 |
| URL (external) | http://165.245.138.91:3001 |
| Username | mike |
| Password | CNI9EgSKBu6vm18t |
| API Key | cd25ef26ae7e4ec9293ce8cdfbc80bcf8ed6ccd1c486922011c1fc9ad5f707ec |

