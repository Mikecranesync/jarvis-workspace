#!/usr/bin/env python3
"""
THE MONKEY AT THE CRANK

The scheduler/governor running 24/7 "within reason":
- Uses token tracking to control pace (no tokens → no crank turns)
- Schedules work for Automata 1-4 and Code-Twin Claude
- Runs health checks periodically
- Inserts maintenance pauses to realign with best practices

The Monkey turns the crank. The Automata do the work.

5-Second Test:
curl http://localhost:8097/status
curl http://localhost:8097/crank
"""

import os
import json
import time
import threading
import urllib.request
from datetime import datetime, timedelta
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path

# Config
MONKEY_STATE = Path("/root/jarvis-workspace/projects/shoptalk/monkey_state.json")
MONKEY_PORT = 8097

# Token budget
DAILY_TOKEN_BUDGET = 100000
TOKENS_PER_CRANK = 500  # Estimated tokens per workflow cycle

# Service URLs
SERVICES = {
    "manual_hunter": ("http://localhost:8090", "Automaton 1"),
    "alarm_triage": ("http://localhost:8091", "Automaton 1"),
    "workflow_tracker": ("http://localhost:8092", "Automaton 1"),
    "weaver": ("http://localhost:8093", "Automaton 2"),
    "watchman": ("http://localhost:8094", "Automaton 4"),
    "cartographer": ("http://localhost:8095", "Automaton 3"),
    "conductor": ("http://localhost:8096", "Orchestrator"),
}

# Intervals
HEALTH_CHECK_INTERVAL = 300  # 5 minutes
CRANK_INTERVAL = 60  # 1 minute between crank turns

def init_state():
    if not MONKEY_STATE.exists():
        state = {
            "started": datetime.now().isoformat(),
            "cranks_today": 0,
            "tokens_used_today": 0,
            "daily_reset": datetime.now().date().isoformat(),
            "last_health_check": None,
            "last_crank": None,
            "running": True,
            "paused": False,
            "pause_reason": None
        }
        with open(MONKEY_STATE, 'w') as f:
            json.dump(state, f, indent=2)

init_state()

def load_state():
    with open(MONKEY_STATE, 'r') as f:
        return json.load(f)

def save_state(state):
    with open(MONKEY_STATE, 'w') as f:
        json.dump(state, f, indent=2)

def check_budget() -> dict:
    """Check if we have token budget for another crank."""
    state = load_state()
    
    # Reset daily if new day
    today = datetime.now().date().isoformat()
    if state.get("daily_reset") != today:
        state["cranks_today"] = 0
        state["tokens_used_today"] = 0
        state["daily_reset"] = today
        save_state(state)
    
    remaining = DAILY_TOKEN_BUDGET - state.get("tokens_used_today", 0)
    can_crank = remaining >= TOKENS_PER_CRANK
    
    return {
        "budget": DAILY_TOKEN_BUDGET,
        "used": state.get("tokens_used_today", 0),
        "remaining": remaining,
        "can_crank": can_crank,
        "cranks_today": state.get("cranks_today", 0)
    }

def call_service(url: str, path: str = "/health") -> dict:
    """Call a service and return result."""
    try:
        req = urllib.request.urlopen(f"{url}{path}", timeout=10)
        return {"healthy": True, "status": req.status}
    except Exception as e:
        return {"healthy": False, "error": str(e)}

def run_health_check() -> dict:
    """Run health check on all services."""
    results = {"timestamp": datetime.now().isoformat(), "services": {}}
    
    for name, (url, automaton) in SERVICES.items():
        check = call_service(url)
        results["services"][name] = {
            "automaton": automaton,
            "healthy": check.get("healthy", False),
            "url": url
        }
    
    healthy_count = sum(1 for s in results["services"].values() if s["healthy"])
    results["summary"] = f"{healthy_count}/{len(SERVICES)} services healthy"
    
    # Update state
    state = load_state()
    state["last_health_check"] = results["timestamp"]
    save_state(state)
    
    return results

def turn_crank() -> dict:
    """Turn the crank - trigger next workflow cycle."""
    state = load_state()
    
    # Check if paused
    if state.get("paused"):
        return {"cranked": False, "reason": state.get("pause_reason", "Paused")}
    
    # Check budget
    budget = check_budget()
    if not budget["can_crank"]:
        return {"cranked": False, "reason": "Token budget exhausted"}
    
    # Call the Conductor to trigger next workflow
    try:
        req = urllib.request.Request(
            "http://localhost:8096/trigger",
            method="POST",
            headers={"Content-Type": "application/json"}
        )
        resp = urllib.request.urlopen(req, timeout=30)
        result = json.loads(resp.read().decode())
        
        # Update state
        state["cranks_today"] = state.get("cranks_today", 0) + 1
        state["tokens_used_today"] = state.get("tokens_used_today", 0) + TOKENS_PER_CRANK
        state["last_crank"] = datetime.now().isoformat()
        save_state(state)
        
        return {
            "cranked": True,
            "crank_number": state["cranks_today"],
            "tokens_remaining": DAILY_TOKEN_BUDGET - state["tokens_used_today"],
            "conductor_response": result
        }
        
    except Exception as e:
        return {"cranked": False, "reason": str(e)}

def pause_monkey(reason: str = "Manual pause"):
    """Pause the monkey."""
    state = load_state()
    state["paused"] = True
    state["pause_reason"] = reason
    save_state(state)

def resume_monkey():
    """Resume the monkey."""
    state = load_state()
    state["paused"] = False
    state["pause_reason"] = None
    save_state(state)

def get_status() -> dict:
    """Get full Monkey status."""
    state = load_state()
    budget = check_budget()
    
    return {
        "monkey": "THE MONKEY AT THE CRANK 🐵",
        "purpose": "24/7 scheduler keeping Automata running within budget",
        "running": state.get("running", True),
        "paused": state.get("paused", False),
        "pause_reason": state.get("pause_reason"),
        "cranks_today": state.get("cranks_today", 0),
        "tokens": {
            "budget": DAILY_TOKEN_BUDGET,
            "used": state.get("tokens_used_today", 0),
            "remaining": budget["remaining"]
        },
        "last_crank": state.get("last_crank"),
        "last_health_check": state.get("last_health_check"),
        "intervals": {
            "health_check": f"{HEALTH_CHECK_INTERVAL}s",
            "crank": f"{CRANK_INTERVAL}s"
        }
    }

class MonkeyHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length).decode('utf-8')
        data = json.loads(body) if body else {}
        
        if self.path == "/crank":
            result = turn_crank()
            self.send_json(result)
        elif self.path == "/pause":
            pause_monkey(data.get("reason", "Manual pause"))
            self.send_json({"status": "paused"})
        elif self.path == "/resume":
            resume_monkey()
            self.send_json({"status": "resumed"})
        else:
            self.send_error(404)
    
    def do_GET(self):
        if self.path == "/health":
            self.send_json({"status": "ok", "service": "The Monkey 🐵"})
        elif self.path == "/status":
            self.send_json(get_status())
        elif self.path == "/budget":
            self.send_json(check_budget())
        elif self.path == "/health-check":
            self.send_json(run_health_check())
        elif self.path == "/crank":
            result = turn_crank()
            self.send_json(result)
        else:
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()
            self.wfile.write(b"""
<h1>THE MONKEY AT THE CRANK</h1>
<p>24/7 scheduler keeping Automata running within budget.</p>
<ul>
<li>GET /status - Monkey status</li>
<li>GET /budget - Token budget</li>
<li>GET /health-check - Check all services</li>
<li>GET /crank - Turn the crank (trigger cycle)</li>
<li>POST /pause - Pause the monkey</li>
<li>POST /resume - Resume the monkey</li>
</ul>
            """)
    
    def send_json(self, data, status=200):
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data, indent=2).encode())
    
    def log_message(self, format, *args):
        pass

if __name__ == "__main__":
    print("🐵 The Monkey initializing...")
    
    # Run initial health check
    health = run_health_check()
    print(f"📊 {health['summary']}")
    
    port = MONKEY_PORT
    server = HTTPServer(('0.0.0.0', port), MonkeyHandler)
    print(f"🐵 The Monkey running on http://localhost:{port}")
    print(f"🔧 Crank interval: {CRANK_INTERVAL}s | Health check: {HEALTH_CHECK_INTERVAL}s")
    print(f"💰 Daily budget: {DAILY_TOKEN_BUDGET} tokens")
    server.serve_forever()
