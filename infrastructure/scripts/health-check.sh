#!/bin/bash
#
# Jarvis Network Health Check
# Checks all nodes in the RemoteMe network
#

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║  🏥 Jarvis Network Health Check                              ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""
echo "Timestamp: $(date -u)"
echo ""

# Node definitions
declare -A NODES
NODES["VPS (factorylm-prod)"]="100.68.120.99"
NODES["PLC Laptop"]="100.72.2.99"
NODES["Travel Laptop"]="100.83.251.23"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
printf "%-25s %-15s %-10s %-15s\n" "NODE" "IP" "PING" "JARVIS NODE"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

for name in "${!NODES[@]}"; do
    ip="${NODES[$name]}"
    
    # Ping check
    if ping -c 1 -W 2 "$ip" &>/dev/null; then
        ping_status="${GREEN}✅ UP${NC}"
    else
        ping_status="${RED}❌ DOWN${NC}"
    fi
    
    # Jarvis Node check (port 8765)
    if curl -s --connect-timeout 2 "http://$ip:8765/health" &>/dev/null; then
        node_status="${GREEN}✅ RUNNING${NC}"
    else
        node_status="${YELLOW}⏳ NOT RUNNING${NC}"
    fi
    
    printf "%-25s %-15s %-10b %-15b\n" "$name" "$ip" "$ping_status" "$node_status"
done

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Tailscale status
echo "📡 Tailscale Status:"
tailscale status 2>/dev/null | head -10

echo ""

# VPS services
echo "🖥️  VPS Services:"
echo -n "   Clawdbot: "
systemctl is-active clawdbot 2>/dev/null || echo "unknown"

echo -n "   Docker: "
systemctl is-active docker 2>/dev/null || echo "unknown"

echo ""

# Docker containers
echo "🐳 Docker Containers:"
docker ps --format "   {{.Names}}: {{.Status}}" 2>/dev/null | head -10

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Health check complete."
