#!/bin/bash
# FactoryLM Edge Agent Server Startup Script

set -e

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install/upgrade dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Create data directory if it doesn't exist
mkdir -p data

# Set environment variables
export DATABASE_PATH="./data/devices.db"
export X_AGENT_TOKEN="${X_AGENT_TOKEN:-factorylm-agent-token-2025}"

# Start the server
echo "Starting FactoryLM Edge Agent Server on port 8090..."
echo "API Documentation: http://localhost:8090/docs"
echo "Health Check: http://localhost:8090/health"
echo ""

python main.py