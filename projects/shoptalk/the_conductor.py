#!/usr/bin/env python3
"""
THE CONDUCTOR (Master of Puppets Orchestration Layer)

The trigger loop that connects all Automata:
1. Receives verified workflow outputs
2. Identifies next highest-priority item to implement
3. Generates approval links for human-in-the-loop verification
4. Tracks approval status
5. Only commits approved workflows

HUMAN-IN-THE-LOOP: Every workflow generates a unique approval URL.
Mike clicks it, sees proof, approves/rejects. Nothing deploys without approval.

5-Second Test:
curl http://localhost:8096/status
curl http://localhost:8096/queue
curl http://localhost:8096/next
"""

import os
import json
import hashlib
import urllib.request
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path
from typing import Dict, List, Optional

# Config
CONDUCTOR_STATE = Path("/root/jarvis-workspace/projects/shoptalk/conductor_state.json")
APPROVAL_QUEUE = Path("/root/jarvis-workspace/projects/shoptalk/approval_queue.json")
PRIORITY_MATRIX = Path("/root/jarvis-workspace/projects/shoptalk/priority_matrix.json")

VPS_IP = "165.245.138.91"
CONDUCTOR_PORT = 8096

# Service URLs
SERVICES = {
    "cartographer": "http://localhost:8095",
    "weaver": "http://localhost:8093",
    "watchman": "http://localhost:8094",
    "tracker": "http://localhost:8092"
}

# Priority scoring (higher = more important)
PRIORITY_WEIGHTS = {
    "is_service": 50,          # HTTP services are high value
    "has_endpoints": 30,       # Endpoints mean user-facing
    "high_line_count": 20,     # Complex code needs attention
    "has_tests": -10,          # Already tested = lower priority
    "recently_modified": 40,   # Active development = important
    "core_functionality": 100, # Keywords like "main", "core", "api"
    "demo_relevant": 80,       # Keywords for Tuesday demo
}

# Keywords that indicate high priority
HIGH_PRIORITY_KEYWORDS = [
    "api", "core", "main", "service", "handler", "endpoint",
    "diagnostic", "alarm", "fault", "plc", "hmi", "maintenance",
    "manual", "troubleshoot", "work_order"
]

DEMO_KEYWORDS = [
    "diagnostic", "alarm", "fault", "triage", "manual", "checklist"
]

def init_files():
    """Initialize conductor files."""
    if not CONDUCTOR_STATE.exists():
        state = {
            "started": datetime.now().isoformat(),
            "cycles_completed": 0,
            "workflows_approved": 0,
            "workflows_rejected": 0,
            "current_priority": None,
            "auto_mode": False  # Human approval required until Mike trusts the system
        }
        with open(CONDUCTOR_STATE, 'w') as f:
            json.dump(state, f, indent=2)
    
    if not APPROVAL_QUEUE.exists():
        with open(APPROVAL_QUEUE, 'w') as f:
            json.dump({"pending": [], "approved": [], "rejected": []}, f, indent=2)
    
    if not PRIORITY_MATRIX.exists():
        with open(PRIORITY_MATRIX, 'w') as f:
            json.dump({"items": [], "last_calculated": None}, f, indent=2)

init_files()

def load_state():
    with open(CONDUCTOR_STATE, 'r') as f:
        return json.load(f)

def save_state(state):
    with open(CONDUCTOR_STATE, 'w') as f:
        json.dump(state, f, indent=2)

def load_queue():
    with open(APPROVAL_QUEUE, 'r') as f:
        return json.load(f)

def save_queue(queue):
    with open(APPROVAL_QUEUE, 'w') as f:
        json.dump(queue, f, indent=2)

def call_service(service: str, path: str, data: dict = None) -> dict:
    """Call an Automaton service."""
    try:
        url = f"{SERVICES[service]}{path}"
        if data:
            req = urllib.request.Request(
                url,
                data=json.dumps(data).encode(),
                headers={'Content-Type': 'application/json'}
            )
        else:
            req = urllib.request.Request(url)
        resp = urllib.request.urlopen(req, timeout=30)
        return json.loads(resp.read().decode())
    except Exception as e:
        return {"error": str(e)}

def calculate_priority_score(file_info: dict) -> int:
    """Calculate priority score for a file based on importance."""
    score = 0
    
    # Service detection
    if file_info.get("is_service"):
        score += PRIORITY_WEIGHTS["is_service"]
    
    # Endpoints
    if file_info.get("endpoints"):
        score += PRIORITY_WEIGHTS["has_endpoints"]
    
    # Line count (complex code)
    if file_info.get("lines", 0) > 500:
        score += PRIORITY_WEIGHTS["high_line_count"]
    
    # Check for high-priority keywords
    file_path = file_info.get("relative_path", "").lower()
    docstring = (file_info.get("docstring") or "").lower()
    
    for keyword in HIGH_PRIORITY_KEYWORDS:
        if keyword in file_path or keyword in docstring:
            score += PRIORITY_WEIGHTS["core_functionality"]
            break
    
    # Demo relevance (Tuesday demo)
    for keyword in DEMO_KEYWORDS:
        if keyword in file_path or keyword in docstring:
            score += PRIORITY_WEIGHTS["demo_relevant"]
            break
    
    return score

def build_priority_matrix() -> dict:
    """Scan all projects and build priority matrix."""
    matrix = {"items": [], "last_calculated": datetime.now().isoformat()}
    
    # Get all mapped projects from Cartographer
    scan_result = call_service("cartographer", "/scan")
    if "error" in scan_result:
        return {"error": scan_result["error"]}
    
    for project in scan_result.get("projects", []):
        # Get detailed map of project
        project_map = call_service("cartographer", f"/map/{project}")
        if "error" in project_map:
            continue
        
        for file_info in project_map.get("files", []):
            # Skip if not convertible to workflow (e.g., __init__.py, tests)
            if "__init__" in file_info.get("relative_path", ""):
                continue
            if "test_" in file_info.get("relative_path", ""):
                continue
            
            score = calculate_priority_score(file_info)
            
            if score > 0:  # Only include items with some priority
                matrix["items"].append({
                    "project": project,
                    "file": file_info.get("relative_path"),
                    "lines": file_info.get("lines", 0),
                    "functions": len(file_info.get("functions", [])),
                    "is_service": file_info.get("is_service", False),
                    "priority_score": score,
                    "status": "pending"
                })
    
    # Sort by priority score (highest first)
    matrix["items"].sort(key=lambda x: x["priority_score"], reverse=True)
    
    # Save matrix
    with open(PRIORITY_MATRIX, 'w') as f:
        json.dump(matrix, f, indent=2)
    
    return matrix

def get_next_priority() -> dict:
    """Get the next highest-priority item to implement."""
    with open(PRIORITY_MATRIX, 'r') as f:
        matrix = json.load(f)
    
    # Find first pending item
    for item in matrix.get("items", []):
        if item.get("status") == "pending":
            return item
    
    return {"message": "No pending items. All workflows processed or matrix empty."}

def generate_approval_token(workflow_id: str) -> str:
    """Generate unique approval token."""
    timestamp = datetime.now().isoformat()
    raw = f"{workflow_id}:{timestamp}"
    return hashlib.sha256(raw.encode()).hexdigest()[:16]

def create_approval_request(workflow_data: dict) -> dict:
    """Create an approval request with a unique link for Mike."""
    queue = load_queue()
    
    # Generate unique token
    workflow_id = f"{workflow_data.get('project', 'unknown')}_{workflow_data.get('file', 'unknown')}"
    token = generate_approval_token(workflow_id)
    
    approval_request = {
        "id": token,
        "workflow_id": workflow_id,
        "project": workflow_data.get("project"),
        "file": workflow_data.get("file"),
        "priority_score": workflow_data.get("priority_score"),
        "created": datetime.now().isoformat(),
        "status": "PENDING",
        "approval_url": f"http://{VPS_IP}:{CONDUCTOR_PORT}/approve/{token}",
        "reject_url": f"http://{VPS_IP}:{CONDUCTOR_PORT}/reject/{token}",
        "details_url": f"http://{VPS_IP}:{CONDUCTOR_PORT}/details/{token}",
        "test_results": workflow_data.get("test_results", {}),
        "proof": workflow_data.get("proof", "No proof provided")
    }
    
    queue["pending"].append(approval_request)
    save_queue(queue)
    
    return approval_request

def approve_workflow(token: str) -> dict:
    """Approve a workflow (human-in-the-loop verification)."""
    queue = load_queue()
    state = load_state()
    
    # Find the pending request
    for i, req in enumerate(queue["pending"]):
        if req["id"] == token:
            req["status"] = "APPROVED"
            req["approved_at"] = datetime.now().isoformat()
            req["approved_by"] = "Mike (Master of Puppets)"
            
            # Move to approved
            queue["approved"].append(req)
            queue["pending"].pop(i)
            save_queue(queue)
            
            # Update state
            state["workflows_approved"] += 1
            state["cycles_completed"] += 1
            save_state(state)
            
            # Update priority matrix
            with open(PRIORITY_MATRIX, 'r') as f:
                matrix = json.load(f)
            for item in matrix["items"]:
                if item.get("file") == req.get("file") and item.get("project") == req.get("project"):
                    item["status"] = "approved"
            with open(PRIORITY_MATRIX, 'w') as f:
                json.dump(matrix, f, indent=2)
            
            return {
                "status": "APPROVED",
                "workflow": req["workflow_id"],
                "message": "Workflow approved! Proceeding to next priority.",
                "next": get_next_priority()
            }
    
    return {"error": "Approval token not found"}

def reject_workflow(token: str, reason: str = "") -> dict:
    """Reject a workflow."""
    queue = load_queue()
    state = load_state()
    
    for i, req in enumerate(queue["pending"]):
        if req["id"] == token:
            req["status"] = "REJECTED"
            req["rejected_at"] = datetime.now().isoformat()
            req["rejection_reason"] = reason
            
            queue["rejected"].append(req)
            queue["pending"].pop(i)
            save_queue(queue)
            
            state["workflows_rejected"] += 1
            save_state(state)
            
            return {
                "status": "REJECTED",
                "workflow": req["workflow_id"],
                "reason": reason,
                "message": "Workflow rejected. Moving to next priority."
            }
    
    return {"error": "Rejection token not found"}

def trigger_next_cycle() -> dict:
    """
    The main trigger loop:
    1. Get next priority item
    2. Propose workflow conversion
    3. Create approval request
    4. Wait for human approval
    """
    # Get next priority
    next_item = get_next_priority()
    if "message" in next_item:
        return next_item
    
    # Create approval request
    approval = create_approval_request(next_item)
    
    return {
        "triggered": True,
        "next_item": next_item,
        "approval_request": {
            "id": approval["id"],
            "approval_link": approval["approval_url"],
            "details_link": approval["details_url"]
        },
        "message": "Approval request created. Waiting for human verification.",
        "instructions": f"Click to approve: {approval['approval_url']}"
    }

def get_conductor_status() -> dict:
    """Get full Conductor status."""
    state = load_state()
    queue = load_queue()
    
    with open(PRIORITY_MATRIX, 'r') as f:
        matrix = json.load(f)
    
    pending_count = len([i for i in matrix.get("items", []) if i.get("status") == "pending"])
    
    return {
        "conductor": "THE CONDUCTOR (Master of Puppets Orchestration)",
        "purpose": "Trigger loop + human-in-the-loop approval",
        "auto_mode": state.get("auto_mode", False),
        "cycles_completed": state.get("cycles_completed", 0),
        "workflows_approved": state.get("workflows_approved", 0),
        "workflows_rejected": state.get("workflows_rejected", 0),
        "pending_approvals": len(queue.get("pending", [])),
        "priority_items_remaining": pending_count,
        "current_priority": get_next_priority()
    }

class ConductorHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length).decode('utf-8')
        
        try:
            data = json.loads(body) if body else {}
            
            if self.path == "/trigger":
                # Trigger next cycle
                result = trigger_next_cycle()
                self.send_json(result)
                
            elif self.path == "/build-matrix":
                # Build priority matrix
                result = build_priority_matrix()
                self.send_json({"items": len(result.get("items", [])), "calculated": result.get("last_calculated")})
                
            elif self.path == "/verified":
                # Receive verified workflow output (trigger for next)
                result = trigger_next_cycle()
                self.send_json(result)
                
            else:
                self.send_error(404)
                
        except Exception as e:
            self.send_json({"error": str(e)}, 500)
    
    def do_GET(self):
        if self.path == "/health":
            self.send_json({"status": "ok", "service": "The Conductor"})
            
        elif self.path == "/status":
            self.send_json(get_conductor_status())
            
        elif self.path == "/queue":
            self.send_json(load_queue())
            
        elif self.path == "/next":
            self.send_json(get_next_priority())
            
        elif self.path == "/matrix":
            with open(PRIORITY_MATRIX, 'r') as f:
                matrix = json.load(f)
            # Return top 10 for readability
            top_10 = matrix.get("items", [])[:10]
            self.send_json({"top_10_priorities": top_10, "total": len(matrix.get("items", []))})
            
        elif self.path.startswith("/approve/"):
            token = self.path.split("/approve/")[1]
            result = approve_workflow(token)
            self.send_html(f"""
<html><body style="font-family: Arial; padding: 40px; text-align: center;">
<h1>✅ WORKFLOW APPROVED</h1>
<p>Token: {token}</p>
<p>Status: {result.get('status', 'Unknown')}</p>
<p>{result.get('message', '')}</p>
<hr>
<h2>Next Priority:</h2>
<pre>{json.dumps(result.get('next', {}), indent=2)}</pre>
<p><a href="/status">View Status</a> | <a href="/queue">View Queue</a></p>
</body></html>
            """)
            
        elif self.path.startswith("/reject/"):
            token = self.path.split("/reject/")[1]
            result = reject_workflow(token)
            self.send_html(f"""
<html><body style="font-family: Arial; padding: 40px; text-align: center;">
<h1>❌ WORKFLOW REJECTED</h1>
<p>Token: {token}</p>
<p>Status: {result.get('status', 'Unknown')}</p>
</body></html>
            """)
            
        elif self.path.startswith("/details/"):
            token = self.path.split("/details/")[1]
            queue = load_queue()
            req = None
            for r in queue.get("pending", []):
                if r["id"] == token:
                    req = r
                    break
            if req:
                self.send_html(f"""
<html><body style="font-family: Arial; padding: 40px;">
<h1>📋 WORKFLOW APPROVAL REQUEST</h1>
<table border="1" cellpadding="10">
<tr><td><b>Project</b></td><td>{req.get('project')}</td></tr>
<tr><td><b>File</b></td><td>{req.get('file')}</td></tr>
<tr><td><b>Priority Score</b></td><td>{req.get('priority_score')}</td></tr>
<tr><td><b>Created</b></td><td>{req.get('created')}</td></tr>
<tr><td><b>Status</b></td><td>{req.get('status')}</td></tr>
</table>
<br>
<h2>Actions:</h2>
<a href="{req.get('approval_url')}" style="background: green; color: white; padding: 20px 40px; text-decoration: none; font-size: 20px;">✅ APPROVE</a>
&nbsp;&nbsp;
<a href="{req.get('reject_url')}" style="background: red; color: white; padding: 20px 40px; text-decoration: none; font-size: 20px;">❌ REJECT</a>
</body></html>
                """)
            else:
                self.send_html("<h1>Request not found</h1>")
            
        else:
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()
            self.wfile.write(b"""
<h1>THE CONDUCTOR (Master of Puppets Orchestration)</h1>
<p>Trigger loop with human-in-the-loop approval.</p>
<ul>
<li>GET /status - Conductor status</li>
<li>GET /queue - Approval queue</li>
<li>GET /next - Next priority item</li>
<li>GET /matrix - Priority matrix (top 10)</li>
<li>POST /build-matrix - Build priority matrix</li>
<li>POST /trigger - Trigger next cycle</li>
<li>GET /approve/{token} - Approve workflow</li>
<li>GET /reject/{token} - Reject workflow</li>
</ul>
            """)
    
    def send_json(self, data, status=200):
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data, indent=2).encode())
    
    def send_html(self, html, status=200):
        self.send_response(status)
        self.send_header('Content-Type', 'text/html')
        self.end_headers()
        self.wfile.write(html.encode())
    
    def log_message(self, format, *args):
        pass

if __name__ == "__main__":
    print("🎼 The Conductor initializing...")
    
    # Only build matrix if it doesn't exist or is empty
    # This prevents blocking on startup
    try:
        with open(PRIORITY_MATRIX, 'r') as f:
            matrix = json.load(f)
        item_count = len(matrix.get('items', []))
        if item_count > 0:
            print(f"📊 Using existing priority matrix ({item_count} items)")
        else:
            print("📊 Matrix empty, will build on first /build-matrix call")
    except:
        print("📊 No matrix found, will build on first /build-matrix call")
    
    port = CONDUCTOR_PORT
    server = HTTPServer(('0.0.0.0', port), ConductorHandler)
    print(f"🎼 The Conductor running on http://localhost:{port}")
    print(f"Test: curl http://localhost:{port}/status")
    server.serve_forever()
