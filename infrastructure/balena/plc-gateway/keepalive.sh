#!/bin/bash
# IP Keepalive - runs forever, maintains eth0 IP
TARGET_IP="$1"

if [ -z "$TARGET_IP" ]; then
    echo "No target IP provided"
    exit 1
fi

echo "🔒 IP Keepalive started for $TARGET_IP"

while true; do
    CURRENT=$(ip addr show eth0 2>/dev/null | grep 'inet ' | grep -v '127.0.0' | awk '{print $2}')
    
    if [ "$CURRENT" != "$TARGET_IP" ]; then
        echo "🔄 $(date): Re-applying $TARGET_IP (current: $CURRENT)"
        ip addr flush dev eth0 2>/dev/null
        ip addr add $TARGET_IP dev eth0
        ip link set eth0 up
    fi
    
    sleep 5
done
