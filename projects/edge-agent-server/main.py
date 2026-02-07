#!/usr/bin/env python3
"""
FactoryLM Edge Agent Server API
A FastAPI server for managing edge devices
"""

import os
import uuid
import sqlite3
from datetime import datetime
from typing import List, Optional, Dict, Any
import logging
import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Depends, Header, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, validator
import aiosqlite

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configuration
DATABASE_PATH = os.getenv("DATABASE_PATH", "./devices.db")
AUTH_TOKEN = os.getenv("X_AGENT_TOKEN", "factorylm-agent-token-2025")

# Pydantic Models
class DeviceConfig(BaseModel):
    """Device configuration schema"""
    lid_close_action: str = Field(default="do_nothing", description="Action when laptop lid closes")
    sleep_timeout_ac: int = Field(default=0, description="Sleep timeout when on AC power (0=never)")
    hibernate: bool = Field(default=False, description="Enable hibernation")
    tailscale_enabled: bool = Field(default=True, description="Enable Tailscale VPN")
    monitoring_interval: int = Field(default=60, description="Heartbeat interval in seconds")
    
    @validator('lid_close_action')
    def validate_lid_action(cls, v):
        valid_actions = ['do_nothing', 'sleep', 'hibernate', 'shutdown']
        if v not in valid_actions:
            raise ValueError(f'lid_close_action must be one of {valid_actions}')
        return v
    
    @validator('sleep_timeout_ac')
    def validate_sleep_timeout(cls, v):
        if v < 0:
            raise ValueError('sleep_timeout_ac must be >= 0')
        return v
    
    @validator('monitoring_interval')
    def validate_interval(cls, v):
        if v < 30 or v > 3600:
            raise ValueError('monitoring_interval must be between 30 and 3600 seconds')
        return v

class DeviceRegistration(BaseModel):
    """Device registration request"""
    hostname: str = Field(..., min_length=1, max_length=255, description="Device hostname")
    os_info: str = Field(..., min_length=1, description="Operating system information")
    ip_address: Optional[str] = Field(None, description="Device IP address")
    mac_address: Optional[str] = Field(None, description="Device MAC address")

class DeviceHeartbeat(BaseModel):
    """Device heartbeat/status update"""
    online: bool = Field(default=True, description="Device online status")
    battery_percent: Optional[float] = Field(None, description="Battery percentage (0-100)")
    plc_connection_status: Optional[str] = Field(None, description="PLC connection status")
    cpu_usage: Optional[float] = Field(None, description="CPU usage percentage")
    memory_usage: Optional[float] = Field(None, description="Memory usage percentage")
    disk_usage: Optional[float] = Field(None, description="Disk usage percentage")
    
    @validator('battery_percent')
    def validate_battery(cls, v):
        if v is not None and (v < 0 or v > 100):
            raise ValueError('battery_percent must be between 0 and 100')
        return v

class Device(BaseModel):
    """Complete device model"""
    device_id: str
    hostname: str
    os_info: str
    ip_address: Optional[str] = None
    mac_address: Optional[str] = None
    config: DeviceConfig
    last_seen: datetime
    online: bool = True
    battery_percent: Optional[float] = None
    plc_connection_status: Optional[str] = None
    cpu_usage: Optional[float] = None
    memory_usage: Optional[float] = None
    disk_usage: Optional[float] = None
    created_at: datetime
    updated_at: datetime

class DeviceResponse(BaseModel):
    """Device response model for API"""
    device_id: str
    hostname: str
    config: DeviceConfig

class DeviceListItem(BaseModel):
    """Device list item for GET /api/devices"""
    device_id: str
    hostname: str
    os_info: str
    last_seen: datetime
    online: bool
    battery_percent: Optional[float] = None
    plc_connection_status: Optional[str] = None
    created_at: datetime

class ErrorResponse(BaseModel):
    """Standard error response"""
    error: str
    detail: Optional[str] = None

# Database functions
async def init_database():
    """Initialize SQLite database with tables"""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS devices (
                device_id TEXT PRIMARY KEY,
                hostname TEXT NOT NULL,
                os_info TEXT NOT NULL,
                ip_address TEXT,
                mac_address TEXT,
                config TEXT NOT NULL,  -- JSON string
                last_seen TEXT NOT NULL,  -- ISO datetime
                online BOOLEAN DEFAULT 1,
                battery_percent REAL,
                plc_connection_status TEXT,
                cpu_usage REAL,
                memory_usage REAL,
                disk_usage REAL,
                created_at TEXT NOT NULL,  -- ISO datetime
                updated_at TEXT NOT NULL   -- ISO datetime
            )
        """)
        await db.execute("""
            CREATE INDEX IF NOT EXISTS idx_devices_hostname ON devices(hostname)
        """)
        await db.execute("""
            CREATE INDEX IF NOT EXISTS idx_devices_last_seen ON devices(last_seen)
        """)
        await db.commit()
    logger.info("Database initialized successfully")

async def get_device_by_id(device_id: str) -> Optional[dict]:
    """Get device by ID from database"""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("SELECT * FROM devices WHERE device_id = ?", (device_id,)) as cursor:
            row = await cursor.fetchone()
            if row:
                return dict(row)
    return None

async def create_device(registration: DeviceRegistration) -> str:
    """Create a new device in database"""
    device_id = str(uuid.uuid4())
    now = datetime.utcnow().isoformat()
    default_config = DeviceConfig()
    
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute("""
            INSERT INTO devices (
                device_id, hostname, os_info, ip_address, mac_address,
                config, last_seen, online, created_at, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            device_id, registration.hostname, registration.os_info,
            registration.ip_address, registration.mac_address,
            default_config.json(), now, True, now, now
        ))
        await db.commit()
    
    logger.info(f"Created new device: {device_id} ({registration.hostname})")
    return device_id

async def update_device_heartbeat(device_id: str, heartbeat: DeviceHeartbeat):
    """Update device heartbeat/status"""
    now = datetime.utcnow().isoformat()
    
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute("""
            UPDATE devices SET
                last_seen = ?,
                online = ?,
                battery_percent = ?,
                plc_connection_status = ?,
                cpu_usage = ?,
                memory_usage = ?,
                disk_usage = ?,
                updated_at = ?
            WHERE device_id = ?
        """, (
            now, heartbeat.online, heartbeat.battery_percent,
            heartbeat.plc_connection_status, heartbeat.cpu_usage,
            heartbeat.memory_usage, heartbeat.disk_usage,
            now, device_id
        ))
        await db.commit()

async def update_device_config(device_id: str, config: DeviceConfig):
    """Update device configuration"""
    now = datetime.utcnow().isoformat()
    
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute("""
            UPDATE devices SET config = ?, updated_at = ? WHERE device_id = ?
        """, (config.json(), now, device_id))
        await db.commit()

async def list_devices() -> List[dict]:
    """List all devices"""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("SELECT * FROM devices ORDER BY last_seen DESC") as cursor:
            rows = await cursor.fetchall()
            return [dict(row) for row in rows]

# Authentication
async def verify_auth_token(x_agent_token: str = Header(alias="X-Agent-Token")):
    """Verify authentication token"""
    if x_agent_token != AUTH_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token"
        )
    return x_agent_token

# Lifespan context manager
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Starting FactoryLM Edge Agent Server...")
    await init_database()
    yield
    # Shutdown
    logger.info("Shutting down FactoryLM Edge Agent Server...")

# FastAPI app
app = FastAPI(
    title="FactoryLM Edge Agent Server",
    description="API for managing FactoryLM edge devices",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Exception handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(error=exc.detail).dict()
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content=ErrorResponse(error="Internal server error", detail=str(exc)).dict()
    )

# Health check endpoint (no auth required)
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}

# API Endpoints
@app.post("/api/devices/register", response_model=DeviceResponse)
async def register_device(
    registration: DeviceRegistration,
    token: str = Depends(verify_auth_token)
):
    """Register a new device"""
    try:
        device_id = await create_device(registration)
        
        # Get the created device
        device_data = await get_device_by_id(device_id)
        if not device_data:
            raise HTTPException(status_code=500, detail="Failed to retrieve created device")
        
        import json
        config = DeviceConfig.parse_raw(device_data['config'])
        
        return DeviceResponse(
            device_id=device_id,
            hostname=device_data['hostname'],
            config=config
        )
    except Exception as e:
        logger.error(f"Error registering device: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/devices/{device_id}/config", response_model=DeviceConfig)
async def get_device_config(
    device_id: str,
    token: str = Depends(verify_auth_token)
):
    """Get device configuration"""
    device_data = await get_device_by_id(device_id)
    if not device_data:
        raise HTTPException(status_code=404, detail="Device not found")
    
    import json
    config = DeviceConfig.parse_raw(device_data['config'])
    return config

@app.post("/api/devices/{device_id}/heartbeat")
async def device_heartbeat(
    device_id: str,
    heartbeat: DeviceHeartbeat,
    token: str = Depends(verify_auth_token)
):
    """Update device heartbeat/status"""
    device_data = await get_device_by_id(device_id)
    if not device_data:
        raise HTTPException(status_code=404, detail="Device not found")
    
    await update_device_heartbeat(device_id, heartbeat)
    return {"status": "success", "timestamp": datetime.utcnow().isoformat()}

@app.get("/api/devices", response_model=List[DeviceListItem])
async def list_all_devices(token: str = Depends(verify_auth_token)):
    """List all registered devices"""
    devices_data = await list_devices()
    
    result = []
    for device_data in devices_data:
        result.append(DeviceListItem(
            device_id=device_data['device_id'],
            hostname=device_data['hostname'],
            os_info=device_data['os_info'],
            last_seen=datetime.fromisoformat(device_data['last_seen']),
            online=bool(device_data['online']),
            battery_percent=device_data['battery_percent'],
            plc_connection_status=device_data['plc_connection_status'],
            created_at=datetime.fromisoformat(device_data['created_at'])
        ))
    
    return result

@app.put("/api/devices/{device_id}/config")
async def update_config(
    device_id: str,
    config: DeviceConfig,
    token: str = Depends(verify_auth_token)
):
    """Update device configuration"""
    device_data = await get_device_by_id(device_id)
    if not device_data:
        raise HTTPException(status_code=404, detail="Device not found")
    
    await update_device_config(device_id, config)
    return {"status": "success", "timestamp": datetime.utcnow().isoformat()}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8090)
# Dashboard route
from fastapi.responses import HTMLResponse, FileResponse

@app.get("/dashboard", response_class=HTMLResponse)
async def serve_dashboard():
    """Serve the web dashboard"""
    dashboard_path = os.path.join(os.path.dirname(__file__), "dashboard.html")
    if os.path.exists(dashboard_path):
        with open(dashboard_path, "r") as f:
            return HTMLResponse(content=f.read())
    return HTMLResponse(content="<h1>Dashboard not found</h1>", status_code=404)
