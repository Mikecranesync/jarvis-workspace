#!/usr/bin/env python3
"""
Jarvis Edge Node Client v2
Connects to VPS server and announces capabilities.
"""

import asyncio
import websockets
import json
import base64
import os
import sys
import subprocess
import platform
from datetime import datetime

# Configuration
SERVER_URL = os.environ.get("JARVIS_SERVER", "ws://100.102.30.102:8765")
NODE_NAME = os.environ.get("JARVIS_NODE_NAME", os.environ.get("COMPUTERNAME", platform.node()))

def detect_capabilities():
    """Auto-detect what this node can do"""
    caps = {
        "ping": True,
        "shell": True,
        "info": True,
    }
    
    # Check for GUI (screenshot/click/type)
    try:
        import pyautogui
        caps["screenshot"] = True
        caps["click"] = True
        caps["type"] = True
        caps["hotkey"] = True
    except ImportError:
        pass
    
    # Check for Ollama
    try:
        result = subprocess.run(["ollama", "--version"], capture_output=True, timeout=5)
        if result.returncode == 0:
            caps["ollama"] = True
    except:
        pass
    
    # Check for GPU
    try:
        result = subprocess.run(["nvidia-smi", "--query-gpu=name", "--format=csv,noheader"], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            caps["gpu"] = result.stdout.strip()
    except:
        pass
    
    return caps

async def handle_command(cmd):
    """Execute command and return result"""
    action = cmd.get("action")
    
    if action == "ping":
        return {"status": "pong", "node": NODE_NAME, "time": datetime.now().isoformat()}
    
    elif action == "info":
        caps = detect_capabilities()
        return {
            "node": NODE_NAME,
            "platform": platform.system(),
            "hostname": platform.node(),
            "capabilities": caps
        }
    
    elif action == "shell":
        try:
            result = subprocess.run(
                cmd.get("command", "echo hi"),
                shell=True,
                capture_output=True,
                text=True,
                timeout=cmd.get("timeout", 30)
            )
            return {"stdout": result.stdout, "stderr": result.stderr, "code": result.returncode}
        except subprocess.TimeoutExpired:
            return {"error": "Command timed out", "code": -1}
        except Exception as e:
            return {"error": str(e), "code": -1}
    
    elif action == "screenshot":
        try:
            import pyautogui
            import io
            img = pyautogui.screenshot()
            buf = io.BytesIO()
            img.save(buf, format='PNG')
            return {"image": base64.b64encode(buf.getvalue()).decode()}
        except Exception as e:
            return {"error": f"Screenshot failed: {e}"}
    
    elif action == "click":
        try:
            import pyautogui
            pyautogui.click(cmd.get("x", 0), cmd.get("y", 0))
            return {"status": "clicked", "x": cmd.get("x"), "y": cmd.get("y")}
        except Exception as e:
            return {"error": f"Click failed: {e}"}
    
    elif action == "type":
        try:
            import pyautogui
            pyautogui.write(cmd.get("text", ""), interval=0.02)
            return {"status": "typed", "length": len(cmd.get("text", ""))}
        except Exception as e:
            return {"error": f"Type failed: {e}"}
    
    elif action == "hotkey":
        try:
            import pyautogui
            pyautogui.hotkey(*cmd.get("keys", []))
            return {"status": "hotkey sent", "keys": cmd.get("keys")}
        except Exception as e:
            return {"error": f"Hotkey failed: {e}"}
    
    elif action == "ollama":
        try:
            model = cmd.get("model", "llama3.1:8b")
            prompt = cmd.get("prompt", "Hello")
            result = subprocess.run(
                ["ollama", "run", model, prompt],
                capture_output=True,
                text=True,
                timeout=cmd.get("timeout", 120)
            )
            return {"response": result.stdout, "stderr": result.stderr, "code": result.returncode}
        except Exception as e:
            return {"error": f"Ollama failed: {e}"}
    
    return {"error": f"Unknown action: {action}"}

async def main():
    capabilities = detect_capabilities()
    print(f"Jarvis Edge Node '{NODE_NAME}' starting...", flush=True)
    print(f"Detected capabilities: {list(capabilities.keys())}", flush=True)
    print(f"Connecting to {SERVER_URL}", flush=True)
    
    while True:
        try:
            async with websockets.connect(SERVER_URL) as ws:
                # Register with capabilities
                await ws.send(json.dumps({
                    "type": "register",
                    "name": NODE_NAME,
                    "capabilities": capabilities
                }))
                
                response = await ws.recv()
                data = json.loads(response)
                print(f"[OK] {data.get('status', 'connected')} as '{NODE_NAME}'", flush=True)
                
                # Handle incoming commands
                async for message in ws:
                    try:
                        cmd = json.loads(message)
                        action = cmd.get('action', 'unknown')
                        print(f"<- Command: {action}", flush=True)
                        result = await handle_command(cmd)
                        await ws.send(json.dumps(result))
                        print(f"-> Response sent", flush=True)
                    except Exception as e:
                        await ws.send(json.dumps({"error": str(e)}))
                        print(f"[ERR] {e}", flush=True)
        
        except Exception as e:
            print(f"[ERR] Connection error: {e}. Retrying in 5s...", flush=True)
            await asyncio.sleep(5)

if __name__ == "__main__":
    asyncio.run(main())
