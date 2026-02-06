#!/usr/bin/env python3
"""
Jarvis Node Control CLI v2
Send commands to connected nodes, query registry.
"""

import asyncio
import websockets
import json
import sys
import base64

SERVER = "ws://127.0.0.1:8765"

async def send_command(target: str, action: dict):
    """Send command to a node and get response"""
    async with websockets.connect(SERVER) as ws:
        cmd = {"type": "command", "target": target, "action": action}
        await ws.send(json.dumps(cmd))
        response = await asyncio.wait_for(ws.recv(), timeout=30)
        return json.loads(response)

async def list_nodes(show_capabilities=False):
    """List connected nodes with optional capabilities"""
    async with websockets.connect(SERVER) as ws:
        await ws.send(json.dumps({"type": "list_nodes"}))
        response = await asyncio.wait_for(ws.recv(), timeout=5)
        data = json.loads(response)
        
        if show_capabilities and "registry" in data:
            print("Connected nodes:")
            for name, info in data["registry"].items():
                caps = list(info.get("capabilities", {}).keys())
                connected = info.get("connected_at", "unknown")
                print(f"  {name}:")
                print(f"    capabilities: {', '.join(caps)}")
                print(f"    connected: {connected}")
        else:
            print("Connected nodes:", data.get("nodes", []))
        
        return data

async def find_by_capability(capability: str):
    """Find nodes that support a capability"""
    async with websockets.connect(SERVER) as ws:
        await ws.send(json.dumps({"type": "find_by_capability", "capability": capability}))
        response = await asyncio.wait_for(ws.recv(), timeout=5)
        data = json.loads(response)
        print(f"Nodes with '{capability}': {data.get('nodes', [])}")
        return data

async def screenshot(target: str, output_path: str = None):
    """Take screenshot from target node"""
    result = await send_command(target, {"action": "screenshot"})
    if "image" in result:
        img_data = base64.b64decode(result["image"])
        path = output_path or f"/tmp/jarvis-screenshot-{target}.png"
        with open(path, "wb") as f:
            f.write(img_data)
        print(f"Screenshot saved to: {path}")
        return path
    else:
        print(f"Error: {result}")
        return None

async def shell(target: str, command: str):
    """Run shell command on target node"""
    result = await send_command(target, {"action": "shell", "command": command})
    print(f"Exit code: {result.get('code')}")
    if result.get('stdout'):
        print(f"STDOUT:\n{result['stdout']}")
    if result.get('stderr'):
        print(f"STDERR:\n{result['stderr']}")
    return result

async def click(target: str, x: int, y: int):
    """Click at coordinates on target node"""
    result = await send_command(target, {"action": "click", "x": x, "y": y})
    print(result)
    return result

async def type_text(target: str, text: str):
    """Type text on target node"""
    result = await send_command(target, {"action": "type", "text": text})
    print(result)
    return result

async def ping(target: str):
    """Ping target node"""
    result = await send_command(target, {"action": "ping"})
    print(result)
    return result

async def info(target: str):
    """Get system info from target node"""
    result = await send_command(target, {"action": "info"})
    print(json.dumps(result, indent=2))
    return result

def print_usage():
    print("""Jarvis Node Control CLI v2

Usage: control.py <command> [args...]

Commands:
  list                     List connected nodes
  list -v                  List with capabilities
  find <capability>        Find nodes by capability
  ping <node>              Ping a node
  info <node>              Get node system info
  screenshot <node>        Take screenshot
  shell <node> <cmd>       Run shell command
  click <node> <x> <y>     Click at coordinates
  type <node> <text>       Type text

Examples:
  control.py list -v
  control.py find ollama
  control.py shell PLC-LAPTOP "ollama list"
  control.py screenshot LAPTOP-0KA3C70H
""")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print_usage()
        sys.exit(1)
    
    cmd = sys.argv[1]
    
    if cmd == "list":
        verbose = len(sys.argv) > 2 and sys.argv[2] == "-v"
        asyncio.run(list_nodes(show_capabilities=verbose))
    elif cmd == "find" and len(sys.argv) >= 3:
        asyncio.run(find_by_capability(sys.argv[2]))
    elif cmd == "ping" and len(sys.argv) >= 3:
        asyncio.run(ping(sys.argv[2]))
    elif cmd == "info" and len(sys.argv) >= 3:
        asyncio.run(info(sys.argv[2]))
    elif cmd == "screenshot" and len(sys.argv) >= 3:
        asyncio.run(screenshot(sys.argv[2]))
    elif cmd == "shell" and len(sys.argv) >= 4:
        asyncio.run(shell(sys.argv[2], " ".join(sys.argv[3:])))
    elif cmd == "click" and len(sys.argv) >= 5:
        asyncio.run(click(sys.argv[2], int(sys.argv[3]), int(sys.argv[4])))
    elif cmd == "type" and len(sys.argv) >= 4:
        asyncio.run(type_text(sys.argv[2], " ".join(sys.argv[3:])))
    else:
        print_usage()
        sys.exit(1)
