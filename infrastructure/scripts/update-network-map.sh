#!/bin/bash
#
# Update Network Map
# Automatically scans network and updates NETWORK_MAP.md
#
# Run periodically or when network changes occur
#

set -e

WORKSPACE="/root/jarvis-workspace"
NETWORK_MAP="$WORKSPACE/NETWORK_MAP.md"
TIMESTAMP=$(date -u +"%Y-%m-%d %H:%M UTC")

echo "🗺️  Updating Network Map..."

# Get Tailscale status
TAILSCALE_STATUS=$(tailscale status 2>/dev/null || echo "Tailscale not available")

# Check each node
check_node() {
    local ip=$1
    local port=$2
    local name=$3
    
    # Ping check
    if ping -c 1 -W 2 "$ip" &>/dev/null; then
        ping_ok="✅ Online"
    else
        ping_ok="❌ Offline"
    fi
    
    # Jarvis Node check
    if [ -n "$port" ]; then
        if curl -s --connect-timeout 2 "http://$ip:$port/health" &>/dev/null; then
            jarvis_ok="✅ Port $port"
        else
            jarvis_ok="❌ Not running"
        fi
    else
        jarvis_ok="N/A"
    fi
    
    echo "$name|$ip|$ping_ok|$jarvis_ok"
}

# Generate status table
VPS_STATUS=$(check_node "100.68.120.99" "" "JarvisVPS")
PLC_STATUS=$(check_node "100.72.2.99" "8765" "PLC Laptop")
TRAVEL_STATUS=$(check_node "100.83.251.23" "8765" "Travel Laptop")

# Log the update
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Network Status @ $TIMESTAMP"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "$VPS_STATUS" | tr '|' '\t'
echo "$PLC_STATUS" | tr '|' '\t'
echo "$TRAVEL_STATUS" | tr '|' '\t'
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Update timestamp in NETWORK_MAP.md
sed -i "s/Last Updated:.*/Last Updated: $TIMESTAMP/" "$NETWORK_MAP"

# Git commit if changes
cd "$WORKSPACE"
if git diff --quiet NETWORK_MAP.md; then
    echo "No changes to commit."
else
    git add NETWORK_MAP.md
    git commit -m "Auto-update network map @ $TIMESTAMP"
    echo "✅ Committed network map update"
fi

echo ""
echo "Done."
