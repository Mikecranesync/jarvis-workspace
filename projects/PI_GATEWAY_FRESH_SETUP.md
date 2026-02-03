# 🚀 Raspberry Pi 4 Gateway - Fresh Setup (30 min)

## What You Need
- Raspberry Pi 4 (2GB+ RAM)
- MicroSD card (16GB+)
- USB-C power supply
- Ethernet cable OR WiFi credentials
- Another computer to flash the SD card

---

## PHASE 1: Flash SD Card (10 min)

### On PLC Laptop or Travel Laptop:

1. **Download Raspberry Pi Imager**
   https://www.raspberrypi.com/software/

2. **Insert SD card** into laptop

3. **Open Raspberry Pi Imager**
   - Choose OS: **Raspberry Pi OS Lite (64-bit)**
   - Choose Storage: Your SD card

4. **Click the ⚙️ gear icon** (CRITICAL - enables headless setup):
   - ✅ Set hostname: `factorylm-edge`
   - ✅ Enable SSH (Use password authentication)
   - ✅ Set username: `pi`
   - ✅ Set password: `factorylm2026` (or your choice)
   - ✅ Configure WiFi (if not using Ethernet):
     - SSID: Your WiFi name
     - Password: Your WiFi password
     - Country: US
   - ✅ Set locale: America/Chicago (or your timezone)

5. **Click WRITE** and wait for completion

---

## PHASE 2: First Boot (5 min)

1. **Insert SD card** into Raspberry Pi
2. **Connect Ethernet** (recommended) OR use WiFi configured above
3. **Power on** the Pi
4. **Wait 2-3 minutes** for first boot

### Find the Pi on network:

**From PLC Laptop PowerShell:**
```powershell
ping factorylm-edge.local
```

**If that doesn't work, check router or run:**
```powershell
arp -a
```

---

## PHASE 3: SSH In & Install Tailscale (10 min)

**From PLC Laptop:**
```powershell
ssh pi@factorylm-edge.local
# Password: factorylm2026 (or what you set)
```

**Once logged in, run these commands:**
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Tailscale
curl -fsSL https://tailscale.com/install.sh | sh

# Connect to Tailscale (will give you a URL)
sudo tailscale up

# Copy the URL, open in browser, approve the device
```

---

## PHASE 4: Tell Jarvis! (1 min)

Once Tailscale shows connected, message Mike:
**"Pi is on Tailscale!"**

Jarvis will then:
1. SSH directly to the Pi
2. Install Python 3.11 + pip
3. Clone pi-gateway repo
4. Install all dependencies
5. Configure .env with your credentials
6. Set up systemd service
7. Test connection

---

## Quick Reference

| Item | Value |
|------|-------|
| Hostname | factorylm-edge |
| Username | pi |
| Password | factorylm2026 |
| SSH | `ssh pi@factorylm-edge.local` |
| Tailscale | `sudo tailscale up` |

---

## After Jarvis Finishes

You'll have:
- ✅ Pi on Tailscale (accessible from anywhere)
- ✅ pi-gateway software installed
- ✅ Web dashboard at http://factorylm-edge.local:8000
- ✅ Ready to connect to PLCs

---

*Total time: ~30 minutes (you do 15 min, Jarvis does 15 min)*
