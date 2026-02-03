#!/bin/bash
# Micro820 Network Scanner
# Handles DHCP default, checks both protocols

set -e

PI_IP="100.97.210.121"

echo "═══════════════════════════════════════════════════"
echo "  MICRO820 NETWORK SCANNER"
echo "═══════════════════════════════════════════════════"
echo ""

# Get Pi's eth0 IP
echo "📡 Checking Pi eth0..."
ETH_INFO=$(ssh -o ConnectTimeout=5 root@$PI_IP "ip addr show eth0 | grep 'inet '" 2>/dev/null)

if [ -z "$ETH_INFO" ]; then
    echo "❌ Pi eth0 has no IP"
    echo ""
    echo "This means either:"
    echo "  1. No Ethernet cable connected"
    echo "  2. PLC is not powered on"
    echo "  3. PLC has no IP (DHCP with no server)"
    echo ""
    echo "💡 TIP: Micro820 defaults to DHCP!"
    echo "   Set a static IP via CCW or BOOTP first."
    exit 1
fi

ETH_IP=$(echo "$ETH_INFO" | awk '{print $2}' | cut -d'/' -f1)
SUBNET=$(echo $ETH_IP | cut -d'.' -f1-3)

echo "✅ Pi eth0: $ETH_IP"
echo "   Subnet: $SUBNET.0/24"
echo ""

echo "🔍 Scanning for PLC..."
echo "─────────────────────────────────────────────────"

# Scan common PLC addresses
FOUND=""
for i in 10 1 2 20 100 50 254; do
    IP="$SUBNET.$i"
    if ssh -o ConnectTimeout=2 root@$PI_IP "ping -c 1 -W 1 $IP" > /dev/null 2>&1; then
        echo "✅ $IP responds"
        FOUND="$FOUND $IP"
    fi
done

if [ -z "$FOUND" ]; then
    echo "❌ No devices found on subnet"
    echo ""
    echo "💡 Micro820 may be in DHCP mode with no IP."
    echo "   Use Rockwell BOOTP/DHCP Server or CCW to assign IP."
    exit 1
fi

echo ""
echo "🔌 Checking protocols on found devices..."
echo "─────────────────────────────────────────────────"

for IP in $FOUND; do
    echo ""
    echo "Device: $IP"
    
    # Check Modbus TCP (502)
    if ssh -o ConnectTimeout=2 root@$PI_IP "timeout 2 bash -c 'echo > /dev/tcp/$IP/502'" 2>/dev/null; then
        echo "  ✅ Port 502 (Modbus TCP) - OPEN"
        echo "     → Primary protocol for Micro820"
    else
        echo "  ❌ Port 502 (Modbus TCP) - closed"
    fi
    
    # Check EtherNet/IP (44818)
    if ssh -o ConnectTimeout=2 root@$PI_IP "timeout 2 bash -c 'echo > /dev/tcp/$IP/44818'" 2>/dev/null; then
        echo "  ✅ Port 44818 (EtherNet/IP) - OPEN"
        echo "     ⚠️  pycomm3 Micro820 support is partial"
    else
        echo "  ⚠️  Port 44818 (EtherNet/IP) - closed"
    fi
    
    # Check HTTP (80) - some PLCs have web interface
    if ssh -o ConnectTimeout=2 root@$PI_IP "timeout 2 bash -c 'echo > /dev/tcp/$IP/80'" 2>/dev/null; then
        echo "  ℹ️  Port 80 (HTTP) - OPEN (web interface?)"
    fi
done

echo ""
echo "═══════════════════════════════════════════════════"
echo "  SCAN COMPLETE"
echo "═══════════════════════════════════════════════════"
