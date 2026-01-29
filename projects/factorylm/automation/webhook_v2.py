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

# Label IDs (for auto-labeling)
LABELS = {
    "CODE": "697a8ed042cd8ccf8d1bc2e2",
    "RESEARCH": "697a8ed0c8df40fb5e71a202",
    "CONTENT": "697a8ed12c8bbc7ab215928b",
    "REVIEW": "697a8ed10d7be46e84596dca",
    "DESIGN": "697a8ed1eed1d0dc6c9d7048",
    "STALE": "697a8ed194a7347a8ab34f2c",
    "BLOCKED": "697a8ed105a7e8d6c128f94a"
}

# Custom Field IDs
CUSTOM_FIELDS = {
    "pr_link": "697a8ec5882ea0cff6ee9554",
    "est_hours": "697a8ec68ebbdac2e7e0a46c",
    "actual_hours": "697a8ec64b4e3f60badc9502",
    "priority": "697a8ec678be42720af3d01e"
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


async def add_label(card_id, label_name):
    """Add a label to a card."""
    label_id = LABELS.get(label_name.upper())
    if label_id:
        await trello_request("POST", f"/cards/{card_id}/idLabels", params={"value": label_id})
        print(f"[OK] Added label {label_name} to {card_id}")


async def auto_label_card(card_id, card_name):
    """Auto-add label based on card name [TYPE] prefix."""
    match = TASK_TYPE_PATTERN.search(card_name)
    if match:
        task_type = match.group(1).upper()
        await add_label(card_id, task_type)
        return task_type
    return None


async def set_due_date(card_id, hours_from_now=24):
    """Set due date on a card."""
    from datetime import datetime, timedelta
    due = (datetime.utcnow() + timedelta(hours=hours_from_now)).isoformat() + "Z"
    await trello_request("PUT", f"/cards/{card_id}", params={"due": due})
    print(f"[OK] Set due date {hours_from_now}h from now on {card_id}")


async def set_custom_field(card_id, field_name, value):
    """Set a custom field value on a card."""
    field_id = CUSTOM_FIELDS.get(field_name)
    if field_id:
        # Custom field value format depends on type
        if field_name in ["est_hours", "actual_hours"]:
            body = {"value": {"number": str(value)}}
        else:
            body = {"value": {"text": str(value)}}
        
        await trello_request("PUT", f"/cards/{card_id}/customField/{field_id}/item", json=body)
        print(f"[OK] Set {field_name}={value} on {card_id}")

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
    """Send task to VPS Jarvis via Telegram (system message injection)."""
    
    # Format task as a system event that VPS Jarvis will pick up
    task_msg = f"""🤖 TRELLO TASK ASSIGNED — {label}

{task}

---
Execute this task now. When done, report completion."""
    
    # Send via Telegram to the chat VPS Jarvis monitors
    # This will appear as a message that Jarvis sees and acts on
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    
    try:
        async with aiohttp.ClientSession() as session:
            # Send as a system-style message to the chat
            await session.post(url, json={
                "chat_id": TELEGRAM_CHAT_ID,
                "text": task_msg,
                "parse_mode": "Markdown"
            })
            print(f"[OK] Task sent to VPS Jarvis via Telegram: {label}")
            return {"status": "sent", "label": label}
    except Exception as e:
        print(f"[ERR] Failed to send task: {e}")
        return None

# ============================================================================
# TASK PROCESSOR
# ============================================================================

async def process_jarvis_task(card_id: str, card_name: str, card_desc: str, card_url: str):
    """Process a @jarvis task from Trello."""
    
    print(f"[TASK] Processing: {card_name}")
    start_time = datetime.now()
    
    # 1. Auto-label based on [TYPE] in name
    task_type = await auto_label_card(card_id, card_name)
    if not task_type:
        task_type = "CODE"  # Default
    
    # 2. Move to In Progress
    await move_card(card_id, "in_progress")
    
    # 3. Set due date (24 hours from now)
    await set_due_date(card_id, hours_from_now=24)
    
    # 4. Add started comment
    await add_comment(card_id, f"🤖 **Jarvis picked up this task**\n\nTask type: `{task_type}`\nStarted: {start_time.strftime('%Y-%m-%d %H:%M UTC')}\nDue: 24 hours")
    
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
        
        # Task sent to VPS Jarvis - it will work on it
        # Don't move to review yet - VPS Jarvis will do that when done
        await asyncio.sleep(2)
        
        # AGILE: Immediately check for more work (parallel processing)
        await check_backlog_for_more()
    else:
        await add_comment(card_id, "❌ **Failed to send task to Jarvis**\n\nManual intervention needed.")
        await send_failure_alert(card_name, card_url, "Task send failed")
        
        # Still check for more work even on failure
        await check_backlog_for_more()


async def check_stale_tasks():
    """Check for tasks stuck in In Progress too long (>48 hours)."""
    print("[STALE] Checking for stale tasks...")
    
    cards = await trello_request("GET", f"/lists/{LISTS['in_progress']}/cards")
    if not cards:
        return
    
    now = datetime.utcnow()
    for card in cards:
        # Check if card has been in progress > 48 hours
        last_activity = card.get("dateLastActivity", "")
        if last_activity:
            try:
                activity_time = datetime.fromisoformat(last_activity.replace("Z", ""))
                hours_since = (now - activity_time).total_seconds() / 3600
                
                if hours_since > 48:
                    card_id = card.get("id")
                    card_name = card.get("name")
                    
                    # Add STALE label
                    await add_label(card_id, "STALE")
                    await add_comment(card_id, f"⚠️ **STALE ALERT**\n\nThis task has been in progress for {int(hours_since)} hours.\n\n@jarvis status update needed!")
                    await send_telegram(f"⚠️ *STALE TASK*\n\n{card_name}\n\nIn progress for {int(hours_since)} hours!")
                    print(f"[STALE] Marked stale: {card_name}")
            except:
                pass


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
        path = self.path
        
        # Health check and manual triggers (handle both direct and proxied paths)
        if "health" in path or path == "/" or path == "/trello-webhook":
            self.send_response(200)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(b"Jarvis Trello Webhook v2 - Autonomous Mode - OK")
        
        elif "check-stale" in path:
            # Manual trigger for stale check
            self.send_response(200)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(b"Checking stale tasks...")
            
            def run_stale():
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                loop.run_until_complete(check_stale_tasks())
                loop.close()
            
            thread = threading.Thread(target=run_stale)
            thread.start()
        
        elif "check-backlog" in path:
            # Manual trigger for backlog check
            self.send_response(200)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(b"Checking backlog for @jarvis tasks...")
            
            def run_backlog():
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                loop.run_until_complete(check_backlog_for_more())
                loop.close()
            
            thread = threading.Thread(target=run_backlog)
            thread.start()
        
        else:
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
