#!/bin/bash
# Deploy ShopTalk Edge AI to BeagleBone
# Run this after install.sh has set up the base system

set -e

echo "========================================"
echo "  ShopTalk Edge AI Deployment"
echo "========================================"
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

log_info() { echo -e "${GREEN}[INFO]${NC} $1"; }
log_warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    echo "Please run as root"
    exit 1
fi

# Create directories
log_info "Creating directories..."
mkdir -p /opt/factorylm/shoptalk
mkdir -p /opt/factorylm/models
mkdir -p /opt/factorylm/data

# Install Python dependencies
log_info "Installing Python dependencies..."
pip3 install --break-system-packages numpy pymodbus fastapi uvicorn pyyaml

# Copy ShopTalk code
log_info "Copying ShopTalk code..."
# This would be rsync from VPS or git clone
# For now, assume code is in /tmp/shoptalk
if [ -d "/tmp/shoptalk" ]; then
    cp -r /tmp/shoptalk/* /opt/factorylm/shoptalk/
else
    log_warn "ShopTalk source not found in /tmp/shoptalk"
    log_warn "Please copy manually or use: rsync from VPS"
fi

# Create systemd service
log_info "Creating systemd service..."
cat > /etc/systemd/system/shoptalk.service << 'EOF'
[Unit]
Description=ShopTalk Edge AI
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/opt/factorylm/shoptalk
ExecStart=/usr/bin/python3 /opt/factorylm/shoptalk/main.py --api --host 0.0.0.0 --port 8080 --language es
Restart=always
RestartSec=10
Environment=PYTHONPATH=/opt/factorylm/shoptalk/src

[Install]
WantedBy=multi-user.target
EOF

# Create integration with gateway
log_info "Creating gateway integration..."
cat > /opt/factorylm/run_edge.py << 'EOF'
#!/usr/bin/env python3
"""
FactoryLM Edge Runner
Runs ShopTalk AI with protocol gateway integration
"""

import asyncio
import sys
sys.path.insert(0, '/opt/factorylm/shoptalk/src')

from model.world_model import create_conveyor_model
from inference.engine import InferenceEngine
from voice.tts import VoiceInterface, DiagnosticAnnouncer

# Try to import gateway
try:
    sys.path.insert(0, '/opt/factorylm/gateway')
    from beaglebone_gateway.src.core.gateway import Gateway
    GATEWAY_AVAILABLE = True
except ImportError:
    GATEWAY_AVAILABLE = False
    print("Gateway not available, using simulation mode")


async def main():
    # Create model
    model = create_conveyor_model()
    
    # Create voice
    voice = VoiceInterface(language="es")
    announcer = DiagnosticAnnouncer(voice, cooldown=30)
    
    # Create engine
    engine = InferenceEngine(model, sample_interval=0.1)
    
    # Setup data source
    if GATEWAY_AVAILABLE:
        # Use gateway tag database
        gateway = Gateway("/opt/factorylm/config/gateway.yaml")
        # TODO: Create data source from gateway.tag_db
        pass
    else:
        # Use simulation
        from inference.engine import SimulatedDataSource
        source = SimulatedDataSource("normal")
        engine.set_data_source(source)
    
    # Train
    print("Training model...")
    training_data = []
    for i in range(100):
        data = source()
        from model.world_model import EquipmentState
        state = EquipmentState(
            timestamp=float(i),
            sensors={k: v for k, v in data.items() if isinstance(v, (int, float))},
            controls={},
            discrete={k: v for k, v in data.items() if isinstance(v, bool)}
        )
        training_data.append(state)
    model.train(training_data)
    print("Training complete")
    
    # Announce ready
    voice.speak("Sistema ShopTalk listo")
    
    # Run
    def on_anomaly(result):
        print(f"Anomaly: {result.diagnosis}")
        announcer.announce(result.diagnosis, result.anomalies)
    
    engine.set_on_anomaly(on_anomaly)
    
    await engine.run_async()


if __name__ == "__main__":
    asyncio.run(main())
EOF

chmod +x /opt/factorylm/run_edge.py

# Enable services
log_info "Enabling services..."
systemctl daemon-reload
systemctl enable shoptalk

echo ""
echo "========================================"
echo "  Deployment Complete!"
echo "========================================"
echo ""
log_info "ShopTalk installed to /opt/factorylm/shoptalk"
log_info "Service: shoptalk (enabled, not started)"
echo ""
echo "To start: systemctl start shoptalk"
echo "To test:  python3 /opt/factorylm/shoptalk/demo.py --test"
echo ""
