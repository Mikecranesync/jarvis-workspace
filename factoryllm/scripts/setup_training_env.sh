#!/bin/bash
# Setup training environment for FactoryLLM fine-tuning
# Run on Vast.ai, RunPod, or local GPU machine

set -e

echo "=== FactoryLLM Training Environment Setup ==="

# Check for GPU
if ! command -v nvidia-smi &> /dev/null; then
    echo "WARNING: No NVIDIA GPU detected. Fine-tuning requires GPU."
    echo "Recommended: Vast.ai or RunPod with A100/A10/RTX 4090"
fi

nvidia-smi || true

# Install Unsloth (fastest fine-tuning library)
echo ""
echo "=== Installing Unsloth ==="
pip install --upgrade pip
pip install "unsloth[colab-new] @ git+https://github.com/unslothai/unsloth.git"

# Install other dependencies
echo ""
echo "=== Installing dependencies ==="
pip install datasets trl transformers accelerate bitsandbytes
pip install sentencepiece protobuf

# Verify installation
echo ""
echo "=== Verifying installation ==="
python3 -c "from unsloth import FastLanguageModel; print('Unsloth: OK')"
python3 -c "from datasets import load_dataset; print('Datasets: OK')"
python3 -c "from trl import SFTTrainer; print('TRL: OK')"

echo ""
echo "=== Setup complete! ==="
echo ""
echo "Next steps:"
echo "1. Upload corpus files: scp -r corpus/ vast:~/factoryllm/"
echo "2. Run training: python scripts/finetune.py --model llama-3.2-3b --epochs 3"
