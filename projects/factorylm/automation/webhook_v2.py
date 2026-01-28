#!/usr/bin/env python3
"""
Trello Webhook Handler v2 — Autonomous Task Processor

When a card with @jarvis is created/updated:
1. Move to "In Progress"
2. Spawn sub-agent to do the work
3. Post results back to card
4. Move to "Review"
5. Notify Mike

Deploy: scp to VPS, replace /opt/trello-webhook/trello_webhook.py
"""

import json
import os
import re
import asyncio
import aiohttp
from http.server import HTTPServer, BaseHTTPRequestHandler
from datetime import datetime
import threading

# ============================================================================
# CONFIG
# ============================================================================

PORT = 8078
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "8387943893:AAEynugW3SP1sWs6An4aNgZParSSRBlWSJk")
TELEGRAM_CHAT_ID = "8445149012"
CLAWDBOT_URL = "http://localhost:18789"  # Local gateway
CLAWDBOT_TOKEN = os.environ.get("CLAWDBOT_TOKEN", "e4d794504a4e47459ac08b26f5c668677aae6088d7f6a841")

TRELLO_KEY = "55029ab0628e6d7ddc1d15bfbe73222f"
TRELLO_TOKEN = os.environ.get("TRELLO_TOKEN", "ATTA21c9138e8d7ddbdde41f94a969cdab79ec966d5875f4f4b286cdd14d2c7083bb6510E2EF")

# List IDs
LISTS = {
    "backlog": "697a8a56b001de1b06c33b76",
    "in_progress": "697a8a57dc04278fbe0b2c68",
    "review": "697a8a57cd3ec2048393bcc2",
    "done": "6979293917d20accb7228e84"
}

TRIGGER_PATTERN = re.compile(r'@jarvis\b', re.IGNORECASE)
TASK_TYPE_PATTERN = re.compile(r'\[(CODE|RESEARCH|CONTENT|REVIEW|DESIGN)\]', re.IGNORECASE)

# ============================================================================
# TRELLO API
# ============================================================================

async def trello_request(method, endpoint, **kwargs):
    """Make Trello API request."""
    url = f"https://api.trello.com/1{endpoint}"
    params = kwargs.get("params", {})
    params["key"] = TRELLO_KEY
    params["token"] = TRELLO_TOKEN
    
    async with aiohttp.ClientSession() as session:
        async with session.request(method, url, params=params, json=kwargs.get("json")) as resp:
            if resp.status in (200, 201):
                return await resp.json()
            else:
                print(f"[ERR] Trello {method} {endpoint}: {resp.status}")
                return None

async def move_card(card_id, list_name):
    """Move card to a list."""
    list_id = LISTS.get(list_name)
    if list_id:
        await trello_request("PUT", f"/cards/{card_id}", params={"idList": list_id})
        print(f"[OK] Moved card {card_id} to {list_name}")

async def add_comment(card_id, text):
    """Add comment to card."""
    await trello_request("POST", f"/cards/{card_id}/actions/comments", params={"text": text})
    print(f"[OK] Added comment to {card_id}")

async def get_card(card_id):
    """Get card details."""
    return await trello_request("GET", f"/cards/{card_id}")

# ============================================================================
# TELEGRAM
# ============================================================================

async def send_telegram(text):
    """Send message to Mike."""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    try:
        async with aiohttp.ClientSession() as session:
            await session.post(url, json={
                "chat_id": TELEGRAM_CHAT_ID,
                "text": text,
                "parse_mode": "Markdown"
            })
        print(f"[OK] Telegram sent")
    except Exception as e:
        print(f"[ERR] Telegram failed: {e}")


async def send_completion_alert(card_name: str, card_url: str, pr_url: str = None, status: str = "Ready for Review", duration: str = "N/A"):
    """Send completion alert to Mike."""
    if pr_url:
        text = f"""✅ *TASK COMPLETED*

📋 {card_name}
🔗 [Trello]({card_url})
🔀 [PR]({pr_url})
📊 Status: {status}

⏱️ Duration: {duration}"""
    else:
        text = f"""✅ *TASK COMPLETED*

📋 {card_name}
🔗 [Trello]({card_url})
📊 Status: {status}

⏱️ Duration: {duration}"""
    
    await send_telegram(text)


async def send_failure_alert(card_name: str, card_url: str, error: str):
    """Send failure alert to Mike."""
    text = f"""❌ *TASK FAILED*

📋 {card_name}
🔗 [Trello]({card_url})
⚠️ Error: {error}

Needs manual intervention."""
    
    await send_telegram(text)

# ============================================================================
# CLAWDBOT SUB-AGENT
# ============================================================================

async def spawn_subagent(task: str, label: str, task_type: str = "CODE"):
    """Spawn a Clawdbot sub-agent to do the work."""
    
    # Select model based on task type
    model = {
        "CODE": "anthropic/claude-sonnet-4-20250514",
        "RESEARCH": "google/gemini-2.5-flash",
        "CONTENT": "anthropic/claude-sonnet-4-20250514",
        "REVIEW": "anthropic/claude-sonnet-4-20250514",
        "DESIGN": "anthropic/claude-sonnet-4-20250514"
    }.get(task_type.upper(), "anthropic/claude-sonnet-4-20250514")
    
    url = f"{CLAWDBOT_URL}/api/sessions/spawn"
    headers = {"Authorization": f"Bearer {CLAWDBOT_TOKEN}"}
    
    payload = {
        "task": task,
        "label": label,
        "model": model,
        "runTimeoutSeconds": 1800,  # 30 min max
        "cleanup": "keep"
    }
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, json=payload) as resp:
                if resp.status == 200:
                    result = await resp.json()
                    print(f"[OK] Sub-agent spawned: {label}")
                    return result
                else:
                    text = await resp.text()
                    print(f"[ERR] Spawn failed: {resp.status} - {text}")
                    return None
    except Exception as e:
        print(f"[ERR] Spawn error: {e}")
        return None

# ============================================================================
# TASK PROCESSOR
# ============================================================================

async def process_jarvis_task(card_id: str, card_name: str, card_desc: str, card_url: str):
    """Process a @jarvis task from Trello."""
    
    print(f"[TASK] Processing: {card_name}")
    
    # 1. Extract task type
    match = TASK_TYPE_PATTERN.search(card_name)
    task_type = match.group(1).upper() if match else "CODE"
    
    # 2. Move to In Progress
    await move_card(card_id, "in_progress")
    await add_comment(card_id, f"🤖 **Jarvis picked up this task**\n\nTask type: `{task_type}`\nStarted: {datetime.now().strftime('%Y-%m-%d %H:%M UTC')}")
    
    # 3. Build prompt with CI/CD workflow
    short_id = card_id[:8]
    branch_name = f"feature/trello-{short_id}"
    
    prompt = f"""You are working on a task from the FactoryLM Trello board.

## Task
**{card_name}**

{card_desc}

## CI/CD Workflow (REQUIRED)
Follow this Git workflow:

1. **Create branch:**
   ```bash
   cd ~/clawd/projects/factorylm
   git checkout main && git pull
   git checkout -b {branch_name}
   ```

2. **Do the work:**
   - Complete all deliverables listed
   - Write code to appropriate locations
   - Test your changes

3. **Commit with clear message:**
   ```bash
   git add .
   git commit -m "feat: {card_name}
   
   Trello: {card_url}
   - [list what you did]"
   ```

4. **Push and create PR:**
   ```bash
   git push -u origin {branch_name}
   gh pr create --title "{card_name}" --body "Trello: {card_url}" --base main
   ```

5. **Report back:**
   - PR URL
   - Summary of changes
   - Any blockers

Start working now. Use the Git workflow above.
"""
    
    # 4. Notify Mike - Task Started
    await send_telegram(f"🤖 *Task Started*\n\n📋 {card_name}\n🌿 Branch: `{branch_name}`\n🔗 {card_url}")
    
    # 5. Spawn sub-agent
    label = f"trello-{card_id[:8]}"
    result = await spawn_subagent(prompt, label, task_type)
    
    if result:
        # 6. Wait for completion and post results
        # Note: In production, this would poll the session or use a callback
        await add_comment(card_id, f"🔄 **Sub-agent working**\n\nSession: `{label}`\nModel: `{task_type}`\n\n_Results will be posted when complete._")
        
        # Move to review after spawning
        await asyncio.sleep(5)
        await move_card(card_id, "review")
        await send_completion_alert(card_name, card_url, status="Sub-agent Working", duration="In Progress")
        
        # AGILE: Immediately check for more work
        await check_backlog_for_more()
    else:
        await add_comment(card_id, "❌ **Failed to spawn sub-agent**\n\nManual intervention needed.")
        await send_failure_alert(card_name, card_url, "Sub-agent spawn failed (405)")
        
        # Still check for more work even on failure
        await check_backlog_for_more()


async def check_backlog_for_more():
    """Agile: Check backlog for more @jarvis tasks and process them."""
    print("[AGILE] Checking backlog for more tasks...")
    
    cards = await trello_request("GET", f"/lists/{LISTS['backlog']}/cards")
    if not cards:
        print("[AGILE] No cards in backlog")
        return
    
    for card in cards:
        card_desc = card.get("desc", "")
        if TRIGGER_PATTERN.search(card_desc):
            card_id = card.get("id")
            card_name = card.get("name")
            card_url = f"https://trello.com/c/{card.get('shortLink', '')}"
            
            print(f"[AGILE] Found task: {card_name}")
            await process_jarvis_task(card_id, card_name, card_desc, card_url)
            return  # Process one at a time, recursion handles the rest
    
    print("[AGILE] No more @jarvis tasks in backlog")

# ============================================================================
# WEBHOOK HANDLER
# ============================================================================

def extract_trello_event(body):
    """Parse Trello webhook payload."""
    try:
        action = body.get("action", {})
        action_type = action.get("type", "")
        data = action.get("data", {})
        card = data.get("card", {})
        
        card_id = card.get("id", "")
        card_name = card.get("name", "")
        card_desc = card.get("desc", "")
        card_url = f"https://trello.com/c/{card.get('shortLink', '')}" if card.get("shortLink") else ""
        
        # Check for @jarvis trigger
        text_to_check = ""
        
        if action_type == "createCard":
            text_to_check = card_name + " " + card_desc
        elif action_type == "commentCard":
            text_to_check = data.get("text", "")
        elif action_type == "updateCard":
            if "desc" in data.get("old", {}):
                text_to_check = card_desc
        
        if TRIGGER_PATTERN.search(text_to_check):
            return (card_id, card_name, card_desc, card_url)
        
        return None
    except Exception as e:
        print(f"[ERR] Parse error: {e}")
        return None


class WebhookHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        print(f"[HTTP] {args[0]}")
    
    def do_HEAD(self):
        self.send_response(200)
        self.end_headers()
    
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write(b"Jarvis Trello Webhook v2 - Autonomous Mode")
    
    def do_POST(self):
        content_length = int(self.headers.get("Content-Length", 0))
        body_raw = self.rfile.read(content_length)
        
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"OK")
        
        if content_length == 0:
            return
        
        try:
            body = json.loads(body_raw)
            event = extract_trello_event(body)
            
            if event:
                card_id, card_name, card_desc, card_url = event
                print(f"[TRIGGER] @jarvis detected: {card_name}")
                
                # Process async in background
                def run_async():
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    loop.run_until_complete(process_jarvis_task(card_id, card_name, card_desc, card_url))
                    loop.close()
                
                thread = threading.Thread(target=run_async)
                thread.start()
                
        except Exception as e:
            print(f"[ERR] POST handler: {e}")


# ============================================================================
# MAIN
# ============================================================================

def main():
    print(f"🤖 Jarvis Trello Webhook v2 starting on port {PORT}")
    print(f"   Telegram: {TELEGRAM_CHAT_ID}")
    print(f"   Clawdbot: {CLAWDBOT_URL}")
    print(f"   Autonomous mode: ENABLED")
    
    server = HTTPServer(("0.0.0.0", PORT), WebhookHandler)
    server.serve_forever()

if __name__ == "__main__":
    main()
