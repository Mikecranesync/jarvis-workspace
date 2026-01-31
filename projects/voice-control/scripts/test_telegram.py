#!/usr/bin/env python3
"""
Test sending messages to Telegram.

Usage:
    export TELEGRAM_BOT_TOKEN="your-token"
    export TELEGRAM_CHAT_ID="your-chat-id"
    python test_telegram.py "Hello from voice control!"

Or run without arguments to use default test message.
"""

import os
import sys

try:
    import requests
except ImportError:
    print("Missing requests. Install with: pip install requests")
    sys.exit(1)


def send_telegram(token: str, chat_id: str, message: str) -> bool:
    """Send a message to Telegram."""
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    
    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "Markdown"
    }
    
    try:
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
        result = response.json()
        
        if result.get("ok"):
            return True
        else:
            print(f"❌ Telegram error: {result.get('description')}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Request error: {e}")
        return False


def main():
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID")
    
    if not token:
        print("❌ TELEGRAM_BOT_TOKEN not set")
        print("\nTo get your bot token:")
        print("  1. Message @BotFather on Telegram")
        print("  2. Send /newbot or use existing bot")
        print("  3. Copy the token")
        print("\nThen run: export TELEGRAM_BOT_TOKEN='your-token'")
        sys.exit(1)
    
    if not chat_id:
        print("❌ TELEGRAM_CHAT_ID not set")
        print("\nTo get your chat ID:")
        print("  1. Message @userinfobot on Telegram")
        print("  2. It will reply with your ID")
        print("\nThen run: export TELEGRAM_CHAT_ID='your-id'")
        sys.exit(1)
    
    # Get message from args or use default
    if len(sys.argv) > 1:
        message = " ".join(sys.argv[1:])
    else:
        message = "🎤 *Voice Control Test*\n\nThis message was sent from the voice control test script!"
    
    print("🚀 Telegram Send Test")
    print("=" * 40)
    print(f"Bot Token: {token[:10]}...{token[-5:]}")
    print(f"Chat ID: {chat_id}")
    print(f"Message: {message[:50]}...")
    print("=" * 40)
    
    print("\n📤 Sending message...")
    
    if send_telegram(token, chat_id, message):
        print("✅ Message sent successfully!")
        print("\nCheck your Telegram for the message.")
    else:
        print("❌ Failed to send message")
        sys.exit(1)


if __name__ == "__main__":
    main()
