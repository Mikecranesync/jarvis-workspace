# Compute Upgrade Plan — VPS Analysis

*Research completed: 2026-01-30 02:50 UTC*

---

## 🚨 Current VPS Status (CRITICAL)

**Hostinger VPS** — Running at the edge!

| Resource | Current | Status |
|----------|---------|--------|
| CPU | 1 core (EPYC) | ⚠️ Limited |
| RAM | 3.8GB (1.8GB free) | ⚠️ Tight |
| Disk | 48GB (6GB free, 88% used) | 🔴 CRITICAL |
| Swap | None | ❌ Risk |
| GPU | None | ❌ |

**Immediate Issues:**
1. **Disk 88% full** — Can't install Manim/FFmpeg
2. **No swap** — OOM risk if RAM spikes
3. **1 core** — LLM inference is slow

---

## Option 1: Upgrade Current Hostinger

**Pros:**
- No migration needed
- Fast (just upgrade plan)

**Cons:**
- Hostinger not optimized for AI/LLM
- Still no GPU option
- More expensive per resource vs alternatives

**Cost:** ~$15-30/mo for more resources

---

## Option 2: Migrate to Hetzner Cloud (RECOMMENDED)

**Why Hetzner:**
- 2x-3x better price/performance
- EU data centers (low latency)
- Better for AI workloads
- Easy migration

**Recommended Plan: CX31**
| Resource | Value | Price |
|----------|-------|-------|
| CPU | 4 vCPU | |
| RAM | 8GB | |
| Disk | 80GB SSD | |
| Transfer | 20TB | |
| **Total** | | **€8.49/mo (~$9)** |

**Or CX41 for headroom:**
- 8 vCPU, 16GB RAM, 160GB SSD — €15.59/mo (~$17)

---

## Option 3: Contabo (Cheapest, Lower Quality)

**VPS M:**
| Resource | Value | Price |
|----------|-------|-------|
| CPU | 6 vCPU | |
| RAM | 16GB | |
| Disk | 400GB SSD | |
| **Total** | | **$6.99/mo** |

**Pros:** Insane value on paper
**Cons:** Poor support, overloaded nodes, latency issues

---

## Option 4: Hybrid (VPS + GPU Cloud)

**Recommended Architecture:**

**Base VPS (Hetzner CX31) — $9/mo**
- Clawdbot/Jarvis core
- Neon DB connection
- Web services
- 24/7 uptime

**GPU Rental (RunPod) — Pay-per-use**
- LLM fine-tuning: $0.34-2/hr
- Video generation (Manim): Use base VPS
- Heavy inference: Spin up as needed

**Estimated Monthly:**
- Base: $9 fixed
- GPU: $5-20 variable
- **Total: ~$15-30/mo**

---

## Migration Plan (15 min)

### If Upgrading Hostinger:
1. Log into Hostinger panel
2. Upgrade to higher tier
3. Wait for provisioning
4. Done

### If Migrating to Hetzner:
1. Sign up at hetzner.com
2. Create CX31 server (Ubuntu 22.04)
3. Install basics: `apt install docker.io nodejs npm git`
4. Export Hostinger: `tar -czvf backup.tar.gz /root/jarvis-workspace /root/.clawdbot /opt/jarvis`
5. SCP to Hetzner: `scp backup.tar.gz root@new-ip:/root/`
6. Restore and reconfigure
7. Update DNS/Tailscale
8. ~2-3 hours total

---

## Immediate Fixes (Hostinger)

**Free up disk NOW:**
```bash
# Clean Docker
docker system prune -a -f

# Clean apt
apt clean && apt autoremove -y

# Remove old logs
journalctl --vacuum-size=100M

# Find big files
du -sh /* | sort -h | tail -20
```

**Add swap (temporary relief):**
```bash
fallocate -l 4G /swapfile
chmod 600 /swapfile
mkswap /swapfile
swapon /swapfile
echo '/swapfile swap swap defaults 0 0' >> /etc/fstab
```

---

## Recommendation

**Short-term (tonight):**
1. Clean disk space (above commands)
2. Add swap file

**Medium-term (this week):**
1. Sign up Hetzner CX31 ($9/mo)
2. Migrate over 2-3 hours
3. Keep Hostinger as backup for 1 month

**Long-term:**
1. Use Hetzner as base
2. RunPod for GPU tasks
3. Scale as needed

---

## Quick Action for Mike

**Option A — Stay on Hostinger (quick):**
1. Run disk cleanup commands above
2. Add swap
3. Upgrade plan if needed

**Option B — Migrate to Hetzner (better):**
1. Go to hetzner.com/cloud
2. Create CX31 Ubuntu server
3. I'll handle the migration

**Your call!**
