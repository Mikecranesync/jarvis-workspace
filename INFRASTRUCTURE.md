# INFRASTRUCTURE.md - Network & Connections Map

*Ground truth for all infrastructure. Update this when things change.*

---

## 🌐 DOMAINS

| Domain | Registrar | DNS Provider | Points To | Status |
|--------|-----------|--------------|-----------|--------|
| factorylm.com | Namecheap | Namecheap | 165.245.138.91 | ✅ Active |
| plane.factorylm.com | Namecheap | Namecheap | 165.245.138.91 | ✅ Active (added 2026-02-02 11:19 UTC) |
| remoteme.factorylm.com | Namecheap | Namecheap | (NOT SET UP) | ❌ Needs DNS |

**Namecheap Login:** ✅ Mike has access (recovered 2026-02-02)

---

## 🖥️ SERVERS

### VPS: factorylm-prod
- **Provider:** DigitalOcean
- **Location:** Atlanta
- **IP (v4):** 165.245.138.91
- **IP (v6):** 2604:a880:5:1::1c73:d000
- **RAM:** 8GB
- **Disk:** 160GB (18% used)
- **Firewall:** UFW + DigitalOcean Cloud Firewall

### Tailscale Network
| Node | Tailscale IP | Status |
|------|--------------|--------|
| VPS (factorylm-prod) | 100.68.120.99 | ✅ |
| PLC Laptop | 100.72.2.99 | ⏳ Needs Jarvis Node |
| Travel Laptop | 100.83.251.23 | ⏳ Needs Jarvis Node |

---

## 🔥 FIREWALL RULES

### UFW (on VPS)
| Port | Service | Status |
|------|---------|--------|
| 22 | SSH | ✅ Open |
| 80 | HTTP/Nginx | ✅ Open |
| 443 | HTTPS | ✅ Open |
| 8070 | Plane | ✅ Open (UFW) |
| 8100 | RemoteMe | Internal only |

### DigitalOcean Cloud Firewall
- **Status:** UNKNOWN - may be blocking 8070
- **Action needed:** Check DO dashboard

---

## 🔌 SERVICES & PORTS

| Port | Service | Access |
|------|---------|--------|
| 80 | Nginx | Public |
| 443 | Nginx SSL | Public |
| 3002 | Grafana | Internal |
| 5432 | PostgreSQL | Internal |
| 5555 | Flower | Internal |
| 6379 | Redis | Internal |
| 8070 | Plane | Blocked externally |
| 8080 | CMMS | Internal |
| 8100 | RemoteMe | Internal |

---

## 🔗 NGINX ROUTING

| Domain/Path | Proxies To | Config File |
|-------------|-----------|-------------|
| factorylm.com | /var/www/html | factorylm-landing |
| plane.factorylm.com | localhost:8070 | plane |
| remoteme.factorylm.com | localhost:8100 | remoteme |

---

## 🔑 ACCOUNTS & ACCESS

| Service | Account | Status |
|---------|---------|--------|
| Namecheap | ? | ❌ Locked out |
| DigitalOcean | ? | ? |
| Cloudflare | ? | ? |
| GitHub | mikecranesync | ✅ |
| Trello | ? | ✅ |
| Stripe | ? | ? |
| LangFuse | ? | ✅ Configured |

---

## ❓ UNKNOWN / NEEDS INFO

1. **Namecheap login** - Mike needs to recover
2. **DigitalOcean firewall** - Is cloud firewall enabled? Rules?
3. **DNS provider** - Is it Namecheap DNS or Cloudflare?
4. **SSL certificates** - Using Let's Encrypt? Certbot?

---

## 📝 TO UPDATE

When Mike provides info, update this file:
- [ ] Namecheap account recovery
- [ ] DO firewall status
- [ ] DNS provider confirmation
- [ ] All account logins

---

*Last updated: 2026-02-02 10:35 UTC*
