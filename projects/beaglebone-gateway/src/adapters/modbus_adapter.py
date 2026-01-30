#!/usr/bin/env python3
"""
Modbus Protocol Adapter - TCP and RTU
Supports reading/writing holding registers, input registers, coils, and discrete inputs
"""

import asyncio
from typing import Dict, Any, Optional, List
from dataclasses import dataclass

try:
    from pymodbus.client import AsyncModbusTcpClient, AsyncModbusSerialClient
    from pymodbus.exceptions import ModbusException
    PYMODBUS_AVAILABLE = True
except ImportError:
    PYMODBUS_AVAILABLE = False

import sys
sys.path.append('..')
from core.gateway import ProtocolAdapter, TagDatabase


@dataclass
class ModbusTag:
    """Modbus tag definition"""
    name: str
    address: int
    length: int = 1
    register_type: str = "holding"  # holding, input, coil, discrete
    data_type: str = "int16"  # int16, uint16, int32, uint32, float32, bool
    scale: float = 1.0
    offset: float = 0.0
    unit_id: int = 1


class ModbusTCPAdapter(ProtocolAdapter):
    """Modbus TCP Client Adapter"""
    
    def __init__(self, name: str, config: Dict, tag_db: TagDatabase):
        super().__init__(name, config, tag_db)
        
        if not PYMODBUS_AVAILABLE:
            raise ImportError("pymodbus is required for Modbus adapter. Install with: pip install pymodbus")
        
        self.host = config.get('host', '127.0.0.1')
        self.port = config.get('port', 502)
        self.unit_id = config.get('unit_id', 1)
        self.client: Optional[AsyncModbusTcpClient] = None
        self.tags: List[ModbusTag] = self._parse_tags(config.get('tags', []))
    
    def _parse_tags(self, tag_configs: List[Dict]) -> List[ModbusTag]:
        """Parse tag configuration into ModbusTag objects"""
        tags = []
        for tc in tag_configs:
            tags.append(ModbusTag(
                name=tc.get('name', f'tag_{len(tags)}'),
                address=tc.get('address', 0),
                length=tc.get('length', 1),
                register_type=tc.get('register_type', 'holding'),
                data_type=tc.get('data_type', 'int16'),
                scale=tc.get('scale', 1.0),
                offset=tc.get('offset', 0.0),
                unit_id=tc.get('unit_id', self.unit_id)
            ))
        return tags
    
    async def connect(self) -> bool:
        """Connect to Modbus TCP device"""
        try:
            self.client = AsyncModbusTcpClient(
                host=self.host,
                port=self.port,
                timeout=5
            )
            connected = await self.client.connect()
            return connected
        except Exception as e:
            self.logger.error(f"Connection error: {e}")
            return False
    
    async def disconnect(self):
        """Disconnect from device"""
        if self.client:
            self.client.close()
            self.client = None
    
    async def read_tags(self) -> Dict[str, Any]:
        """Read all configured tags"""
        values = {}
        
        if not self.client or not self.client.connected:
            return values
        
        for tag in self.tags:
            try:
                value = await self._read_tag(tag)
                if value is not None:
                    values[tag.name] = value
            except Exception as e:
                self.logger.error(f"Error reading tag {tag.name}: {e}")
        
        return values
    
    async def _read_tag(self, tag: ModbusTag) -> Optional[Any]:
        """Read a single tag"""
        try:
            if tag.register_type == 'holding':
                result = await self.client.read_holding_registers(
                    tag.address, tag.length, slave=tag.unit_id
                )
            elif tag.register_type == 'input':
                result = await self.client.read_input_registers(
                    tag.address, tag.length, slave=tag.unit_id
                )
            elif tag.register_type == 'coil':
                result = await self.client.read_coils(
                    tag.address, tag.length, slave=tag.unit_id
                )
            elif tag.register_type == 'discrete':
                result = await self.client.read_discrete_inputs(
                    tag.address, tag.length, slave=tag.unit_id
                )
            else:
                self.logger.error(f"Unknown register type: {tag.register_type}")
                return None
            
            if result.isError():
                self.logger.error(f"Modbus error for {tag.name}: {result}")
                return None
            
            # Convert to appropriate data type
            if tag.register_type in ['coil', 'discrete']:
                return result.bits[0] if tag.length == 1 else result.bits[:tag.length]
            else:
                raw_value = self._decode_registers(result.registers, tag.data_type)
                return raw_value * tag.scale + tag.offset
            
        except ModbusException as e:
            self.logger.error(f"Modbus exception for {tag.name}: {e}")
            return None
    
    def _decode_registers(self, registers: List[int], data_type: str) -> Any:
        """Decode register values to the appropriate data type"""
        import struct
        
        if data_type == 'int16':
            return registers[0] if registers[0] < 32768 else registers[0] - 65536
        elif data_type == 'uint16':
            return registers[0]
        elif data_type == 'int32':
            raw = struct.pack('>HH', registers[0], registers[1])
            return struct.unpack('>i', raw)[0]
        elif data_type == 'uint32':
            raw = struct.pack('>HH', registers[0], registers[1])
            return struct.unpack('>I', raw)[0]
        elif data_type == 'float32':
            raw = struct.pack('>HH', registers[0], registers[1])
            return struct.unpack('>f', raw)[0]
        else:
            return registers[0]
    
    async def write_tag(self, tag_name: str, value: Any) -> bool:
        """Write a value to a tag"""
        tag = next((t for t in self.tags if t.name == tag_name), None)
        if not tag:
            self.logger.error(f"Tag not found: {tag_name}")
            return False
        
        try:
            # Apply inverse scale and offset
            raw_value = int((value - tag.offset) / tag.scale)
            
            if tag.register_type == 'holding':
                result = await self.client.write_register(
                    tag.address, raw_value, slave=tag.unit_id
                )
            elif tag.register_type == 'coil':
                result = await self.client.write_coil(
                    tag.address, bool(value), slave=tag.unit_id
                )
            else:
                self.logger.error(f"Cannot write to {tag.register_type} registers")
                return False
            
            return not result.isError()
            
        except ModbusException as e:
            self.logger.error(f"Write error for {tag_name}: {e}")
            return False


class ModbusRTUAdapter(ModbusTCPAdapter):
    """Modbus RTU (Serial) Client Adapter"""
    
    def __init__(self, name: str, config: Dict, tag_db: TagDatabase):
        # Call parent init but override client creation
        ProtocolAdapter.__init__(self, name, config, tag_db)
        
        if not PYMODBUS_AVAILABLE:
            raise ImportError("pymodbus is required for Modbus adapter")
        
        self.port = config.get('port', '/dev/ttyUSB0')
        self.baudrate = config.get('baudrate', 9600)
        self.parity = config.get('parity', 'N')
        self.stopbits = config.get('stopbits', 1)
        self.bytesize = config.get('bytesize', 8)
        self.unit_id = config.get('unit_id', 1)
        self.client: Optional[AsyncModbusSerialClient] = None
        self.tags: List[ModbusTag] = self._parse_tags(config.get('tags', []))
    
    async def connect(self) -> bool:
        """Connect to Modbus RTU device"""
        try:
            self.client = AsyncModbusSerialClient(
                port=self.port,
                baudrate=self.baudrate,
                parity=self.parity,
                stopbits=self.stopbits,
                bytesize=self.bytesize,
                timeout=3
            )
            connected = await self.client.connect()
            return connected
        except Exception as e:
            self.logger.error(f"Serial connection error: {e}")
            return False
