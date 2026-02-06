# Jarvis Node - Remote Machine Control

Control Windows/Linux machines remotely via WebSocket. Take screenshots, run commands, click, type.

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│  VPS Hub: srv1078052 (100.102.30.102)                       │
│  ├── jarvis-node-server on port 8765                        │
│  └── Clawdbot (this agent)                                  │
└─────────────────────────────────────────────────────────────┘
                           │
            WebSocket connections (ws://100.102.30.102:8765)
                           │
        ┌──────────────────┼──────────────────┐
        ▼                  ▼                  ▼
┌───────────────┐  ┌───────────────┐  ┌───────────────┐
│ Travel Laptop │  │  PLC Laptop   │  │  Future Node  │
│ MIGUELOMANIAC │  │ laptop-0ka3c70h│  │               │
│ 100.83.251.23 │  │ 100.72.2.99   │  │               │
└───────────────┘  └───────────────┘  └───────────────┘
```

## Key IPs (Tailscale)

| Machine | Tailscale IP | Role |
|---------|-------------|------|
| srv1078052 | **100.102.30.102** | Hub VPS (server runs here) |
| factorylm-prod | 100.68.120.99 | Secondary VPS (NOT the hub) |
| miguelomaniac | 100.83.251.23 | Travel Laptop (Windows) |
| laptop-0ka3c70h | 100.72.2.99 | PLC Laptop (Windows) |

**⚠️ IMPORTANT: The Jarvis Node server runs on 100.102.30.102:8765 (srv1078052)**

## Server Location

- **Service:** `jarvis-node-server.service`
- **Code:** `/opt/jarvis-node-server/server.py`
- **Port:** 8765
- **Control script:** `/opt/jarvis-node-server/control.py`

## Client Setup (Windows)

### 1. Create directory
```powershell
mkdir C:\JarvisNode
```

### 2. Install dependencies
```powershell
pip install websockets pyautogui pillow
```

### 3. Create jarvis_node.py
```python
#!/usr/bin/env python3
import asyncio
import websockets
import json
import base64
import pyautogui
import os
import sys
from datetime import datetime

SERVER_URL = "ws://100.102.30.102:8765"  # <-- Hub VPS
NODE_NAME = os.environ.get("JARVIS_NODE_NAME", os.environ.get("COMPUTERNAME", "windows-node"))

async def handle_command(cmd):
    action = cmd.get("action")
    
    if action == "screenshot":
        img = pyautogui.screenshot()
        import io
        buf = io.BytesIO()
        img.save(buf, format='PNG')
        return {"image": base64.b64encode(buf.getvalue()).decode()}
    
    elif action == "shell":
        import subprocess
        result = subprocess.run(cmd.get("command", "echo hi"), shell=True, capture_output=True, text=True)
        return {"stdout": result.stdout, "stderr": result.stderr, "code": result.returncode}
    
    elif action == "click":
        pyautogui.click(cmd.get("x", 0), cmd.get("y", 0))
        return {"status": "clicked"}
    
    elif action == "type":
        pyautogui.write(cmd.get("text", ""), interval=0.02)
        return {"status": "typed"}
    
    elif action == "hotkey":
        pyautogui.hotkey(*cmd.get("keys", []))
        return {"status": "hotkey sent"}
    
    elif action == "ping":
        return {"status": "pong", "node": NODE_NAME, "time": datetime.now().isoformat()}
    
    return {"error": "Unknown action"}

async def main():
    print(f"Jarvis Node '{NODE_NAME}' connecting to {SERVER_URL}...", flush=True)
    
    while True:
        try:
            async with websockets.connect(SERVER_URL) as ws:
                await ws.send(json.dumps({"type": "register", "name": NODE_NAME}))
                print(f"Connected and registered as '{NODE_NAME}'", flush=True)
                
                async for message in ws:
                    try:
                        cmd = json.loads(message)
                        result = await handle_command(cmd)
                        await ws.send(json.dumps(result))
                    except Exception as e:
                        await ws.send(json.dumps({"error": str(e)}))
        
        except Exception as e:
            print(f"Connection error: {e}. Retrying in 5s...", flush=True)
            await asyncio.sleep(5)

if __name__ == "__main__":
    asyncio.run(main())
```

### 4. Run as background task
```powershell
# Start
pythonw C:\JarvisNode\jarvis_node.py

# Or with visible console
python C:\JarvisNode\jarvis_node.py
```

### 5. Auto-start (Task Scheduler)
Create scheduled task to run at login:
- Program: `pythonw`
- Arguments: `C:\JarvisNode\jarvis_node.py`
- Start in: `C:\JarvisNode`

## Controlling Nodes (from VPS)

### Check connected nodes
```bash
python3 /opt/jarvis-node-server/control.py list
```

### Send commands
```bash
# Screenshot
python3 /opt/jarvis-node-server/control.py MIGUELOMANIAC screenshot

# Run shell command
python3 /opt/jarvis-node-server/control.py MIGUELOMANIAC shell "dir C:\\"

# Click at coordinates
python3 /opt/jarvis-node-server/control.py MIGUELOMANIAC click 500 300

# Type text
python3 /opt/jarvis-node-server/control.py MIGUELOMANIAC type "Hello World"

# Ping
python3 /opt/jarvis-node-server/control.py MIGUELOMANIAC ping
```

## Troubleshooting

### Node won't connect
1. Check VPS IP is correct: `ws://100.102.30.102:8765`
2. Check server is running: `systemctl status jarvis-node-server`
3. Check firewall: `ss -tlnp | grep 8765`
4. Test from node: `curl -v http://100.102.30.102:8765` (should get HTTP 426)

### Server not responding
```bash
systemctl restart jarvis-node-server
journalctl -u jarvis-node-server -f
```

### Check server logs
```bash
journalctl -u jarvis-node-server --no-pager -n 50
```

## Claude Code Prompts

### Setup new node
```
Set up Jarvis Node on this Windows machine:
1. Create C:\JarvisNode\jarvis_node.py with the standard client code
2. SERVER_URL must be ws://100.102.30.102:8765
3. Install: pip install websockets pyautogui pillow
4. Start in background and verify "Connected and registered as 'HOSTNAME'"
```

### Fix connection
```
Fix Jarvis Node connection:
1. Edit C:\JarvisNode\jarvis_node.py
2. Set SERVER_URL = "ws://100.102.30.102:8765"
3. Kill python: taskkill /F /IM python.exe
4. Restart: python C:\JarvisNode\jarvis_node.py
5. Verify connection message
```

## Node Status Table

| Node | Tailscale IP | Status | Last Seen |
|------|-------------|--------|-----------|
| MIGUELOMANIAC | 100.83.251.23 | Setup in progress | - |
| PLC-LAPTOP | 100.72.2.99 | Not installed | - |

---

**Remember: Server is at 100.102.30.102:8765 (srv1078052), NOT 100.68.120.99**
