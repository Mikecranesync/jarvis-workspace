# Hetzner VPS Migration Plan

*Research completed: 2026-01-30*
*For: Migrating Jarvis from Hostinger to Hetzner*

---

## Current Hostinger Situation (CRITICAL)

```
CPU:      1 vCPU (AMD EPYC 9354P shared)
RAM:      3.8 GB (2.5 GB used = 66%)
Disk:     48 GB (42 GB used = 88% FULL!)
Free:     Only 6 GB remaining
Plan:     KVM 1 (~$5-8/mo actual)
```

**Problem:** Disk is 88% full. Need to migrate ASAP.

---

## Hetzner Cloud Options (Prices in EUR, add ~7% for USD)

### Best Value: CAX Series (ARM/Ampere)
*Highest price-to-performance ratio*

| Plan | vCPU | RAM | SSD | Bandwidth | Price | Notes |
|------|------|-----|-----|-----------|-------|-------|
| **CAX11** | 2 | 4 GB | 40 GB | 20 TB | €3.79/mo | Best budget |
| **CAX21** | 4 | 8 GB | 80 GB | 20 TB | €6.49/mo | Sweet spot |
| **CAX31** | 8 | 16 GB | 160 GB | 20 TB | €12.49/mo | Room to grow |
| CAX41 | 16 | 32 GB | 320 GB | 20 TB | €24.49/mo | Overkill |

⚠️ **Caveat:** ARM architecture. Most software works, but some edge cases may need x86.

### x86 Option: CX Series (Intel/AMD)
*If you need x86 compatibility*

| Plan | vCPU | RAM | SSD | Bandwidth | Price | Notes |
|------|------|-----|-----|-----------|-------|-------|
| CX22 | 2 | 4 GB | 40 GB | 20 TB | €3.79/mo | Same as current |
| **CX32** | 4 | 8 GB | 80 GB | 20 TB | €6.80/mo | **RECOMMENDED** |
| CX42 | 8 | 16 GB | 160 GB | 20 TB | €16.40/mo | Comfortable |

### Performance Option: CPX Series (NVMe)
*If you want faster disk I/O*

| Plan | vCPU | RAM | NVMe | Bandwidth | Price |
|------|------|-----|------|-----------|-------|
| CPX11 | 2 | 2 GB | 40 GB | 20 TB | €4.35/mo |
| **CPX21** | 3 | 4 GB | 80 GB | 20 TB | €7.55/mo |
| CPX31 | 4 | 8 GB | 160 GB | 20 TB | €13.60/mo |

### Dedicated CPU: CCX Series
*If you need guaranteed CPU resources*

| Plan | vCPU | RAM | SSD | Bandwidth | Price |
|------|------|-----|-----|-----------|-------|
| **CCX13** | 2 dedicated | 8 GB | 80 GB | 20 TB | €12.49/mo |
| CCX23 | 4 dedicated | 16 GB | 160 GB | 20 TB | €24.49/mo |

---

## My Recommendation

### Option A: Budget King — **CAX21** (€6.49/mo ≈ $7)
```
4 vCPU (ARM Ampere)
8 GB RAM (2x current)
80 GB SSD (1.7x current)
20 TB bandwidth (5x Hostinger)
```
**Why:** Best value. 4x the CPU, 2x the RAM, nearly 2x disk for ~same price.

**Risk:** ARM architecture. Test your stack first.

### Option B: Safe x86 — **CX32** (€6.80/mo ≈ $7.30)
```
4 vCPU (Intel/AMD x86)
8 GB RAM (2x current)
80 GB SSD (1.7x current)
20 TB bandwidth (5x Hostinger)
```
**Why:** Guaranteed compatibility. Same architecture as current server.

### Option C: Comfortable — **CX42** (€16.40/mo ≈ $18)
```
8 vCPU (Intel/AMD x86)
16 GB RAM (4x current)
160 GB SSD (3.3x current)
20 TB bandwidth
```
**Why:** Room to grow. Won't hit limits for a long time.

---

## Migration Checklist

### Pre-Migration
- [ ] Sign up at hetzner.com (needs ID verification)
- [ ] Create cloud project
- [ ] Choose datacenter (Nuremberg DE, Falkenstein DE, Helsinki FI, or Ashburn US)
- [ ] Spin up test server

### Migration Steps
1. **Snapshot current server** (if Hostinger supports)
2. **Install fresh Ubuntu 22.04** on Hetzner
3. **Copy data:**
   ```bash
   rsync -avz --progress /root/jarvis-workspace/ root@NEW_IP:/root/jarvis-workspace/
   ```
4. **Install dependencies:**
   - Node.js 22
   - Docker (if using CMMS)
   - Clawdbot
   - Tailscale
5. **Update DNS** (if applicable)
6. **Update Tailscale** config
7. **Test everything**
8. **Cancel Hostinger** after verified

### Data to Migrate (~42 GB used)
- `/root/jarvis-workspace/` — Main workspace
- Clawdbot config
- Docker volumes (if any)
- Cron jobs
- SSH keys
- Tailscale auth

---

## Hetzner Quirks to Know

### Pros
- **5x bandwidth** (20 TB vs 4 TB)
- **3.3x network speed** (1 Gbit vs 300 Mbit)
- **25-second provisioning** (vs 150 sec at Hostinger)
- **Better I/O performance** (benchmarks confirm)
- **Hourly billing** (pay only what you use)
- **API access** (automate everything)

### Cons
- **ID Verification required** (can take 24-48 hours)
- **Stock shortages** (popular plans sell out)
- **No managed backups** by default (extra €0.01/GB/mo)
- **Support is technical** (not hand-holding)
- **EU datacenters** (latency from US, unless using Ashburn)

### Gotchas
- **VAT added** for EU customers (0% for US)
- **No Windows images** (Linux only, bring your own)
- **IPv4 costs extra** on some plans (€0.50/mo)

---

## Ashburn, VA Datacenter (US)
If latency to EU matters, Hetzner has a US datacenter in Ashburn, Virginia. Same pricing, better latency for US users.

---

## Bottom Line

| Current (Hostinger) | Recommended (Hetzner CX32) |
|---------------------|---------------------------|
| 1 vCPU | 4 vCPU |
| 4 GB RAM | 8 GB RAM |
| 48 GB disk (88% full) | 80 GB disk |
| 4 TB bandwidth | 20 TB bandwidth |
| 300 Mbps | 1 Gbps |
| ~$8/mo | ~$7.30/mo |

**Result:** 4x CPU, 2x RAM, 2x disk, 5x bandwidth, 3x speed — for LESS money.

---

*Hetzner is the move. Let me know when you want to start the migration.*
