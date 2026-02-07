# FactoryLLM - Mike's Industrial Maintenance Model

> A fine-tuned LLM trained on 20 years of maintenance expertise.

## Architecture (Layer 0-3)

```
Layer 0: Pure Logic (deterministic, no LLM)
Layer 1: FactoryLLM 3B (Pi/Edge) ← THIS PROJECT
Layer 2: FactoryLLM 7B (Local GPU)
Layer 3: Cloud APIs (fallback)
```

## Training Corpus

| Source | Files | Size | Content |
|--------|-------|------|---------|
| Book Chapters | 9 | 4.8MB | Telegram conversation logs |
| Rivet-PRO | 327 | 18MB | Code, specs, docs |
| Mike's Brain | 15 | 1.1MB | Ideas, processes, architecture |
| Brain Research | 36 | 10MB | Research, troubleshooting sessions |
| Memory | 8 | 132K | Daily context, decisions |

**Total: ~34MB raw text → estimated 50K+ training examples**

## Pipeline

1. `scripts/extract_corpus.py` - Gather all markdown into raw text
2. `scripts/format_instruct.py` - Convert to instruction/response pairs
3. `scripts/prepare_dataset.py` - Create train/val splits, tokenize
4. `scripts/finetune.py` - Run fine-tuning (local or Vast.ai)

## Base Models

- **Edge (3B)**: `meta-llama/Llama-3.2-3B-Instruct`
- **Local (7B)**: `mistralai/Mistral-7B-Instruct-v0.3`

## Quick Start

```bash
# Extract corpus
python scripts/extract_corpus.py

# Format for training
python scripts/format_instruct.py

# Fine-tune (requires GPU)
python scripts/finetune.py --model llama-3.2-3b --epochs 3
```

## Cost Estimate

- Fine-tuning 3B model: ~$20-50 on Vast.ai (A100 for 2-4 hours)
- Fine-tuning 7B model: ~$50-100 on Vast.ai

## Status

- [x] Corpus inventory
- [ ] Corpus extraction
- [ ] Instruction formatting
- [ ] Dataset preparation
- [ ] Fine-tuning run
- [ ] Evaluation
- [ ] Deployment to Pi
