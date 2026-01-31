#!/usr/bin/env python3
"""
Demo Agent - Equipment Manual Q&A
Proves the autonomous agent workflow end-to-end.

Test: curl http://localhost:8090/ask -d '{"question": "How do I reset a Siemens V20 VFD fault?"}'
"""

import os
import json
from http.server import HTTPServer, BaseHTTPRequestHandler

# Pre-loaded manual knowledge (simulating RAG)
MANUAL_KNOWLEDGE = {
    "siemens_v20": {
        "name": "Siemens SINAMICS V20 Operating Instructions",
        "url": "https://support.industry.siemens.com/cs/document/109779715",
        "faults": {
            "F0001": {"page": 127, "description": "Overcurrent", "fix": "Check motor connections, reduce load"},
            "F0002": {"page": 128, "description": "Overvoltage", "fix": "Check DC bus voltage, add braking resistor"},
            "F0003": {"page": 129, "description": "Undervoltage", "fix": "Check power supply voltage"},
            "F0011": {"page": 135, "description": "Motor overtemperature", "fix": "Check ventilation, reduce load"},
        },
        "reset": {"page": 45, "method": "Press and hold the function button (FN) for 2 seconds, or cycle power"}
    },
    "rockwell_powerflex": {
        "name": "Rockwell PowerFlex 4 User Manual",
        "url": "https://literature.rockwellautomation.com/idc/groups/literature/documents/um/22a-um001_-en-e.pdf",
        "faults": {
            "F2": {"page": 78, "description": "Auxiliary input fault", "fix": "Check digital input wiring"},
            "F3": {"page": 79, "description": "Power loss", "fix": "Check incoming power"},
            "F4": {"page": 80, "description": "Undervoltage", "fix": "Check bus voltage"},
            "F7": {"page": 83, "description": "Motor overload", "fix": "Check motor current, reduce load"},
        },
        "reset": {"page": 42, "method": "Press the Stop button, then press Reset, or cycle power"}
    }
}

def find_manual_answer(question: str) -> dict:
    """Search manual knowledge base and return answer with citation."""
    question_lower = question.lower()
    
    # Detect equipment
    if "siemens" in question_lower or "v20" in question_lower or "sinamics" in question_lower:
        manual = MANUAL_KNOWLEDGE["siemens_v20"]
    elif "rockwell" in question_lower or "powerflex" in question_lower or "allen" in question_lower:
        manual = MANUAL_KNOWLEDGE["rockwell_powerflex"]
    else:
        return {"found": False, "message": "Equipment not recognized. Try: Siemens V20, Rockwell PowerFlex"}
    
    # Detect fault code
    for code, info in manual.get("faults", {}).items():
        if code.lower() in question_lower or code.replace("F", "f") in question_lower:
            return {
                "found": True,
                "manual": manual["name"],
                "url": manual["url"],
                "fault_code": code,
                "page": info["page"],
                "description": info["description"],
                "fix": info["fix"]
            }
    
    # Check for reset question
    if "reset" in question_lower or "clear" in question_lower:
        return {
            "found": True,
            "manual": manual["name"],
            "url": manual["url"],
            "page": manual["reset"]["page"],
            "answer": manual["reset"]["method"]
        }
    
    return {"found": False, "message": f"Could not find specific answer. Check manual: {manual['url']}"}

def generate_response(question: str) -> str:
    """Generate human-friendly response using manual knowledge + Claude."""
    knowledge = find_manual_answer(question)
    
    if not knowledge.get("found"):
        return knowledge.get("message", "I couldn't find information about that equipment.")
    
    # Build response with citation
    if "fault_code" in knowledge:
        response = f"""📋 **{knowledge['manual']}**

**Fault {knowledge['fault_code']}**: {knowledge['description']}

**Fix**: {knowledge['fix']}

📄 **Page {knowledge['page']}** | [View Manual]({knowledge['url']})"""
    else:
        response = f"""📋 **{knowledge['manual']}**

{knowledge.get('answer', 'See manual for details.')}

📄 **Page {knowledge['page']}** | [View Manual]({knowledge['url']})"""
    
    return response

class AgentHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == "/ask":
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length).decode('utf-8')
            
            try:
                data = json.loads(body)
                question = data.get("question", "")
                
                if not question:
                    self.send_response(400)
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({"error": "No question provided"}).encode())
                    return
                
                answer = generate_response(question)
                
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({
                    "question": question,
                    "answer": answer,
                    "source": "Manual Hunter Agent"
                }).encode())
                
            except json.JSONDecodeError:
                self.send_response(400)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"error": "Invalid JSON"}).encode())
        else:
            self.send_response(404)
            self.end_headers()
    
    def do_GET(self):
        if self.path == "/health":
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"status": "ok", "agent": "Manual Hunter"}).encode())
        else:
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()
            self.wfile.write(b"""
<h1>Manual Hunter Agent</h1>
<p>POST /ask with {"question": "your question"}</p>
<p>Example: How do I reset a Siemens V20 fault?</p>
            """)

if __name__ == "__main__":
    port = 8090
    server = HTTPServer(('0.0.0.0', port), AgentHandler)
    print(f"🤖 Manual Hunter Agent running on http://localhost:{port}")
    print(f"Test: curl http://localhost:{port}/ask -d '{{\"question\": \"How do I reset Siemens V20 fault F0001?\"}}'")
    server.serve_forever()
