#!/bin/bash
# BeagleBone Edge Gateway Installation Script
# Run as root on a fresh Debian BeagleBone

set -e

echo "========================================"
echo "  BeagleBone Edge Gateway Installer"
echo "  FactoryLM Industrial AI Platform"
echo "========================================"
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

log_info() { echo -e "${GREEN}[INFO]${NC} $1"; }
log_warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    log_error "Please run as root (sudo ./install.sh)"
    exit 1
fi

# Update system
log_info "Updating system packages..."
apt update && apt upgrade -y

# Install essential packages
log_info "Installing essential packages..."
apt install -y \
    python3 \
    python3-pip \
    python3-venv \
    git \
    curl \
    wget \
    wireguard \
    htop \
    vim \
    screen \
    net-tools

# Install Python packages
log_info "Installing Python packages..."
pip3 install --break-system-packages \
    pymodbus \
    python-snap7 \
    asyncua \
    fastapi \
    uvicorn \
    pyyaml \
    python-dotenv \
    requests

# Create project directory
log_info "Setting up project directory..."
mkdir -p /opt/factorylm
cd /opt/factorylm

# Copy WireGuard config if provided
if [ -f "/tmp/wg0.conf" ]; then
    log_info "Setting up WireGuard..."
    cp /tmp/wg0.conf /etc/wireguard/wg0.conf
    chmod 600 /etc/wireguard/wg0.conf
    systemctl enable wg-quick@wg0
    systemctl start wg-quick@wg0
    log_info "WireGuard started. VPN IP: $(ip addr show wg0 | grep inet | awk '{print $2}')"
else
    log_warn "No WireGuard config found at /tmp/wg0.conf"
    log_warn "Copy the config manually and run: systemctl start wg-quick@wg0"
fi

# Set hostname
log_info "Setting hostname..."
hostnamectl set-hostname factorylm-edge-01

# Create gateway service
log_info "Creating systemd service..."
cat > /etc/systemd/system/factorylm-gateway.service << 'EOF'
[Unit]
Description=FactoryLM Edge Gateway
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/opt/factorylm
ExecStart=/usr/bin/python3 /opt/factorylm/gateway.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Create placeholder gateway script
cat > /opt/factorylm/gateway.py << 'EOF'
#!/usr/bin/env python3
"""
FactoryLM Edge Gateway - Placeholder
This will be replaced with the full gateway code
"""
import time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("FactoryLM")

logger.info("FactoryLM Edge Gateway Starting...")
logger.info("Waiting for configuration...")

while True:
    time.sleep(60)
    logger.info("Gateway running. Awaiting world model deployment.")
EOF

# Enable service but don't start yet
systemctl daemon-reload
systemctl enable factorylm-gateway

# Print summary
echo ""
echo "========================================"
echo "  Installation Complete!"
echo "========================================"
echo ""
log_info "Hostname: factorylm-edge-01"
log_info "Project directory: /opt/factorylm"
log_info "Service: factorylm-gateway (enabled, not started)"
echo ""

# Check WireGuard status
if systemctl is-active --quiet wg-quick@wg0; then
    log_info "WireGuard: ACTIVE"
    wg show wg0
else
    log_warn "WireGuard: NOT ACTIVE (configure manually)"
fi

echo ""
log_info "Next steps:"
echo "  1. Configure WireGuard if not done"
echo "  2. Test VPN connection to VPS"
echo "  3. Deploy world model"
echo "  4. Start gateway: systemctl start factorylm-gateway"
echo ""
echo "For remote access, Jarvis can SSH to: 10.100.0.10"
echo ""
