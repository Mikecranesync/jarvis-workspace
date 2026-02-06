# FactoryLM Compute Stack
*Updated: 2026-02-06*

## ACTIVE SERVERS

### 1. DigitalOcean VPS (factorylm-prod)
- Location: Atlanta
- CPU: 2 vCPU
- RAM: 4GB
- Storage: ~100GB
- Cost: ~$24/mo
- Tailscale: 100.68.120.99
- Role: Main Jarvis brain, Telegram bot, CMMS

### 2. Hetzner VPS (factorylm-hetzner) - NEW!
- Location: Ashburn VA
- CPU: 4 AMD vCPU
- RAM: 8GB
- Storage: 160GB SSD
- Cost: ~€15/mo (~$16)
- Tailscale: 100.67.25.53
- Public: 178.156.173.186
- SSH: `ssh -i ~/.ssh/hetzner_key root@178.156.173.186`
- Role: Heavy workloads, AI inference, Docker services

### 3. Web Server (srv1078052)
- IP: 72.60.175.144
- Role: factorylm.com website
- Cost: ~$5/mo (estimate)

### 4. PLC Laptop (Windows)
- CPU: Intel + Quadro P620 GPU
- RAM: 16GB (estimate)
- Tailscale: 100.72.2.99
- Role: Factory I/O, CCW, Ollama local AI
- Cost: $0 (owned hardware)

### 5. Travel Laptop (Windows)
- Tailscale: 100.83.251.23
- Role: Mobile dev

### 6. Raspberry Pi (factorylm-edge-pi)
- Tailscale: 100.97.210.121
- Role: PLC gateway (offline)
- Cost: $0 (owned hardware)

### 7. Pixel 9a (Android)
- Tailscale: 100.73.197.64
- Role: Mobile interface

---

## TOTALS

| Resource | Amount |
|----------|--------|
| Cloud vCPUs | 6+ |
| Cloud RAM | 12GB |
| Cloud Storage | 260GB+ |
| GPU | 1x Quadro P620 (local) |
| Monthly Cost | ~$45 |
| Edge Devices | 3 (Pi, phone, PLC laptop) |

---

## AI API ACCESS
- Anthropic Claude (Opus 4) - Main reasoning
- Groq (fast inference) - Quick tasks
- Google Gemini - Backup/comparison
- Perplexity - Research
- ElevenLabs TTS - Voice output
- LangFuse - Observability

---

## COMPARISON TO TYPICAL AI STARTUP

| Metric | FactoryLM | Typical Seed Stage | Our Advantage |
|--------|-----------|-------------------|---------------|
| Cloud Spend | $45/mo | $500-2000/mo | **10-40x cheaper** |
| GPU Access | 1 local | 0-1 cloud | Same capability, $0 |
| API Costs | ~$100/mo | ~$200-500/mo | **2-5x cheaper** |
| Edge Devices | 3 | 0 | **UNIQUE** |
| Real PLC Hardware | YES | NO | **UNIQUE** |
| Digital Twin | YES (Factory I/O) | NO | **UNIQUE** |

---

## COMPETITIVE MOAT

1. **Real Industrial Hardware** - Micro820 PLC, VFD, 3-phase motor, actual conveyor
2. **Hybrid Edge-Cloud** - Intelligence runs anywhere (cloud, local GPU, edge Pi)
3. **Factory I/O Digital Twin** - Virtual matches physical, AI watches both
4. **Telegram-Native** - No app install, works on any phone
5. **Ultra-Lean** - <$200/mo total infrastructure cost
6. **Father-Son Built** - Authentic maker story

---

## YC-RELEVANT METRICS

- **Burn Rate**: ~$150/mo (infra + APIs)
- **Runway at $0 revenue**: Infinite (bootstrapped)
- **Hardware Investment**: ~$500 (VFD, motor, conveyor parts)
- **Time to Demo**: 1 weekend build
- **Scalability**: Add customers without adding servers (edge-first)
