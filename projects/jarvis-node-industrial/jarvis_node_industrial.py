#!/usr/bin/env python3
"""
Jarvis Node Industrial Edition - Enhanced edge agent for industrial automation
Extends base Jarvis Node with PLC/VFD connectivity, edge AI, and auto-discovery
"""

import os
import sys
import json
import base64
import subprocess
import socket
import asyncio
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, Dict, List, Any, Union
from dataclasses import dataclass, asdict
from enum import Enum

# FastAPI and web components
from fastapi import FastAPI, HTTPException, WebSocket, Depends, BackgroundTasks
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, Field
import uvicorn

# Base Jarvis Node capabilities
import mss
import mss.tools

# Industrial protocol libraries (graceful imports)
INDUSTRIAL_PROTOCOLS = {}

try:
    from pylogix import PLC
    INDUSTRIAL_PROTOCOLS['allen_bradley'] = True
except ImportError:
    INDUSTRIAL_PROTOCOLS['allen_bradley'] = False

try:
    import snap7
    INDUSTRIAL_PROTOCOLS['siemens_s7'] = True
except ImportError:
    INDUSTRIAL_PROTOCOLS['siemens_s7'] = False

try:
    from pymodbus.client import ModbusTcpClient, ModbusSerialClient
    INDUSTRIAL_PROTOCOLS['modbus'] = True
except ImportError:
    INDUSTRIAL_PROTOCOLS['modbus'] = False

try:
    from opcua import Client as OPCUAClient
    INDUSTRIAL_PROTOCOLS['opcua'] = True
except ImportError:
    INDUSTRIAL_PROTOCOLS['opcua'] = False

# AI and ML libraries
try:
    import requests
    HAS_OLLAMA_CLIENT = True
except ImportError:
    HAS_OLLAMA_CLIENT = False

try:
    from sklearn.ensemble import IsolationForest
    from sklearn.neighbors import LocalOutlierFactor
    import numpy as np
    HAS_ML = True
except ImportError:
    HAS_ML = False

# Discovery and networking
try:
    import nmap
    import netifaces
    HAS_NETWORK_DISCOVERY = True
except ImportError:
    HAS_NETWORK_DISCOVERY = False

# Optional imports from base Jarvis Node
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

# =============================================================================
# CONFIGURATION
# =============================================================================
MACHINE_NAME = os.environ.get("JARVIS_MACHINE_NAME", socket.gethostname())
PORT = int(os.environ.get("JARVIS_PORT", 8765))
WORKSPACE = Path(os.environ.get("JARVIS_WORKSPACE", Path.home() / "jarvis-workspace"))
WORKSPACE.mkdir(exist_ok=True)

# Industrial-specific configuration
OLLAMA_HOST = os.environ.get("OLLAMA_HOST", "localhost:11434")
INDUSTRIAL_CONFIG = WORKSPACE / "industrial_config.json"
DEVICE_DATABASE = WORKSPACE / "devices.json"

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(WORKSPACE / 'jarvis_industrial.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("jarvis_industrial")

# =============================================================================
# DATA MODELS
# =============================================================================
class DeviceProtocol(str, Enum):
    ALLEN_BRADLEY = "allen_bradley"
    SIEMENS_S7 = "siemens_s7"
    MODBUS_TCP = "modbus_tcp"
    MODBUS_RTU = "modbus_rtu"
    OPCUA = "opcua"

@dataclass
class IndustrialTag:
    name: str
    address: str
    data_type: str
    description: Optional[str] = None
    unit: Optional[str] = None
    min_value: Optional[float] = None
    max_value: Optional[float] = None
    last_value: Optional[Any] = None
    last_update: Optional[datetime] = None

@dataclass
class IndustrialDevice:
    id: str
    name: str
    protocol: DeviceProtocol
    ip_address: str
    port: int = None
    slot: int = 0
    unit_id: int = 1  # For Modbus
    description: Optional[str] = None
    manufacturer: Optional[str] = None
    model: Optional[str] = None
    firmware_version: Optional[str] = None
    tags: List[IndustrialTag] = None
    last_seen: Optional[datetime] = None
    connection_status: str = "unknown"
    auto_discovered: bool = False

class DeviceRequest(BaseModel):
    name: str
    protocol: DeviceProtocol
    ip_address: str
    port: Optional[int] = None
    slot: Optional[int] = 0
    unit_id: Optional[int] = 1
    description: Optional[str] = None

class TagReadRequest(BaseModel):
    device_id: str
    tag_name: str

class TagWriteRequest(BaseModel):
    device_id: str
    tag_name: str
    value: Any

class BatchTagRequest(BaseModel):
    device_id: str
    operations: List[Dict[str, Any]]

class AIQueryRequest(BaseModel):
    query: str
    context: Optional[Dict[str, Any]] = None
    model: str = "llama3.2:3b"

class DiscoveryRequest(BaseModel):
    network_range: Optional[str] = None
    protocols: Optional[List[DeviceProtocol]] = None
    timeout: int = 30

# =============================================================================
# INDUSTRIAL DEVICE ABSTRACTIONS
# =============================================================================
class IndustrialDeviceInterface:
    """Abstract base class for industrial device communication"""
    
    def __init__(self, device: IndustrialDevice):
        self.device = device
        self.connected = False
        
    async def connect(self) -> bool:
        """Connect to the device"""
        raise NotImplementedError
    
    async def disconnect(self):
        """Disconnect from the device"""
        raise NotImplementedError
    
    async def read_tag(self, tag_name: str) -> Any:
        """Read a single tag value"""
        raise NotImplementedError
    
    async def write_tag(self, tag_name: str, value: Any) -> bool:
        """Write a value to a tag"""
        raise NotImplementedError
    
    async def get_tag_list(self) -> List[IndustrialTag]:
        """Get list of available tags"""
        raise NotImplementedError
    
    async def get_device_info(self) -> Dict[str, Any]:
        """Get device information"""
        raise NotImplementedError

class AllenBradleyDevice(IndustrialDeviceInterface):
    """Allen-Bradley PLC interface using pylogix"""
    
    def __init__(self, device: IndustrialDevice):
        super().__init__(device)
        self.comm = None
        
    async def connect(self) -> bool:
        if not INDUSTRIAL_PROTOCOLS['allen_bradley']:
            raise HTTPException(501, "pylogix not installed. Run: pip install pylogix")
            
        try:
            self.comm = PLC()
            self.comm.IPAddress = self.device.ip_address
            if self.device.slot is not None:
                self.comm.ProcessorSlot = self.device.slot
            
            # Test connection
            test_read = self.comm.Read('Program:MainProgram.Test', datatype=1)  # Try to read a common location
            self.connected = test_read.Status == 'Success' or 'does not exist' in str(test_read.Status)
            return self.connected
        except Exception as e:
            logger.error(f"Failed to connect to Allen-Bradley device {self.device.id}: {e}")
            return False
    
    async def disconnect(self):
        if self.comm:
            self.comm.Close()
            self.connected = False
    
    async def read_tag(self, tag_name: str) -> Any:
        if not self.connected:
            await self.connect()
        
        try:
            result = self.comm.Read(tag_name)
            if result.Status == 'Success':
                return result.Value
            else:
                raise HTTPException(400, f"Failed to read tag {tag_name}: {result.Status}")
        except Exception as e:
            raise HTTPException(500, f"Error reading tag {tag_name}: {e}")
    
    async def write_tag(self, tag_name: str, value: Any) -> bool:
        if not self.connected:
            await self.connect()
        
        try:
            result = self.comm.Write(tag_name, value)
            return result.Status == 'Success'
        except Exception as e:
            logger.error(f"Error writing tag {tag_name}: {e}")
            return False
    
    async def get_tag_list(self) -> List[IndustrialTag]:
        if not self.connected:
            await self.connect()
        
        try:
            tag_list = self.comm.GetTagList()
            tags = []
            for tag_info in tag_list.Value:
                tag = IndustrialTag(
                    name=tag_info['TagName'],
                    address=tag_info['TagName'],
                    data_type=tag_info['DataType'],
                    description=tag_info.get('Description', ''),
                    last_update=datetime.now()
                )
                tags.append(tag)
            return tags
        except Exception as e:
            logger.error(f"Error getting tag list: {e}")
            return []

class ModbusDevice(IndustrialDeviceInterface):
    """Modbus TCP/RTU device interface using pymodbus"""
    
    def __init__(self, device: IndustrialDevice):
        super().__init__(device)
        self.client = None
        
    async def connect(self) -> bool:
        if not INDUSTRIAL_PROTOCOLS['modbus']:
            raise HTTPException(501, "pymodbus not installed. Run: pip install pymodbus")
        
        try:
            if self.device.protocol == DeviceProtocol.MODBUS_TCP:
                self.client = ModbusTcpClient(
                    self.device.ip_address,
                    port=self.device.port or 502
                )
            else:
                # RTU would need additional configuration
                raise HTTPException(501, "Modbus RTU not yet implemented")
            
            self.connected = self.client.connect()
            return self.connected
        except Exception as e:
            logger.error(f"Failed to connect to Modbus device {self.device.id}: {e}")
            return False
    
    async def disconnect(self):
        if self.client:
            self.client.close()
            self.connected = False
    
    async def read_tag(self, tag_name: str) -> Any:
        # For Modbus, tag_name format: "holding:40001" or "input:30001"
        if not self.connected:
            await self.connect()
        
        try:
            register_type, address = tag_name.split(':')
            address = int(address)
            
            if register_type == 'holding':
                result = self.client.read_holding_registers(address, 1, unit=self.device.unit_id)
            elif register_type == 'input':
                result = self.client.read_input_registers(address, 1, unit=self.device.unit_id)
            elif register_type == 'coil':
                result = self.client.read_coils(address, 1, unit=self.device.unit_id)
            elif register_type == 'discrete':
                result = self.client.read_discrete_inputs(address, 1, unit=self.device.unit_id)
            else:
                raise HTTPException(400, f"Invalid register type: {register_type}")
            
            if not result.isError():
                return result.registers[0] if hasattr(result, 'registers') else result.bits[0]
            else:
                raise HTTPException(400, f"Modbus error reading {tag_name}")
        except Exception as e:
            raise HTTPException(500, f"Error reading tag {tag_name}: {e}")
    
    async def write_tag(self, tag_name: str, value: Any) -> bool:
        if not self.connected:
            await self.connect()
        
        try:
            register_type, address = tag_name.split(':')
            address = int(address)
            
            if register_type == 'holding':
                result = self.client.write_register(address, value, unit=self.device.unit_id)
            elif register_type == 'coil':
                result = self.client.write_coil(address, bool(value), unit=self.device.unit_id)
            else:
                raise HTTPException(400, f"Cannot write to register type: {register_type}")
            
            return not result.isError()
        except Exception as e:
            logger.error(f"Error writing tag {tag_name}: {e}")
            return False

# =============================================================================
# DEVICE FACTORY
# =============================================================================
class DeviceFactory:
    """Factory for creating device interface instances"""
    
    @staticmethod
    def create(device: IndustrialDevice) -> IndustrialDeviceInterface:
        if device.protocol == DeviceProtocol.ALLEN_BRADLEY:
            return AllenBradleyDevice(device)
        elif device.protocol in [DeviceProtocol.MODBUS_TCP, DeviceProtocol.MODBUS_RTU]:
            return ModbusDevice(device)
        elif device.protocol == DeviceProtocol.SIEMENS_S7:
            # TODO: Implement Siemens S7 device
            raise HTTPException(501, "Siemens S7 protocol not yet implemented")
        elif device.protocol == DeviceProtocol.OPCUA:
            # TODO: Implement OPC-UA device
            raise HTTPException(501, "OPC-UA protocol not yet implemented")
        else:
            raise HTTPException(400, f"Unknown protocol: {device.protocol}")

# =============================================================================
# AI INTEGRATION
# =============================================================================
class OllamaClient:
    """Client for local Ollama LLM integration"""
    
    def __init__(self, host: str = OLLAMA_HOST):
        self.host = host
        self.base_url = f"http://{host}"
    
    async def query(self, prompt: str, model: str = "llama3.2:3b", context: Dict = None) -> str:
        if not HAS_OLLAMA_CLIENT:
            raise HTTPException(501, "requests library not available for Ollama client")
        
        try:
            # Add industrial context to prompt
            if context:
                industrial_context = f"""
Industrial Context:
- Active Devices: {len(context.get('devices', []))}
- Recent Alarms: {len(context.get('alarms', []))}
- System Status: {context.get('system_status', 'Unknown')}

User Query: {prompt}

Please provide a helpful response based on the industrial automation context.
"""
            else:
                industrial_context = f"Industrial Automation Query: {prompt}"
            
            response = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": model,
                    "prompt": industrial_context,
                    "stream": False
                },
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json()['response']
            else:
                raise HTTPException(500, f"Ollama API error: {response.status_code}")
        
        except requests.exceptions.RequestException as e:
            raise HTTPException(500, f"Failed to connect to Ollama: {e}")

class AnomalyDetector:
    """Multi-model anomaly detection system"""
    
    def __init__(self):
        if HAS_ML:
            self.isolation_forest = IsolationForest(contamination=0.1, random_state=42)
            self.lof = LocalOutlierFactor(n_neighbors=20, contamination=0.1)
        
    def detect_anomalies(self, data: List[float], method: str = "isolation_forest") -> Dict[str, Any]:
        if not HAS_ML:
            return {"error": "ML libraries not available"}
        
        if len(data) < 10:
            return {"error": "Insufficient data for anomaly detection"}
        
        try:
            data_array = np.array(data).reshape(-1, 1)
            
            if method == "isolation_forest":
                outliers = self.isolation_forest.fit_predict(data_array)
                scores = self.isolation_forest.decision_function(data_array)
            elif method == "local_outlier_factor":
                outliers = self.lof.fit_predict(data_array)
                scores = self.lof.negative_outlier_factor_
            else:
                return {"error": f"Unknown method: {method}"}
            
            anomaly_indices = [i for i, outlier in enumerate(outliers) if outlier == -1]
            
            return {
                "anomaly_count": len(anomaly_indices),
                "anomaly_indices": anomaly_indices,
                "anomaly_scores": scores.tolist(),
                "method": method,
                "timestamp": datetime.now().isoformat()
            }
        
        except Exception as e:
            return {"error": f"Anomaly detection failed: {e}"}

# =============================================================================
# DEVICE DISCOVERY
# =============================================================================
class IndustrialDiscovery:
    """Auto-discovery system for industrial devices"""
    
    INDUSTRIAL_PORTS = {
        502: 'Modbus TCP',
        44818: 'EtherNet/IP',
        4840: 'OPC-UA',
        102: 'S7 Communication',
        2404: 'IEC 61850',
        20000: 'DNP3'
    }
    
    def __init__(self):
        self.discovered_devices = []
    
    async def discover_network(self, network_range: str = None, timeout: int = 30) -> List[Dict[str, Any]]:
        """Discover industrial devices on the network"""
        if not HAS_NETWORK_DISCOVERY:
            logger.warning("Network discovery libraries not available")
            return []
        
        discovered = []
        
        try:
            # Determine network range
            if not network_range:
                # Get local network range
                gateways = netifaces.gateways()
                default_gw = gateways['default'][netifaces.AF_INET][0]
                network_range = f"{'.'.join(default_gw.split('.')[:-1])}.0/24"
            
            # Port scanning for industrial protocols
            nm = nmap.PortScanner()
            
            for port, protocol in self.INDUSTRIAL_PORTS.items():
                logger.info(f"Scanning for {protocol} devices on port {port}")
                
                try:
                    result = nm.scan(network_range, str(port), timeout=timeout//len(self.INDUSTRIAL_PORTS))
                    
                    for host in nm.all_hosts():
                        if nm[host]['tcp'][port]['state'] == 'open':
                            device_info = {
                                'ip_address': host,
                                'port': port,
                                'protocol': protocol,
                                'hostname': nm[host].hostname(),
                                'mac_address': nm[host]['addresses'].get('mac', ''),
                                'discovered_at': datetime.now().isoformat(),
                                'auto_discovered': True
                            }
                            
                            # Try to identify device type
                            device_type = await self._identify_device(host, port, protocol)
                            device_info.update(device_type)
                            
                            discovered.append(device_info)
                
                except Exception as e:
                    logger.error(f"Error scanning port {port}: {e}")
            
            logger.info(f"Discovery completed. Found {len(discovered)} devices.")
            return discovered
        
        except Exception as e:
            logger.error(f"Network discovery failed: {e}")
            return []
    
    async def _identify_device(self, ip: str, port: int, protocol: str) -> Dict[str, Any]:
        """Try to identify device manufacturer and model"""
        identification = {
            'manufacturer': 'Unknown',
            'model': 'Unknown',
            'device_type': 'Industrial Device'
        }
        
        try:
            if protocol == 'EtherNet/IP' and INDUSTRIAL_PROTOCOLS['allen_bradley']:
                # Try Allen-Bradley identification
                comm = PLC()
                comm.IPAddress = ip
                info = comm.GetDeviceProperties()
                if info.Value:
                    identification.update({
                        'manufacturer': 'Rockwell Automation',
                        'model': info.Value.get('ProductName', 'Unknown'),
                        'device_type': 'Allen-Bradley PLC'
                    })
            
            elif protocol == 'Modbus TCP':
                # Basic Modbus identification
                identification.update({
                    'device_type': 'Modbus Device (VFD/Instrument)',
                    'manufacturer': 'Unknown (Modbus)'
                })
        
        except Exception as e:
            logger.debug(f"Device identification failed for {ip}:{port} - {e}")
        
        return identification

# =============================================================================
# DEVICE MANAGER
# =============================================================================
class IndustrialDeviceManager:
    """Manages all industrial devices and their connections"""
    
    def __init__(self):
        self.devices: Dict[str, IndustrialDevice] = {}
        self.device_interfaces: Dict[str, IndustrialDeviceInterface] = {}
        self.load_devices()
    
    def load_devices(self):
        """Load devices from configuration file"""
        if DEVICE_DATABASE.exists():
            try:
                with open(DEVICE_DATABASE, 'r') as f:
                    device_data = json.load(f)
                    
                for device_id, device_dict in device_data.items():
                    device = IndustrialDevice(**device_dict)
                    device.tags = [IndustrialTag(**tag) for tag in device_dict.get('tags', [])]
                    self.devices[device_id] = device
                    
                logger.info(f"Loaded {len(self.devices)} devices from configuration")
            except Exception as e:
                logger.error(f"Failed to load device database: {e}")
    
    def save_devices(self):
        """Save devices to configuration file"""
        try:
            device_data = {}
            for device_id, device in self.devices.items():
                device_dict = asdict(device)
                # Convert datetime objects to ISO strings
                if device_dict['last_seen']:
                    device_dict['last_seen'] = device.last_seen.isoformat()
                device_data[device_id] = device_dict
                
            with open(DEVICE_DATABASE, 'w') as f:
                json.dump(device_data, f, indent=2)
                
        except Exception as e:
            logger.error(f"Failed to save device database: {e}")
    
    async def add_device(self, device_req: DeviceRequest) -> IndustrialDevice:
        """Add a new industrial device"""
        device_id = f"{device_req.protocol}_{device_req.ip_address.replace('.', '_')}"
        
        device = IndustrialDevice(
            id=device_id,
            name=device_req.name,
            protocol=device_req.protocol,
            ip_address=device_req.ip_address,
            port=device_req.port,
            slot=device_req.slot,
            unit_id=device_req.unit_id,
            description=device_req.description,
            last_seen=datetime.now(),
            connection_status="configured"
        )
        
        # Test connection
        interface = DeviceFactory.create(device)
        if await interface.connect():
            device.connection_status = "connected"
            # Get device info and tags
            try:
                device_info = await interface.get_device_info()
                device.manufacturer = device_info.get('manufacturer')
                device.model = device_info.get('model')
                device.firmware_version = device_info.get('firmware')
                
                tags = await interface.get_tag_list()
                device.tags = tags
                
            except Exception as e:
                logger.warning(f"Could not get device info: {e}")
            
            await interface.disconnect()
        else:
            device.connection_status = "failed"
        
        self.devices[device_id] = device
        self.save_devices()
        
        return device
    
    def get_device(self, device_id: str) -> Optional[IndustrialDevice]:
        """Get device by ID"""
        return self.devices.get(device_id)
    
    def list_devices(self) -> List[IndustrialDevice]:
        """List all devices"""
        return list(self.devices.values())
    
    async def get_device_interface(self, device_id: str) -> IndustrialDeviceInterface:
        """Get or create device interface"""
        if device_id not in self.device_interfaces:
            device = self.get_device(device_id)
            if not device:
                raise HTTPException(404, f"Device {device_id} not found")
            
            interface = DeviceFactory.create(device)
            self.device_interfaces[device_id] = interface
        
        return self.device_interfaces[device_id]

# =============================================================================
# FASTAPI APPLICATION
# =============================================================================
app = FastAPI(
    title=f"Jarvis Node Industrial Edition - {MACHINE_NAME}",
    description="Enhanced edge agent for industrial automation",
    version="2.0.0"
)

# Initialize components
device_manager = IndustrialDeviceManager()
ollama_client = OllamaClient()
anomaly_detector = AnomalyDetector()
discovery_engine = IndustrialDiscovery()

# Security
security = HTTPBearer(auto_error=False)

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Simple token-based authentication (implement proper auth in production)"""
    # For now, just return a default user - implement proper auth later
    return {"username": "operator", "role": "operator"}

# =============================================================================
# ENHANCED ENDPOINTS
# =============================================================================

@app.get("/health")
def health():
    """Enhanced health check with industrial capabilities"""
    return {
        "status": "online",
        "machine": MACHINE_NAME,
        "hostname": socket.gethostname(),
        "workspace": str(WORKSPACE),
        "capabilities": {
            # Base capabilities
            "shell": True,
            "screenshot": True,
            "gui": HAS_PYAUTOGUI,
            "camera": HAS_CAMERA,
            "files": True,
            # Industrial capabilities
            "protocols": INDUSTRIAL_PROTOCOLS,
            "ai": HAS_OLLAMA_CLIENT,
            "ml": HAS_ML,
            "discovery": HAS_NETWORK_DISCOVERY
        },
        "device_count": len(device_manager.devices),
        "active_connections": len(device_manager.device_interfaces),
        "timestamp": datetime.now().isoformat()
    }

# =============================================================================
# DEVICE MANAGEMENT ENDPOINTS
# =============================================================================

@app.get("/api/v1/devices")
async def list_devices():
    """List all industrial devices"""
    devices = device_manager.list_devices()
    return {
        "devices": [asdict(device) for device in devices],
        "count": len(devices),
        "timestamp": datetime.now().isoformat()
    }

@app.post("/api/v1/devices")
async def add_device(device_req: DeviceRequest):
    """Add a new industrial device"""
    device = await device_manager.add_device(device_req)
    return {
        "device": asdict(device),
        "status": "added",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/api/v1/devices/{device_id}")
async def get_device(device_id: str):
    """Get device details"""
    device = device_manager.get_device(device_id)
    if not device:
        raise HTTPException(404, f"Device {device_id} not found")
    
    return {
        "device": asdict(device),
        "timestamp": datetime.now().isoformat()
    }

@app.delete("/api/v1/devices/{device_id}")
async def remove_device(device_id: str):
    """Remove a device"""
    if device_id not in device_manager.devices:
        raise HTTPException(404, f"Device {device_id} not found")
    
    # Disconnect if connected
    if device_id in device_manager.device_interfaces:
        await device_manager.device_interfaces[device_id].disconnect()
        del device_manager.device_interfaces[device_id]
    
    del device_manager.devices[device_id]
    device_manager.save_devices()
    
    return {
        "status": "removed",
        "device_id": device_id,
        "timestamp": datetime.now().isoformat()
    }

# =============================================================================
# TAG OPERATIONS ENDPOINTS
# =============================================================================

@app.get("/api/v1/devices/{device_id}/tags")
async def list_device_tags(device_id: str):
    """List all tags for a device"""
    device = device_manager.get_device(device_id)
    if not device:
        raise HTTPException(404, f"Device {device_id} not found")
    
    interface = await device_manager.get_device_interface(device_id)
    
    try:
        if not interface.connected:
            await interface.connect()
        
        tags = await interface.get_tag_list()
        
        return {
            "device_id": device_id,
            "tags": [asdict(tag) for tag in tags],
            "count": len(tags),
            "timestamp": datetime.now().isoformat()
        }
    
    except Exception as e:
        raise HTTPException(500, f"Failed to get tags: {e}")

@app.get("/api/v1/devices/{device_id}/tags/{tag_name}")
async def read_tag(device_id: str, tag_name: str):
    """Read a single tag value"""
    interface = await device_manager.get_device_interface(device_id)
    
    try:
        value = await interface.read_tag(tag_name)
        
        return {
            "device_id": device_id,
            "tag_name": tag_name,
            "value": value,
            "timestamp": datetime.now().isoformat()
        }
    
    except Exception as e:
        raise HTTPException(500, f"Failed to read tag: {e}")

@app.post("/api/v1/devices/{device_id}/tags/{tag_name}")
async def write_tag(device_id: str, tag_name: str, request: Dict[str, Any]):
    """Write a value to a tag"""
    if "value" not in request:
        raise HTTPException(400, "Missing 'value' in request body")
    
    interface = await device_manager.get_device_interface(device_id)
    
    try:
        success = await interface.write_tag(tag_name, request["value"])
        
        return {
            "device_id": device_id,
            "tag_name": tag_name,
            "value": request["value"],
            "success": success,
            "timestamp": datetime.now().isoformat()
        }
    
    except Exception as e:
        raise HTTPException(500, f"Failed to write tag: {e}")

# =============================================================================
# AI INTEGRATION ENDPOINTS
# =============================================================================

@app.post("/api/v1/ai/query")
async def ai_query(request: AIQueryRequest):
    """Query the local AI system"""
    try:
        # Add system context
        context = {
            "devices": [asdict(device) for device in device_manager.list_devices()],
            "system_status": "operational",
            "alarms": []  # TODO: Implement alarm system
        }
        
        response = await ollama_client.query(
            prompt=request.query,
            model=request.model,
            context=context
        )
        
        return {
            "query": request.query,
            "response": response,
            "model": request.model,
            "timestamp": datetime.now().isoformat()
        }
    
    except Exception as e:
        raise HTTPException(500, f"AI query failed: {e}")

@app.post("/api/v1/ai/anomaly-detection")
async def detect_anomalies(data: List[float], method: str = "isolation_forest"):
    """Detect anomalies in time series data"""
    result = anomaly_detector.detect_anomalies(data, method)
    return result

# =============================================================================
# DISCOVERY ENDPOINTS
# =============================================================================

@app.post("/api/v1/discovery/scan")
async def discover_devices(request: DiscoveryRequest):
    """Discover industrial devices on the network"""
    try:
        discovered = await discovery_engine.discover_network(
            network_range=request.network_range,
            timeout=request.timeout
        )
        
        return {
            "discovered_devices": discovered,
            "count": len(discovered),
            "network_range": request.network_range,
            "timestamp": datetime.now().isoformat()
        }
    
    except Exception as e:
        raise HTTPException(500, f"Discovery failed: {e}")

# =============================================================================
# WEBSOCKET REAL-TIME ENDPOINTS
# =============================================================================

@app.websocket("/ws/devices/{device_id}/tags")
async def websocket_device_tags(websocket: WebSocket, device_id: str):
    """WebSocket for real-time tag data streaming"""
    await websocket.accept()
    
    try:
        device = device_manager.get_device(device_id)
        if not device:
            await websocket.send_json({"error": f"Device {device_id} not found"})
            return
        
        interface = await device_manager.get_device_interface(device_id)
        
        # Send initial device info
        await websocket.send_json({
            "type": "device_info",
            "device": asdict(device),
            "timestamp": datetime.now().isoformat()
        })
        
        # Stream tag values (simple polling for now - optimize later)
        while True:
            try:
                if device.tags:
                    for tag in device.tags[:5]:  # Limit to first 5 tags for demo
                        try:
                            value = await interface.read_tag(tag.name)
                            await websocket.send_json({
                                "type": "tag_update",
                                "device_id": device_id,
                                "tag_name": tag.name,
                                "value": value,
                                "timestamp": datetime.now().isoformat()
                            })
                        except Exception as e:
                            logger.warning(f"Error reading tag {tag.name}: {e}")
                
                await asyncio.sleep(1)  # 1 Hz update rate
                
            except Exception as e:
                logger.error(f"WebSocket error: {e}")
                break
    
    except Exception as e:
        logger.error(f"WebSocket connection error: {e}")
        await websocket.send_json({"error": str(e)})

# =============================================================================
# MAIN APPLICATION
# =============================================================================

if __name__ == "__main__":
    print(f"""
╔════════════════════════════════════════════════════════════════════════════╗
║  🏭 Jarvis Node Industrial Edition - {MACHINE_NAME:^40} ║
╠════════════════════════════════════════════════════════════════════════════╣
║  Workspace: {str(WORKSPACE):<60} ║
║  Port:      {PORT:<60} ║
║  Docs:      http://localhost:{PORT}/docs{' ' * (52 - len(str(PORT)))} ║
║                                                                            ║
║  🔌 Industrial Protocols:                                                   ║
║     Allen-Bradley: {'✅' if INDUSTRIAL_PROTOCOLS['allen_bradley'] else '❌':<55} ║
║     Siemens S7:    {'✅' if INDUSTRIAL_PROTOCOLS['siemens_s7'] else '❌':<55} ║
║     Modbus:        {'✅' if INDUSTRIAL_PROTOCOLS['modbus'] else '❌':<55} ║
║     OPC-UA:        {'✅' if INDUSTRIAL_PROTOCOLS['opcua'] else '❌':<55} ║
║                                                                            ║
║  🧠 AI Capabilities:                                                        ║
║     Local LLM:     {'✅' if HAS_OLLAMA_CLIENT else '❌':<55} ║
║     ML Analytics:  {'✅' if HAS_ML else '❌':<55} ║
║     Discovery:     {'✅' if HAS_NETWORK_DISCOVERY else '❌':<55} ║
╚════════════════════════════════════════════════════════════════════════════╝
    """)
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=PORT,
        log_level="info"
    )