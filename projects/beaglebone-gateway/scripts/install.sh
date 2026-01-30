#!/bin/bash
#
# Industrial Gateway Installation Script for BeagleBone
# Run this on a fresh Debian installation
#
# Usage: sudo ./install.sh
#

set -e

echo "============================================"
echo "  Industrial Gateway Installer"
echo "  FactoryLM - Sub-$500 Industrial Gateway"
echo "============================================"
echo ""

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    echo "Please run as root: sudo ./install.sh"
    exit 1
fi

# Detect architecture
ARCH=$(uname -m)
echo "Detected architecture: $ARCH"

# Update system
echo ""
echo "[1/7] Updating system packages..."
apt update && apt upgrade -y

# Install system dependencies
echo ""
echo "[2/7] Installing system dependencies..."
apt install -y \
    python3 \
    python3-pip \
    python3-venv \
    python3-dev \
    build-essential \
    git \
    hostapd \
    dnsmasq \
    iptables \
    libusb-1.0-0-dev \
    libudev-dev

# Create virtual environment
echo ""
echo "[3/7] Creating Python virtual environment..."
INSTALL_DIR="/opt/industrial-gateway"
mkdir -p $INSTALL_DIR
cd $INSTALL_DIR

python3 -m venv venv
source venv/bin/activate

# Install Python packages
echo ""
echo "[4/7] Installing Python packages..."
pip install --upgrade pip

# Core packages
pip install \
    pyyaml \
    quart \
    hypercorn \
    aiohttp

# Protocol libraries
echo "Installing Modbus library..."
pip install pymodbus

echo "Installing Allen-Bradley library..."
pip install pycomm3

echo "Installing Mitsubishi library..."
pip install pymcprotocol

echo "Installing OPC UA library..."
pip install asyncua

# Snap7 for Siemens (requires compilation)
echo ""
echo "[5/7] Installing Snap7 (Siemens S7 protocol)..."
cd /tmp
if [ ! -d "snap7" ]; then
    git clone https://github.com/gijzelaerr/snap7.git
fi
cd snap7/build/unix

# Detect ARM version and compile
if [[ "$ARCH" == "armv7"* ]] || [[ "$ARCH" == "armhf" ]]; then
    make -f arm_v7_linux.mk clean
    make -f arm_v7_linux.mk
    make -f arm_v7_linux.mk install
elif [[ "$ARCH" == "aarch64" ]] || [[ "$ARCH" == "arm64" ]]; then
    make -f arm_v8_linux.mk clean
    make -f arm_v8_linux.mk
    make -f arm_v8_linux.mk install
else
    make -f x86_64_linux.mk clean
    make -f x86_64_linux.mk
    make -f x86_64_linux.mk install
fi

ldconfig

# Install python-snap7
source $INSTALL_DIR/venv/bin/activate
pip install python-snap7

# Copy application files
echo ""
echo "[6/7] Installing gateway application..."
cd $INSTALL_DIR

# Create directory structure
mkdir -p src/adapters src/core src/web config logs

# Copy files (assumes running from the project directory)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

if [ -d "$PROJECT_DIR/src" ]; then
    cp -r "$PROJECT_DIR/src/"* $INSTALL_DIR/src/
    cp -r "$PROJECT_DIR/config/"* $INSTALL_DIR/config/
    echo "Application files copied"
else
    echo "Warning: Source files not found at $PROJECT_DIR/src"
    echo "Please manually copy src/ and config/ to $INSTALL_DIR/"
fi

# Create systemd service
echo ""
echo "[7/7] Creating systemd service..."
cat > /etc/systemd/system/industrial-gateway.service << EOF
[Unit]
Description=Industrial Protocol Gateway
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/opt/industrial-gateway
ExecStart=/opt/industrial-gateway/venv/bin/python -m src.core.gateway -c config/gateway.yaml
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable industrial-gateway

echo ""
echo "============================================"
echo "  Installation Complete!"
echo "============================================"
echo ""
echo "Next steps:"
echo "1. Edit configuration: nano $INSTALL_DIR/config/gateway.yaml"
echo "2. Start the service: systemctl start industrial-gateway"
echo "3. Check status: systemctl status industrial-gateway"
echo "4. View logs: journalctl -u industrial-gateway -f"
echo ""
echo "Web interface will be available at: http://$(hostname -I | awk '{print $1}'):8080"
echo "OPC UA endpoint: opc.tcp://$(hostname -I | awk '{print $1}'):4840"
echo ""
