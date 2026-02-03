#!/bin/bash
# Run Micro820 Zero-Shot Test
# Usage: ./scripts/test-micro820.sh

echo "Starting Micro820 Zero-Shot Test..."
echo ""

# Run the test locally (it SSHs to Pi)
python3 /root/jarvis-workspace/infrastructure/balena/plc-gateway/app/plc_test.py

exit $?
