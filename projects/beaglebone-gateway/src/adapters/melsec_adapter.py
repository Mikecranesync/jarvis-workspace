#!/usr/bin/env python3
"""
Mitsubishi MELSEC Protocol Adapter
Supports MELSEC Communication Protocol (MC Protocol)
Uses pymcprotocol library for communication
"""

import asyncio
from typing import Dict, Any, Optional, List
from dataclasses import dataclass

try:
    import pymcprotocol
    PYMCPROTOCOL_AVAILABLE = True
except ImportError:
    PYMCPROTOCOL_AVAILABLE = False

import sys
sys.path.append('..')
from core.gateway import ProtocolAdapter, TagDatabase


@dataclass
class MelsecTag:
    """Mitsubishi MELSEC tag definition"""
    name: str
    device: str  # D (data register), M (internal relay), X (input), Y (output), etc.
    address: int
    data_type: str = "word"  # bit, word, dword, float
    length: int = 1


class MelsecAdapter(ProtocolAdapter):
    """Mitsubishi MELSEC Protocol Adapter"""
    
    def __init__(self, name: str, config: Dict, tag_db: TagDatabase):
        super().__init__(name, config, tag_db)
        
        if not PYMCPROTOCOL_AVAILABLE:
            raise ImportError("pymcprotocol is required for MELSEC adapter. Install with: pip install pymcprotocol")
        
        self.host = config.get('host', '192.168.1.1')
        self.port = config.get('port', 5007)
        self.plc_type = config.get('plc_type', 'Q')  # Q, L, iQ-R, iQ-L
        self.client = None
        self.tags: List[MelsecTag] = self._parse_tags(config.get('tags', []))
        self._lock = asyncio.Lock()
    
    def _parse_tags(self, tag_configs: List[Dict]) -> List[MelsecTag]:
        """Parse tag configuration into MelsecTag objects"""
        tags = []
        for tc in tag_configs:
            tags.append(MelsecTag(
                name=tc.get('name', f'tag_{len(tags)}'),
                device=tc.get('device', 'D'),
                address=tc.get('address', 0),
                data_type=tc.get('data_type', 'word'),
                length=tc.get('length', 1)
            ))
        return tags
    
    async def connect(self) -> bool:
        """Connect to Mitsubishi PLC"""
        try:
            loop = asyncio.get_event_loop()
            
            def _connect():
                # Determine protocol type based on PLC type
                if self.plc_type.upper() in ['Q', 'L']:
                    client = pymcprotocol.Type3E()
                else:  # iQ-R, iQ-L use 4E frame
                    client = pymcprotocol.Type4E()
                
                client.connect(self.host, self.port)
                return client
            
            self.client = await loop.run_in_executor(None, _connect)
            return True
            
        except Exception as e:
            self.logger.error(f"MELSEC connection error: {e}")
            return False
    
    async def disconnect(self):
        """Disconnect from PLC"""
        if self.client:
            try:
                loop = asyncio.get_event_loop()
                await loop.run_in_executor(None, self.client.close)
            except:
                pass
            self.client = None
    
    async def read_tags(self) -> Dict[str, Any]:
        """Read all configured tags"""
        values = {}
        
        if not self.client:
            return values
        
        async with self._lock:
            for tag in self.tags:
                try:
                    value = await self._read_tag(tag)
                    if value is not None:
                        values[tag.name] = value
                except Exception as e:
                    self.logger.error(f"Error reading tag {tag.name}: {e}")
        
        return values
    
    async def _read_tag(self, tag: MelsecTag) -> Optional[Any]:
        """Read a single tag"""
        try:
            loop = asyncio.get_event_loop()
            
            def _read():
                if tag.data_type == 'bit':
                    # Read bits (M, X, Y, etc.)
                    head_device = f"{tag.device}{tag.address}"
                    result = self.client.batchread_bitunits(head_device, tag.length)
                    return result[0] if tag.length == 1 else result
                else:
                    # Read words (D, W, R, etc.)
                    head_device = f"{tag.device}{tag.address}"
                    result = self.client.batchread_wordunits(head_device, tag.length)
                    
                    if tag.data_type == 'word':
                        return result[0] if tag.length == 1 else result
                    elif tag.data_type == 'dword':
                        # Combine two words into a 32-bit value
                        if len(result) >= 2:
                            return result[0] + (result[1] << 16)
                        return result[0]
                    elif tag.data_type == 'float':
                        # Convert two words to float
                        import struct
                        if len(result) >= 2:
                            raw = struct.pack('<HH', result[0], result[1])
                            return struct.unpack('<f', raw)[0]
                        return 0.0
                    else:
                        return result[0] if tag.length == 1 else result
            
            return await loop.run_in_executor(None, _read)
            
        except Exception as e:
            self.logger.error(f"MELSEC read error for {tag.name}: {e}")
            return None
    
    async def write_tag(self, tag_name: str, value: Any) -> bool:
        """Write a value to a tag"""
        tag = next((t for t in self.tags if t.name == tag_name), None)
        if not tag:
            self.logger.error(f"Tag not found: {tag_name}")
            return False
        
        async with self._lock:
            try:
                loop = asyncio.get_event_loop()
                
                def _write():
                    head_device = f"{tag.device}{tag.address}"
                    
                    if tag.data_type == 'bit':
                        self.client.batchwrite_bitunits(head_device, [int(value)])
                    else:
                        if tag.data_type == 'word':
                            self.client.batchwrite_wordunits(head_device, [int(value)])
                        elif tag.data_type == 'dword':
                            low = value & 0xFFFF
                            high = (value >> 16) & 0xFFFF
                            self.client.batchwrite_wordunits(head_device, [low, high])
                        elif tag.data_type == 'float':
                            import struct
                            raw = struct.pack('<f', float(value))
                            words = struct.unpack('<HH', raw)
                            self.client.batchwrite_wordunits(head_device, list(words))
                        else:
                            self.client.batchwrite_wordunits(head_device, [int(value)])
                
                await loop.run_in_executor(None, _write)
                return True
                
            except Exception as e:
                self.logger.error(f"MELSEC write error for {tag_name}: {e}")
                return False
