#!/bin/bash
echo "=== FactoryLM Edge Starting ==="

# Configure ethernet interface
ip addr add 192.168.1.1/24 dev eth0 2>/dev/null || true
ip link set eth0 up

echo "✅ Ethernet configured: 192.168.1.1/24"

# Start DHCP server
echo "Starting DHCP server..."
dnsmasq --keep-in-foreground --log-facility=- &
DNSMASQ_PID=$!
echo "✅ DHCP server running (PID: $DNSMASQ_PID)"

# Start the Python app
echo "Starting PLC Gateway..."
exec python /app/main.py
