#!/usr/bin/env python3
"""
Jarvis Node - Remote control agent for FactoryLM Windows laptops
Lean FastAPI server accessible via Tailscale
"""

import os
import sys
import json
import base64
import subprocess
import socket
from datetime import datetime
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import mss
import mss.tools

# Optional imports - graceful degradation
try:
    import pyautogui
    HAS_PYAUTOGUI = True
except ImportError:
    HAS_PYAUTOGUI = False

try:
    import cv2
    HAS_CAMERA = True
except ImportError:
    HAS_CAMERA = False

try:
    import pyperclip
    HAS_CLIPBOARD = True
except ImportError:
    HAS_CLIPBOARD = False

try:
    from interpreter import interpreter
    HAS_INTERPRETER = True
except ImportError:
    HAS_INTERPRETER = False

# =============================================================================
# CONFIGURATION
# =============================================================================
MACHINE_NAME = os.environ.get("JARVIS_MACHINE_NAME", socket.gethostname())
PORT = int(os.environ.get("JARVIS_PORT", 8765))
WORKSPACE = Path(os.environ.get("JARVIS_WORKSPACE", Path.home() / "jarvis-workspace"))
WORKSPACE.mkdir(exist_ok=True)

# =============================================================================
# FASTAPI APP
# =============================================================================
app = FastAPI(
    title=f"Jarvis Node - {MACHINE_NAME}",
    description="Remote control agent for FactoryLM",
    version="1.0.0"
)

# =============================================================================
# REQUEST MODELS
# =============================================================================
class ShellRequest(BaseModel):
    command: str
    timeout: int = 30

class ClickRequest(BaseModel):
    x: int
    y: int
    button: str = "left"
    clicks: int = 1

class TypeRequest(BaseModel):
    text: str
    interval: float = 0.0

class FileReadRequest(BaseModel):
    path: str

class FileWriteRequest(BaseModel):
    path: str
    content: str

class FileListRequest(BaseModel):
    path: str

class ClipboardRequest(BaseModel):
    action: str  # "copy" or "paste"
    content: Optional[str] = None

class InterpreterRequest(BaseModel):
    command: str
    model: str = "ollama/llama3.2:latest"
    auto_run: bool = True  # For RemoteMe, auto-execute

# =============================================================================
# ENDPOINTS
# =============================================================================

@app.get("/health")
def health():
    """Health check endpoint"""
    return {
        "status": "online",
        "machine": MACHINE_NAME,
        "hostname": socket.gethostname(),
        "workspace": str(WORKSPACE),
        "capabilities": {
            "shell": True,
            "screenshot": True,
            "gui": HAS_PYAUTOGUI,
            "camera": HAS_CAMERA,
            "clipboard": HAS_CLIPBOARD,
            "files": True,
            "interpreter": HAS_INTERPRETER
        },
        "timestamp": datetime.now().isoformat()
    }

@app.post("/shell")
def shell(req: ShellRequest):
    """Execute shell command"""
    try:
        result = subprocess.run(
            req.command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=req.timeout,
            cwd=str(WORKSPACE)
        )
        return {
            "stdout": result.stdout,
            "stderr": result.stderr,
            "returncode": result.returncode,
            "command": req.command,
            "timestamp": datetime.now().isoformat()
        }
    except subprocess.TimeoutExpired:
        raise HTTPException(408, f"Command timed out after {req.timeout}s")
    except Exception as e:
        raise HTTPException(500, str(e))

@app.get("/screenshot")
def screenshot(monitor: int = 0):
    """Take screenshot"""
    try:
        with mss.mss() as sct:
            monitors = sct.monitors
            if monitor >= len(monitors):
                monitor = 0
            
            img = sct.grab(monitors[monitor])
            
            # Save locally
            filename = f"screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            filepath = WORKSPACE / filename
            mss.tools.to_png(img.rgb, img.size, output=str(filepath))
            
            # Read and encode
            with open(filepath, "rb") as f:
                img_base64 = base64.b64encode(f.read()).decode()
            
            return {
                "filepath": str(filepath),
                "filename": filename,
                "size": [img.width, img.height],
                "image_base64": img_base64,
                "timestamp": datetime.now().isoformat()
            }
    except Exception as e:
        raise HTTPException(500, str(e))

@app.post("/click")
def click(req: ClickRequest):
    """Click at coordinates"""
    if not HAS_PYAUTOGUI:
        raise HTTPException(501, "pyautogui not installed")
    
    try:
        pyautogui.click(req.x, req.y, button=req.button, clicks=req.clicks)
        return {
            "clicked": [req.x, req.y],
            "button": req.button,
            "clicks": req.clicks,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(500, str(e))

@app.post("/type")
def type_text(req: TypeRequest):
    """Type text"""
    if not HAS_PYAUTOGUI:
        raise HTTPException(501, "pyautogui not installed")
    
    try:
        pyautogui.write(req.text, interval=req.interval)
        return {
            "typed": req.text,
            "length": len(req.text),
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(500, str(e))

@app.post("/keypress")
def keypress(key: str):
    """Press a key or key combination"""
    if not HAS_PYAUTOGUI:
        raise HTTPException(501, "pyautogui not installed")
    
    try:
        if "+" in key:
            # Key combination like "ctrl+s"
            keys = key.split("+")
            pyautogui.hotkey(*keys)
        else:
            pyautogui.press(key)
        return {
            "pressed": key,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(500, str(e))

@app.get("/camera")
def camera(device: int = 0):
    """Capture from camera"""
    if not HAS_CAMERA:
        raise HTTPException(501, "opencv-python not installed")
    
    try:
        cap = cv2.VideoCapture(device)
        if not cap.isOpened():
            raise HTTPException(404, f"Camera {device} not available")
        
        ret, frame = cap.read()
        cap.release()
        
        if not ret:
            raise HTTPException(500, "Failed to capture frame")
        
        # Save
        filename = f"camera_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
        filepath = WORKSPACE / filename
        cv2.imwrite(str(filepath), frame)
        
        # Encode
        with open(filepath, "rb") as f:
            img_base64 = base64.b64encode(f.read()).decode()
        
        return {
            "filepath": str(filepath),
            "filename": filename,
            "size": [frame.shape[1], frame.shape[0]],
            "image_base64": img_base64,
            "timestamp": datetime.now().isoformat()
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, str(e))

@app.post("/clipboard")
def clipboard(req: ClipboardRequest):
    """Read/write clipboard"""
    if not HAS_CLIPBOARD:
        raise HTTPException(501, "pyperclip not installed")
    
    try:
        if req.action == "copy":
            pyperclip.copy(req.content or "")
            return {
                "action": "copy",
                "content": req.content,
                "timestamp": datetime.now().isoformat()
            }
        elif req.action == "paste":
            content = pyperclip.paste()
            return {
                "action": "paste",
                "content": content,
                "timestamp": datetime.now().isoformat()
            }
        else:
            raise HTTPException(400, f"Unknown action: {req.action}")
    except Exception as e:
        raise HTTPException(500, str(e))

@app.post("/file/read")
def file_read(req: FileReadRequest):
    """Read file contents"""
    try:
        path = Path(req.path)
        if not path.exists():
            raise HTTPException(404, f"File not found: {req.path}")
        
        # For binary files, return base64
        try:
            content = path.read_text()
            is_binary = False
        except UnicodeDecodeError:
            content = base64.b64encode(path.read_bytes()).decode()
            is_binary = True
        
        return {
            "path": str(path),
            "content": content,
            "is_binary": is_binary,
            "size": path.stat().st_size,
            "timestamp": datetime.now().isoformat()
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, str(e))

@app.post("/file/write")
def file_write(req: FileWriteRequest):
    """Write file contents"""
    try:
        path = Path(req.path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(req.content)
        
        return {
            "path": str(path),
            "size": len(req.content),
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(500, str(e))

@app.post("/file/list")
def file_list(req: FileListRequest):
    """List directory contents"""
    try:
        path = Path(req.path)
        if not path.exists():
            raise HTTPException(404, f"Path not found: {req.path}")
        if not path.is_dir():
            raise HTTPException(400, f"Not a directory: {req.path}")
        
        items = []
        for item in path.iterdir():
            items.append({
                "name": item.name,
                "path": str(item),
                "is_dir": item.is_dir(),
                "size": item.stat().st_size if item.is_file() else None
            })
        
        return {
            "path": str(path),
            "items": items,
            "count": len(items),
            "timestamp": datetime.now().isoformat()
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, str(e))

@app.post("/interpret")
def interpret(req: InterpreterRequest):
    """Execute natural language command via Open Interpreter"""
    if not HAS_INTERPRETER:
        raise HTTPException(501, "open-interpreter not installed. Run: pip install open-interpreter")
    
    try:
        # Configure interpreter
        interpreter.llm.model = req.model
        interpreter.auto_run = req.auto_run
        interpreter.computer.import_computer_api = True
        
        # Enable computer use features
        interpreter.computer.display.enabled = True
        interpreter.computer.mouse.enabled = True
        interpreter.computer.keyboard.enabled = True
        interpreter.computer.clipboard.enabled = True
        interpreter.computer.files.enabled = True
        interpreter.computer.browser.enabled = True
        
        # Execute command
        result = interpreter.chat(req.command, display=False)
        
        # Extract output
        output_text = ""
        for message in result:
            if hasattr(message, 'content'):
                output_text += str(message.content) + "\n"
            elif isinstance(message, dict) and 'content' in message:
                output_text += str(message['content']) + "\n"
        
        return {
            "command": req.command,
            "output": output_text.strip(),
            "model": req.model,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(500, str(e))

@app.get("/processes")
def processes():
    """List running processes"""
    try:
        if sys.platform == "win32":
            result = subprocess.run(
                ["tasklist", "/FO", "CSV"],
                capture_output=True,
                text=True
            )
        else:
            result = subprocess.run(
                ["ps", "aux"],
                capture_output=True,
                text=True
            )
        
        return {
            "output": result.stdout,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(500, str(e))

# =============================================================================
# MAIN
# =============================================================================
if __name__ == "__main__":
    import uvicorn
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║  🤖 Jarvis Node - {MACHINE_NAME:^40} ║
╠══════════════════════════════════════════════════════════════╣
║  Workspace: {str(WORKSPACE):<46} ║
║  Port:      {PORT:<46} ║
║  Docs:      http://localhost:{PORT}/docs{' ' * (40 - len(str(PORT)))} ║
╚══════════════════════════════════════════════════════════════╝
    """)
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=PORT,
        log_level="info"
    )
