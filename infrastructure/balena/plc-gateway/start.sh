#!/bin/bash
echo "=================================================="
echo "   FactoryLM Edge Gateway v2.0.1"
echo "=================================================="

ip link set eth0 up

echo "🔍 Running network auto-detection..."
python3 /app/network_detect.py

ETH_IP=$(ip addr show eth0 | grep 'inet ' | grep -v '127.0.0' | awk '{print $2}' | head -1)
echo "📍 Detected config: $ETH_IP"

# Start keepalive as background process (not subshell)
if [ -n "$ETH_IP" ]; then
    /app/keepalive.sh "$ETH_IP" &
    KEEPALIVE_PID=$!
    echo "🔒 Keepalive PID: $KEEPALIVE_PID"
fi

# Fallback DHCP
if [ "$ETH_IP" = "192.168.1.1/24" ]; then
    dnsmasq --keep-in-foreground --log-facility=- &
fi

echo "🚀 Starting PLC Gateway..."
exec python /app/main.py
