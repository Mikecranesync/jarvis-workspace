# Stealth Industrial Network Tap — Research

**Date:** 2026-01-29  
**Vision:** P1 - Edge Adapter (Network Ninja Mode)

---

## Goal: Complete Network Invisibility

The device must be **undetectable** to:
- Network scanners (nmap, etc.)
- IT monitoring tools
- Switch port security
- ARP tables
- DHCP logs

---

## Stealth Technique: "Ghost Mode"

### 1. No IP Address
```bash
# Bring interface UP but with NO IP
ip link set eth0 up
# Do NOT run: ip addr add ...
# Result: Interface active, but no Layer 3 identity
```

### 2. Disable ARP Completely
```bash
# Interface won't respond to ARP requests
ip link set eth0 arp off
# Or via sysctl
echo 1 > /proc/sys/net/ipv4/conf/eth0/arp_ignore
```

### 3. Disable All Broadcasts
```bash
# No DHCP, no mDNS, no NetBIOS
systemctl disable avahi-daemon
systemctl disable systemd-resolved
# Block outgoing broadcasts at firewall
iptables -A OUTPUT -d 255.255.255.255 -j DROP
```

### 4. Promiscuous Mode (Silent Listening)
```bash
# Enable promiscuous mode - sees ALL packets on segment
ip link set eth0 promisc on
# Verify
ip link show eth0 | grep PROMISC
```

### 5. Randomize MAC Address
```bash
# Change MAC on every boot
ip link set eth0 down
ip link set eth0 address $(openssl rand -hex 6 | sed 's/\(..\)/\1:/g; s/:$//')
ip link set eth0 up
```

### 6. Firewall: Drop ALL Inbound
```bash
# Accept nothing, send nothing (except WireGuard on separate interface)
iptables -P INPUT DROP
iptables -P OUTPUT DROP
iptables -A OUTPUT -o wg0 -j ACCEPT  # Only WireGuard out
```

---

## Network Visibility Comparison

| Feature | Normal Device | Stealth Tap |
|---------|---------------|-------------|
| IP Address | Yes (DHCP/Static) | **None** |
| ARP Response | Yes | **Disabled** |
| DHCP Request | Yes | **None** |
| Hostname Broadcast | Yes | **Disabled** |
| Responds to Ping | Yes | **No** |
| Visible on Switch | MAC in table | **Minimal** |
| Sends Any Packets | Yes | **Zero** (capture only) |

---

## Packet Capture Stack

### Layer 1: libpcap/tcpdump
```bash
# Capture all traffic on eth0
tcpdump -i eth0 -w capture.pcap -U
```

### Layer 2: Scapy (Python)
```python
from scapy.all import *
import scapy.contrib.modbus as mb

def process_packet(pkt):
    if TCP in pkt and (pkt[TCP].sport == 502 or pkt[TCP].dport == 502):
        # It's Modbus TCP
        modbus = mb.ModbusADURequest(bytes(pkt[TCP].payload))
        print(f"Modbus: {modbus.funcCode}")

# Sniff in promiscuous mode
sniff(iface="eth0", prn=process_packet, store=0)
```

### Layer 3: Protocol Decoders

**Modbus TCP (Port 502):**
```python
# Scapy has built-in Modbus support
import scapy.contrib.modbus as mb

# Decode captured packet
modbus_pkt = mb.ModbusADUResponse(raw_data)
print(modbus_pkt.funcCode)  # 3 = Read Holding Registers
print(modbus_pkt.registerVal)  # Actual values
```

**OPC UA (Port 4840):**
```python
# Use opcua-asyncio for decoding
# Or parse raw with struct
```

**EtherNet/IP (Port 44818):**
```python
# cpppo library has EtherNet/IP support
# Or use Scapy contrib layer
```

---

## Dual-NIC Architecture (Recommended)

```
┌─────────────────────────────────────────────────────┐
│              BeagleBone Black                       │
│                                                     │
│  eth0 (Stealth)          USB-Ethernet (WireGuard)  │
│  ├── No IP               ├── Has IP (private)      │
│  ├── No ARP              ├── WireGuard tunnel      │
│  ├── Promisc mode        └── Connects to VPS       │
│  └── Capture only                                  │
│                                                     │
└─────────────────────────────────────────────────────┘
        │                           │
        │                           │
   [PLC Network]              [Internet/4G]
   (invisible)                (encrypted)
```

**Why two NICs:**
- eth0 = 100% stealth, zero packets out
- USB-Ethernet = WireGuard tunnel to your backend
- Complete isolation between sniff and transmit

---

## BeagleBone Setup Script

```bash
#!/bin/bash
# ghost-mode.sh - Make BeagleBone invisible on PLC network

IFACE="eth0"

# 1. Bring down interface
ip link set $IFACE down

# 2. Randomize MAC
NEW_MAC=$(openssl rand -hex 6 | sed 's/\(..\)/\1:/g; s/:$//')
ip link set $IFACE address $NEW_MAC

# 3. Bring up WITHOUT IP
ip link set $IFACE up

# 4. Enable promiscuous mode
ip link set $IFACE promisc on

# 5. Disable ARP
ip link set $IFACE arp off

# 6. Firewall - drop everything on this interface
iptables -A INPUT -i $IFACE -j DROP
iptables -A OUTPUT -o $IFACE -j DROP

echo "Ghost mode active on $IFACE (MAC: $NEW_MAC)"
```

---

## Detection Risks & Mitigations

| Risk | Mitigation |
|------|------------|
| MAC appears in switch CAM table | Randomize MAC, minimal traffic |
| Port security violation | Use unmanaged switch section |
| Traffic analysis | We send zero packets |
| Physical inspection | Small enclosure, label as "diagnostic" |
| Promiscuous mode detection | Only detectable if they scan our device (they can't) |

---

## Libraries to Install

```bash
# On BeagleBone (Debian)
apt install tcpdump python3-scapy wireguard-tools

# Python packages
pip install scapy pymodbus opcua-asyncio paho-mqtt
```

---

## Test Plan

1. **Lab test:** BeagleBone + Factory IO + Wireshark on laptop
2. **Verify stealth:** Run nmap against BeagleBone from another machine
3. **Capture Modbus:** Decode register values from Factory IO traffic
4. **Forward data:** Send decoded values through WireGuard to Telegram

---

*Network Ninja Mode: See everything, be nothing.*
