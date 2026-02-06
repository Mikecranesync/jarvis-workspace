#!/bin/bash
set -e

# Jarvis Memory System Lite Installation Script
# Uses ChromaDB default embeddings for fast setup without PyTorch

echo "🚀 Installing Jarvis Memory System (ChromaDB Lite - No PyTorch)"
echo "=================================================================="

# Configuration
INSTALL_DIR="/root/jarvis-workspace/infrastructure/memory-system"
SERVICE_PORT="5432"
MEMORY_DIR="/root/jarvis-workspace/memory"
SERVICE_NAME="jarvis-memory-lite"

# Check if running as root
if [ "$EUID" -ne 0 ]; then 
    echo "❌ Please run as root (required for systemd service)"
    exit 1
fi

echo "📁 Working directory: $INSTALL_DIR"
cd "$INSTALL_DIR"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "🐍 Creating Python virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "📦 Upgrading pip..."
pip install --upgrade pip

# Install lightweight requirements (no PyTorch)
echo "⬇️  Installing lightweight dependencies..."
pip install -r requirements-lite.txt

# Test ChromaDB installation
echo "🔍 Testing ChromaDB installation..."
python3 -c "
import chromadb
print('Creating test ChromaDB client...')
client = chromadb.Client()
print('ChromaDB installation successful!')
print('Using default embeddings (no external model required)')
"

# Create systemd service file (using lite version)
echo "⚙️  Creating systemd service..."
cat > /etc/systemd/system/${SERVICE_NAME}.service << EOF
[Unit]
Description=Jarvis Memory System (ChromaDB Lite)
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=${INSTALL_DIR}
Environment=PATH=${INSTALL_DIR}/venv/bin:/usr/local/bin:/usr/bin:/bin
ExecStart=${INSTALL_DIR}/venv/bin/python memory_service_lite.py
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

# Resource limits (lower for lite version)
MemoryHigh=150M
MemoryMax=250M

[Install]
WantedBy=multi-user.target
EOF

# Create config file (same as before)
if [ ! -f "config.py" ]; then
    echo "📝 Creating configuration file..."
    cat > config.py << EOF
"""Configuration for Jarvis Memory System"""
import os

# Service configuration
SERVICE_HOST = "127.0.0.1"
SERVICE_PORT = ${SERVICE_PORT}

# Memory configuration
MEMORY_DIR = "${MEMORY_DIR}"
CHROMADB_DIR = "${INSTALL_DIR}/chromadb_data"
COLLECTION_NAME = "jarvis_memory"

# Model configuration (lite version uses ChromaDB defaults)
EMBEDDING_MODEL = "default"
EMBEDDING_DIM = 384

# Search configuration
DEFAULT_MAX_RESULTS = 6
DEFAULT_MIN_SCORE = 0.35
CHUNK_SIZE = 400  # tokens
CHUNK_OVERLAP = 80  # tokens

# Approximate chars per token for chunking
CHARS_PER_TOKEN = 4

# File watching
WATCH_DEBOUNCE_SECONDS = 2

# Logging
LOG_LEVEL = "INFO"
EOF
fi

# Check if memory directory exists
if [ ! -d "$MEMORY_DIR" ]; then
    echo "📁 Creating memory directory: $MEMORY_DIR"
    mkdir -p "$MEMORY_DIR"
fi

# Count memory files
MEMORY_FILES=$(find "$MEMORY_DIR" -name "*.md" -type f | wc -l)
echo "📊 Found $MEMORY_FILES memory files to index"

# Create ChromaDB data directory
mkdir -p chromadb_data

# Create cron directory and script (same as before)
mkdir -p cron

echo "⏰ Creating auto-indexing cron job..."
cat > cron/auto_index.py << 'EOF'
#!/usr/bin/env python3
"""
Auto-indexing cron job for Jarvis Memory System (Lite)
Runs every 5 minutes to index new/modified memory files
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import asyncio
from memory_service_lite import MemoryService
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def main():
    """Index any new or modified memory files"""
    try:
        service = MemoryService()
        await service.initialize()
        
        # Force re-index of all files (checks timestamps internally)
        await service.index_memory_files()
        
        logger.info("Auto-indexing completed successfully")
    except Exception as e:
        logger.error(f"Auto-indexing failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
EOF

chmod +x cron/auto_index.py

# Add cron job entry
echo "⏰ Setting up cron job for auto-indexing..."
CRON_JOB="*/5 * * * * cd ${INSTALL_DIR} && ${INSTALL_DIR}/venv/bin/python cron/auto_index.py >> /var/log/jarvis-memory-cron.log 2>&1"

# Remove any existing cron job for this service
crontab -l 2>/dev/null | grep -v "jarvis-memory-cron" | crontab -

# Add the new cron job
(crontab -l 2>/dev/null; echo "$CRON_JOB") | crontab -

echo "✅ Cron job installed: runs every 5 minutes"

# Initial indexing (if there are memory files)
if [ "$MEMORY_FILES" -gt 0 ]; then
    echo "🔄 Performing initial indexing of memory files..."
    python3 -c "
import asyncio
import sys
sys.path.append('.')
from memory_service_lite import MemoryService

async def initial_index():
    service = MemoryService()
    await service.initialize()
    await service.index_memory_files()
    print(f'Successfully indexed memory files!')

asyncio.run(initial_index())
"
else
    echo "⚠️  No memory files found to index"
fi

# Start and enable service
echo "🚀 Starting Jarvis Memory System (lite) service..."
systemctl daemon-reload
systemctl enable ${SERVICE_NAME}
systemctl start ${SERVICE_NAME}

# Wait a moment for service to start
sleep 3

# Check service status
if systemctl is-active --quiet ${SERVICE_NAME}; then
    echo "✅ Service started successfully!"
    systemctl status ${SERVICE_NAME} --no-pager -l
else
    echo "❌ Service failed to start. Checking logs..."
    systemctl status ${SERVICE_NAME} --no-pager -l
    echo "Recent logs:"
    journalctl -u ${SERVICE_NAME} --no-pager -l -n 20
    exit 1
fi

# Test the API
echo "🔍 Testing memory search API..."
python3 -c "
import requests
import time

# Wait for service to be fully ready
time.sleep(2)

try:
    response = requests.post(
        'http://127.0.0.1:${SERVICE_PORT}/search',
        json={'query': 'test', 'max_results': 1}
    )
    if response.status_code == 200:
        result = response.json()
        print(f'✅ API test successful!')
        print(f'   Results: {len(result.get(\"results\", []))}')
        print(f'   Provider: {result.get(\"provider\")}')
        print(f'   Model: {result.get(\"model\")}')
    else:
        print(f'❌ API test failed: {response.status_code} - {response.text}')
except Exception as e:
    print(f'❌ API test error: {e}')
"

echo ""
echo "🎉 Installation Complete (Lite Version)!"
echo "========================================"
echo "✅ ChromaDB with default embeddings installed"
echo "✅ Memory service running on http://127.0.0.1:${SERVICE_PORT}"
echo "✅ Auto-indexing cron job configured (every 5 minutes)"
echo "✅ $MEMORY_FILES memory files indexed"
echo ""
echo "📋 Lite Version Features:"
echo "   • No external model dependencies (uses ChromaDB default embeddings)"
echo "   • Fast installation (~2 minutes vs 30+ minutes for full version)"
echo "   • Lower memory usage (~100MB vs 300MB+)"
echo "   • Still provides semantic search capabilities"
echo ""
echo "🔧 Management Commands:"
echo "   Status:  systemctl status ${SERVICE_NAME}"
echo "   Logs:    journalctl -u ${SERVICE_NAME} -f"
echo "   Restart: systemctl restart ${SERVICE_NAME}"
echo "   Stop:    systemctl stop ${SERVICE_NAME}"
echo ""
echo "🔗 Integration:"
echo "   API URL: http://127.0.0.1:${SERVICE_PORT}"
echo "   Update Clawdbot config to use local provider with this URL"
echo ""
echo "📋 Next Steps:"
echo "   1. Run test script: ./test_memory_search.py"
echo "   2. Update Clawdbot memory configuration"
echo "   3. Test memory_search tool integration"
echo ""