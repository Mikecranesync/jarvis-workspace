# Industrial Edge Adapter — Cost Estimate

**Project:** Network Ninja Passive Tap  
**Date:** 2026-01-29

---

## Hardware Costs

| Item | Cost | Notes |
|------|------|-------|
| BeagleBone Black Industrial | $0 | Already owned |
| USB-to-Ethernet Adapter | $15-25 | For WireGuard tunnel (2nd NIC) |
| MicroSD Card (32GB) | $8-12 | For OS if not using eMMC |
| 5V 2A Power Supply | $10-15 | Or use PoE splitter |
| Ethernet Cables (x2) | $5-10 | One for PLC, one for internet |
| Enclosure (optional) | $15-30 | DIN-rail or project box |
| **Hardware Total** | **$53-92** | (You may have most of this) |

---

## Software Costs

| Software | Cost | Notes |
|----------|------|-------|
| Debian Linux | **FREE** | Open source |
| Python 3 | **FREE** | Pre-installed |
| Scapy | **FREE** | Open source packet manipulation |
| WireGuard | **FREE** | Open source VPN |
| tcpdump/libpcap | **FREE** | Open source |
| Mosquitto MQTT | **FREE** | Open source broker |
| pymodbus | **FREE** | Open source Modbus library |
| opcua-asyncio | **FREE** | Open source OPC UA |
| **Software Total** | **$0** | 100% open source |

---

## Cloud/Service Costs

| Service | Cost | Notes |
|---------|------|-------|
| VPS (already have) | $0 | Using existing server |
| WireGuard server | $0 | Runs on your VPS |
| Telegram Bot API | **FREE** | No cost |
| Claude API (optional) | $0-20/mo | For AI diagnostics |
| Domain (optional) | $0 | Not needed for MVP |
| **Services Total** | **$0-20/mo** | |

---

## Total Project Cost

| Category | One-Time | Monthly |
|----------|----------|---------|
| Hardware | $53-92 | $0 |
| Software | $0 | $0 |
| Services | $0 | $0-20 |
| **TOTAL** | **$53-92** | **$0-20** |

---

## What You Likely Already Have

- ✅ BeagleBone Black Industrial
- ✅ VPS with WireGuard capability
- ✅ Telegram bot (Jarvis)
- ✅ Claude API access
- ✅ Factory IO for testing
- ? USB-Ethernet adapter
- ? MicroSD card
- ? 5V power supply

---

## Cost to Scale (Per Unit)

If you build these for customers:

| Volume | Unit Cost | Notes |
|--------|-----------|-------|
| 1 unit | ~$150 | BeagleBone + accessories |
| 10 units | ~$120/ea | Bulk discount |
| 50 units | ~$100/ea | Volume pricing |
| 100+ units | ~$85/ea | Manufacturing pricing |

**Potential SaaS pricing:** $29-99/mo per adapter for monitoring service

---

*Total MVP cost: Under $100 (mostly stuff you already have)*
