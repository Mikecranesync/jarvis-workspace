#!/bin/bash
# ShopTalk Edge Installer
# Run as root on target device

set -e

echo "=========================================="
echo "ShopTalk Edge Installer"
echo "=========================================="

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    echo "Please run as root (sudo ./install.sh)"
    exit 1
fi

# Detect architecture
ARCH=$(uname -m)
echo "Detected architecture: $ARCH"

# Install dependencies
echo ""
echo "Installing system dependencies..."
apt-get update
apt-get install -y python3 python3-pip python3-venv curl

# Install Ollama
echo ""
echo "Installing Ollama..."
if ! command -v ollama &> /dev/null; then
    curl -fsSL https://ollama.com/install.sh | sh
else
    echo "Ollama already installed"
fi

# Create user and directories
echo ""
echo "Setting up ShopTalk user and directories..."
useradd -r -s /bin/false shoptalk 2>/dev/null || true
mkdir -p /opt/shoptalk/{data,logs}

# Copy application files
echo ""
echo "Installing ShopTalk..."
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cp -r "$SCRIPT_DIR/../"* /opt/shoptalk/
chown -R shoptalk:shoptalk /opt/shoptalk

# Create virtual environment
echo ""
echo "Setting up Python environment..."
cd /opt/shoptalk
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements-edge.txt

# Install systemd service
echo ""
echo "Installing systemd service..."
cp /opt/shoptalk/deploy/shoptalk.service /etc/systemd/system/
systemctl daemon-reload
systemctl enable shoptalk

# Pull LLM model
echo ""
echo "Pulling LLM model (this may take a few minutes)..."
ollama pull qwen2:0.5b

# Start service
echo ""
echo "Starting ShopTalk..."
systemctl start shoptalk

# Show status
echo ""
echo "=========================================="
echo "Installation complete!"
echo "=========================================="
echo ""
echo "ShopTalk is now running on port 8000"
echo ""
echo "Commands:"
echo "  systemctl status shoptalk    - Check status"
echo "  systemctl restart shoptalk   - Restart"
echo "  journalctl -u shoptalk -f    - View logs"
echo ""
echo "API: http://localhost:8000"
echo "Health: http://localhost:8000/health"
echo ""
