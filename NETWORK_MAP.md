# 🗺️ NETWORK MAP

**Auto-updated by Jarvis. Every connection gets documented here.**

Last Updated: 2026-02-03 02:16 UTC

---

## 🌐 Tailscale Mesh Network

| Device | Tailscale IP | Hostname | OS | Status | Jarvis Node |
|--------|--------------|----------|-----|--------|-------------|
| JarvisVPS | 100.68.120.99 | factorylm-prod | Ubuntu 24.04 | ✅ Online | Brain (not node) |
| PLC Laptop | 100.72.2.99 | laptop-0ka3c70h | Windows | ✅ Online | ❌ Not installed |
| Travel Laptop | 100.83.251.23 | miguelomaniac | Windows | ✅ Online | ✅ Port 8765 |
| Old VPS | 100.102.30.102 | srv1078052 | Linux | ⚠️ Legacy | N/A |
| Raspberry Pi | TBD | jarvis-pi | Linux | ⏳ Pending | ⏳ Pending |

---

## 🖥️ VPS Details (factorylm-prod)

| Property | Value |
|----------|-------|
| Provider | DigitalOcean |
| Region | Atlanta |
| Public IP | 165.245.138.91 |
| Tailscale IP | 100.68.120.99 |
| RAM | 8GB |
| OS | Ubuntu 24.04.3 LTS |
| Hostname | factorylm-prod |

### Services Running
| Service | Port | Status |
|---------|------|--------|
| Clawdbot | - | systemd |
| SSH | 22 | ✅ |
| Nginx | 80, 443 | ✅ |
| Plane (Web) | 8070 | ✅ |
| Plane (API) | 8080 | ✅ |
| Docker | - | ✅ |

### Docker Containers
| Container | Port | Purpose |
|-----------|------|---------|
| plane-web | 3000 | Plane frontend |
| plane-api | 8000 | Plane backend |
| plane-worker | - | Background jobs |
| plane-beat-worker | - | Scheduled tasks |
| plane-postgres | 5432 | Database |
| plane-redis | 6379 | Cache |
| plane-minio | 9000 | Object storage |

---

## 💻 Laptops

### PLC Laptop (100.72.2.99)
| Property | Value |
|----------|-------|
| OS | Windows |
| GPU | Quadro P620 |
| Software | RSLogix, Ollama, OBS |
| Tailscale | laptop-0ka3c70h |
| SSH | ❌ Key not authorized |
| Jarvis Node | ❌ Not installed |

### Travel Laptop (100.83.251.23)
| Property | Value |
|----------|-------|
| OS | Windows |
| Tailscale | miguelomaniac |
| SSH | ❌ Key not authorized |
| Jarvis Node | ✅ Port 8765 |

---

## 🍓 Raspberry Pi (Pending)

| Property | Value |
|----------|-------|
| Model | TBD |
| OS | Raspberry Pi OS |
| Tailscale IP | TBD |
| SSH | ⏳ Pending |
| Jarvis Node | ⏳ Pending |
| Camera | TBD |
| GPIO | TBD |

---

## 🌍 Domains & DNS

| Domain | Points To | Purpose |
|--------|-----------|---------|
| factorylm.com | 72.60.175.144 | Marketing site |
| plane.factorylm.com | 165.245.138.91 | Project management |
| api.factorylm.com | TBD | API (future) |

---

## 🔌 API Endpoints

### Jarvis Node Endpoints (Port 8765)
| Endpoint | Method | Description |
|----------|--------|-------------|
| /health | GET | Node health status |
| /shell | POST | Run shell command |
| /screenshot | GET | Capture screen |
| /click | POST | Mouse click |
| /type | POST | Type text |
| /interpret | POST | Open Interpreter |
| /camera/photo | GET | Pi camera capture |
| /gpio | POST | Pi GPIO control |

### External APIs Used
| Service | Purpose | Key Location |
|---------|---------|--------------|
| Anthropic | Claude API | ANTHROPIC_API_KEY |
| Groq | Fast inference | /opt/master_of_puppets/.env |
| Gemini | Google AI | /opt/master_of_puppets/.env |
| Perplexity | Search | /root/.config/jarvis/perplexity.env |
| LangFuse | Observability | /opt/master_of_puppets/.env |
| Telegram | Bot API | Clawdbot config |
| GitHub | API | gh CLI authenticated |
| DigitalOcean | Hosting | DO API token |

---

## 📞 Contact Points

| Type | Value | Notes |
|------|-------|-------|
| Telegram Bot | @JarvisVPS | Main interface |
| Email | mike@factorylm.com | Plane account |

---

## 🔗 GitHub Repos

| Repo | URL | Purpose |
|------|-----|---------|
| factorylm-landing | github.com/mikecranesync/factorylm-landing | Marketing site |
| Rivet-PRO | github.com/mikecranesync/Rivet-PRO | Main product |
| jarvis-workspace | This repo | Jarvis brain |

---

## 📊 Connection Log

*Auto-appended when new connections are discovered*

| Date | Connection Type | Details |
|------|-----------------|---------|
| 2026-02-02 | Tailscale | VPS joined mesh |
| 2026-02-02 | Tailscale | PLC Laptop visible |
| 2026-02-02 | Tailscale | Travel Laptop visible |
| 2026-02-02 | HTTP | Plane deployed at plane.factorylm.com |
| 2026-02-03 | HTTP | Travel Laptop Jarvis Node responding |

---

*This file is the source of truth for network topology. Update it whenever anything changes.*

---

## 🌊 Flowise (Added 2026-02-03)

| Property | Value |
|----------|-------|
| Port | 3001 |
| Container | flowise |
| Status | ✅ Running |
| Auth | Username/Password |

