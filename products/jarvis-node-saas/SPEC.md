# Jarvis Node SaaS - MVP Spec

**Goal:** Turn Jarvis Node into a sellable product for quick recurring revenue.

**Timeline:** 2 weeks to MVP, 1 month to paying customers

---

## 🎯 Product: "NodeBot" (working name)

**One-liner:** Control any computer remotely with AI - screenshot, run commands, automate tasks.

**Target customers:**
1. **Solo IT consultants** - manage client machines remotely
2. **Small dev teams** - access work machines from home
3. **AI tinkerers** - run local models, automate workflows
4. **Streamers/creators** - control streaming PC from laptop

---

## 💰 Pricing

| Tier | Price | Nodes | Features |
|------|-------|-------|----------|
| **Free** | $0 | 1 node | Screenshot, basic commands |
| **Pro** | $9/mo | 5 nodes | All features, file transfer, scheduling |
| **Team** | $29/mo | 20 nodes | Multi-user, audit logs, API access |

**Revenue targets:**
- 100 Pro users = $900/mo
- 50 Team users = $1,450/mo
- Combined = $2,350/mo recurring

---

## 🏗️ MVP Features (Week 1-2)

### Must Have
- [ ] One-click Windows installer (.exe)
- [ ] 6-digit pairing code (no Tailscale needed)
- [ ] Web dashboard to see online nodes
- [ ] Screenshot on demand
- [ ] Run shell commands
- [ ] Basic auth (API key per user)

### Nice to Have (Week 3-4)
- [ ] Mac installer (.dmg)
- [ ] File upload/download
- [ ] Scheduled screenshots
- [ ] Keyboard/mouse control
- [ ] Stripe billing integration

---

## 🔧 Technical Architecture

```
[User's Computer]          [Our Cloud]              [Web Dashboard]
     │                          │                         │
 NodeBot.exe ──WebSocket──► node-relay.factorylm.com ◄── React app
     │                          │                         │
  (runs locally)          (routes commands)         (user control panel)
```

**Key insight:** We already built the hard parts:
- `jarvis_node.py` → NodeBot agent (needs installer wrapper)
- `server.py` → Relay server (needs multi-tenant auth)
- Control protocol → Already working

---

## 📦 Build Plan

### Week 1: Core
**Day 1-2:** Multi-tenant relay server
- Add user accounts + API keys
- Route WebSocket by user_id
- Deploy to Oracle free tier

**Day 3-4:** Windows installer
- PyInstaller → .exe
- NSIS installer with system tray
- Auto-start on boot

**Day 5:** Web dashboard v1
- Login/signup (Clerk or Auth0)
- List nodes, online status
- Screenshot button

### Week 2: Polish
**Day 6-7:** Pairing flow
- Generate 6-digit code on dashboard
- Enter code in NodeBot app
- Secure handshake

**Day 8-9:** Stripe integration
- Free tier limits (1 node)
- Upgrade flow
- Webhook for subscription status

**Day 10:** Launch prep
- Landing page on factorylm.com/nodebot
- ProductHunt draft
- Twitter/LinkedIn posts

---

## 🚀 Go-to-Market

### Launch channels (free)
1. **ProductHunt** - "Remote PC control for AI age"
2. **Reddit** - r/selfhosted, r/sysadmin, r/homelab
3. **Twitter/X** - Demo video thread
4. **Hacker News** - Show HN post

### Content marketing
- "Control your PC from anywhere without TeamViewer"
- "Run Ollama on your gaming PC from your laptop"
- "The self-hosted alternative to Parsec/AnyDesk"

---

## 🎬 Demo Script (for video)

1. Download NodeBot.exe (10 seconds)
2. Run installer, get pairing code (20 seconds)
3. Enter code in web dashboard (10 seconds)
4. Click "Screenshot" - see desktop (10 seconds)
5. Run `nvidia-smi` - see GPU stats (10 seconds)
6. "That's it. Your PC is now AI-controllable."

Total: 60 second demo video

---

## Competition

| Product | Price | Our Advantage |
|---------|-------|---------------|
| TeamViewer | $50/mo | We're cheaper, AI-native |
| Parsec | $10/mo | We do automation, not just streaming |
| AnyDesk | $15/mo | We're developer-focused |
| Tailscale | Free | We add the control layer on top |

**Positioning:** "Tailscale + automation in one package"

---

## Risks & Mitigations

| Risk | Mitigation |
|------|------------|
| Security concerns | End-to-end encryption, open source agent |
| "Just use SSH" | GUI automation, screenshots, ease of use |
| Enterprise won't trust | Start with indie/prosumer, enterprise later |

---

## Next Steps

1. **Mike decides:** Go or no-go?
2. **If go:** I start on multi-tenant relay server TODAY
3. **Parallel:** You create Stripe account + landing page copy
4. **Day 5:** First working demo
5. **Day 14:** Soft launch to Reddit

---

## Revenue Projection (Conservative)

| Month | Users | MRR |
|-------|-------|-----|
| 1 | 20 | $180 |
| 2 | 50 | $450 |
| 3 | 100 | $900 |
| 6 | 300 | $2,700 |
| 12 | 1,000 | $9,000 |

**Break-even:** ~50 users covers Oracle/infra costs (which are $0 on free tier)
