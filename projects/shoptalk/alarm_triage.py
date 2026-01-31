#!/usr/bin/env python3
"""
Alarm Triage & Operator Cheat-Sheet
Part of the Automaton - turns alarm codes into actionable checklists.

Workflow:
1. Takes alarm code + operator note
2. Calls Manual Hunter to find relevant manual page
3. Generates step-by-step troubleshooting checklist
4. Logs to CSV
5. Returns JSON with everything

5-Second Test:
curl http://localhost:8091/triage -d '{"alarm": "F0001", "equipment": "Siemens V20", "note": "drive won't start"}'
"""

import os
import json
import csv
import requests
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path

# Config
MANUAL_HUNTER_URL = "http://localhost:8090/ask"
LOG_FILE = Path("/root/jarvis-workspace/projects/shoptalk/alarm_log.csv")

# Ensure log file exists with headers
if not LOG_FILE.exists():
    with open(LOG_FILE, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['timestamp', 'alarm_code', 'equipment', 'operator_note', 'fault_description', 'page_number', 'manual_url', 'checklist_generated'])

def call_manual_hunter(equipment: str, alarm: str) -> dict:
    """Call Manual Hunter API to get fault info."""
    try:
        response = requests.post(
            MANUAL_HUNTER_URL,
            json={"question": f"{equipment} {alarm}"},
            timeout=10
        )
        if response.status_code == 200:
            return response.json()
        return {"error": f"Manual Hunter returned {response.status_code}"}
    except Exception as e:
        return {"error": str(e)}

def generate_checklist(alarm: str, equipment: str, note: str, manual_info: str) -> list:
    """Generate step-by-step troubleshooting checklist."""
    
    # Parse manual info for specific details
    checklist = []
    
    # Standard safety first
    checklist.append("⚠️ SAFETY: Ensure equipment is in safe state before proceeding")
    checklist.append("📋 Document current alarm state (take photo if possible)")
    
    # Equipment-specific checks based on fault type
    alarm_upper = alarm.upper()
    
    if "F0001" in alarm_upper or "OVERCURRENT" in manual_info.upper():
        checklist.extend([
            "🔌 Check motor connections - look for loose wires",
            "📊 Measure motor current with clamp meter",
            "🔍 Inspect motor for signs of overheating",
            "⚙️ Verify load is not jammed or excessive",
            "🔧 Check coupling alignment if applicable"
        ])
    elif "F0002" in alarm_upper or "OVERVOLTAGE" in manual_info.upper():
        checklist.extend([
            "📊 Measure DC bus voltage",
            "🔍 Check for regenerative loads (lowering, deceleration)",
            "⚙️ Verify braking resistor is connected and functional",
            "📈 Review deceleration time settings"
        ])
    elif "F0003" in alarm_upper or "UNDERVOLTAGE" in manual_info.upper():
        checklist.extend([
            "📊 Measure incoming supply voltage",
            "🔌 Check all power connections",
            "🔍 Verify utility power is stable",
            "⚙️ Check for voltage drops during motor start"
        ])
    elif "F7" in alarm_upper or "OVERLOAD" in manual_info.upper():
        checklist.extend([
            "📊 Check motor current vs nameplate rating",
            "🔍 Verify motor thermal overload settings",
            "⚙️ Check for mechanical binding or obstruction",
            "📈 Review acceleration time settings"
        ])
    else:
        # Generic troubleshooting
        checklist.extend([
            "📖 Review fault code in manual (see page reference below)",
            "🔍 Check all connections and wiring",
            "📊 Verify parameter settings match application",
            "🔄 Try fault reset procedure"
        ])
    
    # Add operator note context
    note_lower = note.lower()
    if "won't start" in note_lower or "not starting" in note_lower:
        checklist.append("🚫 Check enable/start signal path")
        checklist.append("🔒 Verify safety interlocks are satisfied")
    if "hot" in note_lower or "overheat" in note_lower:
        checklist.append("🌡️ Allow equipment to cool before reset")
        checklist.append("🌀 Check cooling fans and ventilation")
    if "noise" in note_lower or "vibration" in note_lower:
        checklist.append("🔊 Check for bearing wear or mechanical issues")
        checklist.append("⚙️ Verify coupling and alignment")
    
    # Always end with reset and documentation
    checklist.append("🔄 Attempt fault reset (see manual for procedure)")
    checklist.append("📝 Document actions taken and results")
    
    return checklist

def log_alarm(alarm: str, equipment: str, note: str, fault_desc: str, page: str, url: str) -> str:
    """Log alarm to CSV file."""
    timestamp = datetime.now().isoformat()
    
    with open(LOG_FILE, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([timestamp, alarm, equipment, note, fault_desc, page, url, "YES"])
    
    return str(LOG_FILE)

def triage_alarm(alarm: str, equipment: str, note: str) -> dict:
    """Main triage function - orchestrates the full workflow."""
    
    # Step 1: Call Manual Hunter
    manual_result = call_manual_hunter(equipment, alarm)
    manual_answer = manual_result.get("answer", "No manual info found")
    
    # Extract page number and URL from answer
    page_number = "N/A"
    manual_url = "N/A"
    fault_description = "Unknown fault"
    
    if "Page" in manual_answer:
        # Parse "Page 127" from the answer
        import re
        page_match = re.search(r'Page (\d+)', manual_answer)
        if page_match:
            page_number = page_match.group(1)
    
    if "http" in manual_answer:
        url_match = re.search(r'(https?://[^\s\)]+)', manual_answer)
        if url_match:
            manual_url = url_match.group(1)
    
    if "Fault" in manual_answer:
        fault_match = re.search(r'Fault [A-Z0-9]+\*\*: ([^\n]+)', manual_answer)
        if fault_match:
            fault_description = fault_match.group(1)
        else:
            # Try alternate format
            fault_match = re.search(r'\*\*Fault [A-Z0-9]+\*\*: ([^\n]+)', manual_answer)
            if fault_match:
                fault_description = fault_match.group(1)
    
    # Step 2: Generate checklist
    checklist = generate_checklist(alarm, equipment, note, manual_answer)
    
    # Step 3: Log to CSV
    log_location = log_alarm(alarm, equipment, note, fault_description, page_number, manual_url)
    
    # Step 4: Build response
    summary = f"Alarm {alarm} on {equipment}: {fault_description}. See page {page_number} of manual."
    
    return {
        "input_alarm": alarm,
        "equipment": equipment,
        "operator_note": note,
        "summary": summary,
        "fault_description": fault_description,
        "manual_page": page_number,
        "manual_url": manual_url,
        "checklist": checklist,
        "log_location": log_location,
        "timestamp": datetime.now().isoformat()
    }

class TriageHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == "/triage":
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length).decode('utf-8')
            
            try:
                data = json.loads(body)
                alarm = data.get("alarm", "")
                equipment = data.get("equipment", "")
                note = data.get("note", "")
                
                if not alarm:
                    self.send_response(400)
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({"error": "No alarm code provided"}).encode())
                    return
                
                result = triage_alarm(alarm, equipment, note)
                
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(result, indent=2).encode())
                
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
            self.wfile.write(json.dumps({"status": "ok", "service": "Alarm Triage"}).encode())
        elif self.path == "/log":
            # Return recent log entries
            self.send_response(200)
            self.send_header('Content-Type', 'text/plain')
            self.end_headers()
            if LOG_FILE.exists():
                with open(LOG_FILE, 'r') as f:
                    self.wfile.write(f.read().encode())
            else:
                self.wfile.write(b"No logs yet")
        else:
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()
            self.wfile.write(b"""
<h1>Alarm Triage & Operator Cheat-Sheet</h1>
<p>POST /triage with {"alarm": "F0001", "equipment": "Siemens V20", "note": "drive won't start"}</p>
<p>GET /log to see alarm history</p>
            """)
    
    def log_message(self, format, *args):
        # Suppress default logging
        pass

if __name__ == "__main__":
    port = 8091
    server = HTTPServer(('0.0.0.0', port), TriageHandler)
    print(f"🚨 Alarm Triage Service running on http://localhost:{port}")
    print(f"Test: curl http://localhost:{port}/triage -d '{{\"alarm\": \"F0001\", \"equipment\": \"Siemens V20\", \"note\": \"drive won't start\"}}'")
    server.serve_forever()
