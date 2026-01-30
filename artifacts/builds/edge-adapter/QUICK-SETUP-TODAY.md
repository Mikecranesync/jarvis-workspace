# Quick Setup: Get Jarvis Remote Access TODAY

**Goal:** BeagleBone online with WireGuard so Jarvis can SSH in tonight

**Time needed:** ~20 minutes

---

## What You Need Right Now

- BeagleBone Black Industrial
- 5V power supply (or USB)
- Ethernet cable to your home router (for internet)
- Your laptop (for initial setup)

---

## Step 1: Power On & Connect (5 min)

```
1. Plug Ethernet cable from BeagleBone to your HOME ROUTER
   (Not the PLC network yet - just your regular internet)

2. Plug in 5V power (or Mini-USB to your laptop)

3. Wait 60-90 seconds for boot (blue LED on, USR0 blinking)
```

---

## Step 2: Find BeagleBone IP (2 min)

**Option A: Check your router**
- Log into router admin (usually 192.168.1.1)
- Look for "beaglebone" in connected devices
- Note the IP address

**Option B: From your laptop (if USB connected)**
```bash
# BeagleBone is always at this IP over USB
ssh debian@192.168.7.2
# Password: temppwd
```

**Option C: Scan network**
```bash
# From Mac/Linux terminal
ping beaglebone.local
# or
nmap -sn 192.168.1.0/24 | grep -B2 -i beagle
```

---

## Step 3: SSH In (1 min)

```bash
ssh debian@<BEAGLEBONE_IP>
# Password: temppwd

# Become root
sudo -i
```

---

## Step 4: Install WireGuard (3 min)

```bash
apt update
apt install -y wireguard wireguard-tools

# Generate keys
cd /etc/wireguard
wg genkey | tee privatekey | wg pubkey > publickey
chmod 600 privatekey

# Show your public key - SEND THIS TO JARVIS
echo "=== SEND THIS TO JARVIS ==="
cat publickey
echo "==========================="
```

**📱 Send me that public key via Telegram!**

---

## Step 5: Wait for Jarvis Config

Once you send me the public key, I will:
1. Add your BeagleBone as a WireGuard peer on the VPS
2. Send you back the config to paste

---

## Step 6: Apply WireGuard Config (2 min)

I'll send you a config. Paste it:

```bash
# I'll give you the exact command, but it will look like:
cat > /etc/wireguard/wg0.conf << 'EOF'
[Interface]
PrivateKey = <your-private-key>
Address = 10.100.0.10/24

[Peer]
PublicKey = <vps-public-key>
Endpoint = 72.60.175.144:51820
AllowedIPs = 10.100.0.0/24
PersistentKeepalive = 25
EOF
```

Then:
```bash
# Start WireGuard
systemctl enable wg-quick@wg0
systemctl start wg-quick@wg0

# Verify connection
wg show
ping 10.100.0.1
```

---

## Step 7: Enable SSH Over Tunnel (1 min)

```bash
# Make sure SSH listens on WireGuard interface
systemctl enable ssh
systemctl start ssh

# Test from BeagleBone
ssh debian@10.100.0.10
# Should connect to itself
```

---

## Step 8: Leave It Running

```
1. Make sure Ethernet is connected to router (internet)
2. Power stays on
3. That's it - go to work!
```

---

## What Jarvis Can Do Tonight

Once connected, I can:
- SSH into BeagleBone via `ssh debian@10.100.0.10`
- Install all the capture software
- Set up the stealth mode scripts
- Test everything
- Have it ready for you tomorrow

---

## Quick Checklist

```
□ BeagleBone powered on
□ Ethernet to home router (internet)
□ Found IP address
□ SSH'd in successfully
□ Installed WireGuard
□ Sent public key to Jarvis
□ Applied config from Jarvis
□ WireGuard shows "latest handshake"
□ Can ping 10.100.0.1
□ Left it running, went to work
```

---

## If Something Goes Wrong

**Can't find BeagleBone on network:**
- Try USB connection (192.168.7.2)
- Check router DHCP leases
- Make sure Ethernet LED is lit

**WireGuard won't connect:**
- Check your home router isn't blocking UDP 51820 outbound
- Verify the config I send you
- Run `journalctl -u wg-quick@wg0` for errors

**Send me a message** - I can troubleshoot via Telegram while you set it up!

---

*20 minutes and I'll have remote access to build your network ninja.*
