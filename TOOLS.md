# TOOLS.md - Jarvis Local Notes

## Configured Skills

### Gemini ♊️
- **API Key:** Configured in clawdbot.json
- **Models available:** gemini-2.5-flash, gemini-2.5-pro, gemini-2.0-flash
- **Use for:** Quick queries, second opinions, cheap token usage

### Coding Agent 🤖
- **Status:** Available
- **Use for:** Spawn sub-agents for complex/long-running coding tasks

### GitHub
- **CLI:** `gh` installed and authenticated
- **Use for:** Repo management, PRs, issues

---

## Mike's Environment

### Hardware
- **Main laptop:** Windows, Clawdbot host
- **Second laptop:** Connected to Micro 820 PLC + push button panel (Factory I/O)
- **Phone:** Android (RideView testing)

### Projects
- **FactoryLM:** Industrial AI platform (factorylm.com)
- **RideView:** Torque stripe inspection camera
- **Factory I/O:** PLC simulation integration

### GitHub
- https://github.com/Mikecranesync

---

## Future Skills to Consider

| Skill | What For | Needs |
|-------|----------|-------|
| **sag** | Voice TTS output | ElevenLabs API key |
| **discord** | Community management | Discord bot token |
| **openai-whisper-api** | Transcribe audio | OpenAI API key |

---

## Hostinger VPS (Production Server)

| Spec | Value |
|------|-------|
| **Hostname** | srv1078052.hstgr.cloud |
| **IP** | 72.60.175.144 |
| **OS** | Ubuntu 24.04 LTS |
| **CPU** | 1 core |
| **RAM** | 4 GB |
| **Disk** | 50 GB |
| **Location** | Boston, USA |
| **SSH User** | root |
| **Expires** | Feb 21, 2026 (auto-renew ON) |

### Deployed Services (TODO)
- [ ] Clawdbot (Jarvis)
- [ ] Rivet-PRO (PLC-Copilot bot)
- [ ] PostgreSQL
- [ ] Nginx
- [ ] Twilio WhatsApp webhook

---

*Updated: 2026-01-26*
