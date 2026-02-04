# FactoryLM Mini - Project Plan

**Created:** 2026-02-04  
**Target Demo:** 2026-02-10 (6 days)  
**Owner:** Mike Harper + Jarvis

---

## This Week's Goals

### Mike (Hardware + Business)
- [ ] Order hardware from Amazon BOM (Day 1-2)
- [ ] Review firmware when hardware arrives
- [ ] Test with real PLC/VFD when ready
- [ ] Prepare demo talking points

### Jarvis (Software + Integration)
- [ ] Complete sensor node firmware (Day 1-2)
- [ ] Set up edge gateway stack (Day 2-3)
- [ ] Integrate with Telegram/WhatsApp (Day 3-4)
- [ ] Build basic web dashboard (Day 4-5)
- [ ] Testing and bug fixes (Day 5-6)

---

## Day-by-Day Breakdown

### Day 1 (Feb 4) - Foundation
**Mike:**
- ✅ Strategy session complete
- ⬜ Order Starter Kit from Amazon

**Jarvis:**
- ✅ Create GitHub repo structure
- ✅ Write sensor node firmware skeleton
- ⬜ Test compile firmware
- ⬜ Set up MQTT broker on VPS

### Day 2 (Feb 5) - Firmware
**Mike:**
- ⬜ Hardware ships (Prime)

**Jarvis:**
- ⬜ Complete Modbus TCP client in firmware
- ⬜ Add OTA update capability
- ⬜ Create edge gateway Docker compose
- ⬜ Set up InfluxDB for time series data

### Day 3 (Feb 6) - Gateway
**Mike:**
- ⬜ Hardware arrives
- ⬜ Flash Pi with base OS

**Jarvis:**
- ⬜ FactoryLM engine integration
- ⬜ MQTT → InfluxDB pipeline
- ⬜ Basic anomaly detection logic
- ⬜ Telegram bot integration

### Day 4 (Feb 7) - Integration
**Mike:**
- ⬜ Flash ESP32 sensor nodes
- ⬜ Connect to test network

**Jarvis:**
- ⬜ WhatsApp integration
- ⬜ Natural language query handler
- ⬜ Alert/notification system
- ⬜ Web dashboard (Grafana or custom)

### Day 5 (Feb 8) - Testing
**Mike:**
- ⬜ Test with real VFD if available
- ⬜ Feedback on UX

**Jarvis:**
- ⬜ End-to-end testing
- ⬜ Bug fixes
- ⬜ Performance optimization
- ⬜ Documentation

### Day 6 (Feb 9) - Polish
**Mike:**
- ⬜ Demo rehearsal
- ⬜ Prepare slides/talking points

**Jarvis:**
- ⬜ Final bug fixes
- ⬜ Demo environment stable
- ⬜ Backup/recovery tested

### Day 7 (Feb 10) - DEMO DAY
- ⬜ Live demo to prospect
- ⬜ Collect feedback
- ⬜ Plan next iteration

---

## Hardware Order Checklist

**Order Today (Feb 4):**

| Item | Qty | Price | Status |
|------|-----|-------|--------|
| LILYGO T-ETH-Lite ESP32-S3 | 3 | $75 | ⬜ |
| Raspberry Pi 4 (4GB) | 1 | $55 | ⬜ |
| Google Coral USB | 1 | $60 | ⬜ |
| Pi Power Supply | 1 | $10 | ⬜ |
| microSD 64GB | 1 | $10 | ⬜ |
| Ethernet cables 5-pack | 1 | $12 | ⬜ |
| USB-C cables | 1 | $10 | ⬜ |
| **TOTAL** | | **~$232** | |

---

## Software Components

### Sensor Node (ESP32)
```
firmware/sensor-node/
├── platformio.ini       ✅ Created
├── src/
│   └── main.cpp         ✅ Created
├── include/
│   └── config.h         ⬜ TODO
└── lib/                 ⬜ TODO
```

### Edge Gateway (Pi)
```
server/
├── docker-compose.yml   ⬜ TODO
├── mosquitto/           ⬜ MQTT broker config
├── influxdb/            ⬜ Time series DB
├── factorylm/           ⬜ Main engine
│   ├── ingest.py        ⬜ MQTT consumer
│   ├── analyze.py       ⬜ Anomaly detection
│   ├── llm.py           ⬜ Natural language
│   └── notify.py        ⬜ Alerts
├── grafana/             ⬜ Dashboard
└── nginx/               ⬜ Web server
```

### Messaging Integration
```
Already have via Clawdbot:
✅ Telegram
✅ WhatsApp (pending phone #)
✅ Signal (optional)
```

---

## GitHub Repository

**Repo:** `mikecranesync/factorylm-mini`

**Branches:**
- `main` - Stable releases
- `develop` - Active development
- `feature/*` - New features

**CI/CD:**
- GitHub Actions for firmware builds
- Auto-release on tag

---

## Success Metrics (Demo Day)

1. ✅ Sensor node connects to network
2. ✅ Data flows to edge gateway
3. ✅ Can query via Telegram: "What's the status?"
4. ✅ Alerts fire on simulated fault
5. ✅ Dashboard shows real-time data
6. ✅ Runs without cloud connection

---

## Risk Mitigation

| Risk | Mitigation |
|------|------------|
| Hardware delayed | Order today, Prime shipping |
| Firmware bugs | Test on VPS simulator first |
| Demo environment unstable | Prepare recorded backup demo |
| Network issues at demo site | Bring portable router |

---

## Communication

**Daily Check-in:** Jarvis reports progress via Telegram at 9 AM and 5 PM

**Blocker Protocol:** 
- Jarvis flags immediately via Telegram
- Mike provides direction or unblocks

**Code Reviews:**
- Jarvis pushes to `develop`
- Mike reviews before merge to `main`

---

## Budget Summary

| Category | Amount |
|----------|--------|
| Hardware (Starter Kit) | $232 |
| Cloud (VPS, already have) | $0 |
| Software (open source) | $0 |
| **TOTAL** | **$232** |

---

## Post-Demo Roadmap

### v0.2 (Week 2)
- CraneSync specialization
- More robust anomaly detection
- Mobile app prototype

### v0.3 (Week 3)
- Vehicle/OBD2 support
- Multi-gateway orchestration
- Customer pilot deployment

### v1.0 (Month 2)
- Production hardening
- Security audit
- Documentation complete
- First paying customer

---

**Document Status:** ACTIVE  
**Last Updated:** 2026-02-04 02:50 UTC
