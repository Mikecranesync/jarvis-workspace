#!/bin/bash
# FactoryLM Edge - Raspberry Pi Auto-Setup
# Run this when Pi is detected on network

PI_IP="${1:-factorylm-edge.local}"
PI_USER="pi"
PI_PASS="factorylm2026"

echo "🍓 FactoryLM Edge Setup Script"
echo "Target: $PI_IP"
echo ""

# Test SSH connection
echo "=== Testing SSH connection ==="
if ! sshpass -p "$PI_PASS" ssh -o StrictHostKeyChecking=no -o ConnectTimeout=10 $PI_USER@$PI_IP "hostname" 2>/dev/null; then
    echo "❌ Cannot connect to Pi at $PI_IP"
    exit 1
fi
echo "✅ SSH connection successful"

# Install Tailscale
echo ""
echo "=== Installing Tailscale ==="
sshpass -p "$PI_PASS" ssh $PI_USER@$PI_IP "curl -fsSL https://tailscale.com/install.sh | sh"

echo ""
echo "=== Starting Tailscale ==="
sshpass -p "$PI_PASS" ssh $PI_USER@$PI_IP "sudo tailscale up --authkey=YOUR_AUTH_KEY_HERE"

# Update system
echo ""
echo "=== Updating system ==="
sshpass -p "$PI_PASS" ssh $PI_USER@$PI_IP "sudo apt update && sudo apt upgrade -y"

# Install Python and dependencies
echo ""
echo "=== Installing Python dependencies ==="
sshpass -p "$PI_PASS" ssh $PI_USER@$PI_IP "sudo apt install -y python3-pip python3-venv git"

# Clone pi-gateway
echo ""
echo "=== Cloning pi-gateway ==="
sshpass -p "$PI_PASS" ssh $PI_USER@$PI_IP "cd ~ && git clone https://github.com/mikecranesync/pi-gateway.git"

# Setup virtual environment
echo ""
echo "=== Setting up Python environment ==="
sshpass -p "$PI_PASS" ssh $PI_USER@$PI_IP "cd ~/pi-gateway && python3 -m venv venv && ./venv/bin/pip install -r requirements.txt"

# Create .env file
echo ""
echo "=== Creating configuration ==="
sshpass -p "$PI_PASS" ssh $PI_USER@$PI_IP "cat > ~/pi-gateway/.env << 'ENV'
DATABASE_URL=sqlite:///./pi-gateway.db
SECRET_KEY=$(openssl rand -hex 32)
GATEWAY_ID=factorylm-edge-001
GATEWAY_NAME=FactoryLM Edge Gateway
API_HOST=0.0.0.0
API_PORT=8000
MQTT_BROKER=100.102.30.102
MQTT_PORT=1883
TELEGRAM_BOT_TOKEN=YOUR_BOT_TOKEN
TELEGRAM_CHAT_ID=8445149012
LOG_LEVEL=INFO
ENV"

# Create systemd service
echo ""
echo "=== Creating systemd service ==="
sshpass -p "$PI_PASS" ssh $PI_USER@$PI_IP "sudo tee /etc/systemd/system/pi-gateway.service << 'SERVICE'
[Unit]
Description=Pi Gateway Service
After=network.target

[Service]
Type=simple
User=pi
WorkingDirectory=/home/pi/pi-gateway
ExecStart=/home/pi/pi-gateway/venv/bin/python -m uvicorn src.api.main:app --host 0.0.0.0 --port 8000
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
SERVICE"

# Enable and start service
echo ""
echo "=== Starting pi-gateway service ==="
sshpass -p "$PI_PASS" ssh $PI_USER@$PI_IP "sudo systemctl daemon-reload && sudo systemctl enable pi-gateway && sudo systemctl start pi-gateway"

# Verify
echo ""
echo "=== Verifying installation ==="
sshpass -p "$PI_PASS" ssh $PI_USER@$PI_IP "sudo systemctl status pi-gateway"

echo ""
echo "🎉 FactoryLM Edge setup complete!"
echo "Dashboard: http://$PI_IP:8000"
