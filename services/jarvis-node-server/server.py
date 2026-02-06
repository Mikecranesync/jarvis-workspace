#!/usr/bin/env python3
"""
Jarvis Node Server v4 - With Agent Registry
Tracks connected nodes and their capabilities for intelligent routing.
"""

import asyncio
import websockets
import json
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
log = logging.getLogger("jarvis-node-server")

# Node Registry: {name: {"ws": websocket, "queue": Queue, "capabilities": dict, "connected_at": str}}
nodes = {}

def get_registry():
    """Get registry snapshot for API responses"""
    return {
        name: {
            "capabilities": info.get("capabilities", {}),
            "connected_at": info.get("connected_at"),
            "online": True
        }
        for name, info in nodes.items()
    }

async def handle_client(websocket):
    """Handle a connected client (node or controller)"""
    node_name = None
    response_queue = asyncio.Queue()
    
    try:
        log.info("connection open")
        async for message in websocket:
            try:
                data = json.loads(message)
                msg_type = data.get("type")
                
                # Node registration with capabilities
                if msg_type == "register":
                    node_name = data.get("name", "unknown")
                    capabilities = data.get("capabilities", {})
                    
                    # Default capabilities if not provided
                    if not capabilities:
                        capabilities = {
                            "screenshot": True,
                            "shell": True,
                            "click": True,
                            "type": True,
                            "ping": True
                        }
                    
                    nodes[node_name] = {
                        "ws": websocket,
                        "queue": response_queue,
                        "capabilities": capabilities,
                        "connected_at": datetime.utcnow().isoformat()
                    }
                    log.info(f"Node registered: {node_name} | capabilities: {list(capabilities.keys())}")
                    await websocket.send(json.dumps({
                        "status": "registered",
                        "name": node_name,
                        "capabilities_received": list(capabilities.keys())
                    }))
                
                # Controller sending command to a node
                elif msg_type == "command":
                    target = data.get("target")
                    action = data.get("action", {})
                    
                    if target not in nodes:
                        await websocket.send(json.dumps({
                            "error": f"Node '{target}' not connected",
                            "available_nodes": list(nodes.keys())
                        }))
                        continue
                    
                    # Check capability
                    action_type = action.get("action", "unknown")
                    target_caps = nodes[target].get("capabilities", {})
                    if action_type not in target_caps and action_type != "unknown":
                        await websocket.send(json.dumps({
                            "error": f"Node '{target}' doesn't support '{action_type}'",
                            "node_capabilities": list(target_caps.keys())
                        }))
                        continue
                    
                    target_node = nodes[target]
                    target_ws = target_node["ws"]
                    target_queue = target_node["queue"]
                    
                    # Drain any old responses
                    while not target_queue.empty():
                        try:
                            target_queue.get_nowait()
                        except:
                            break
                    
                    await target_ws.send(json.dumps(action))
                    log.info(f"Sent command to {target}: {action_type}")
                    
                    # Wait for response
                    try:
                        response = await asyncio.wait_for(target_queue.get(), timeout=30)
                        await websocket.send(response)
                        log.info(f"Relayed response from {target}")
                    except asyncio.TimeoutError:
                        await websocket.send(json.dumps({"error": "Command timed out"}))
                
                # List connected nodes with capabilities
                elif msg_type == "list_nodes":
                    registry = get_registry()
                    await websocket.send(json.dumps({
                        "nodes": list(nodes.keys()),
                        "registry": registry
                    }))
                
                # Find nodes by capability
                elif msg_type == "find_by_capability":
                    capability = data.get("capability")
                    matching = [
                        name for name, info in nodes.items()
                        if info.get("capabilities", {}).get(capability)
                    ]
                    await websocket.send(json.dumps({
                        "capability": capability,
                        "nodes": matching
                    }))
                
                # Response from a node
                else:
                    if node_name and node_name in nodes:
                        await nodes[node_name]["queue"].put(message)
                        log.info(f"Queued response from {node_name}")
                    
            except json.JSONDecodeError:
                log.error("Invalid JSON")
                
    except websockets.exceptions.ConnectionClosed:
        log.info(f"Disconnected: {node_name or 'client'}")
    except Exception as e:
        log.error(f"Error: {e}")
    finally:
        if node_name and node_name in nodes:
            del nodes[node_name]
            log.info(f"Node removed: {node_name}")

async def main():
    log.info("Jarvis Node Server v4 (with Registry) starting on ws://0.0.0.0:8765")
    async with websockets.serve(handle_client, "0.0.0.0", 8765):
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())
