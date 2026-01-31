#!/usr/bin/env python3
"""
ShopTalk Auto-Connect Service
Runs on BeagleBone/edge device to automatically discover and connect to PLCs.

Features:
- Network scanning on startup
- Continuous monitoring of discovered devices
- Auto-reconnection on disconnect
- Profile-based register mapping
- REST API for status and control
"""

import asyncio
import json
import logging
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict, field
from datetime import datetime

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import uvicorn

# Import our scanner
from scanner import NetworkScanner, DiscoveredDevice

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("AutoConnect")

# Try to import pymodbus
try:
    from pymodbus.client import ModbusTcpClient
    HAS_PYMODBUS = True
except ImportError:
    HAS_PYMODBUS = False


@dataclass
class ConnectedDevice:
    """A device we're actively monitoring."""
    device: DiscoveredDevice
    connected: bool = False
    last_seen: Optional[str] = None
    last_values: Dict = field(default_factory=dict)
    error_count: int = 0


class AutoConnectService:
    """Manages auto-discovery and connection to industrial devices."""
    
    def __init__(self, config_path: str = None):
        self.scanner = NetworkScanner(timeout=2.0)
        self.devices: Dict[str, ConnectedDevice] = {}
        self.clients: Dict[str, ModbusTcpClient] = {}
        self.running = False
        self.scan_interval = 300  # Rescan every 5 minutes
        self.poll_interval = 1.0  # Poll devices every second
        
        # Load config
        self.config = self._load_config(config_path)
        
        # Load profiles
        self.profiles = self.scanner.profiles
    
    def _load_config(self, config_path: str) -> Dict:
        """Load configuration."""
        default_config = {
            "network": None,  # Auto-detect
            "scan_on_startup": True,
            "auto_connect": True,
            "poll_interval": 1.0,
            "rescan_interval": 300
        }
        
        if config_path and Path(config_path).exists():
            with open(config_path) as f:
                user_config = json.load(f)
            default_config.update(user_config)
        
        return default_config
    
    async def start(self):
        """Start the auto-connect service."""
        logger.info("🚀 Starting ShopTalk Auto-Connect Service")
        self.running = True
        
        # Initial scan
        if self.config.get("scan_on_startup", True):
            await self.scan_network()
        
        # Start background tasks
        asyncio.create_task(self._poll_loop())
        asyncio.create_task(self._rescan_loop())
        
        logger.info("✅ Auto-Connect Service running")
    
    async def stop(self):
        """Stop the service."""
        logger.info("Stopping Auto-Connect Service...")
        self.running = False
        
        # Disconnect all clients
        for ip, client in self.clients.items():
            try:
                client.close()
            except:
                pass
        
        self.clients.clear()
    
    async def scan_network(self, network: str = None) -> List[DiscoveredDevice]:
        """Scan network for devices."""
        network = network or self.config.get("network") or self.scanner.get_local_network()
        
        logger.info(f"🔍 Scanning network: {network}")
        
        # Run scan in thread pool (blocking operation)
        loop = asyncio.get_event_loop()
        devices = await loop.run_in_executor(
            None, 
            self.scanner.scan_network, 
            network
        )
        
        logger.info(f"📡 Found {len(devices)} device(s)")
        
        # Update our device list
        for device in devices:
            key = f"{device.ip}:{device.port}"
            if key not in self.devices:
                self.devices[key] = ConnectedDevice(device=device)
                logger.info(f"  ✅ New device: {key} ({device.protocol})")
                
                if self.config.get("auto_connect", True):
                    await self.connect_device(key)
        
        return devices
    
    async def connect_device(self, device_key: str) -> bool:
        """Connect to a specific device."""
        if device_key not in self.devices:
            return False
        
        conn = self.devices[device_key]
        device = conn.device
        
        if device.protocol != "modbus_tcp" or not HAS_PYMODBUS:
            logger.warning(f"Cannot connect to {device_key}: unsupported protocol")
            return False
        
        try:
            client = ModbusTcpClient(device.ip, port=device.port, timeout=2)
            if client.connect():
                self.clients[device_key] = client
                conn.connected = True
                conn.last_seen = datetime.now().isoformat()
                logger.info(f"🔗 Connected to {device_key}")
                return True
            else:
                logger.error(f"Failed to connect to {device_key}")
                return False
        except Exception as e:
            logger.error(f"Connection error for {device_key}: {e}")
            return False
    
    async def _poll_loop(self):
        """Continuously poll connected devices."""
        while self.running:
            for device_key, conn in self.devices.items():
                if not conn.connected:
                    continue
                
                client = self.clients.get(device_key)
                if not client:
                    continue
                
                try:
                    device = conn.device
                    slave_id = device.slave_id or 1
                    
                    # Read registers based on profile or default
                    if device.profile_match and device.profile_match in self.profiles:
                        profile = self.profiles[device.profile_match]
                        values = await self._read_profile_registers(client, profile, slave_id)
                    else:
                        # Default: read first 10 holding registers
                        result = client.read_holding_registers(0, 10, slave=slave_id)
                        if not result.isError():
                            values = {f"register_{i}": v for i, v in enumerate(result.registers)}
                        else:
                            values = {}
                    
                    conn.last_values = values
                    conn.last_seen = datetime.now().isoformat()
                    conn.error_count = 0
                    
                except Exception as e:
                    conn.error_count += 1
                    if conn.error_count >= 3:
                        logger.warning(f"Lost connection to {device_key}")
                        conn.connected = False
                        try:
                            client.close()
                        except:
                            pass
            
            await asyncio.sleep(self.poll_interval)
    
    async def _read_profile_registers(self, client, profile: Dict, slave_id: int) -> Dict:
        """Read registers according to device profile."""
        values = {}
        
        for addr_str, reg_info in profile.get("registers", {}).items():
            try:
                # Parse address
                addr = int(addr_str.replace("4", "", 1)) if addr_str.startswith("4") else int(addr_str)
                
                # Read based on type
                reg_type = reg_info.get("type", "uint16")
                if reg_type in ["uint16", "int16"]:
                    result = client.read_holding_registers(addr, 1, slave=slave_id)
                    if not result.isError():
                        value = result.registers[0]
                        scale = reg_info.get("scale", 1)
                        values[reg_info["name"]] = value * scale
                elif reg_type == "coil":
                    result = client.read_coils(addr, 1, slave=slave_id)
                    if not result.isError():
                        values[reg_info["name"]] = result.bits[0]
            except:
                pass
        
        return values
    
    async def _rescan_loop(self):
        """Periodically rescan the network."""
        while self.running:
            await asyncio.sleep(self.scan_interval)
            await self.scan_network()
    
    def get_status(self) -> Dict:
        """Get current status of all devices."""
        return {
            "running": self.running,
            "device_count": len(self.devices),
            "connected_count": sum(1 for d in self.devices.values() if d.connected),
            "devices": {
                key: {
                    "ip": conn.device.ip,
                    "port": conn.device.port,
                    "protocol": conn.device.protocol,
                    "connected": conn.connected,
                    "last_seen": conn.last_seen,
                    "profile": conn.device.profile_match,
                    "values": conn.last_values
                }
                for key, conn in self.devices.items()
            }
        }


# FastAPI app
app = FastAPI(title="ShopTalk Auto-Connect", version="1.0")
service = AutoConnectService()


@app.on_event("startup")
async def startup():
    await service.start()


@app.on_event("shutdown")
async def shutdown():
    await service.stop()


@app.get("/")
async def root():
    return {"service": "ShopTalk Auto-Connect", "status": "running"}


@app.get("/status")
async def status():
    return service.get_status()


@app.post("/scan")
async def scan(network: str = None):
    devices = await service.scan_network(network)
    return {"scanned": True, "devices_found": len(devices)}


@app.get("/devices")
async def devices():
    return {"devices": service.get_status()["devices"]}


@app.get("/devices/{device_key}/values")
async def device_values(device_key: str):
    if device_key not in service.devices:
        raise HTTPException(status_code=404, detail="Device not found")
    return service.devices[device_key].last_values


@app.post("/devices/{device_key}/connect")
async def connect_device(device_key: str):
    success = await service.connect_device(device_key)
    return {"connected": success}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
