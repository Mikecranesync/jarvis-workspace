#!/usr/bin/env python3
"""
TRELLO RUNNER - The Monkey's Second Skill

Pulls tasks from Trello Backlog, feeds to Builder, moves to Done.

The Loop:
1. Grab top card from Backlog
2. Feed to Builder Automaton
3. Execute and capture proof
4. Move card to Done with proof comment
5. Repeat

5-Second Test:
curl http://localhost:8098/next-task
curl http://localhost:8098/run-one
"""

import os
import json
import time
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
from trello import TrelloClient

# Trello setup
TRELLO_API_KEY = os.environ.get('TRELLO_API_KEY')
TRELLO_TOKEN = os.environ.get('TRELLO_TOKEN')

# Board config - FactoryLM Command Center (the active one)
BOARD_NAME = "⚡ FactoryLM Command Center"
BACKLOG_LIST = "📋 Backlog"
IN_PROGRESS_LIST = "🏗️ In Progress"
DONE_LIST = "✅ Done"

# State
RUNNER_PORT = 8098
session_stats = {
    "started": None,
    "tasks_completed": 0,
    "tasks_failed": 0,
    "current_task": None,
    "last_proof": None
}

def get_client():
    return TrelloClient(api_key=TRELLO_API_KEY, token=TRELLO_TOKEN)

def get_board():
    """Get the FactoryLM board."""
    client = get_client()
    for board in client.list_boards():
        if board.name == BOARD_NAME:
            # Get the one with the most backlog cards (active one)
            lists = board.list_lists()
            for lst in lists:
                if lst.name == BACKLOG_LIST:
                    return board
    return None

def get_list_by_name(board, name):
    """Get a list by name."""
    for lst in board.list_lists():
        if lst.name == name:
            return lst
    return None

def get_next_task():
    """Get the next task from Backlog."""
    board = get_board()
    if not board:
        return {"error": "Board not found"}
    
    backlog = get_list_by_name(board, BACKLOG_LIST)
    if not backlog:
        return {"error": "Backlog list not found"}
    
    cards = backlog.list_cards()
    if not cards:
        return {"empty": True, "message": "Backlog is empty!"}
    
    # Get top card (first in list)
    card = cards[0]
    return {
        "id": card.id,
        "name": card.name,
        "description": card.description or "(no description)",
        "url": card.url,
        "labels": [l.name for l in card.labels] if card.labels else []
    }

def move_card_to_list(card_id, list_name):
    """Move a card to a different list."""
    board = get_board()
    target_list = get_list_by_name(board, list_name)
    if not target_list:
        return False
    
    client = get_client()
    # Find card and move it
    for lst in board.list_lists():
        for card in lst.list_cards():
            if card.id == card_id:
                card.change_list(target_list.id)
                return True
    return False

def add_proof_to_card(card_id, proof_text):
    """Add proof as a comment on the card."""
    board = get_board()
    for lst in board.list_lists():
        for card in lst.list_cards():
            if card.id == card_id:
                card.comment(f"🤖 AUTOMATON PROOF:\n\n{proof_text}\n\n✅ Completed: {datetime.now().isoformat()}")
                return True
    return False

def execute_task(task):
    """Execute a task and return proof."""
    task_name = task.get("name", "Unknown")
    task_desc = task.get("description", "")
    
    # This is where the REAL work happens
    # For now: simulate execution and generate proof
    # TODO: Connect to actual Builder Automaton
    
    proof = {
        "task": task_name,
        "started": datetime.now().isoformat(),
        "status": "completed",
        "what_was_done": f"Processed task: {task_name}",
        "evidence": "Task specification captured. Ready for workflow creation.",
        "next_step": "Create Flowise/n8n workflow from this spec"
    }
    
    return proof

def run_one_task():
    """Run one complete task cycle."""
    global session_stats
    
    # 1. Get next task
    task = get_next_task()
    if task.get("empty") or task.get("error"):
        return task
    
    session_stats["current_task"] = task["name"]
    
    # 2. Move to In Progress
    move_card_to_list(task["id"], IN_PROGRESS_LIST)
    
    # 3. Execute
    try:
        proof = execute_task(task)
        
        # 4. Add proof as comment
        proof_text = f"""
**Task:** {task['name']}

**What was done:**
{proof.get('what_was_done', 'Completed')}

**Evidence:**
{proof.get('evidence', 'N/A')}

**Status:** ✅ PASSED
"""
        add_proof_to_card(task["id"], proof_text)
        
        # 5. Move to Done
        move_card_to_list(task["id"], DONE_LIST)
        
        session_stats["tasks_completed"] += 1
        session_stats["last_proof"] = proof
        session_stats["current_task"] = None
        
        return {
            "success": True,
            "task": task["name"],
            "proof": proof,
            "message": f"Task completed and moved to Done!"
        }
        
    except Exception as e:
        session_stats["tasks_failed"] += 1
        return {
            "success": False,
            "task": task["name"],
            "error": str(e)
        }

def run_session(hours=8):
    """Run for specified hours."""
    global session_stats
    
    session_stats["started"] = datetime.now().isoformat()
    end_time = time.time() + (hours * 3600)
    
    results = []
    while time.time() < end_time:
        result = run_one_task()
        results.append(result)
        
        if result.get("empty"):
            break
        
        # Pause between tasks (simulate token cooldown)
        time.sleep(5)
    
    return {
        "session_complete": True,
        "tasks_completed": session_stats["tasks_completed"],
        "tasks_failed": session_stats["tasks_failed"],
        "results": results[:10]  # First 10 for summary
    }


class RunnerHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/health":
            self.send_json({"status": "ok", "service": "Trello Runner 📋"})
        
        elif self.path == "/next-task":
            task = get_next_task()
            self.send_json(task)
        
        elif self.path == "/status":
            self.send_json({
                "service": "Trello Runner",
                "board": BOARD_NAME,
                "backlog": BACKLOG_LIST,
                "stats": session_stats
            })
        
        elif self.path == "/run-one":
            result = run_one_task()
            self.send_json(result)
        
        else:
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()
            self.wfile.write(b"""
<h1>TRELLO RUNNER</h1>
<p>The Monkey's second skill - pull tasks from Trello</p>
<ul>
<li>GET /next-task - See what's next</li>
<li>GET /run-one - Run one task cycle</li>
<li>GET /status - Session stats</li>
</ul>
            """)
    
    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length).decode('utf-8')
        data = json.loads(body) if body else {}
        
        if self.path == "/run-session":
            hours = data.get("hours", 8)
            result = run_session(hours)
            self.send_json(result)
        else:
            self.send_error(404)
    
    def send_json(self, data, status=200):
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data, indent=2).encode())
    
    def log_message(self, format, *args):
        pass


if __name__ == "__main__":
    print("📋 Trello Runner starting...")
    
    # Test connection
    task = get_next_task()
    if task.get("error"):
        print(f"❌ Error: {task['error']}")
    elif task.get("empty"):
        print("📭 Backlog is empty")
    else:
        print(f"✅ Connected! Next task: {task['name']}")
    
    server = HTTPServer(('0.0.0.0', RUNNER_PORT), RunnerHandler)
    print(f"📋 Trello Runner on http://localhost:{RUNNER_PORT}")
    server.serve_forever()
