#!/usr/bin/env python3
"""
Extract training corpus from Mike's knowledge base.
Converts markdown files and conversation logs into raw text corpus.
"""

import os
import re
import json
from pathlib import Path
from datetime import datetime

WORKSPACE = Path("/root/jarvis-workspace")
OUTPUT_DIR = WORKSPACE / "factoryllm" / "corpus"

# Source directories
SOURCES = {
    "book_chapters": WORKSPACE / "book" / "chapters",
    "rivet_pro": WORKSPACE / "projects" / "Rivet-PRO",
    "mikes_brain": WORKSPACE / "mikes-brain",
    "brain": WORKSPACE / "brain",
    "memory": WORKSPACE / "memory",
    "agents_sprint": WORKSPACE / "agents" / "accelerator-sprint" / "deliverables",
}

def extract_conversations(content: str) -> list[dict]:
    """Extract Mike/Jarvis conversation pairs from book chapters."""
    conversations = []
    
    # Pattern: **Mike H:** ... followed by **Jarvis:** ...
    # Split by speaker markers
    parts = re.split(r'\*\*(?:Mike H?|Jarvis):\*\*', content)
    speakers = re.findall(r'\*\*(Mike H?|Jarvis):\*\*', content)
    
    if len(speakers) < 2:
        return conversations
    
    current_mike = None
    for i, speaker in enumerate(speakers):
        text = parts[i + 1].strip() if i + 1 < len(parts) else ""
        
        # Clean up the text
        text = re.sub(r'\[message_id: \d+\]', '', text)
        text = re.sub(r'\[Telegram.*?\]', '', text)
        text = text.strip()
        
        if not text or len(text) < 20:
            continue
            
        if speaker.startswith("Mike"):
            current_mike = text
        elif speaker == "Jarvis" and current_mike:
            conversations.append({
                "instruction": current_mike,
                "response": text,
                "source": "telegram_conversation"
            })
            current_mike = None
    
    return conversations

def extract_documentation(content: str, filepath: str) -> list[dict]:
    """Extract documentation as Q&A pairs."""
    examples = []
    
    # Extract headers and their content as implicit Q&A
    sections = re.split(r'\n##+ ', content)
    
    for section in sections[1:]:  # Skip content before first header
        lines = section.split('\n', 1)
        if len(lines) < 2:
            continue
            
        header = lines[0].strip()
        body = lines[1].strip()
        
        if len(body) < 50:
            continue
        
        # Create instruction from header
        instruction = f"Explain {header}" if not header.endswith('?') else header
        
        examples.append({
            "instruction": instruction,
            "response": body[:2000],  # Truncate long responses
            "source": f"documentation:{filepath}"
        })
    
    return examples

def extract_code_examples(content: str, filepath: str) -> list[dict]:
    """Extract code blocks with context."""
    examples = []
    
    # Find code blocks with preceding context
    pattern = r'([^\n]+)\n```(\w+)?\n(.*?)```'
    matches = re.findall(pattern, content, re.DOTALL)
    
    for context, lang, code in matches:
        if len(code.strip()) < 20:
            continue
            
        lang = lang or "code"
        examples.append({
            "instruction": f"Write {lang} code to: {context.strip()}",
            "response": code.strip(),
            "source": f"code_example:{filepath}"
        })
    
    return examples

def process_file(filepath: Path) -> list[dict]:
    """Process a single file and extract training examples."""
    try:
        content = filepath.read_text(encoding='utf-8', errors='ignore')
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return []
    
    examples = []
    rel_path = str(filepath.relative_to(WORKSPACE))
    
    # Book chapters get conversation extraction
    if "book/chapters" in str(filepath):
        examples.extend(extract_conversations(content))
    
    # All markdown gets documentation extraction
    if filepath.suffix == '.md':
        examples.extend(extract_documentation(content, rel_path))
    
    # Python files get code extraction
    if filepath.suffix == '.py':
        examples.extend(extract_code_examples(content, rel_path))
    
    return examples

def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    all_examples = []
    stats = {}
    
    for source_name, source_path in SOURCES.items():
        if not source_path.exists():
            print(f"Skipping {source_name}: path not found")
            continue
            
        source_examples = []
        
        # Process markdown files
        for md_file in source_path.rglob("*.md"):
            # Skip node_modules and other noise
            if "node_modules" in str(md_file):
                continue
            examples = process_file(md_file)
            source_examples.extend(examples)
        
        # Process Python files (for code examples)
        for py_file in source_path.rglob("*.py"):
            if "node_modules" in str(py_file) or "__pycache__" in str(py_file):
                continue
            examples = process_file(py_file)
            source_examples.extend(examples)
        
        stats[source_name] = len(source_examples)
        all_examples.extend(source_examples)
        print(f"{source_name}: {len(source_examples)} examples")
    
    # Deduplicate by instruction
    seen = set()
    unique_examples = []
    for ex in all_examples:
        key = ex["instruction"][:100]
        if key not in seen:
            seen.add(key)
            unique_examples.append(ex)
    
    print(f"\nTotal: {len(all_examples)} raw, {len(unique_examples)} unique")
    
    # Save as JSONL
    output_file = OUTPUT_DIR / "corpus_raw.jsonl"
    with open(output_file, 'w') as f:
        for ex in unique_examples:
            f.write(json.dumps(ex) + '\n')
    
    print(f"Saved to {output_file}")
    
    # Save stats
    stats_file = OUTPUT_DIR / "extraction_stats.json"
    with open(stats_file, 'w') as f:
        json.dump({
            "timestamp": datetime.now().isoformat(),
            "sources": stats,
            "total_raw": len(all_examples),
            "total_unique": len(unique_examples)
        }, f, indent=2)
    
    print(f"Stats saved to {stats_file}")
    
    # Preview
    print("\n=== Sample examples ===")
    for ex in unique_examples[:3]:
        print(f"\nINSTRUCT: {ex['instruction'][:100]}...")
        print(f"RESPONSE: {ex['response'][:100]}...")
        print(f"SOURCE: {ex['source']}")

if __name__ == "__main__":
    main()
