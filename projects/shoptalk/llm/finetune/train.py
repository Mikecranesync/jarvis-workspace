#!/usr/bin/env python3
"""
ShopTalk Fine-Tuning Script
Fine-tune small models (Phi-3, Qwen, etc.) for industrial diagnostics.

This uses LoRA/QLoRA for efficient fine-tuning that can run on consumer hardware.
The resulting adapter can be merged for edge deployment.
"""

import json
import argparse
from pathlib import Path

# Check for required libraries
DEPS_AVAILABLE = True
try:
    import torch
    from transformers import (
        AutoModelForCausalLM,
        AutoTokenizer,
        TrainingArguments,
        Trainer,
        DataCollatorForLanguageModeling
    )
    from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
    from datasets import Dataset
except ImportError as e:
    DEPS_AVAILABLE = False
    print(f"Missing dependencies: {e}")
    print("Install with: pip install torch transformers peft datasets bitsandbytes")


# Supported base models
MODELS = {
    "phi3-mini": "microsoft/Phi-3-mini-4k-instruct",
    "phi3.5-mini": "microsoft/Phi-3.5-mini-instruct", 
    "qwen2-1.5b": "Qwen/Qwen2-1.5B-Instruct",
    "qwen2-0.5b": "Qwen/Qwen2-0.5B-Instruct",
    "tinyllama": "TinyLlama/TinyLlama-1.1B-Chat-v1.0",
}

# LoRA configuration for efficient fine-tuning
LORA_CONFIG = {
    "r": 16,  # Rank
    "lora_alpha": 32,
    "lora_dropout": 0.05,
    "bias": "none",
    "task_type": "CAUSAL_LM",
    "target_modules": ["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"]
}


def load_dataset(data_path: str, tokenizer, max_length: int = 512):
    """Load and tokenize training data."""
    with open(data_path) as f:
        data = json.load(f)
    
    def format_example(example):
        """Format as instruction-following conversation."""
        if example.get("input"):
            text = f"### Instruction:\n{example['instruction']}\n\n### Input:\n{example['input']}\n\n### Response:\n{example['output']}"
        else:
            text = f"### Instruction:\n{example['instruction']}\n\n### Response:\n{example['output']}"
        return text
    
    texts = [format_example(ex) for ex in data]
    
    # Tokenize
    tokenized = tokenizer(
        texts,
        truncation=True,
        max_length=max_length,
        padding="max_length",
        return_tensors="pt"
    )
    
    dataset = Dataset.from_dict({
        "input_ids": tokenized["input_ids"],
        "attention_mask": tokenized["attention_mask"],
        "labels": tokenized["input_ids"].clone()
    })
    
    return dataset


def setup_model(model_name: str, use_4bit: bool = True):
    """Load and prepare model for fine-tuning."""
    model_path = MODELS.get(model_name, model_name)
    
    print(f"Loading model: {model_path}")
    
    # Quantization config for memory efficiency
    if use_4bit:
        from transformers import BitsAndBytesConfig
        bnb_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_compute_dtype=torch.float16,
            bnb_4bit_use_double_quant=True,
        )
        model = AutoModelForCausalLM.from_pretrained(
            model_path,
            quantization_config=bnb_config,
            device_map="auto",
            trust_remote_code=True
        )
    else:
        model = AutoModelForCausalLM.from_pretrained(
            model_path,
            torch_dtype=torch.float16,
            device_map="auto",
            trust_remote_code=True
        )
    
    tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)
    
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    
    # Prepare for training
    model = prepare_model_for_kbit_training(model)
    
    # Add LoRA adapters
    lora_config = LoraConfig(**LORA_CONFIG)
    model = get_peft_model(model, lora_config)
    
    model.print_trainable_parameters()
    
    return model, tokenizer


def train(
    model_name: str,
    data_path: str,
    output_dir: str,
    epochs: int = 3,
    batch_size: int = 4,
    learning_rate: float = 2e-4,
    use_4bit: bool = True
):
    """Run fine-tuning."""
    
    if not DEPS_AVAILABLE:
        print("Cannot train - missing dependencies")
        return
    
    # Setup
    model, tokenizer = setup_model(model_name, use_4bit)
    dataset = load_dataset(data_path, tokenizer)
    
    # Training arguments
    training_args = TrainingArguments(
        output_dir=output_dir,
        num_train_epochs=epochs,
        per_device_train_batch_size=batch_size,
        gradient_accumulation_steps=4,
        warmup_steps=100,
        learning_rate=learning_rate,
        fp16=True,
        logging_steps=10,
        save_strategy="epoch",
        save_total_limit=2,
        report_to="none",
    )
    
    # Data collator
    data_collator = DataCollatorForLanguageModeling(
        tokenizer=tokenizer,
        mlm=False
    )
    
    # Trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=dataset,
        data_collator=data_collator,
    )
    
    # Train
    print("Starting training...")
    trainer.train()
    
    # Save
    print(f"Saving model to {output_dir}")
    trainer.save_model(output_dir)
    tokenizer.save_pretrained(output_dir)
    
    print("Training complete!")


def merge_adapter(base_model: str, adapter_path: str, output_path: str):
    """Merge LoRA adapter with base model for deployment."""
    from peft import PeftModel
    
    print(f"Loading base model: {base_model}")
    model = AutoModelForCausalLM.from_pretrained(
        MODELS.get(base_model, base_model),
        torch_dtype=torch.float16,
        device_map="auto",
        trust_remote_code=True
    )
    
    print(f"Loading adapter: {adapter_path}")
    model = PeftModel.from_pretrained(model, adapter_path)
    
    print("Merging weights...")
    model = model.merge_and_unload()
    
    print(f"Saving merged model to {output_path}")
    model.save_pretrained(output_path)
    
    # Also save tokenizer
    tokenizer = AutoTokenizer.from_pretrained(MODELS.get(base_model, base_model))
    tokenizer.save_pretrained(output_path)
    
    print("Merge complete!")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="ShopTalk Fine-Tuning")
    subparsers = parser.add_subparsers(dest="command")
    
    # Train command
    train_parser = subparsers.add_parser("train", help="Fine-tune a model")
    train_parser.add_argument("--model", default="phi3-mini", choices=list(MODELS.keys()))
    train_parser.add_argument("--data", required=True, help="Path to training data JSON")
    train_parser.add_argument("--output", default="./shoptalk-adapter", help="Output directory")
    train_parser.add_argument("--epochs", type=int, default=3)
    train_parser.add_argument("--batch-size", type=int, default=4)
    train_parser.add_argument("--lr", type=float, default=2e-4)
    
    # Merge command
    merge_parser = subparsers.add_parser("merge", help="Merge adapter with base model")
    merge_parser.add_argument("--base", required=True, help="Base model name")
    merge_parser.add_argument("--adapter", required=True, help="Adapter path")
    merge_parser.add_argument("--output", required=True, help="Output path")
    
    # List models
    list_parser = subparsers.add_parser("list", help="List supported models")
    
    args = parser.parse_args()
    
    if args.command == "train":
        train(
            model_name=args.model,
            data_path=args.data,
            output_dir=args.output,
            epochs=args.epochs,
            batch_size=args.batch_size,
            learning_rate=args.lr
        )
    elif args.command == "merge":
        merge_adapter(args.base, args.adapter, args.output)
    elif args.command == "list":
        print("Supported base models:")
        for name, path in MODELS.items():
            print(f"  {name}: {path}")
    else:
        parser.print_help()
