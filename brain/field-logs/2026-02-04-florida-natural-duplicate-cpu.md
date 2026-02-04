# Field Log: Duplicate CPU Module Incident

**Date:** 2026-02-04  
**Customer:** Florida's Natural (beverage/citrus processing)  
**Equipment:** Palletizer + Conveyor Line (Allen Bradley)  
**Reported By:** Mike Harper  
**Classification:** Network Identity Conflict / Asset Mismanagement

---

## Incident Summary

A conveyor line was experiencing intermittent issues - "limping along" with unexplained faults. Root cause investigation revealed:

1. **Palletizer** on the same network had been **shut down for extended period**
2. Someone **removed the CPU module** from the offline palletizer
3. That CPU was **installed into the conveyor line** (likely as a replacement/spare)
4. Eventually, the **palletizer was powered back on** (with its original or a different CPU)
5. **Two devices now had conflicting network identities** (same IP, node address, or device name)
6. Result: Network message collisions, intermittent communication failures, unpredictable behavior

## Why Allen Bradley Didn't Catch It

- PLCs don't have self-awareness of network topology changes
- No asset tracking - PLC doesn't know "which CPU am I?"
- No network anomaly detection built-in
- FactoryTalk diagnostics require active monitoring setup (rarely configured)
- The conveyor PLC was still executing its program, so no fault was triggered
- Symptoms were intermittent, making traditional troubleshooting difficult

---

## How FactoryLM Would Detect This

### Layer 1: Network Sentinel (ESP32 nodes - $15 each)

Each sensor node monitors:
- **ARP table changes** - alerts if MAC/IP mapping changes
- **Device presence** - heartbeat detection for each PLC/drive
- **Network traffic patterns** - baseline vs anomaly
- **Duplicate IP detection** - passive ARP monitoring

**Detection trigger:** "ALERT: IP 192.168.1.50 responding from two different MAC addresses"

### Layer 2: Asset Identity Tracking

FactoryLM reads PLC identity on startup:
- Serial number
- Firmware version  
- Project name
- Last download timestamp

**Detection trigger:** "ALERT: Conveyor Line CPU serial number changed from ABC123 to XYZ789"

### Layer 3: Communication Health Scoring

Monitor CIP connection statistics:
- Message timeouts
- Retry counts
- Connection re-establishments
- Produced/consumed tag failures

**Detection trigger:** "ALERT: Conveyor Line showing 47% message retry rate (baseline: 2%)"

### Layer 4: LLM Correlation

When alerts fire, the LLM correlates:
- "Palletizer came online 2 hours ago"
- "Conveyor communication degraded starting 2 hours ago"  
- "Two devices responding to same IP"

**LLM conclusion:** "Probable duplicate network identity. Palletizer and Conveyor may have conflicting IP addresses or a CPU module was moved between systems."

---

## $300 Budget Deployment Strategy

### Hardware Cost Breakdown

| Device | Unit Cost | Quantity | Total |
|--------|-----------|----------|-------|
| ESP32-S3 DevKit | $15 | 12 | $180 |
| Ethernet adapter (W5500) | $5 | 12 | $60 |
| Enclosures + mounting | $3 | 12 | $36 |
| Power supplies (USB) | $2 | 12 | $24 |
| **TOTAL** | | **12 nodes** | **$300** |

### What 12 Nodes Covers

Typical citrus processing line:
1. **Extractor** - 1 node
2. **Pasteurizer** - 1 node  
3. **Evaporator** - 1 node
4. **Blending tank** - 1 node
5. **Filler** - 1 node
6. **Capper** - 1 node
7. **Labeler** - 1 node
8. **Case packer** - 1 node
9. **Palletizer** - 1 node
10. **Conveyor line** - 1 node
11. **Network switch #1** - 1 node (monitors backbone)
12. **Network switch #2** - 1 node (monitors backbone)

**Coverage:** Entire packaging hall with $300

### What Each Node Does

```
┌─────────────────────────────────────────────────┐
│  ESP32 SENTINEL NODE ($15)                      │
├─────────────────────────────────────────────────┤
│  • Ping PLC every 5 seconds                     │
│  • Monitor ARP table for changes                │
│  • Track device presence (online/offline)       │
│  • Measure response latency                     │
│  • Count communication errors                   │
│  • Report to Edge Gateway via MQTT              │
│  • Local LED: Green=OK, Red=Fault, Blue=Comm    │
└─────────────────────────────────────────────────┘
```

### In This Incident

If deployed, the system would have:

1. **T+0:** Palletizer powered on
2. **T+1 sec:** Node 9 (Palletizer) reports "Device online"
3. **T+2 sec:** Node 10 (Conveyor) reports "ARP conflict detected - IP 192.168.1.50 has two MACs"
4. **T+3 sec:** Edge Gateway correlates events
5. **T+5 sec:** LLM generates alert: "Network identity conflict between Palletizer and Conveyor. Check for duplicate IP or moved CPU module."
6. **T+10 sec:** Maintenance tech receives Telegram/WhatsApp alert with diagnosis

**Time to detection: 10 seconds** (vs. days/weeks of "limping along")

---

## Lessons Learned

1. **PLCs are dumb about identity** - they don't know if they're in the right chassis
2. **Network conflicts are silent killers** - no alarms, just degraded performance
3. **Cheap sensors beat expensive ignorance** - $15 per node prevents $50K+ downtime
4. **Asset tracking is undervalued** - knowing which CPU is where prevents this class of error
5. **Edge-first architecture enables air-gapped detection** - no cloud needed

---

## Recommended FactoryLM Features (from this incident)

- [ ] **CPU Serial Tracking** - alert on serial number change
- [ ] **Network Identity Guardian** - continuous ARP/IP monitoring  
- [ ] **Asset Topology Map** - visual "what's connected where"
- [ ] **Swap Detection** - "Module moved from Slot A to Slot B"
- [ ] **Communication Health Score** - per-device reliability metric

---

**Field Log Status:** CAPTURED  
**Knowledge Base:** Ready for ingestion  
**Created:** 2026-02-04 01:53 UTC  
