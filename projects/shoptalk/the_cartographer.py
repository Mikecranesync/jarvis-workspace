#!/usr/bin/env python3
"""
THE CODE CARTOGRAPHER (Automaton 3)

Scans existing codebases, maps files → functions → services,
proposes workflow boundaries, and feeds specs to Automaton 1.

DIGITAL TWIN PARADIGM (Three Levels):
- Level 1: WORKING COPY - where Automata make changes (sandbox/working/)
- Level 2: PRISTINE COPY - never changes, baseline for comparison (sandbox/pristine/)  
- Level 3: GITHUB - only changes when code is PROVEN through our process

SAFETY RULE: Cartographer and all Automata NEVER touch GitHub directly.
They only work within the sandbox. This protects production.

5-Second Test:
curl http://localhost:8095/status
curl http://localhost:8095/scan
curl http://localhost:8095/map/shoptalk
"""

import os
import ast
import json
import shutil
import hashlib
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path
from typing import Dict, List, Optional
import re

# Config
SANDBOX_ROOT = Path("/root/jarvis-workspace/sandbox")
WORKING_DIR = SANDBOX_ROOT / "working"
PRISTINE_DIR = SANDBOX_ROOT / "pristine"
SOURCE_DIR = Path("/root/jarvis-workspace/projects")

CARTOGRAPHER_STATE = Path("/root/jarvis-workspace/projects/shoptalk/cartographer_state.json")
WORKFLOW_PROPOSALS = Path("/root/jarvis-workspace/projects/shoptalk/workflow_proposals.json")

# Initialize state
def init_sandbox():
    """Initialize the digital twin sandbox structure."""
    SANDBOX_ROOT.mkdir(parents=True, exist_ok=True)
    WORKING_DIR.mkdir(parents=True, exist_ok=True)
    PRISTINE_DIR.mkdir(parents=True, exist_ok=True)
    
    if not CARTOGRAPHER_STATE.exists():
        initial_state = {
            "initialized": datetime.now().isoformat(),
            "last_scan": None,
            "projects_mapped": [],
            "total_files": 0,
            "total_lines": 0,
            "total_functions": 0,
            "sandbox_synced": False
        }
        with open(CARTOGRAPHER_STATE, 'w') as f:
            json.dump(initial_state, f, indent=2)
    
    if not WORKFLOW_PROPOSALS.exists():
        with open(WORKFLOW_PROPOSALS, 'w') as f:
            json.dump({"proposals": [], "next_id": 1}, f, indent=2)

init_sandbox()

def load_state():
    with open(CARTOGRAPHER_STATE, 'r') as f:
        return json.load(f)

def save_state(state):
    with open(CARTOGRAPHER_STATE, 'w') as f:
        json.dump(state, f, indent=2)

def sync_to_sandbox(project_name: str = None) -> dict:
    """
    Sync source code to sandbox (PRISTINE first, then WORKING).
    NEVER syncs TO GitHub. Only FROM source TO sandbox.
    """
    results = {"synced": [], "errors": []}
    
    projects = [project_name] if project_name else [p.name for p in SOURCE_DIR.iterdir() if p.is_dir()]
    
    for proj in projects:
        src = SOURCE_DIR / proj
        if not src.exists():
            results["errors"].append(f"Project {proj} not found")
            continue
        
        # Sync to PRISTINE (baseline - only if not exists)
        pristine_dest = PRISTINE_DIR / proj
        if not pristine_dest.exists():
            try:
                shutil.copytree(src, pristine_dest, dirs_exist_ok=True)
                results["synced"].append(f"PRISTINE/{proj}")
            except Exception as e:
                results["errors"].append(f"PRISTINE/{proj}: {str(e)}")
        
        # Sync to WORKING (where Automata make changes)
        working_dest = WORKING_DIR / proj
        try:
            if working_dest.exists():
                shutil.rmtree(working_dest)
            shutil.copytree(src, working_dest, dirs_exist_ok=True)
            results["synced"].append(f"WORKING/{proj}")
        except Exception as e:
            results["errors"].append(f"WORKING/{proj}: {str(e)}")
    
    # Update state
    state = load_state()
    state["sandbox_synced"] = True
    state["last_sync"] = datetime.now().isoformat()
    save_state(state)
    
    return results

def analyze_python_file(filepath: Path) -> dict:
    """Analyze a single Python file and extract structure."""
    result = {
        "file": str(filepath),
        "lines": 0,
        "classes": [],
        "functions": [],
        "imports": [],
        "docstring": None,
        "has_main": False,
        "is_service": False,
        "port": None,
        "endpoints": [],
        "hash": None
    }
    
    try:
        content = filepath.read_text(encoding='utf-8', errors='ignore')
        result["lines"] = len(content.splitlines())
        result["hash"] = hashlib.md5(content.encode()).hexdigest()[:12]
        
        # Check for service indicators
        result["is_service"] = "HTTPServer" in content or "BaseHTTPRequestHandler" in content
        
        # Extract port
        port_match = re.search(r'port\s*=\s*(\d+)', content)
        if port_match:
            result["port"] = int(port_match.group(1))
        
        # Extract endpoints
        endpoint_matches = re.findall(r'self\.path\s*==\s*["\']([^"\']+)["\']', content)
        result["endpoints"] = list(set(endpoint_matches))
        
        # Parse AST for structure
        try:
            tree = ast.parse(content)
            
            # Get module docstring
            result["docstring"] = ast.get_docstring(tree)
            
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    class_info = {
                        "name": node.name,
                        "methods": [m.name for m in node.body if isinstance(m, ast.FunctionDef)],
                        "line": node.lineno
                    }
                    result["classes"].append(class_info)
                    
                elif isinstance(node, ast.FunctionDef) and node.col_offset == 0:
                    # Top-level function
                    func_info = {
                        "name": node.name,
                        "args": [a.arg for a in node.args.args],
                        "line": node.lineno,
                        "docstring": ast.get_docstring(node)
                    }
                    result["functions"].append(func_info)
                    
                    if node.name == "main" or node.name == "__main__":
                        result["has_main"] = True
                
                elif isinstance(node, ast.Import):
                    for alias in node.names:
                        result["imports"].append(alias.name)
                        
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        result["imports"].append(node.module)
                        
        except SyntaxError:
            pass  # File has syntax errors, skip AST parsing
            
    except Exception as e:
        result["error"] = str(e)
    
    return result

def scan_project(project_name: str, use_working: bool = True) -> dict:
    """
    Scan a project in the sandbox and build a complete map.
    Always uses sandbox, NEVER touches GitHub.
    """
    base_dir = WORKING_DIR if use_working else PRISTINE_DIR
    project_dir = base_dir / project_name
    
    if not project_dir.exists():
        return {"error": f"Project {project_name} not found in sandbox. Run /sync first."}
    
    result = {
        "project": project_name,
        "sandbox": "WORKING" if use_working else "PRISTINE",
        "scanned_at": datetime.now().isoformat(),
        "total_files": 0,
        "total_lines": 0,
        "total_functions": 0,
        "total_classes": 0,
        "services": [],
        "modules": [],
        "files": []
    }
    
    for py_file in project_dir.rglob("*.py"):
        if "__pycache__" in str(py_file):
            continue
            
        file_analysis = analyze_python_file(py_file)
        file_analysis["relative_path"] = str(py_file.relative_to(project_dir))
        
        result["files"].append(file_analysis)
        result["total_files"] += 1
        result["total_lines"] += file_analysis["lines"]
        result["total_functions"] += len(file_analysis["functions"])
        result["total_classes"] += len(file_analysis["classes"])
        
        if file_analysis["is_service"]:
            result["services"].append({
                "file": file_analysis["relative_path"],
                "port": file_analysis["port"],
                "endpoints": file_analysis["endpoints"]
            })
    
    # Update state
    state = load_state()
    state["last_scan"] = datetime.now().isoformat()
    if project_name not in state["projects_mapped"]:
        state["projects_mapped"].append(project_name)
    state["total_files"] = result["total_files"]
    state["total_lines"] = result["total_lines"]
    state["total_functions"] = result["total_functions"]
    save_state(state)
    
    return result

def compare_working_vs_pristine(project_name: str) -> dict:
    """
    Compare WORKING copy against PRISTINE copy.
    This shows what changes the Automata have made.
    """
    working_dir = WORKING_DIR / project_name
    pristine_dir = PRISTINE_DIR / project_name
    
    if not working_dir.exists() or not pristine_dir.exists():
        return {"error": "Both WORKING and PRISTINE copies must exist. Run /sync first."}
    
    changes = {
        "project": project_name,
        "compared_at": datetime.now().isoformat(),
        "modified": [],
        "added": [],
        "deleted": [],
        "unchanged": 0
    }
    
    # Get all files in both
    working_files = {str(f.relative_to(working_dir)): f for f in working_dir.rglob("*.py") if "__pycache__" not in str(f)}
    pristine_files = {str(f.relative_to(pristine_dir)): f for f in pristine_dir.rglob("*.py") if "__pycache__" not in str(f)}
    
    # Find changes
    for rel_path, working_file in working_files.items():
        if rel_path not in pristine_files:
            changes["added"].append(rel_path)
        else:
            working_hash = hashlib.md5(working_file.read_bytes()).hexdigest()
            pristine_hash = hashlib.md5(pristine_files[rel_path].read_bytes()).hexdigest()
            if working_hash != pristine_hash:
                changes["modified"].append(rel_path)
            else:
                changes["unchanged"] += 1
    
    for rel_path in pristine_files:
        if rel_path not in working_files:
            changes["deleted"].append(rel_path)
    
    return changes

def propose_workflow(project_name: str, file_path: str, description: str) -> dict:
    """
    Propose a file/module to be converted into a workflow.
    This feeds to Automaton 1 (Spec-Maker).
    """
    with open(WORKFLOW_PROPOSALS, 'r') as f:
        proposals = json.load(f)
    
    proposal = {
        "id": proposals["next_id"],
        "project": project_name,
        "file": file_path,
        "description": description,
        "status": "PROPOSED",
        "created": datetime.now().isoformat(),
        "assigned_to": "Automaton 1 (Spec-Maker)",
        "sandbox_only": True,  # NEVER touches GitHub
        "proven": False
    }
    
    proposals["proposals"].append(proposal)
    proposals["next_id"] += 1
    
    with open(WORKFLOW_PROPOSALS, 'w') as f:
        json.dump(proposals, f, indent=2)
    
    return proposal

def get_cartographer_status() -> dict:
    """Get full Cartographer status."""
    state = load_state()
    
    # Check sandbox status
    working_projects = list(WORKING_DIR.iterdir()) if WORKING_DIR.exists() else []
    pristine_projects = list(PRISTINE_DIR.iterdir()) if PRISTINE_DIR.exists() else []
    
    return {
        "cartographer": "THE CODE CARTOGRAPHER (Automaton 3)",
        "purpose": "Map code → functions → workflows (SANDBOX ONLY)",
        "safety": "NEVER touches GitHub directly",
        "digital_twin": {
            "level_1_working": len([p for p in working_projects if p.is_dir()]),
            "level_2_pristine": len([p for p in pristine_projects if p.is_dir()]),
            "level_3_github": "PROTECTED (Automata never touch)"
        },
        "last_scan": state.get("last_scan"),
        "projects_mapped": state.get("projects_mapped", []),
        "total_files": state.get("total_files", 0),
        "total_lines": state.get("total_lines", 0),
        "total_functions": state.get("total_functions", 0)
    }

class CartographerHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length).decode('utf-8')
        
        try:
            data = json.loads(body) if body else {}
            
            if self.path == "/sync":
                project = data.get("project")
                result = sync_to_sandbox(project)
                self.send_json(result)
                
            elif self.path == "/propose":
                proposal = propose_workflow(
                    data.get("project", ""),
                    data.get("file", ""),
                    data.get("description", "")
                )
                self.send_json(proposal)
                
            else:
                self.send_error(404)
                
        except Exception as e:
            self.send_json({"error": str(e)}, 500)
    
    def do_GET(self):
        if self.path == "/health":
            self.send_json({"status": "ok", "service": "The Cartographer", "github_access": "DENIED"})
            
        elif self.path == "/status":
            self.send_json(get_cartographer_status())
            
        elif self.path == "/sync":
            result = sync_to_sandbox()
            self.send_json(result)
            
        elif self.path == "/scan":
            # Scan all synced projects
            results = {}
            for proj_dir in WORKING_DIR.iterdir():
                if proj_dir.is_dir():
                    results[proj_dir.name] = scan_project(proj_dir.name)
            self.send_json({"scanned": len(results), "projects": list(results.keys())})
            
        elif self.path.startswith("/map/"):
            project = self.path.split("/map/")[1]
            result = scan_project(project)
            self.send_json(result)
            
        elif self.path.startswith("/compare/"):
            project = self.path.split("/compare/")[1]
            result = compare_working_vs_pristine(project)
            self.send_json(result)
            
        elif self.path == "/proposals":
            with open(WORKFLOW_PROPOSALS, 'r') as f:
                self.send_json(json.load(f))
                
        elif self.path == "/safety":
            # Explicit safety check
            self.send_json({
                "github_write_access": False,
                "github_push_allowed": False,
                "sandbox_only": True,
                "message": "Cartographer NEVER touches GitHub. All work in sandbox."
            })
            
        else:
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()
            self.wfile.write(b"""
<h1>THE CODE CARTOGRAPHER (Automaton 3)</h1>
<p><b>SAFETY: NEVER touches GitHub. Sandbox only.</b></p>
<ul>
<li>GET /status - Cartographer status</li>
<li>GET /sync - Sync source to sandbox</li>
<li>GET /scan - Scan all projects in sandbox</li>
<li>GET /map/{project} - Map a specific project</li>
<li>GET /compare/{project} - Compare WORKING vs PRISTINE</li>
<li>GET /proposals - View workflow proposals</li>
<li>GET /safety - Verify safety constraints</li>
<li>POST /propose - Propose a workflow conversion</li>
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
    print("🗺️ The Code Cartographer initializing...")
    print("⚠️ SAFETY: GitHub access DENIED. Sandbox only.")
    
    # Initialize sandbox
    init_sandbox()
    print(f"📁 Sandbox root: {SANDBOX_ROOT}")
    
    # Initial sync
    print("🔄 Syncing to sandbox...")
    sync_result = sync_to_sandbox()
    print(f"✅ Synced: {len(sync_result['synced'])} items")
    
    port = 8095
    server = HTTPServer(('0.0.0.0', port), CartographerHandler)
    print(f"🗺️ The Cartographer running on http://localhost:{port}")
    print(f"Test: curl http://localhost:{port}/status")
    server.serve_forever()
