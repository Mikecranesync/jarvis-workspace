#!/bin/bash
# FactoryLM Network Health Check
# Run via heartbeat or cron

LOG_FILE="/root/jarvis-workspace/memory/network-health.log"
ALERT_FILE="/root/jarvis-workspace/signals/alerts/network-down.txt"

mkdir -p /root/jarvis-workspace/memory
mkdir -p /root/jarvis-workspace/signals/alerts

TIMESTAMP=$(date -u +"%Y-%m-%d %H:%M:%S UTC")

echo "=== Network Health Check: $TIMESTAMP ===" >> "$LOG_FILE"

declare -A DEVICES=(
    ["Pi-Edge"]="100.97.210.121"
    ["PLC-Laptop"]="100.72.2.99"
    ["Travel-Laptop"]="100.83.251.23"
)

ALL_OK=true

for NAME in "${!DEVICES[@]}"; do
    IP="${DEVICES[$NAME]}"
    if ping -c 1 -W 3 "$IP" > /dev/null 2>&1; then
        echo "  ✅ $NAME ($IP): ONLINE" >> "$LOG_FILE"
    else
        echo "  ❌ $NAME ($IP): OFFLINE" >> "$LOG_FILE"
        ALL_OK=false
        echo "[$TIMESTAMP] $NAME ($IP) is OFFLINE" >> "$ALERT_FILE"
    fi
done

if $ALL_OK; then
    echo "  🟢 All devices healthy" >> "$LOG_FILE"
    # Clear alerts if all OK
    rm -f "$ALERT_FILE" 2>/dev/null
fi

echo "" >> "$LOG_FILE"
