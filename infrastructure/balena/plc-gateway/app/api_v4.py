#!/usr/bin/env python3
"""
FactoryLM Edge v4.0 - Unified API
Bridges React Dashboard to Micro820 via EtherNet/IP (pycomm3)

Endpoints match the existing React frontend expectations:
- GET /api/plc/status
- GET /api/plc/io
- POST /api/plc/connect
- POST /api/plc/write-coil
- WebSocket /ws/io
"""

import asyncio
import json
import logging
from datetime import datetime
from typing import Optional, Set

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from pycomm3 import LogixDriver

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("plc-gateway-v4")

app = FastAPI(title="FactoryLM Edge v4.0", version="4.0.0")

# CORS for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global PLC connection state
plc_state = {
    "connected": False,
    "ip": None,
    "port": 44818,
    "last_seen": None,
    "driver": None,
}

# WebSocket clients
ws_clients: Set[WebSocket] = set()


# ═══════════════════════════════════════════════════════════════
# MODELS
# ═══════════════════════════════════════════════════════════════

class ConnectRequest(BaseModel):
    ip: str
    port: int = 44818

class WriteCoilRequest(BaseModel):
    address: int
    value: bool

class WriteTagRequest(BaseModel):
    tag: str
    value: any


# ═══════════════════════════════════════════════════════════════
# TAG MAPPINGS (Micro820 specific)
# ═══════════════════════════════════════════════════════════════

# Map frontend coil addresses to actual Micro820 tags
COIL_TO_TAG = {
    # Program variables (0-6)
    0: "motor_running",
    1: "motor_stopped",
    2: "fault_alarm",
    3: "conveyor_running",
    4: "sensor_1_active",
    5: "sensor_2_active",
    6: "e_stop_active",
    # Physical outputs (15-17) - these ARE controllable
    15: "_IO_EM_DO_00",
    16: "_IO_EM_DO_01",
    17: "_IO_EM_DO_03",
}

# Physical I/O tags
INPUT_TAGS = [
    "_IO_EM_DI_00", "_IO_EM_DI_01", "_IO_EM_DI_02", "_IO_EM_DI_03",
    "_IO_EM_DI_04", "_IO_EM_DI_05", "_IO_EM_DI_06", "_IO_EM_DI_07",
    "_IO_EM_DI_08", "_IO_EM_DI_09", "_IO_EM_DI_10", "_IO_EM_DI_11",
]

OUTPUT_TAGS = [
    "_IO_EM_DO_00", "_IO_EM_DO_01", "_IO_EM_DO_02", "_IO_EM_DO_03",
    "_IO_EM_DO_04", "_IO_EM_DO_05", "_IO_EM_DO_06",
]


# ═══════════════════════════════════════════════════════════════
# PLC CONNECTION
# ═══════════════════════════════════════════════════════════════

def get_driver() -> Optional[LogixDriver]:
    """Get or create PLC driver."""
    if plc_state["driver"] and plc_state["connected"]:
        return plc_state["driver"]
    return None


def connect_plc(ip: str) -> bool:
    """Connect to PLC via EtherNet/IP."""
    try:
        # Close existing connection
        if plc_state["driver"]:
            try:
                plc_state["driver"].close()
            except:
                pass

        driver = LogixDriver(ip)
        driver.open()

        plc_state["driver"] = driver
        plc_state["connected"] = True
        plc_state["ip"] = ip
        plc_state["last_seen"] = datetime.now().isoformat()

        logger.info(f"✅ Connected to PLC at {ip}")
        return True

    except Exception as e:
        logger.error(f"❌ Connection failed: {e}")
        plc_state["connected"] = False
        plc_state["driver"] = None
        return False


def read_all_io() -> dict:
    """Read all I/O from PLC."""
    driver = get_driver()
    if not driver:
        return {"error": "Not connected", "connected": False}

    try:
        # Read all inputs
        inputs = {}
        for i, tag in enumerate(INPUT_TAGS):
            result = driver.read(tag)
            if result.value is not None:
                inputs[f"DI_{i:02d}"] = bool(result.value)

        # Read all outputs
        outputs = {}
        for i, tag in enumerate(OUTPUT_TAGS):
            result = driver.read(tag)
            if result.value is not None:
                outputs[f"DO_{i:02d}"] = bool(result.value)

        # Read program variables (if they exist)
        coils = {
            "motor_running": False,
            "motor_stopped": False,
            "fault_alarm": False,
            "conveyor_running": False,
            "sensor_1_active": False,
            "sensor_2_active": False,
            "e_stop_active": False,
        }

        for name in coils.keys():
            try:
                result = driver.read(name)
                if result.value is not None:
                    coils[name] = bool(result.value)
            except:
                pass  # Tag might not exist

        # Read registers (if they exist)
        registers = {
            "motor_speed": 0,
            "motor_current": 0,
            "temperature": 0,
            "pressure": 0,
            "conveyor_speed": 0,
            "error_code": 0,
        }

        for name in registers.keys():
            try:
                result = driver.read(name)
                if result.value is not None:
                    registers[name] = result.value
            except:
                pass

        plc_state["last_seen"] = datetime.now().isoformat()

        return {
            "coils": coils,
            "inputs": inputs,
            "outputs": outputs,
            "registers": registers,
            "timestamp": datetime.now().isoformat(),
            "connected": True,
        }

    except Exception as e:
        logger.error(f"Read error: {e}")
        plc_state["connected"] = False
        return {"error": str(e), "connected": False}


# ═══════════════════════════════════════════════════════════════
# API ENDPOINTS
# ═══════════════════════════════════════════════════════════════

@app.get("/api/health")
async def health():
    return {"status": "healthy", "version": "4.0.0"}


@app.get("/api/plc/status")
async def plc_status():
    """Get PLC connection status."""
    return {
        "connected": plc_state["connected"],
        "ip": plc_state["ip"],
        "port": plc_state["port"],
        "last_seen": plc_state["last_seen"],
    }


@app.post("/api/plc/connect")
async def plc_connect(request: ConnectRequest):
    """Connect to PLC."""
    success = connect_plc(request.ip)
    return {
        "success": success,
        "message": "Connected" if success else "Connection failed",
    }


@app.get("/api/plc/io")
async def plc_io():
    """Read all I/O from PLC."""
    if not plc_state["connected"]:
        raise HTTPException(status_code=503, detail="Not connected to PLC")

    data = read_all_io()
    if "error" in data:
        raise HTTPException(status_code=503, detail=data["error"])

    return data


@app.post("/api/plc/write-coil")
async def write_coil(request: WriteCoilRequest):
    """Write to a coil/output."""
    driver = get_driver()
    if not driver:
        raise HTTPException(status_code=503, detail="Not connected to PLC")

    tag = COIL_TO_TAG.get(request.address)
    if not tag:
        raise HTTPException(status_code=400, detail=f"Unknown coil address: {request.address}")

    try:
        result = driver.write(tag, request.value)
        if result.value is not None:
            logger.info(f"✅ Wrote {tag} = {request.value}")
            return {"success": True, "tag": tag, "value": request.value}
        else:
            raise HTTPException(status_code=500, detail=f"Write failed: {result.error}")
    except Exception as e:
        logger.error(f"Write error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/plc/write")
async def write_tag(request: WriteTagRequest):
    """Write to any tag by name."""
    driver = get_driver()
    if not driver:
        raise HTTPException(status_code=503, detail="Not connected to PLC")

    try:
        result = driver.write(request.tag, request.value)
        if result.value is not None:
            return {"success": True, "tag": request.tag, "value": request.value}
        else:
            raise HTTPException(status_code=500, detail=f"Write failed")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ═══════════════════════════════════════════════════════════════
# WEBSOCKET FOR REAL-TIME I/O
# ═══════════════════════════════════════════════════════════════

@app.websocket("/ws/io")
async def websocket_io(websocket: WebSocket):
    """WebSocket endpoint for real-time I/O updates."""
    await websocket.accept()
    ws_clients.add(websocket)
    logger.info(f"WebSocket client connected ({len(ws_clients)} total)")

    try:
        while True:
            if plc_state["connected"]:
                data = read_all_io()
                await websocket.send_json(data)
            else:
                await websocket.send_json({
                    "error": "Not connected to PLC",
                    "connected": False,
                })
            await asyncio.sleep(0.1)  # 100ms updates

    except WebSocketDisconnect:
        ws_clients.discard(websocket)
        logger.info(f"WebSocket client disconnected ({len(ws_clients)} remaining)")


# ═══════════════════════════════════════════════════════════════
# STATIC FILES (React Dashboard)
# ═══════════════════════════════════════════════════════════════

# Serve React build from /static
import os
STATIC_DIR = "/app/static"
if os.path.exists(STATIC_DIR):
    app.mount("/assets", StaticFiles(directory=f"{STATIC_DIR}/assets"), name="assets")

    @app.get("/")
    async def serve_spa():
        return FileResponse(f"{STATIC_DIR}/index.html")

    @app.get("/{path:path}")
    async def serve_spa_routes(path: str):
        # API routes handled above
        if path.startswith("api/") or path.startswith("ws/"):
            raise HTTPException(status_code=404)
        return FileResponse(f"{STATIC_DIR}/index.html")


# ═══════════════════════════════════════════════════════════════
# AUTO-CONNECT ON STARTUP
# ═══════════════════════════════════════════════════════════════

@app.on_event("startup")
async def startup():
    """Try to connect to PLC on startup."""
    default_ip = os.environ.get("PLC_IP", "192.168.1.100")
    logger.info(f"🚀 FactoryLM Edge v4.0 starting...")
    logger.info(f"🔌 Attempting connection to {default_ip}...")
    connect_plc(default_ip)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)
