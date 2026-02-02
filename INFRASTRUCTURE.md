# INFRASTRUCTURE.md - Digital Quadruplet State

**Last Updated:** 2026-02-02
**Ground Truth Version:** 1.0

---

## Overview

This file documents the intended state of all machines in the Digital Quadruplet. Any drift from this document must be either:
1. Corrected to match this document, OR
2. This document updated to reflect intentional changes

---

## Machines

### 1. VPS - Hostinger (Primary)
| Property | Value |
|----------|-------|
| Hostname | srv1078052 |
| Public IP | 72.60.175.144 |
| Tailscale IP | 100.102.30.102 |
| OS | Ubuntu 24.04 LTS |
| vCPU | 1 |
| RAM | 4 GB |
| Disk | 48 GB NVMe |
| Provider | Hostinger KVM |

**Services:**
- `clawdbot.service` - Jarvis AI Gateway (port 18789)
- `plc-copilot.service` - PLC diagnostic service
- Docker containers: atlas-cmms, atlas-frontend, redis, postgres, n8n, mautic, mautic_db

**Key Paths:**
- Workspace: `/root/jarvis-workspace/`
- Clawdbot config: `/root/.clawdbot/`
- Docker data: `/var/lib/docker/`

### 2. VPS - DigitalOcean (Standby/Twin)
| Property | Value |
|----------|-------|
| Hostname | factorylm-prod |
| Public IP | 165.245.138.91 |
| Tailscale IP | 100.68.120.99 |
| OS | Ubuntu 24.04 LTS |
| vCPU | 4 |
| RAM | 8 GB |
| Disk | 160 GB NVMe |
| Region | Atlanta (nyc1) |
| Provider | DigitalOcean |

**Services:**
- `clawdbot.service` - Jarvis AI Gateway (standby)
- Docker containers: mirror of primary

**Status:** Configured as warm standby. Not actively serving traffic.

### 3. PLC Laptop
| Property | Value |
|----------|-------|
| Hostname | TBD |
| Tailscale IP | TBD |
| OS | Windows 11 |
| Purpose | PLC programming, field diagnostics |

**Status:** Pending setup

### 4. Travel Laptop (miguelomaniac)
| Property | Value |
|----------|-------|
| Hostname | miguelomaniac |
| Tailscale IP | 100.83.251.23 |
| OS | Windows |
| Purpose | Mike's mobile workstation |

**Status:** Active, intermittently online

---

## Shared Configuration

### Git Repository
- **Local:** `/root/jarvis-workspace/`
- **Remote:** `git@github.com:mikecranesync/jarvis-workspace.git` (or equivalent)
- **Branch:** `main`

### Tailscale Network
- Network: Mike's tailnet
- All machines should be members
- Used for secure inter-machine communication

### Required Software (All Machines)
- Git
- Tailscale
- Node.js 22.x (for Clawdbot)

### Required Software (VPS Only)
- Docker + Docker Compose
- Clawdbot (npm global)

---

## Sync Protocol

### Workspace Sync
```bash
# From primary to standby
rsync -avz /root/jarvis-workspace/ root@165.245.138.91:/root/jarvis-workspace/

# Clawdbot config
rsync -avz /root/.clawdbot/ root@165.245.138.91:/root/.clawdbot/
```

### Docker Volume Sync
```bash
# Stop services first, then:
rsync -avz /var/lib/docker/ root@165.245.138.91:/var/lib/docker/
```

---

## Change Log

| Date | Machine | Change | By | Evidence |
|------|---------|--------|-------|----------|
| 2026-01-30 | DigitalOcean | Initial setup: Node, Docker, Tailscale, Clawdbot | Jarvis | memory/2026-01-30.md |
| 2026-01-30 | DigitalOcean | Data migration from Hostinger | Jarvis | memory/2026-01-30.md |
| 2026-02-02 | All | Zero-Drift guardrails implemented | Jarvis | This commit |

---

## Drift Detection

Run `scripts/drift_check.sh` to compare actual state vs this document.

Expected checks:
- [ ] Hostnames match
- [ ] Services are running as documented
- [ ] Docker containers match list
- [ ] Workspace is in sync with Git
- [ ] Tailscale IPs are correct

---

*This is the source of truth. If reality differs, either fix reality or update this doc.*
