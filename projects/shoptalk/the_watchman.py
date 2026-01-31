#!/usr/bin/env python3
"""
THE WATCHMAN (Automaton 4)

Watches runtime behavior of all deployed workflows:
- Logs, token usage, errors, latency, success/failure
- Detects drift, hallucination risks, brittle edges
- Opens "maintenance tickets" back to Automaton 1 & 2 when:
  - A workflow fails tests
  - Answers look implausible
  - Token cost is too high
  - User feedback is bad

Keeps products durable, safe, and economically sensible.

5-Second Test:
curl http://localhost:8094/status
curl http://localhost:8094/health-check
curl http://localhost:8094/tickets
"""

import os
import json
import time
import urllib.request
from datetime import datetime, timedelta
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path
from collections import defaultdict

# Config
WATCHMAN_STATE = Path("/root/jarvis-workspace/projects/shoptalk/watchman_state.json")
TICKETS_FILE = Path("/root/jarvis-workspace/projects/shoptalk/maintenance_tickets.json")

# Services to monitor
SERVICES = {
    "manual_hunter": {"url": "http://localhost:8090", "budget_per_call": 500},
    "alarm_triage": {"url": "http://localhost:8091", "budget_per_call": 1000},
    "workflow_tracker": {"url": "http://localhost:8092", "budget_per_call": 200},
    "the_weaver": {"url": "http://localhost:8093", "budget_per_call": 2000},
}

# Thresholds
TOKEN_BUDGET_DAILY = 100000  # Daily token budget
LATENCY_THRESHOLD_MS = 5000  # 5 seconds max
ERROR_RATE_THRESHOLD = 0.1  # 10% error rate triggers alert
HALLUCINATION_KEYWORDS = ["might be", "possibly", "i think", "maybe", "not sure", "could be"]

# Initialize state
def init_state():
    if not WATCHMAN_STATE.exists():
        initial_state = {
            "started": datetime.now().isoformat(),
            "checks_run": 0,
            "services": {},
            "daily_tokens": 0,
            "daily_reset": datetime.now().date().isoformat(),
            "alerts": []
        }
        with open(WATCHMAN_STATE, 'w') as f:
            json.dump(initial_state, f, indent=2)
    
    if not TICKETS_FILE.exists():
        with open(TICKETS_FILE, 'w') as f:
            json.dump({"tickets": [], "next_id": 1}, f, indent=2)

init_state()

def load_state():
    with open(WATCHMAN_STATE, 'r') as f:
        return json.load(f)

def save_state(state):
    with open(WATCHMAN_STATE, 'w') as f:
        json.dump(state, f, indent=2)

def load_tickets():
    with open(TICKETS_FILE, 'r') as f:
        return json.load(f)

def save_tickets(tickets_data):
    with open(TICKETS_FILE, 'w') as f:
        json.dump(tickets_data, f, indent=2)

def check_service_health(name: str, config: dict) -> dict:
    """Check a single service's health."""
    result = {
        "service": name,
        "timestamp": datetime.now().isoformat(),
        "healthy": False,
        "latency_ms": None,
        "error": None
    }
    
    try:
        start = time.time()
        req = urllib.request.urlopen(f"{config['url']}/health", timeout=10)
        latency = (time.time() - start) * 1000
        
        result["healthy"] = req.status == 200
        result["latency_ms"] = round(latency, 2)
        
        # Check latency threshold
        if latency > LATENCY_THRESHOLD_MS:
            result["warning"] = f"High latency: {latency:.0f}ms > {LATENCY_THRESHOLD_MS}ms threshold"
            
    except Exception as e:
        result["error"] = str(e)
        result["healthy"] = False
    
    return result

def detect_hallucination_risk(text: str) -> dict:
    """Check if a response might be hallucinated."""
    text_lower = text.lower()
    
    risks = []
    for keyword in HALLUCINATION_KEYWORDS:
        if keyword in text_lower:
            risks.append(f"Contains vague language: '{keyword}'")
    
    # Check for missing citations
    if "page" not in text_lower and "manual" not in text_lower:
        risks.append("No citation to manual or page number")
    
    # Check for specific actions (good sign)
    action_words = ["check", "verify", "inspect", "measure", "replace", "reset"]
    has_actions = any(word in text_lower for word in action_words)
    if not has_actions:
        risks.append("No specific actionable steps")
    
    return {
        "risk_level": "HIGH" if len(risks) >= 2 else "MEDIUM" if len(risks) == 1 else "LOW",
        "risks": risks,
        "grounded": len(risks) == 0
    }

def create_ticket(title: str, severity: str, source: str, details: dict) -> dict:
    """Create a maintenance ticket."""
    tickets_data = load_tickets()
    
    ticket = {
        "id": tickets_data["next_id"],
        "title": title,
        "severity": severity,  # CRITICAL, HIGH, MEDIUM, LOW
        "source": source,  # Which automaton detected it
        "status": "OPEN",
        "created": datetime.now().isoformat(),
        "details": details,
        "assigned_to": "Automaton 1 & 2"  # For spec & weaver to fix
    }
    
    tickets_data["tickets"].append(ticket)
    tickets_data["next_id"] += 1
    save_tickets(tickets_data)
    
    return ticket

def run_health_checks() -> dict:
    """Run health checks on all services."""
    state = load_state()
    results = {
        "timestamp": datetime.now().isoformat(),
        "services": {},
        "overall_health": True,
        "alerts": []
    }
    
    for name, config in SERVICES.items():
        check = check_service_health(name, config)
        results["services"][name] = check
        
        if not check["healthy"]:
            results["overall_health"] = False
            results["alerts"].append(f"{name} is DOWN")
            
            # Create ticket for down service
            create_ticket(
                title=f"Service {name} is DOWN",
                severity="CRITICAL",
                source="The Watchman",
                details=check
            )
        
        elif check.get("warning"):
            results["alerts"].append(check["warning"])
            create_ticket(
                title=f"Service {name} has high latency",
                severity="MEDIUM",
                source="The Watchman",
                details=check
            )
    
    # Update state
    state["checks_run"] += 1
    state["services"] = results["services"]
    state["alerts"] = results["alerts"]
    save_state(state)
    
    return results

def check_token_budget() -> dict:
    """Check if we're within token budget."""
    state = load_state()
    
    # Reset daily if new day
    today = datetime.now().date().isoformat()
    if state.get("daily_reset") != today:
        state["daily_tokens"] = 0
        state["daily_reset"] = today
        save_state(state)
    
    # Try to get actual token usage from workflow tracker
    try:
        req = urllib.request.urlopen("http://localhost:8092/report", timeout=5)
        data = json.loads(req.read().decode())
        total_tokens = data.get("total_tokens_used", 0)
    except:
        total_tokens = state.get("daily_tokens", 0)
    
    budget_used = (total_tokens / TOKEN_BUDGET_DAILY) * 100
    
    result = {
        "daily_budget": TOKEN_BUDGET_DAILY,
        "tokens_used": total_tokens,
        "budget_used_percent": round(budget_used, 1),
        "status": "OK" if budget_used < 80 else "WARNING" if budget_used < 100 else "EXCEEDED"
    }
    
    if result["status"] == "EXCEEDED":
        create_ticket(
            title="Daily token budget exceeded",
            severity="HIGH",
            source="The Watchman",
            details=result
        )
    elif result["status"] == "WARNING":
        create_ticket(
            title="Token budget at 80%",
            severity="LOW",
            source="The Watchman",
            details=result
        )
    
    return result

def test_workflow_grounding() -> dict:
    """Test a workflow and check for hallucination."""
    # Run a test question through The Weaver
    test_cases = [
        {"question": "Why did my machine stop?", "context": "Siemens V20 F0001"},
        {"question": "What causes overcurrent?", "context": "VFD drive"},
    ]
    
    results = []
    for test in test_cases:
        try:
            req = urllib.request.Request(
                "http://localhost:8093/test",
                data=json.dumps(test).encode(),
                headers={'Content-Type': 'application/json'}
            )
            resp = urllib.request.urlopen(req, timeout=30)
            data = json.loads(resp.read().decode())
            
            # Check the reality check results
            reality = data.get("reality_check", {})
            
            test_result = {
                "test": test,
                "passed": reality.get("grounded", False),
                "score": reality.get("score", "0/0"),
                "verdict": reality.get("verdict", "UNKNOWN")
            }
            
            if not test_result["passed"]:
                create_ticket(
                    title=f"Workflow failed grounding test",
                    severity="HIGH",
                    source="The Watchman",
                    details=test_result
                )
            
            results.append(test_result)
            
        except Exception as e:
            results.append({
                "test": test,
                "passed": False,
                "error": str(e)
            })
    
    return {
        "tests_run": len(results),
        "tests_passed": sum(1 for r in results if r.get("passed")),
        "results": results
    }

def get_watchman_status() -> dict:
    """Get full Watchman status."""
    state = load_state()
    tickets_data = load_tickets()
    
    open_tickets = [t for t in tickets_data["tickets"] if t["status"] == "OPEN"]
    
    return {
        "watchman": "THE WATCHMAN (Automaton 4)",
        "purpose": "Monitor runtime, detect drift, open maintenance tickets",
        "started": state.get("started"),
        "checks_run": state.get("checks_run", 0),
        "daily_budget": f"{state.get('daily_tokens', 0)}/{TOKEN_BUDGET_DAILY} tokens",
        "open_tickets": len(open_tickets),
        "services_monitored": len(SERVICES),
        "thresholds": {
            "latency_ms": LATENCY_THRESHOLD_MS,
            "error_rate": ERROR_RATE_THRESHOLD,
            "daily_token_budget": TOKEN_BUDGET_DAILY
        }
    }

class WatchmanHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length).decode('utf-8')
        
        try:
            data = json.loads(body) if body else {}
            
            if self.path == "/check-hallucination":
                text = data.get("text", "")
                result = detect_hallucination_risk(text)
                self.send_json(result)
                
            elif self.path == "/create-ticket":
                ticket = create_ticket(
                    title=data.get("title", "Manual ticket"),
                    severity=data.get("severity", "MEDIUM"),
                    source=data.get("source", "Manual"),
                    details=data.get("details", {})
                )
                self.send_json(ticket)
                
            elif self.path == "/close-ticket":
                ticket_id = data.get("id")
                tickets_data = load_tickets()
                for t in tickets_data["tickets"]:
                    if t["id"] == ticket_id:
                        t["status"] = "CLOSED"
                        t["closed"] = datetime.now().isoformat()
                save_tickets(tickets_data)
                self.send_json({"status": "closed", "id": ticket_id})
                
            else:
                self.send_error(404)
                
        except Exception as e:
            self.send_json({"error": str(e)}, 500)
    
    def do_GET(self):
        if self.path == "/health":
            self.send_json({"status": "ok", "service": "The Watchman"})
            
        elif self.path == "/status":
            self.send_json(get_watchman_status())
            
        elif self.path == "/health-check":
            results = run_health_checks()
            self.send_json(results)
            
        elif self.path == "/budget":
            self.send_json(check_token_budget())
            
        elif self.path == "/grounding-test":
            self.send_json(test_workflow_grounding())
            
        elif self.path == "/tickets":
            tickets_data = load_tickets()
            open_tickets = [t for t in tickets_data["tickets"] if t["status"] == "OPEN"]
            self.send_json({"open": len(open_tickets), "tickets": open_tickets})
            
        elif self.path == "/all-tickets":
            self.send_json(load_tickets())
            
        else:
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()
            self.wfile.write(b"""
<h1>THE WATCHMAN (Automaton 4)</h1>
<p>Monitors runtime, detects drift, opens maintenance tickets.</p>
<ul>
<li>GET /status - Watchman status</li>
<li>GET /health-check - Run health checks on all services</li>
<li>GET /budget - Check token budget</li>
<li>GET /grounding-test - Test workflow for hallucinations</li>
<li>GET /tickets - View open maintenance tickets</li>
<li>POST /check-hallucination - Check text for hallucination risk</li>
<li>POST /create-ticket - Create maintenance ticket</li>
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
    print("👁️ The Watchman initializing...")
    
    # Run initial health check
    results = run_health_checks()
    healthy = sum(1 for s in results["services"].values() if s["healthy"])
    print(f"📊 {healthy}/{len(SERVICES)} services healthy")
    
    port = 8094
    server = HTTPServer(('0.0.0.0', port), WatchmanHandler)
    print(f"👁️ The Watchman running on http://localhost:{port}")
    print(f"Test: curl http://localhost:{port}/status")
    server.serve_forever()
