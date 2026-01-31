#!/bin/bash
# FactoryLM Signup API Deployment Script

set -e

echo "🏭 Deploying FactoryLM Signup API..."

# Create directories
echo "Creating directories..."
sudo mkdir -p /opt/factorylm/api
sudo mkdir -p /opt/factorylm/data

# Copy application files
echo "Copying application files..."
sudo cp main.py /opt/factorylm/api/
sudo cp requirements.txt /opt/factorylm/api/

# Set permissions
echo "Setting permissions..."
sudo chown -R www-data:www-data /opt/factorylm/
sudo chmod 755 /opt/factorylm/api/
sudo chmod 644 /opt/factorylm/api/main.py
sudo chmod 644 /opt/factorylm/api/requirements.txt
sudo chmod 755 /opt/factorylm/data/

# Install Python dependencies
echo "Installing Python dependencies..."
sudo -u www-data python3 -m pip install --user -r /opt/factorylm/api/requirements.txt

# Install systemd service
echo "Installing systemd service..."
sudo cp factorylm-api.service /etc/systemd/system/
sudo systemctl daemon-reload

# Enable and start service
echo "Starting FactoryLM API service..."
sudo systemctl enable factorylm-api
sudo systemctl start factorylm-api

# Check status
echo "Checking service status..."
sudo systemctl status factorylm-api --no-pager

echo "✅ FactoryLM Signup API deployed successfully!"
echo ""
echo "Service commands:"
echo "  sudo systemctl start factorylm-api"
echo "  sudo systemctl stop factorylm-api"
echo "  sudo systemctl restart factorylm-api"
echo "  sudo systemctl status factorylm-api"
echo "  sudo journalctl -u factorylm-api -f"
echo ""
echo "API will be available at: http://127.0.0.1:8090"
echo "Health check: http://127.0.0.1:8090/health"
echo "API docs: http://127.0.0.1:8090/docs"