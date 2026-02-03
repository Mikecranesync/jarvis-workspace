# Raspberry Pi Zero-Touch Deployment

## Quick Start

### 1. Flash SD Card with Raspberry Pi Imager

1. Download: https://www.raspberrypi.com/software/
2. Select:
   - Device: Raspberry Pi 4/5
   - OS: Raspberry Pi OS Lite (64-bit)
3. Click ⚙️ gear icon and configure:
   - Hostname: `factory-pi`
   - Enable SSH ✅
   - Username: `pi`
   - Password: (your choice)
   - Wi-Fi SSID & Password
   - Country: US
4. Click Write

### 2. Add Boot Files

Before ejecting, copy these to the `/boot` partition:

```
boot/
├── firstrun.sh          # Auto-setup script
├── wpa_supplicant.conf  # Wi-Fi credentials (if not set in Imager)
└── ssh                  # Empty file to enable SSH
```

### 3. Get Tailscale Auth Key

1. Go to: https://login.tailscale.com/admin/settings/keys
2. Create new key with:
   - ✅ Reusable
   - ✅ Pre-approved
   - Expiry: 90 days (or no expiry)
3. Copy key and paste into `firstrun.sh`

### 4. Edit cmdline.txt

Add to END of the single line (no newlines!):

```
systemd.run=/boot/firstrun.sh systemd.run_success_action=none
```

### 5. Boot the Pi

1. Insert SD card into Pi
2. Power on
3. Wait 3-5 minutes
4. Check Tailscale admin for new device

## Verification

- Pi appears in Tailscale admin console
- SSH via Tailscale: `ssh pi@100.x.x.x`
- SSH via ethernet: `ssh pi@192.168.5.2`
- Check logs: `cat /var/log/firstrun.log`

## Files

| File | Purpose |
|------|---------|
| `firstrun.sh` | Auto-installs Tailscale, configures network |
| `wpa_supplicant.conf.template` | Wi-Fi credentials template |

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Pi not on Tailscale | Check `/var/log/firstrun.log` |
| Wi-Fi not connecting | Verify country code & credentials |
| Script didn't run | Check cmdline.txt modification |
| Static IP not working | Check `/etc/dhcpcd.conf` |
