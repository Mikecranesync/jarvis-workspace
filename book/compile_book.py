#!/usr/bin/env python3
"""
Compile Clawdbot Telegram conversations into a book format.
"""

import json
import os
import re
from datetime import datetime
from pathlib import Path
from collections import defaultdict

SESSIONS_DIR = Path.home() / ".clawdbot/agents/main/sessions"
OUTPUT_DIR = Path("/root/jarvis-workspace/book")

def parse_timestamp(ts_str):
    """Parse ISO timestamp."""
    try:
        return datetime.fromisoformat(ts_str.replace('Z', '+00:00'))
    except:
        return None

def extract_telegram_info(text):
    """Extract sender info from Telegram message format."""
    # Pattern: [Telegram Name id:123 timestamp] message
    match = re.match(r'\[Telegram ([^\]]+) id:(\d+)[^\]]*\]\s*(.*)', text, re.DOTALL)
    if match:
        return {
            'sender': match.group(1).strip(),
            'id': match.group(2),
            'content': match.group(3).strip()
        }
    return None

def process_session(filepath):
    """Process a single session file and extract messages."""
    messages = []
    
    with open(filepath, 'r') as f:
        for line in f:
            try:
                entry = json.loads(line.strip())
                if entry.get('type') == 'message' and 'message' in entry:
                    msg = entry['message']
                    role = msg.get('role', '')
                    timestamp = parse_timestamp(entry.get('timestamp', ''))
                    
                    # Extract text content
                    content_parts = []
                    for item in msg.get('content', []):
                        if isinstance(item, dict) and item.get('type') == 'text':
                            content_parts.append(item.get('text', ''))
                        elif isinstance(item, str):
                            content_parts.append(item)
                    
                    text = '\n'.join(content_parts)
                    if not text.strip():
                        continue
                    
                    # Skip tool calls, heartbeats, and system messages
                    if 'HEARTBEAT_OK' in text or 'NO_REPLY' in text:
                        continue
                    if text.startswith('System:') and 'heartbeat' in text.lower():
                        continue
                    
                    # Parse telegram info if present
                    telegram_info = extract_telegram_info(text)
                    
                    messages.append({
                        'timestamp': timestamp,
                        'role': role,
                        'text': text,
                        'telegram_info': telegram_info
                    })
            except json.JSONDecodeError:
                continue
            except Exception as e:
                continue
    
    return messages

def group_by_date(messages):
    """Group messages by date."""
    by_date = defaultdict(list)
    for msg in messages:
        if msg['timestamp']:
            date_key = msg['timestamp'].strftime('%Y-%m-%d')
            by_date[date_key].append(msg)
    return dict(sorted(by_date.items()))

def format_message(msg):
    """Format a single message for the book."""
    if msg['role'] == 'user':
        if msg['telegram_info']:
            sender = msg['telegram_info']['sender']
            content = msg['telegram_info']['content']
            return f"**{sender}:** {content}"
        else:
            return f"**User:** {msg['text'][:500]}..."
    else:
        # Assistant message - clean up tool outputs
        text = msg['text']
        # Truncate very long responses
        if len(text) > 2000:
            text = text[:2000] + "\n\n*[Message truncated for brevity]*"
        return f"**Jarvis:** {text}"

def generate_chapter(date_str, messages):
    """Generate a markdown chapter for a single day."""
    date_obj = datetime.strptime(date_str, '%Y-%m-%d')
    chapter_title = date_obj.strftime('%B %d, %Y')
    
    lines = [f"# {chapter_title}\n\n"]
    
    # Group into conversation segments
    current_hour = None
    for msg in messages:
        if msg['timestamp']:
            hour = msg['timestamp'].strftime('%H:00')
            if hour != current_hour:
                current_hour = hour
                lines.append(f"\n### {msg['timestamp'].strftime('%I:%M %p')}\n\n")
        
        formatted = format_message(msg)
        if formatted:
            lines.append(formatted + "\n\n---\n\n")
    
    return ''.join(lines)

def main():
    print("📚 Compiling FactoryLM Book from Telegram Conversations...")
    
    # Collect all messages from all sessions
    all_messages = []
    
    for session_file in SESSIONS_DIR.glob("*.jsonl"):
        print(f"  Processing {session_file.name}...")
        messages = process_session(session_file)
        all_messages.extend(messages)
        print(f"    Found {len(messages)} messages")
    
    # Sort by timestamp
    all_messages.sort(key=lambda x: x['timestamp'] or datetime.min)
    
    # Group by date
    by_date = group_by_date(all_messages)
    
    print(f"\n📅 Found conversations from {len(by_date)} days")
    
    # Generate chapters
    chapters_dir = OUTPUT_DIR / "chapters"
    chapters_dir.mkdir(exist_ok=True)
    
    toc_entries = []
    
    for i, (date_str, messages) in enumerate(by_date.items(), 1):
        chapter_content = generate_chapter(date_str, messages)
        chapter_file = chapters_dir / f"chapter_{i:02d}_{date_str}.md"
        
        with open(chapter_file, 'w') as f:
            f.write(chapter_content)
        
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        toc_entries.append(f"{i}. [{date_obj.strftime('%B %d, %Y')}](chapters/chapter_{i:02d}_{date_str}.md) - {len(messages)} exchanges")
        print(f"  ✓ Chapter {i}: {date_str} ({len(messages)} messages)")
    
    # Generate main book file
    book_content = f"""# Building FactoryLM
## A Real-Time AI Startup Journal

*Conversations between Mike Crane and Jarvis (Claude/Clawdbot)*

*Compiled: {datetime.now().strftime('%B %d, %Y')}*

---

## About This Book

This book is an automatically compiled record of the conversations between Mike Crane (founder of FactoryLM) and his AI assistant Jarvis, running on Clawdbot. It documents the real-time building of an AI-powered industrial automation startup.

**What you'll find here:**
- Technical architecture discussions
- Product development decisions  
- Infrastructure planning
- Marketing strategy
- The human-AI collaboration in action

---

## Table of Contents

{chr(10).join(toc_entries)}

---

## Statistics

- **Total Days:** {len(by_date)}
- **Total Messages:** {len(all_messages)}
- **Date Range:** {min(by_date.keys())} to {max(by_date.keys())}

---

*This document was automatically generated from Clawdbot session logs.*
"""
    
    with open(OUTPUT_DIR / "BOOK.md", 'w') as f:
        f.write(book_content)
    
    print(f"\n✅ Book compiled!")
    print(f"   Main file: {OUTPUT_DIR}/BOOK.md")
    print(f"   Chapters: {chapters_dir}/")
    print(f"   Total messages: {len(all_messages)}")

if __name__ == "__main__":
    main()
