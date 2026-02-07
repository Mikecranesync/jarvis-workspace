#!/usr/bin/env python3
"""
Format extracted corpus into instruction-following format for fine-tuning.
Supports multiple output formats: Alpaca, ChatML, Llama-3.
"""

import json
import random
from pathlib import Path

CORPUS_DIR = Path("/root/jarvis-workspace/factoryllm/corpus")
INPUT_FILE = CORPUS_DIR / "corpus_raw.jsonl"

# System prompt for FactoryLLM
SYSTEM_PROMPT = """You are FactoryLLM, an AI assistant specialized in industrial maintenance, PLC programming, and manufacturing automation. You were trained by Mike Crane, a 20-year veteran of crane and industrial maintenance.

Your expertise includes:
- Allen-Bradley, Siemens, and other PLC troubleshooting
- VFD configuration and fault diagnosis
- CMMS systems and maintenance workflows
- Industrial communication protocols (Modbus, Ethernet/IP)
- Predictive maintenance and reliability engineering

Be practical, direct, and technically accurate. When troubleshooting, think step-by-step like an experienced technician."""

def format_alpaca(example: dict) -> dict:
    """Format as Alpaca-style instruction/input/output."""
    return {
        "instruction": example["instruction"],
        "input": "",
        "output": example["response"],
        "system": SYSTEM_PROMPT
    }

def format_chatml(example: dict) -> str:
    """Format as ChatML for most modern fine-tuning."""
    return f"""<|im_start|>system
{SYSTEM_PROMPT}<|im_end|>
<|im_start|>user
{example["instruction"]}<|im_end|>
<|im_start|>assistant
{example["response"]}<|im_end|>"""

def format_llama3(example: dict) -> str:
    """Format for Llama 3 instruction tuning."""
    return (
        "<|begin_of_text|><|start_header_id|>system<|end_header_id|>\n\n"
        f"{SYSTEM_PROMPT}<|eot_id|><|start_header_id|>user<|end_header_id|>\n\n"
        f"{example['instruction']}<|eot_id|><|start_header_id|>assistant<|end_header_id|>\n\n"
        f"{example['response']}<|eot_id|>"
    )

def format_sharegpt(example: dict) -> dict:
    """Format as ShareGPT-style conversations (used by axolotl, etc)."""
    return {
        "conversations": [
            {"from": "system", "value": SYSTEM_PROMPT},
            {"from": "human", "value": example["instruction"]},
            {"from": "gpt", "value": example["response"]}
        ]
    }

def clean_example(example: dict) -> dict:
    """Clean and validate example."""
    # Remove very short examples
    if len(example.get("instruction", "")) < 10:
        return None
    if len(example.get("response", "")) < 20:
        return None
    
    # Remove examples that are mostly code/logs
    response = example["response"]
    if response.count('\n') > 50 and len(response) > 3000:
        # Truncate very long responses
        response = response[:2000] + "\n\n[truncated]"
        example["response"] = response
    
    # Remove problematic patterns
    if "[message_id:" in example["instruction"]:
        example["instruction"] = example["instruction"].split("[message_id:")[0].strip()
    
    return example

def main():
    # Load raw corpus
    examples = []
    with open(INPUT_FILE) as f:
        for line in f:
            ex = json.loads(line)
            cleaned = clean_example(ex)
            if cleaned:
                examples.append(cleaned)
    
    print(f"Loaded {len(examples)} examples after cleaning")
    
    # Shuffle
    random.seed(42)
    random.shuffle(examples)
    
    # Split train/val (95/5)
    split_idx = int(len(examples) * 0.95)
    train_examples = examples[:split_idx]
    val_examples = examples[split_idx:]
    
    print(f"Train: {len(train_examples)}, Val: {len(val_examples)}")
    
    # Save in multiple formats
    
    # 1. ShareGPT format (for axolotl)
    sharegpt_train = [format_sharegpt(ex) for ex in train_examples]
    sharegpt_val = [format_sharegpt(ex) for ex in val_examples]
    
    with open(CORPUS_DIR / "train_sharegpt.json", 'w') as f:
        json.dump(sharegpt_train, f, indent=2)
    with open(CORPUS_DIR / "val_sharegpt.json", 'w') as f:
        json.dump(sharegpt_val, f, indent=2)
    
    # 2. Alpaca format (for simple fine-tuning)
    alpaca_train = [format_alpaca(ex) for ex in train_examples]
    alpaca_val = [format_alpaca(ex) for ex in val_examples]
    
    with open(CORPUS_DIR / "train_alpaca.json", 'w') as f:
        json.dump(alpaca_train, f, indent=2)
    with open(CORPUS_DIR / "val_alpaca.json", 'w') as f:
        json.dump(alpaca_val, f, indent=2)
    
    # 3. Raw text for verification
    with open(CORPUS_DIR / "train_text.txt", 'w') as f:
        for ex in train_examples[:100]:  # Just first 100 for inspection
            f.write(f"=== INSTRUCTION ===\n{ex['instruction']}\n\n")
            f.write(f"=== RESPONSE ===\n{ex['response']}\n\n")
            f.write("=" * 80 + "\n\n")
    
    print(f"\nSaved:")
    print(f"  - train_sharegpt.json ({len(train_examples)} examples)")
    print(f"  - val_sharegpt.json ({len(val_examples)} examples)")
    print(f"  - train_alpaca.json")
    print(f"  - val_alpaca.json")
    print(f"  - train_text.txt (first 100 for review)")
    
    # Stats
    total_tokens_est = sum(len(ex["instruction"]) + len(ex["response"]) for ex in examples) // 4
    print(f"\nEstimated total tokens: ~{total_tokens_est:,}")
    print(f"Estimated fine-tuning cost (A100): ~${total_tokens_est / 1_000_000 * 3:.2f}")

if __name__ == "__main__":
    main()
