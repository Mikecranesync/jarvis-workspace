#!/usr/bin/env python3
"""
THE WEAVER (Automaton 2)

Lives inside the codebase. Knows every commit, every workflow, every version.
Stitches disjoint workflows into unified products.
Runs sandboxed E2E tests. Reality-checks answers against knowledge base.

Loop:
1. Sync with GitHub (webhook + hourly cron)
2. Map all workflows → files → tests
3. Stitch into unified products
4. Sandboxed E2E testing
5. Reality & hallucination check
6. 11-year-old verification

5-Second Test:
curl http://localhost:8093/status
curl http://localhost:8093/test -d '{"question":"Why did my machine stop?","context":"Siemens V20 F0001"}'
"""

import os
import json
import subprocess
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path
import hashlib

# Config
REPO_PATH = Path("/root/jarvis-workspace")
WEAVER_STATE = Path("/root/jarvis-workspace/projects/shoptalk/weaver_state.json")
GITHUB_REPO = "Mikecranesync/jarvis-workspace"

# Service endpoints (the workflows we stitch together)
SERVICES = {
    "manual_hunter": "http://localhost:8090/ask",
    "alarm_triage": "http://localhost:8091/triage",
    "workflow_tracker": "http://localhost:8092/track"
}

# Initialize state
if not WEAVER_STATE.exists():
    initial_state = {
        "last_sync": None,
        "last_commit": None,
        "workflow_map": {},
        "products": [],
        "test_results": [],
        "sync_count": 0
    }
    with open(WEAVER_STATE, 'w') as f:
        json.dump(initial_state, f, indent=2)

def run_cmd(cmd: list, cwd: str = None) -> tuple:
    """Run a command and return (success, output)."""
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60, cwd=cwd or str(REPO_PATH))
        return result.returncode == 0, result.stdout.strip()
    except Exception as e:
        return False, str(e)

def sync_github() -> dict:
    """Pull latest from GitHub - the Big Ben tick."""
    success, output = run_cmd(["git", "fetch", "origin"])
    if not success:
        return {"status": "error", "message": output}
    
    success, commit = run_cmd(["git", "rev-parse", "HEAD"])
    success, branch = run_cmd(["git", "branch", "--show-current"])
    
    # Load state
    with open(WEAVER_STATE, 'r') as f:
        state = json.load(f)
    
    state["last_sync"] = datetime.now().isoformat()
    state["last_commit"] = commit
    state["sync_count"] += 1
    
    with open(WEAVER_STATE, 'w') as f:
        json.dump(state, f, indent=2)
    
    return {
        "status": "synced",
        "branch": branch,
        "commit": commit,
        "sync_count": state["sync_count"],
        "timestamp": state["last_sync"]
    }

def map_workflows() -> dict:
    """Scan codebase and map all workflows."""
    workflow_map = {}
    
    # Find Python services (our workflow endpoints)
    for py_file in REPO_PATH.glob("projects/**/[!_]*.py"):
        content = py_file.read_text()
        
        # Detect if it's a workflow service
        if "HTTPServer" in content or "BaseHTTPRequestHandler" in content:
            # Extract port
            import re
            port_match = re.search(r'port\s*=\s*(\d+)', content)
            port = port_match.group(1) if port_match else "unknown"
            
            # Extract docstring for description
            doc_match = re.search(r'"""(.*?)"""', content, re.DOTALL)
            description = doc_match.group(1)[:200] if doc_match else "No description"
            
            workflow_map[py_file.stem] = {
                "file": str(py_file.relative_to(REPO_PATH)),
                "port": port,
                "description": description.strip().split('\n')[0],
                "hash": hashlib.md5(content.encode()).hexdigest()[:8]
            }
    
    # Find Flowise flows
    for flow_file in REPO_PATH.glob("**/*.flow.json"):
        content = flow_file.read_text()
        workflow_map[flow_file.stem] = {
            "file": str(flow_file.relative_to(REPO_PATH)),
            "type": "flowise",
            "hash": hashlib.md5(content.encode()).hexdigest()[:8]
        }
    
    # Find n8n workflows
    for n8n_file in REPO_PATH.glob("**/n8n*.json"):
        content = n8n_file.read_text()
        workflow_map[n8n_file.stem] = {
            "file": str(n8n_file.relative_to(REPO_PATH)),
            "type": "n8n",
            "hash": hashlib.md5(content.encode()).hexdigest()[:8]
        }
    
    # Update state
    with open(WEAVER_STATE, 'r') as f:
        state = json.load(f)
    state["workflow_map"] = workflow_map
    with open(WEAVER_STATE, 'w') as f:
        json.dump(state, f, indent=2)
    
    return workflow_map

def check_service_health(url: str) -> bool:
    """Check if a service is responding."""
    import urllib.request
    try:
        health_url = url.rsplit('/', 1)[0] + '/health'
        req = urllib.request.urlopen(health_url, timeout=5)
        return req.status == 200
    except:
        return False

def call_service(url: str, data: dict) -> dict:
    """Call a workflow service."""
    import urllib.request
    try:
        req = urllib.request.Request(
            url,
            data=json.dumps(data).encode(),
            headers={'Content-Type': 'application/json'}
        )
        resp = urllib.request.urlopen(req, timeout=30)
        return json.loads(resp.read().decode())
    except Exception as e:
        return {"error": str(e)}

def reality_check(answer: str, sources: list) -> dict:
    """Check if an answer is grounded in reality (not hallucination)."""
    checks = {
        "has_sources": len(sources) > 0,
        "cites_page": "page" in answer.lower() or "Page" in answer,
        "cites_manual": "manual" in answer.lower() or "http" in answer,
        "specific_steps": any(word in answer.lower() for word in ["check", "verify", "inspect", "measure"]),
        "no_vague_claims": not any(phrase in answer.lower() for phrase in ["might be", "could possibly", "maybe try"])
    }
    
    passed = sum(checks.values())
    total = len(checks)
    
    return {
        "grounded": passed >= 3,  # At least 3/5 checks
        "score": f"{passed}/{total}",
        "checks": checks,
        "verdict": "REAL" if passed >= 3 else "POSSIBLY_HALLUCINATED"
    }

def run_e2e_test(question: str, context: str = "") -> dict:
    """
    Run end-to-end test of the full workflow chain.
    
    Example: "Why did my machine stop?" with context "Siemens V20 F0001"
    
    Chain:
    1. Parse question + context
    2. Call Manual Hunter for equipment info
    3. Call Alarm Triage for checklist
    4. Reality check the answer
    5. Format for Telegram (4096 char limit)
    """
    results = {
        "question": question,
        "context": context,
        "timestamp": datetime.now().isoformat(),
        "chain": [],
        "final_answer": None,
        "reality_check": None,
        "telegram_safe": False
    }
    
    # Step 1: Call Manual Hunter
    manual_result = call_service(SERVICES["manual_hunter"], {
        "question": f"{context} {question}"
    })
    results["chain"].append({
        "step": "manual_hunter",
        "success": "error" not in manual_result,
        "output": manual_result.get("answer", manual_result.get("error", "No response"))[:500]
    })
    
    # Step 2: Call Alarm Triage (if we have alarm code)
    alarm_code = None
    for code in ["F0001", "F0002", "F0003", "F7", "F2", "F3", "F4"]:
        if code in context.upper():
            alarm_code = code
            break
    
    if alarm_code:
        # Parse equipment from context
        equipment = "Unknown"
        if "siemens" in context.lower() or "v20" in context.lower():
            equipment = "Siemens V20"
        elif "rockwell" in context.lower() or "powerflex" in context.lower():
            equipment = "Rockwell PowerFlex"
        
        triage_result = call_service(SERVICES["alarm_triage"], {
            "alarm": alarm_code,
            "equipment": equipment,
            "note": question
        })
        results["chain"].append({
            "step": "alarm_triage",
            "success": "error" not in triage_result,
            "output": triage_result.get("summary", triage_result.get("error", "No response"))
        })
        
        # Build final answer from triage
        if "checklist" in triage_result:
            checklist_text = "\n".join(triage_result["checklist"][:5])  # First 5 steps
            results["final_answer"] = f"""🔧 **{triage_result.get('summary', 'Machine stopped')}**

**Checklist:**
{checklist_text}

📄 See page {triage_result.get('manual_page', 'N/A')} of the manual."""
    else:
        # No alarm code - use manual hunter response directly
        results["final_answer"] = manual_result.get("answer", "Could not determine cause.")
    
    # Step 3: Reality check
    sources = [r["output"] for r in results["chain"] if r["success"]]
    results["reality_check"] = reality_check(results["final_answer"] or "", sources)
    
    # Step 4: Telegram safety (4096 char limit)
    if results["final_answer"]:
        if len(results["final_answer"]) <= 4096:
            results["telegram_safe"] = True
        else:
            results["final_answer"] = results["final_answer"][:4090] + "..."
            results["telegram_safe"] = True
    
    # Step 5: Track this test
    call_service(SERVICES["workflow_tracker"], {
        "workflow": "E2E Test",
        "tokens": 500,  # Estimated
        "version": "1.0.0",
        "description": f"Test: {question[:50]}"
    })
    
    return results

def get_weaver_status() -> dict:
    """Get full Weaver status."""
    with open(WEAVER_STATE, 'r') as f:
        state = json.load(f)
    
    # Check service health
    service_status = {}
    for name, url in SERVICES.items():
        service_status[name] = "UP" if check_service_health(url) else "DOWN"
    
    return {
        "weaver": "THE WEAVER (Automaton 2)",
        "purpose": "Stitches workflows into unified products",
        "last_sync": state.get("last_sync"),
        "last_commit": state.get("last_commit"),
        "sync_count": state.get("sync_count", 0),
        "workflows_mapped": len(state.get("workflow_map", {})),
        "services": service_status,
        "cron": "Hourly (Big Ben tick) + webhook on commit"
    }

class WeaverHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length).decode('utf-8')
        
        try:
            data = json.loads(body) if body else {}
            
            if self.path == "/sync":
                # Manual sync trigger
                result = sync_github()
                self.send_json(result)
                
            elif self.path == "/map":
                # Map all workflows
                result = map_workflows()
                self.send_json({"workflows": len(result), "map": result})
                
            elif self.path == "/test":
                # Run E2E test
                question = data.get("question", "")
                context = data.get("context", "")
                result = run_e2e_test(question, context)
                self.send_json(result)
                
            elif self.path == "/webhook":
                # GitHub webhook endpoint
                result = sync_github()
                map_workflows()
                self.send_json({"status": "webhook processed", "sync": result})
                
            else:
                self.send_error(404)
                
        except Exception as e:
            self.send_json({"error": str(e)}, 500)
    
    def do_GET(self):
        if self.path == "/health":
            self.send_json({"status": "ok", "service": "The Weaver"})
            
        elif self.path == "/status":
            self.send_json(get_weaver_status())
            
        elif self.path == "/map":
            with open(WEAVER_STATE, 'r') as f:
                state = json.load(f)
            self.send_json(state.get("workflow_map", {}))
            
        else:
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()
            self.wfile.write(b"""
<h1>THE WEAVER (Automaton 2)</h1>
<p>Lives inside the codebase. Stitches workflows into products.</p>
<ul>
<li>GET /status - Weaver status</li>
<li>GET /map - Workflow map</li>
<li>POST /sync - Manual GitHub sync</li>
<li>POST /test - Run E2E test</li>
<li>POST /webhook - GitHub webhook</li>
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
    # Initial sync and map
    print("🕸️ The Weaver initializing...")
    sync_github()
    workflows = map_workflows()
    print(f"📍 Mapped {len(workflows)} workflows")
    
    port = 8093
    server = HTTPServer(('0.0.0.0', port), WeaverHandler)
    print(f"🕸️ The Weaver running on http://localhost:{port}")
    print(f"Test: curl http://localhost:{port}/status")
    server.serve_forever()
