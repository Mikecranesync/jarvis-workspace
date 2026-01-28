"""
Trello Webhook Receiver for Jarvis
Listens for Trello board activity, filters for @jarvis mentions,
and forwards them to Telegram via bot API.
"""
import json
import os
import re
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.request
import urllib.parse
from datetime import datetime

# Config
PORT = 8078
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = "8445149012"  # Mike
TRIGGER_PATTERN = re.compile(r'@jarvis\b', re.IGNORECASE)

def send_telegram(text):
    """Send message to Mike via Telegram bot API."""
    if not TELEGRAM_BOT_TOKEN:
        print(f"[WARN] No TELEGRAM_BOT_TOKEN set, would send: {text[:100]}")
        return
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = urllib.parse.urlencode({
        "chat_id": TELEGRAM_CHAT_ID,
        "text": text,
        "parse_mode": "Markdown"
    }).encode()
    try:
        req = urllib.request.Request(url, data=data, method="POST")
        urllib.request.urlopen(req, timeout=10)
        print(f"[OK] Telegram sent")
    except Exception as e:
        print(f"[ERR] Telegram send failed: {e}")


def extract_trello_event(body):
    """Parse Trello webhook payload, return (event_type, card_name, text, member, url) or None."""
    try:
        action = body.get("action", {})
        action_type = action.get("type", "")
        member = action.get("memberCreator", {}).get("fullName", "Unknown")
        
        data = action.get("data", {})
        card = data.get("card", {})
        card_name = card.get("name", "")
        card_url = f"https://trello.com/c/{card.get('shortLink', '')}" if card.get("shortLink") else ""
        
        # Comment added
        if action_type == "commentCard":
            text = data.get("text", "")
            return ("comment", card_name, text, member, card_url)
        
        # Card created
        if action_type == "createCard":
            return ("card_created", card_name, card.get("desc", ""), member, card_url)
        
        # Card description updated
        if action_type == "updateCard" and "desc" in data.get("old", {}):
            new_desc = data.get("card", {}).get("desc", "")
            return ("card_updated", card_name, new_desc, member, card_url)
        
        # Card name updated
        if action_type == "updateCard" and "name" in data.get("old", {}):
            return ("card_renamed", card_name, card_name, member, card_url)
        
        return None
    except Exception as e:
        print(f"[ERR] Parse error: {e}")
        return None


class WebhookHandler(BaseHTTPRequestHandler):
    def do_HEAD(self):
        """Trello sends HEAD to verify webhook URL exists."""
        self.send_response(200)
        self.end_headers()
    
    def do_GET(self):
        """Health check."""
        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write(b"Jarvis Trello Webhook - OK")
    
    def do_POST(self):
        """Receive Trello webhook events."""
        content_length = int(self.headers.get("Content-Length", 0))
        body_raw = self.rfile.read(content_length)
        
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"OK")
        
        print(f"[DEBUG] Raw body ({content_length} bytes): {body_raw[:500]}")
        
        if content_length == 0:
            print("[INFO] Empty body (likely HEAD verification)")
            return
        
        try:
            body = json.loads(body_raw)
        except json.JSONDecodeError as e:
            print(f"[WARN] Invalid JSON: {e}")
            return
        
        event = extract_trello_event(body)
        if not event:
            return
        
        event_type, card_name, text, member, card_url = event
        
        # Check for @jarvis mention
        check_text = f"{card_name} {text}"
        if not TRIGGER_PATTERN.search(check_text):
            return
        
        # Strip @jarvis from the text for cleaner display
        clean_text = TRIGGER_PATTERN.sub("", text).strip()
        
        timestamp = datetime.now().strftime("%H:%M")
        
        if event_type == "comment":
            msg = f"📋 *Trello @jarvis* ({timestamp})\n\n*Card:* {card_name}\n*From:* {member}\n*Message:* {clean_text}\n\n{card_url}"
        elif event_type == "card_created":
            msg = f"📋 *Trello @jarvis* ({timestamp})\n\n*New card:* {card_name}\n*From:* {member}\n{f'*Details:* {clean_text}' if clean_text else ''}\n\n{card_url}"
        else:
            msg = f"📋 *Trello @jarvis* ({timestamp})\n\n*Card updated:* {card_name}\n*From:* {member}\n*Content:* {clean_text}\n\n{card_url}"
        
        print(f"[TRIGGER] @jarvis in {event_type} on '{card_name}'")
        send_telegram(msg)
    
    def log_message(self, format, *args):
        """Custom logging."""
        print(f"[{datetime.now().strftime('%H:%M:%S')}] {format % args}")


if __name__ == "__main__":
    print(f"🤖 Jarvis Trello Webhook starting on port {PORT}")
    server = HTTPServer(("0.0.0.0", PORT), WebhookHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down...")
        server.server_close()
