#!/bin/bash
#
# Raspberry Pi First Boot Setup for Jarvis Node
# Run this script on first boot after flashing SD card
#
# Usage: curl -sL https://raw.githubusercontent.com/.../first-boot.sh | sudo bash
#

set -e

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║  🍓 Jarvis Node - Raspberry Pi Setup                         ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

# Update system
echo "📦 Updating system..."
apt update && apt upgrade -y

# Install dependencies
echo "📦 Installing dependencies..."
apt install -y \
    python3-pip \
    python3-venv \
    git \
    curl \
    htop \
    vim \
    libcamera-apps \
    python3-picamera2

# Install Tailscale
echo "🔗 Installing Tailscale..."
curl -fsSL https://tailscale.com/install.sh | sh

# Create Jarvis directory
echo "📁 Creating directories..."
mkdir -p /opt/jarvis-node
mkdir -p /home/pi/jarvis-workspace

# Create virtual environment
echo "🐍 Setting up Python environment..."
python3 -m venv /opt/jarvis-node/venv
source /opt/jarvis-node/venv/bin/activate

# Install Python packages
pip install --upgrade pip
pip install \
    fastapi \
    uvicorn \
    picamera2 \
    pillow \
    requests \
    psutil \
    RPi.GPIO

# Download Jarvis Node
echo "⬇️  Downloading Jarvis Node..."
cat > /opt/jarvis-node/jarvis_node_pi.py << 'PYTHON_EOF'
"""
Jarvis Node - Raspberry Pi Edition
==================================
Remote control server for Raspberry Pi
"""

import os
import io
import base64
import subprocess
from datetime import datetime
from typing import Optional

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import psutil

# Try to import Pi-specific modules
try:
    from picamera2 import Picamera2
    HAS_CAMERA = True
except ImportError:
    HAS_CAMERA = False

try:
    import RPi.GPIO as GPIO
    HAS_GPIO = True
    GPIO.setmode(GPIO.BCM)
except ImportError:
    HAS_GPIO = False

app = FastAPI(title="Jarvis Node - Raspberry Pi", version="1.0.0")

# =============================================================================
# MODELS
# =============================================================================

class ShellRequest(BaseModel):
    command: str
    timeout: int = 30

class GPIORequest(BaseModel):
    pin: int
    mode: str = "OUT"  # OUT or IN
    value: Optional[int] = None  # For OUT mode

# =============================================================================
# HEALTH & STATUS
# =============================================================================

@app.get("/")
async def root():
    return {"status": "ok", "node": "raspberry-pi", "timestamp": datetime.now().isoformat()}

@app.get("/health")
async def health():
    cpu_percent = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    
    # Get CPU temperature
    try:
        with open('/sys/class/thermal/thermal_zone0/temp', 'r') as f:
            cpu_temp = float(f.read()) / 1000
    except:
        cpu_temp = None
    
    return {
        "status": "healthy",
        "hostname": os.uname().nodename,
        "uptime": datetime.now().timestamp() - psutil.boot_time(),
        "cpu_percent": cpu_percent,
        "cpu_temp_c": cpu_temp,
        "memory_percent": memory.percent,
        "memory_available_mb": memory.available / (1024 * 1024),
        "disk_percent": disk.percent,
        "disk_free_gb": disk.free / (1024 * 1024 * 1024),
        "capabilities": {
            "camera": HAS_CAMERA,
            "gpio": HAS_GPIO
        },
        "timestamp": datetime.now().isoformat()
    }

# =============================================================================
# SHELL COMMANDS
# =============================================================================

@app.post("/shell")
async def shell(request: ShellRequest):
    try:
        result = subprocess.run(
            request.command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=request.timeout
        )
        return {
            "stdout": result.stdout,
            "stderr": result.stderr,
            "return_code": result.returncode,
            "command": request.command
        }
    except subprocess.TimeoutExpired:
        raise HTTPException(status_code=408, detail="Command timed out")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# =============================================================================
# CAMERA
# =============================================================================

@app.get("/camera/photo")
async def camera_photo(width: int = 1920, height: int = 1080):
    if not HAS_CAMERA:
        raise HTTPException(status_code=501, detail="Camera not available")
    
    try:
        picam2 = Picamera2()
        config = picam2.create_still_configuration(main={"size": (width, height)})
        picam2.configure(config)
        picam2.start()
        
        # Capture to bytes
        data = io.BytesIO()
        picam2.capture_file(data, format='jpeg')
        picam2.stop()
        picam2.close()
        
        # Encode to base64
        data.seek(0)
        image_base64 = base64.b64encode(data.read()).decode('utf-8')
        
        return {
            "image_base64": image_base64,
            "width": width,
            "height": height,
            "format": "jpeg",
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# =============================================================================
# GPIO
# =============================================================================

@app.post("/gpio")
async def gpio_control(request: GPIORequest):
    if not HAS_GPIO:
        raise HTTPException(status_code=501, detail="GPIO not available")
    
    try:
        if request.mode == "OUT":
            GPIO.setup(request.pin, GPIO.OUT)
            if request.value is not None:
                GPIO.output(request.pin, request.value)
            return {"pin": request.pin, "mode": "OUT", "value": request.value}
        
        elif request.mode == "IN":
            GPIO.setup(request.pin, GPIO.IN)
            value = GPIO.input(request.pin)
            return {"pin": request.pin, "mode": "IN", "value": value}
        
        else:
            raise HTTPException(status_code=400, detail="Mode must be OUT or IN")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/gpio/{pin}")
async def gpio_read(pin: int):
    if not HAS_GPIO:
        raise HTTPException(status_code=501, detail="GPIO not available")
    
    try:
        GPIO.setup(pin, GPIO.IN)
        value = GPIO.input(pin)
        return {"pin": pin, "value": value}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# =============================================================================
# SYSTEM INFO
# =============================================================================

@app.get("/system")
async def system_info():
    return {
        "hostname": os.uname().nodename,
        "platform": os.uname().sysname,
        "release": os.uname().release,
        "machine": os.uname().machine,
        "cpu_count": psutil.cpu_count(),
        "memory_total_mb": psutil.virtual_memory().total / (1024 * 1024),
        "disk_total_gb": psutil.disk_usage('/').total / (1024 * 1024 * 1024),
        "boot_time": datetime.fromtimestamp(psutil.boot_time()).isoformat(),
        "timestamp": datetime.now().isoformat()
    }

# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8765)
PYTHON_EOF

# Create systemd service
echo "⚙️  Creating systemd service..."
cat > /etc/systemd/system/jarvis-node.service << 'SERVICE_EOF'
[Unit]
Description=Jarvis Node - Raspberry Pi
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
User=root
WorkingDirectory=/opt/jarvis-node
ExecStart=/opt/jarvis-node/venv/bin/python jarvis_node_pi.py
Restart=always
RestartSec=10
Environment=PYTHONUNBUFFERED=1

[Install]
WantedBy=multi-user.target
SERVICE_EOF

# Enable and start service
systemctl daemon-reload
systemctl enable jarvis-node.service
systemctl start jarvis-node.service

# Add VPS SSH key
echo "🔑 Adding VPS SSH key..."
mkdir -p /root/.ssh
echo "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIOY0hljziGSbgrv8E/wmCXovYypHw1IKWX5XYyw/hqvY root@srv1078052" >> /root/.ssh/authorized_keys
chmod 700 /root/.ssh
chmod 600 /root/.ssh/authorized_keys

# Set hostname
echo "🏷️  Setting hostname..."
hostnamectl set-hostname jarvis-pi

# Final status
echo ""
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║  ✅ SETUP COMPLETE                                           ║"
echo "╠══════════════════════════════════════════════════════════════╣"
echo "║                                                              ║"
echo "║  Next steps:                                                 ║"
echo "║  1. Connect to Tailscale:                                    ║"
echo "║     sudo tailscale up                                        ║"
echo "║                                                              ║"
echo "║  2. Test Jarvis Node:                                        ║"
echo "║     curl http://localhost:8765/health                        ║"
echo "║                                                              ║"
echo "║  3. From VPS, test connection:                               ║"
echo "║     curl http://<pi-tailscale-ip>:8765/health                ║"
echo "║                                                              ║"
echo "╚══════════════════════════════════════════════════════════════╝"

# Show service status
systemctl status jarvis-node.service --no-pager
