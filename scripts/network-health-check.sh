#!/bin/bash
# FactoryLM Network Health Check with Telegram Alerts
# Run via cron every 5-15 minutes

LOG_FILE="/root/jarvis-workspace/memory/network-health.log"
ALERT_FILE="/root/jarvis-workspace/signals/alerts/network-down.txt"
STATE_FILE="/root/jarvis-workspace/signals/network-state.json"
ALERT_SCRIPT="/root/jarvis-workspace/scripts/telegram-alert.sh"

mkdir -p /root/jarvis-workspace/memory
mkdir -p /root/jarvis-workspace/signals/alerts

TIMESTAMP=$(date -u +"%Y-%m-%d %H:%M:%S UTC")

echo "=== Network Health Check: $TIMESTAMP ===" >> "$LOG_FILE"

# Devices to monitor
declare -A DEVICES=(
    ["Pi-Edge"]="100.97.210.121"
    ["PLC-Laptop"]="100.72.2.99"
    ["Travel-Laptop"]="100.83.251.23"
)

# Load previous state (which devices were already reported as down)
if [ -f "$STATE_FILE" ]; then
    PREV_STATE=$(cat "$STATE_FILE")
else
    PREV_STATE="{}"
fi

ALL_OK=true
NEWLY_DOWN=""
RECOVERED=""
CURRENT_DOWN=""

for NAME in "${!DEVICES[@]}"; do
    IP="${DEVICES[$NAME]}"
    WAS_DOWN=$(echo "$PREV_STATE" | python3 -c "import sys,json; d=json.load(sys.stdin); print('yes' if d.get('$NAME') else 'no')" 2>/dev/null || echo "no")
    
    if ping -c 2 -W 3 "$IP" > /dev/null 2>&1; then
        echo "  ✅ $NAME ($IP): ONLINE" >> "$LOG_FILE"
        
        # Check if it just recovered
        if [ "$WAS_DOWN" = "yes" ]; then
            RECOVERED="$RECOVERED\n✅ $NAME ($IP) is back ONLINE"
        fi
    else
        echo "  ❌ $NAME ($IP): OFFLINE" >> "$LOG_FILE"
        ALL_OK=false
        CURRENT_DOWN="$CURRENT_DOWN \"$NAME\": true,"
        
        # Only alert if newly down (not already reported)
        if [ "$WAS_DOWN" = "no" ]; then
            NEWLY_DOWN="$NEWLY_DOWN\n🚨 $NAME ($IP) just went OFFLINE"
            echo "[$TIMESTAMP] $NAME ($IP) is OFFLINE" >> "$ALERT_FILE"
        fi
    fi
done

# Build new state JSON
if [ -z "$CURRENT_DOWN" ]; then
    NEW_STATE="{}"
else
    # Remove trailing comma and wrap
    CURRENT_DOWN=$(echo "$CURRENT_DOWN" | sed 's/,$//')
    NEW_STATE="{$CURRENT_DOWN}"
fi
echo "$NEW_STATE" > "$STATE_FILE"

# Send Telegram alert if anything changed
if [ -n "$NEWLY_DOWN" ]; then
    ALERT_MSG="🔴 <b>Network Alert</b>$NEWLY_DOWN"
    bash "$ALERT_SCRIPT" "$ALERT_MSG"
    echo "  📤 Telegram alert sent for newly offline devices" >> "$LOG_FILE"
fi

if [ -n "$RECOVERED" ]; then
    RECOVERY_MSG="🟢 <b>Network Recovery</b>$RECOVERED"
    bash "$ALERT_SCRIPT" "$RECOVERY_MSG"
    echo "  📤 Telegram recovery notice sent" >> "$LOG_FILE"
fi

if $ALL_OK; then
    echo "  🟢 All devices healthy" >> "$LOG_FILE"
    # Clear alerts file if all OK
    > "$ALERT_FILE"
fi

echo "" >> "$LOG_FILE"
