# FactoryLM Network Credentials
## Tailscale Network Nodes

### VPS (JarvisVPS / Brain)
- **Hostname:** srv1078052
- **Tailscale IP:** 100.102.30.102
- **SSH User:** root
- **SSH Command:** `ssh root@100.102.30.102`

### DigitalOcean VPS (Standby)
- **Hostname:** factorylm-prod
- **Tailscale IP:** 100.68.120.99
- **SSH User:** root
- **SSH Command:** `ssh root@100.68.120.99`

### Travel Laptop (miguelomaniac)
- **Hostname:** Miguelomaniac
- **Tailscale IP:** 100.83.251.23
- **SSH User:** hharp
- **SSH Command:** `ssh hharp@100.83.251.23`

### PLC Laptop
- **Hostname:** laptop-0ka3c70h
- **Tailscale IP:** 100.72.2.99
- **SSH User:** TBD
- **Status:** Pending SSH setup

---

## Quick Connection Commands

From any node to VPS:
```bash
ssh root@100.102.30.102
```

From VPS to Travel Laptop:
```bash
ssh hharp@100.83.251.23
```

From VPS to PLC Laptop (once configured):
```bash
ssh [user]@100.72.2.99
```

---

## SSH Key Location
VPS public key (add to authorized_keys on nodes):
```
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIOY0hljziGSbgrv8E/wmCXovYypHw1IKWX5XYyw/hqvY root@srv1078052
```

---
Generated: $(date)
