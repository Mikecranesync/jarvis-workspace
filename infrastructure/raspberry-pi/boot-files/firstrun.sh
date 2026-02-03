#!/bin/bash
set -e

# ============================================
# FactoryLM Raspberry Pi First Run Setup
# ============================================
# This script runs once on first boot to:
# 1. Install Tailscale
# 2. Authenticate to Tailscale network
# 3. Configure static eth0 IP
# ============================================

# ⚠️ REPLACE THIS WITH YOUR TAILSCALE AUTH KEY
TAILSCALE_AUTHKEY="tskey-auth-XXXXX-XXXXXXXXXXXXXXXXX"

STATIC_ETH0_IP="192.168.5.2"
HOSTNAME_PREFIX="factory-pi"
LOG_FILE="/var/log/firstrun.log"

exec > >(tee -a "$LOG_FILE") 2>&1

echo "==========================================" 
echo "FactoryLM First Run - $(date)"
echo "==========================================" 

# Check if already completed
if [ -f /boot/firstrun_complete ]; then
    echo "First run already completed. Exiting."
    exit 0
fi

# Wait for network
echo "[1/6] Waiting for network..."
for i in {1..30}; do
    if ping -c 1 google.com &>/dev/null; then
        echo "Network available"
        break
    fi
    echo "  Waiting... ($i/30)"
    sleep 2
done

# Update system
echo "[2/6] Updating package lists..."
apt-get update

# Install Tailscale
echo "[3/6] Installing Tailscale..."
curl -fsSL https://tailscale.com/install.sh | sh

# Authenticate Tailscale
echo "[4/6] Authenticating Tailscale..."
MACHINE_ID=$(cat /etc/machine-id | cut -c1-8)
tailscale up \
    --authkey="$TAILSCALE_AUTHKEY" \
    --accept-routes \
    --ssh \
    --hostname="${HOSTNAME_PREFIX}-${MACHINE_ID}"

# Configure static IP on eth0 (for direct laptop connection)
echo "[5/6] Configuring static eth0 IP..."
cat >> /etc/dhcpcd.conf << EOF

# Static IP for direct laptop connection (FactoryLM)
interface eth0
static ip_address=${STATIC_ETH0_IP}/24
static routers=192.168.5.1
static domain_name_servers=8.8.8.8
EOF

# Finalize
echo "[6/6] Finalizing..."
TAILSCALE_IP=$(tailscale ip -4 2>/dev/null || echo "unknown")
echo "Tailscale IP: $TAILSCALE_IP"

# Mark setup complete
touch /boot/firstrun_complete
echo "TAILSCALE_IP=$TAILSCALE_IP" > /boot/setup_info.txt
echo "MACHINE_ID=$MACHINE_ID" >> /boot/setup_info.txt
echo "HOSTNAME=${HOSTNAME_PREFIX}-${MACHINE_ID}" >> /boot/setup_info.txt
echo "SETUP_DATE=$(date -Iseconds)" >> /boot/setup_info.txt

echo "==========================================" 
echo "Setup complete at $(date)"
echo "Tailscale IP: $TAILSCALE_IP"
echo "Hostname: ${HOSTNAME_PREFIX}-${MACHINE_ID}"
echo "==========================================" 

# Clean up - remove from future boots
sed -i '/firstrun.sh/d' /etc/rc.local 2>/dev/null || true

# Reboot to apply network changes
echo "Rebooting in 5 seconds..."
sleep 5
reboot
