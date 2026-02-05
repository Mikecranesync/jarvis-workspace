# 🗺️ NETWORK MAP

**Auto-updated by Jarvis. Every connection gets documented here.**

Last Updated: 2026-02-05 00:00 UTC

---

## 🌐 Tailscale Mesh Network

| Device | Tailscale IP | Hostname | OS | Status | ShowUI | Jarvis Node |
|--------|--------------|----------|-----|--------|--------|-------------|
| JarvisVPS | 100.68.120.99 | factorylm-prod | Ubuntu 24.04 | ✅ Online | N/A | Brain |
| PLC Laptop | 100.72.2.99 | laptop-0ka3c70h | Windows | ✅ Active | ⏳ Installing | ❌ Pending |
| Travel Laptop | 100.83.251.23 | miguelomaniac | Windows | ✅ Online | ✅ Live | ❌ Pending |
| Raspberry Pi | 100.97.210.121 | factorylm-edge-pi | balenaOS | ❌ Offline (1d) | N/A | Edge Gateway |
| Old VPS | 100.102.30.102 | srv1078052 | Linux | ⚠️ Legacy | N/A | N/A |

---

## 🎮 ShowUI Computer Use (Visual Control)

| Laptop | Gradio URL | Expires | GPU | Status |
|--------|------------|---------|-----|--------|
| Travel Laptop | https://a5f0c2094e874e1cee.gradio.live | ~Feb 10 | Integrated | ✅ Live |
| PLC Laptop | TBD | TBD | Quadro P620 | ⏳ Installing |

### ShowUI Architecture
- **Planner** (Claude/GPT-4) → decides WHAT to do (needs API key)
- **Actor** (ShowUI) → finds WHERE to click (free, local)
- **Executor** (pyautogui) → performs mouse/keyboard actions

---

## 🖥️ VPS Details (factorylm-prod)

| Property | Value |
|----------|-------|
| Provider | DigitalOcean |
| Region | Atlanta |
| Public IP | 165.245.138.91 |
| Tailscale IP | 100.68.120.99 |
| RAM | 8GB |
| Disk | 154GB (36% used) |
| OS | Ubuntu 24.04.3 LTS |
| Hostname | factorylm-prod |

### Services Running
| Service | Port | Status |
|---------|------|--------|
| Clawdbot Gateway | 18789 | ✅ systemd |
| SSH | 22 | ✅ |
| Flowise | 3001 | ✅ Docker |
| n8n | 5678 | ✅ Docker |
| Flower (Celery) | 5555 | ✅ systemd |
| Redis | 6379 | ✅ Docker |
| PostgreSQL | 5432 | ✅ Docker |

### Docker Containers
| Container | Status | Purpose |
|-----------|--------|---------|
| flowise | Up 30h | AI workflow builder |
| n8n | Up 30h | Automation |
| infra_redis_1 | Up 5d (healthy) | Cache |
| infra_postgres_1 | Up 5d (healthy) | Database |

### Celery Workers
| Worker | Tasks | Status |
|--------|-------|--------|
| celery@factorylm-prod | 3,111+ completed | ✅ Running |

---

## 💻 Laptops

### PLC Laptop (100.72.2.99)
| Property | Value |
|----------|-------|
| Hostname | laptop-0ka3c70h |
| OS | Windows |
| GPU | Quadro P620 |
| Software | Factory I/O, CCW, Ollama |
| Connected PLC | Micro820 |
| Tailscale | ✅ Active (direct: 47.195.139.124:61826) |
| ShowUI | ⏳ Installing at `C:\Users\hharp\Desktop\computer_use_ootb` |
| SSH | ❌ Not configured |

### Travel Laptop (100.83.251.23)
| Property | Value |
|----------|-------|
| Hostname | miguelomaniac |
| OS | Windows |
| ShowUI URL | https://a5f0c2094e874e1cee.gradio.live |
| ShowUI Status | ✅ Live (expires ~Feb 10) |
| SSH | ❌ Not configured |

---

## 🍓 Raspberry Pi Edge (100.97.210.121)

| Property | Value |
|----------|-------|
| Hostname | factorylm-edge-pi |
| OS | balenaOS 6.10.24 |
| Tailscale IP | 100.97.210.121 |
| Status | ❌ Offline (last seen 1d ago) |
| Balena Dashboard | https://dashboard.balena-cloud.com/devices/9cc587cafd03a9fe57d2480bc0bff931 |
| Purpose | Micro820 PLC gateway |

---

## 🌍 Domains & DNS

| Domain | Points To | Purpose |
|--------|-----------|---------|
| factorylm.com | 72.60.175.144 (srv1078052) | Marketing site |
| plane.factorylm.com | 165.245.138.91 | Project management |
| api.factorylm.com | TBD | API (future) |

---

## 🔑 API Keys & Secrets

| Service | Purpose | Location |
|---------|---------|----------|
| Anthropic | Claude API | Clawdbot managed |
| Groq | Fast inference | /opt/master_of_puppets/.env |
| Gemini | Google AI | Clawdbot config |
| Perplexity | Search | /root/.config/jarvis/perplexity.env |
| Brave | Web search | Clawdbot config |
| Telegram | Bot API | Clawdbot config |
| Trello | Project mgmt | Clawdbot config |
| GitHub | CLI | gh auth |
| Doppler | Secrets mgmt | TBD (setting up) |

---

## 🔗 GitHub Repos

| Repo | URL | Purpose |
|------|-----|---------|
| factorylm-landing | github.com/mikecranesync/factorylm-landing | Marketing site |
| Rivet-PRO | github.com/mikecranesync/Rivet-PRO | Main product |
| jarvis-workspace | github.com/mikecranesync/jarvis-workspace | Jarvis brain (private) |
| factorylm | github.com/mikecranesync/factorylm | Monolith (WIP) |

---

## 📊 Connection Log

| Date | Event | Details |
|------|-------|---------|
| 2026-02-02 | Tailscale | VPS, PLC Laptop, Travel Laptop joined mesh |
| 2026-02-03 | Balena | Pi Edge deployed |
| 2026-02-04 18:00 | ShowUI | Travel laptop Gradio live |
| 2026-02-04 23:51 | ShowUI | PLC laptop install started |
| 2026-02-05 00:00 | Network | PLC laptop active, Pi offline |

---

*This file is the source of truth for network topology. Update whenever anything changes.*
