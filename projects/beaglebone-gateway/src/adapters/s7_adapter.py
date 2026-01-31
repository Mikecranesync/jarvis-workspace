#!/usr/bin/env python3
"""
Siemens S7 Protocol Adapter
Supports S7-300, S7-400, S7-1200, S7-1500 PLCs
Uses snap7 library for communication
"""

import asyncio
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
import struct

try:
    import snap7
    from snap7.util import get_bool, get_int, get_real, get_dword, get_word
    from snap7.util import set_bool, set_int, set_real, set_dword, set_word
    SNAP7_AVAILABLE = True
except ImportError:
    SNAP7_AVAILABLE = False

import sys
sys.path.append('..')
from core.gateway import ProtocolAdapter, TagDatabase


@dataclass
class S7Tag:
    """S7 tag definition"""
    name: str
    area: str  # DB, M, I, Q, T, C
    db_number: int = 0  # Only for DB area
    offset: int = 0  # Byte offset
    bit: int = 0  # Bit offset (for bool)
    data_type: str = "int"  # bool, byte, int, dint, real, word, dword
    length: int = 1  # For arrays/strings


class S7Adapter(ProtocolAdapter):
    """Siemens S7 Protocol Adapter"""
    
    # Area codes for snap7
    AREAS = {
        'DB': 0x84,  # Data blocks
        'M': 0x83,   # Merkers (flags)
        'I': 0x81,   # Inputs
        'Q': 0x82,   # Outputs
        'T': 0x1D,   # Timers
        'C': 0x1C    # Counters
    }
    
    def __init__(self, name: str, config: Dict, tag_db: TagDatabase):
        super().__init__(name, config, tag_db)
        
        if not SNAP7_AVAILABLE:
            raise ImportError("snap7 is required for S7 adapter. Install with: pip install python-snap7")
        
        self.host = config.get('host', '192.168.1.1')
        self.rack = config.get('rack', 0)
        self.slot = config.get('slot', 1)  # S7-1200/1500 use slot 1, S7-300/400 use slot 2
        self.client: Optional[snap7.client.Client] = None
        self.tags: List[S7Tag] = self._parse_tags(config.get('tags', []))
        self._loop = None
    
    def _parse_tags(self, tag_configs: List[Dict]) -> List[S7Tag]:
        """Parse tag configuration into S7Tag objects"""
        tags = []
        for tc in tag_configs:
            tags.append(S7Tag(
                name=tc.get('name', f'tag_{len(tags)}'),
                area=tc.get('area', 'DB').upper(),
                db_number=tc.get('db_number', 0),
                offset=tc.get('offset', 0),
                bit=tc.get('bit', 0),
                data_type=tc.get('data_type', 'int'),
                length=tc.get('length', 1)
            ))
        return tags
    
    async def connect(self) -> bool:
        """Connect to S7 PLC"""
        try:
            # snap7 is synchronous, run in executor
            loop = asyncio.get_event_loop()
            self._loop = loop
            
            def _connect():
                client = snap7.client.Client()
                client.connect(self.host, self.rack, self.slot)
                return client
            
            self.client = await loop.run_in_executor(None, _connect)
            return self.client.get_connected()
            
        except Exception as e:
            self.logger.error(f"S7 connection error: {e}")
            return False
    
    async def disconnect(self):
        """Disconnect from PLC"""
        if self.client:
            try:
                loop = asyncio.get_event_loop()
                await loop.run_in_executor(None, self.client.disconnect)
            except:
                pass
            self.client = None
    
    async def read_tags(self) -> Dict[str, Any]:
        """Read all configured tags"""
        values = {}
        
        if not self.client:
            return values
        
        for tag in self.tags:
            try:
                value = await self._read_tag(tag)
                if value is not None:
                    values[tag.name] = value
            except Exception as e:
                self.logger.error(f"Error reading tag {tag.name}: {e}")
        
        return values
    
    async def _read_tag(self, tag: S7Tag) -> Optional[Any]:
        """Read a single tag"""
        try:
            loop = asyncio.get_event_loop()
            
            # Calculate byte size needed
            size = self._get_data_size(tag.data_type, tag.length)
            
            # Read data from PLC
            def _read():
                if tag.area == 'DB':
                    return self.client.db_read(tag.db_number, tag.offset, size)
                else:
                    area_code = self.AREAS.get(tag.area)
                    if area_code is None:
                        raise ValueError(f"Unknown area: {tag.area}")
                    return self.client.read_area(area_code, 0, tag.offset, size)
            
            data = await loop.run_in_executor(None, _read)
            
            # Decode the value
            return self._decode_value(data, tag)
            
        except Exception as e:
            self.logger.error(f"S7 read error for {tag.name}: {e}")
            return None
    
    def _get_data_size(self, data_type: str, length: int = 1) -> int:
        """Get the byte size for a data type"""
        sizes = {
            'bool': 1,
            'byte': 1,
            'word': 2,
            'int': 2,
            'dword': 4,
            'dint': 4,
            'real': 4,
            'string': length + 2  # S7 strings have 2-byte header
        }
        return sizes.get(data_type.lower(), 2) * (1 if data_type.lower() in ['string'] else length)
    
    def _decode_value(self, data: bytes, tag: S7Tag) -> Any:
        """Decode bytes to the appropriate data type"""
        dt = tag.data_type.lower()
        
        if dt == 'bool':
            return get_bool(data, 0, tag.bit)
        elif dt == 'byte':
            return data[0]
        elif dt == 'word':
            return get_word(data, 0)
        elif dt == 'int':
            return get_int(data, 0)
        elif dt == 'dword':
            return get_dword(data, 0)
        elif dt == 'dint':
            return struct.unpack('>i', data[:4])[0]
        elif dt == 'real':
            return get_real(data, 0)
        elif dt == 'string':
            # S7 string: byte 0 = max length, byte 1 = actual length, rest = chars
            actual_len = data[1]
            return data[2:2+actual_len].decode('ascii', errors='ignore')
        else:
            return get_int(data, 0)
    
    async def write_tag(self, tag_name: str, value: Any) -> bool:
        """Write a value to a tag"""
        tag = next((t for t in self.tags if t.name == tag_name), None)
        if not tag:
            self.logger.error(f"Tag not found: {tag_name}")
            return False
        
        try:
            loop = asyncio.get_event_loop()
            
            # Read current data first (for bool writes)
            size = self._get_data_size(tag.data_type, tag.length)
            
            def _read():
                if tag.area == 'DB':
                    return bytearray(self.client.db_read(tag.db_number, tag.offset, size))
                else:
                    area_code = self.AREAS[tag.area]
                    return bytearray(self.client.read_area(area_code, 0, tag.offset, size))
            
            data = await loop.run_in_executor(None, _read)
            
            # Encode the value
            self._encode_value(data, tag, value)
            
            # Write back
            def _write():
                if tag.area == 'DB':
                    self.client.db_write(tag.db_number, tag.offset, data)
                else:
                    area_code = self.AREAS[tag.area]
                    self.client.write_area(area_code, 0, tag.offset, data)
            
            await loop.run_in_executor(None, _write)
            return True
            
        except Exception as e:
            self.logger.error(f"S7 write error for {tag_name}: {e}")
            return False
    
    def _encode_value(self, data: bytearray, tag: S7Tag, value: Any):
        """Encode a value into bytes"""
        dt = tag.data_type.lower()
        
        if dt == 'bool':
            set_bool(data, 0, tag.bit, bool(value))
        elif dt == 'byte':
            data[0] = int(value) & 0xFF
        elif dt == 'word':
            set_word(data, 0, int(value))
        elif dt == 'int':
            set_int(data, 0, int(value))
        elif dt == 'dword':
            set_dword(data, 0, int(value))
        elif dt == 'dint':
            data[:4] = struct.pack('>i', int(value))
        elif dt == 'real':
            set_real(data, 0, float(value))
