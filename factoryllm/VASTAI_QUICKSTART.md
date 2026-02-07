# FactoryLLM - Vast.ai Quick Start

## 1. Rent a GPU (~$0.50-1/hr)

Go to [vast.ai](https://vast.ai) and rent:
- **Cheapest that works:** RTX 3090 24GB (~$0.30/hr)
- **Recommended:** A10 24GB (~$0.50/hr) 
- **Fastest:** A100 40GB (~$0.80/hr)

Search filters:
- GPU RAM: >= 24 GB
- Disk: >= 50 GB
- CUDA: >= 12.0

## 2. Connect and Setup

```bash
# SSH to your instance (Vast gives you the command)
ssh -p <port> root@<ip>

# Clone/download corpus
cd ~
mkdir factoryllm && cd factoryllm

# Option A: If you have the files locally
# (from your local machine)
scp -P <port> -r /root/jarvis-workspace/factoryllm/* root@<ip>:~/factoryllm/

# Option B: Download from VPS
scp -r root@<vps-ip>:/root/jarvis-workspace/factoryllm/* ~/factoryllm/
```

## 3. Install Dependencies

```bash
cd ~/factoryllm
bash scripts/setup_training_env.sh
```

## 4. Run Training

```bash
# 3B model (fastest, fits on 16GB GPU)
python scripts/finetune.py --model llama-3.2-3b --epochs 3

# 1B model (tiny, runs anywhere)
python scripts/finetune.py --model llama-3.2-1b --epochs 3

# 7B model (needs 24GB+ GPU)
python scripts/finetune.py --model mistral-7b --epochs 2
```

Training time estimates:
- 3B model, 3 epochs, ~7K examples: **~30-60 min on A10**
- 7B model, 2 epochs: **~2-3 hours on A100**

## 5. Download Your Model

```bash
# After training completes, download the GGUF
scp -P <port> root@<ip>:~/factoryllm/output/*.gguf ~/

# Or the full model
scp -P <port> -r root@<ip>:~/factoryllm/output/merged/ ~/factoryllm-merged/
```

## 6. Deploy to Ollama

```bash
# On your PLC laptop or any machine with Ollama
ollama create factoryllm -f Modelfile

# Modelfile contents:
FROM ./factoryllm.Q4_K_M.gguf
SYSTEM "You are FactoryLLM, an AI assistant specialized in industrial maintenance..."
```

## Cost Summary

| Model | GPU | Time | Cost |
|-------|-----|------|------|
| Llama 3.2 1B | RTX 3090 | ~20 min | ~$0.10 |
| Llama 3.2 3B | A10 | ~45 min | ~$0.40 |
| Mistral 7B | A100 | ~2 hrs | ~$1.60 |

**Your estimated cost: ~$1-2 total**

## Troubleshooting

### Out of Memory
- Reduce batch size: `--batch-size 2`
- Use smaller model: `--model llama-3.2-1b`
- Reduce LoRA rank: `--lora-rank 32`

### Training too slow
- Rent bigger GPU (A100 vs 3090)
- Reduce epochs: `--epochs 2`

### Can't connect to Vast instance
- Wait 2-3 min after rental for setup
- Check Vast dashboard for actual SSH command
