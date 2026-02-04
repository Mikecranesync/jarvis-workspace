#!/bin/bash
# Plug-and-Play Experiment Monitor
# Runs every 30 seconds, logs Pi status

LOG="/root/jarvis-workspace/experiments/2026-02-03-plug-and-play-test.md"
STATE_FILE="/tmp/pi_state"

# Initialize state
if [ ! -f "$STATE_FILE" ]; then
    echo "UNKNOWN" > "$STATE_FILE"
fi

LAST_STATE=$(cat "$STATE_FILE")
TIMESTAMP=$(date -u +"%Y-%m-%d %H:%M:%S UTC")

# Ping test
if ping -c 1 -W 3 100.97.210.121 > /dev/null 2>&1; then
    CURRENT_STATE="ONLINE"
    PING_MS=$(ping -c 1 100.97.210.121 | grep -oP 'time=\K[0-9.]+')
else
    CURRENT_STATE="OFFLINE"
    PING_MS="N/A"
fi

# Log state changes
if [ "$LAST_STATE" != "$CURRENT_STATE" ]; then
    if [ "$CURRENT_STATE" == "OFFLINE" ]; then
        echo "$TIMESTAMP | PI WENT OFFLINE | Last ping: $PING_MS ms" >> "$LOG"
        echo "🔴 Pi offline detected"
    else
        echo "$TIMESTAMP | PI CAME ONLINE | Ping: $PING_MS ms" >> "$LOG"
        echo "🟢 Pi online detected"
        
        # Check DHCP leases
        sleep 5
        DHCP_LOG=$(ssh -o ConnectTimeout=10 -o StrictHostKeyChecking=no root@100.97.210.121 "cat /var/lib/misc/dnsmasq.leases 2>/dev/null" 2>/dev/null)
        if [ -n "$DHCP_LOG" ]; then
            echo "$TIMESTAMP | DHCP LEASE DETECTED | $DHCP_LOG" >> "$LOG"
        fi
        
        # Test API
        API_RESULT=$(curl -s --connect-timeout 5 http://100.97.210.121:5000/health 2>/dev/null)
        if [ -n "$API_RESULT" ]; then
            echo "$TIMESTAMP | API RESPONDING | $API_RESULT" >> "$LOG"
        fi
    fi
fi

echo "$CURRENT_STATE" > "$STATE_FILE"
