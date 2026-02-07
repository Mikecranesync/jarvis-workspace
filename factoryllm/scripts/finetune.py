#!/usr/bin/env python3
"""
Fine-tune FactoryLLM using Unsloth (2x faster, 60% less VRAM).
Run on Vast.ai, RunPod, or local GPU with 16GB+ VRAM.
"""

import os
import json
import argparse
from pathlib import Path

def main():
    parser = argparse.ArgumentParser(description="Fine-tune FactoryLLM")
    parser.add_argument("--model", default="llama-3.2-3b", 
                       choices=["llama-3.2-3b", "llama-3.2-1b", "mistral-7b", "phi-3-mini"])
    parser.add_argument("--epochs", type=int, default=3)
    parser.add_argument("--batch-size", type=int, default=4)
    parser.add_argument("--lr", type=float, default=2e-4)
    parser.add_argument("--lora-rank", type=int, default=64)
    parser.add_argument("--output-dir", default="/root/jarvis-workspace/factoryllm/output")
    parser.add_argument("--push-to-hub", action="store_true")
    parser.add_argument("--hub-model-id", default="mikecranesync/factoryllm-3b")
    args = parser.parse_args()
    
    # Model mapping
    MODEL_MAP = {
        "llama-3.2-3b": "unsloth/Llama-3.2-3B-Instruct",
        "llama-3.2-1b": "unsloth/Llama-3.2-1B-Instruct", 
        "mistral-7b": "unsloth/mistral-7b-instruct-v0.3-bnb-4bit",
        "phi-3-mini": "unsloth/Phi-3-mini-4k-instruct",
    }
    
    base_model = MODEL_MAP[args.model]
    
    print(f"=== FactoryLLM Fine-tuning ===")
    print(f"Base model: {base_model}")
    print(f"Epochs: {args.epochs}")
    print(f"LoRA rank: {args.lora_rank}")
    print()
    
    # Import here so we can check dependencies
    try:
        from unsloth import FastLanguageModel
        from datasets import load_dataset
        from trl import SFTTrainer
        from transformers import TrainingArguments
    except ImportError as e:
        print(f"Missing dependency: {e}")
        print("\nInstall with:")
        print("  pip install unsloth datasets trl transformers")
        print("\nOr run setup script first:")
        print("  bash scripts/setup_training_env.sh")
        return 1
    
    # Load model with LoRA
    print("Loading model...")
    model, tokenizer = FastLanguageModel.from_pretrained(
        model_name=base_model,
        max_seq_length=2048,
        dtype=None,  # Auto-detect
        load_in_4bit=True,
    )
    
    # Add LoRA adapters
    model = FastLanguageModel.get_peft_model(
        model,
        r=args.lora_rank,
        target_modules=["q_proj", "k_proj", "v_proj", "o_proj",
                       "gate_proj", "up_proj", "down_proj"],
        lora_alpha=args.lora_rank,
        lora_dropout=0,
        bias="none",
        use_gradient_checkpointing="unsloth",
        random_state=42,
    )
    
    # Load dataset
    print("Loading dataset...")
    corpus_dir = Path("/root/jarvis-workspace/factoryllm/corpus")
    
    # Use ShareGPT format
    train_data = json.loads((corpus_dir / "train_sharegpt.json").read_text())
    val_data = json.loads((corpus_dir / "val_sharegpt.json").read_text())
    
    # Convert to HF dataset format
    from datasets import Dataset
    
    def format_conversation(example):
        """Format ShareGPT conversation for training."""
        messages = example["conversations"]
        text = ""
        for msg in messages:
            role = msg["from"]
            content = msg["value"]
            if role == "system":
                text += f"<|start_header_id|>system<|end_header_id|>\n\n{content}<|eot_id|>"
            elif role == "human":
                text += f"<|start_header_id|>user<|end_header_id|>\n\n{content}<|eot_id|>"
            elif role == "gpt":
                text += f"<|start_header_id|>assistant<|end_header_id|>\n\n{content}<|eot_id|>"
        return {"text": text}
    
    train_dataset = Dataset.from_list(train_data).map(format_conversation)
    val_dataset = Dataset.from_list(val_data).map(format_conversation)
    
    print(f"Train examples: {len(train_dataset)}")
    print(f"Val examples: {len(val_dataset)}")
    
    # Training config
    training_args = TrainingArguments(
        per_device_train_batch_size=args.batch_size,
        gradient_accumulation_steps=4,
        warmup_steps=50,
        num_train_epochs=args.epochs,
        learning_rate=args.lr,
        fp16=True,
        logging_steps=10,
        optim="adamw_8bit",
        weight_decay=0.01,
        lr_scheduler_type="cosine",
        seed=42,
        output_dir=args.output_dir,
        save_strategy="epoch",
        evaluation_strategy="epoch",
        load_best_model_at_end=True,
    )
    
    # Trainer
    trainer = SFTTrainer(
        model=model,
        tokenizer=tokenizer,
        train_dataset=train_dataset,
        eval_dataset=val_dataset,
        dataset_text_field="text",
        max_seq_length=2048,
        dataset_num_proc=2,
        packing=True,
        args=training_args,
    )
    
    # Train
    print("\n=== Starting training ===")
    trainer.train()
    
    # Save
    print("\n=== Saving model ===")
    model.save_pretrained(args.output_dir)
    tokenizer.save_pretrained(args.output_dir)
    
    # Optionally save merged model (for deployment)
    merged_dir = Path(args.output_dir) / "merged"
    print(f"Saving merged model to {merged_dir}...")
    model.save_pretrained_merged(str(merged_dir), tokenizer, save_method="merged_16bit")
    
    # Push to Hub if requested
    if args.push_to_hub:
        print(f"Pushing to Hub: {args.hub_model_id}")
        model.push_to_hub(args.hub_model_id, token=os.environ.get("HF_TOKEN"))
        tokenizer.push_to_hub(args.hub_model_id, token=os.environ.get("HF_TOKEN"))
    
    print("\n=== Training complete! ===")
    print(f"Model saved to: {args.output_dir}")
    print(f"Merged model: {merged_dir}")
    
    # Export to GGUF for llama.cpp/Ollama
    print("\n=== Exporting to GGUF ===")
    gguf_path = Path(args.output_dir) / "factoryllm.gguf"
    model.save_pretrained_gguf(
        str(gguf_path.parent),
        tokenizer,
        quantization_method="q4_k_m"  # Good balance of size/quality
    )
    print(f"GGUF saved to: {gguf_path.parent}/unsloth.Q4_K_M.gguf")
    
    return 0

if __name__ == "__main__":
    exit(main())
