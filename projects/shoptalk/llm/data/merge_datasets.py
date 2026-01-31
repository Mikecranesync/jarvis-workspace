#!/usr/bin/env python3
"""
Merge all ShopTalk training datasets into unified files.
Creates both Alpaca and ShareGPT formats for fine-tuning.
"""

import json
import random
from pathlib import Path
from datetime import datetime
from collections import Counter

DATA_DIR = Path(__file__).parent
OUTPUT_DIR = DATA_DIR / "merged"


def load_all_datasets() -> list:
    """Load all training JSON files."""
    all_samples = []
    sources = {}
    
    for json_file in DATA_DIR.glob("*.json"):
        # Skip non-training files
        if any(skip in json_file.name for skip in ["benchmark", "knowledge", "merged"]):
            continue
        
        try:
            with open(json_file) as f:
                data = json.load(f)
            
            if isinstance(data, list) and len(data) > 0:
                # Check if it's training data format
                if "instruction" in data[0] or "conversations" in data[0]:
                    all_samples.extend(data)
                    sources[json_file.name] = len(data)
                    print(f"  ✓ {json_file.name}: {len(data)} samples")
        except Exception as e:
            print(f"  ✗ {json_file.name}: {e}")
    
    return all_samples, sources


def to_alpaca_format(sample: dict) -> dict:
    """Convert sample to Alpaca format."""
    if "instruction" in sample:
        return {
            "instruction": sample["instruction"],
            "input": sample.get("input", ""),
            "output": sample["output"]
        }
    elif "conversations" in sample:
        # Convert from ShareGPT
        convs = sample["conversations"]
        instruction = ""
        output = ""
        for turn in convs:
            if turn["from"] == "human":
                instruction = turn["value"]
            elif turn["from"] == "gpt":
                output = turn["value"]
        return {"instruction": instruction, "input": "", "output": output}
    return sample


def to_sharegpt_format(sample: dict) -> dict:
    """Convert sample to ShareGPT format."""
    if "conversations" in sample:
        return sample
    elif "instruction" in sample:
        return {
            "conversations": [
                {"from": "human", "value": sample["instruction"] + ("\n" + sample["input"] if sample.get("input") else "")},
                {"from": "gpt", "value": sample["output"]}
            ]
        }
    return sample


def deduplicate(samples: list) -> list:
    """Remove duplicate samples based on instruction."""
    seen = set()
    unique = []
    
    for sample in samples:
        key = sample.get("instruction", str(sample.get("conversations", "")))[:200]
        if key not in seen:
            seen.add(key)
            unique.append(sample)
    
    return unique


def create_train_val_split(samples: list, val_ratio: float = 0.1) -> tuple:
    """Split into training and validation sets."""
    random.shuffle(samples)
    split_idx = int(len(samples) * (1 - val_ratio))
    return samples[:split_idx], samples[split_idx:]


def main():
    print("=" * 50)
    print("ShopTalk Training Data Merger")
    print("=" * 50)
    
    # Create output directory
    OUTPUT_DIR.mkdir(exist_ok=True)
    
    # Load all datasets
    print("\nLoading datasets:")
    all_samples, sources = load_all_datasets()
    
    print(f"\nTotal raw samples: {len(all_samples)}")
    
    # Convert to Alpaca format for consistency
    print("\nConverting to Alpaca format...")
    alpaca_samples = [to_alpaca_format(s) for s in all_samples]
    
    # Deduplicate
    print("Deduplicating...")
    unique_samples = deduplicate(alpaca_samples)
    print(f"Unique samples: {len(unique_samples)}")
    
    # Create train/val split
    print("\nCreating train/validation split (90/10)...")
    train_samples, val_samples = create_train_val_split(unique_samples)
    print(f"  Training: {len(train_samples)}")
    print(f"  Validation: {len(val_samples)}")
    
    # Save merged datasets
    timestamp = datetime.now().strftime("%Y%m%d")
    
    # Alpaca format
    train_alpaca = OUTPUT_DIR / f"shoptalk_train_{timestamp}.json"
    val_alpaca = OUTPUT_DIR / f"shoptalk_val_{timestamp}.json"
    
    with open(train_alpaca, 'w') as f:
        json.dump(train_samples, f, indent=2)
    print(f"\n✓ Saved: {train_alpaca}")
    
    with open(val_alpaca, 'w') as f:
        json.dump(val_samples, f, indent=2)
    print(f"✓ Saved: {val_alpaca}")
    
    # ShareGPT format
    train_sharegpt = OUTPUT_DIR / f"shoptalk_train_sharegpt_{timestamp}.json"
    sharegpt_samples = [to_sharegpt_format(s) for s in train_samples]
    
    with open(train_sharegpt, 'w') as f:
        json.dump(sharegpt_samples, f, indent=2)
    print(f"✓ Saved: {train_sharegpt}")
    
    # Summary
    print("\n" + "=" * 50)
    print("SUMMARY")
    print("=" * 50)
    print(f"Source files: {len(sources)}")
    for name, count in sorted(sources.items()):
        print(f"  - {name}: {count}")
    print(f"\nTotal unique samples: {len(unique_samples)}")
    print(f"Training samples: {len(train_samples)}")
    print(f"Validation samples: {len(val_samples)}")
    print(f"\nOutput directory: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
