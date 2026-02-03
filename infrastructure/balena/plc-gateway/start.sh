#!/bin/bash
echo "=================================================="
echo "   FactoryLM Edge Gateway Starting"
echo "=================================================="

# Bring up eth0
ip link set eth0 up

# Run auto network detection
echo ""
echo "🔍 Running network auto-detection..."
python3 /app/network_detect.py

# Get the configured IP for PLC communication
ETH_IP=$(ip addr show eth0 | grep 'inet ' | awk '{print $2}' | cut -d/ -f1)
echo ""
echo "📍 eth0 configured: $ETH_IP"

# Only start DHCP server if we're in fallback mode (192.168.1.1)
if [ "$ETH_IP" = "192.168.1.1" ]; then
    echo "📡 Starting DHCP server..."
    dnsmasq --keep-in-foreground --log-facility=- &
    echo "✅ DHCP server running"
fi

echo ""
echo "🚀 Starting PLC Gateway..."
echo "=================================================="

# Start the Python app
exec python /app/main.py
