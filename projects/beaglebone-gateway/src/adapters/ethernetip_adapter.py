#!/usr/bin/env python3
"""
Allen-Bradley EtherNet/IP Protocol Adapter
Supports CompactLogix, ControlLogix, Micro800 series
Uses pycomm3 library for communication
"""

import asyncio
from typing import Dict, Any, Optional, List
from dataclasses import dataclass

try:
    from pycomm3 import LogixDriver, SLCDriver
    from pycomm3.exceptions import CommError
    PYCOMM3_AVAILABLE = True
except ImportError:
    PYCOMM3_AVAILABLE = False

import sys
sys.path.append('..')
from core.gateway import ProtocolAdapter, TagDatabase


@dataclass
class EIPTag:
    """EtherNet/IP tag definition"""
    name: str
    plc_tag: str  # The actual tag name in the PLC
    data_type: str = "auto"  # auto, bool, int, dint, real, string
    array_index: Optional[int] = None
    bit: Optional[int] = None


class EtherNetIPAdapter(ProtocolAdapter):
    """Allen-Bradley EtherNet/IP Protocol Adapter"""
    
    def __init__(self, name: str, config: Dict, tag_db: TagDatabase):
        super().__init__(name, config, tag_db)
        
        if not PYCOMM3_AVAILABLE:
            raise ImportError("pycomm3 is required for EtherNet/IP adapter. Install with: pip install pycomm3")
        
        self.host = config.get('host', '192.168.1.1')
        self.slot = config.get('slot', 0)
        self.plc_type = config.get('plc_type', 'logix')  # logix or slc
        self.client = None
        self.tags: List[EIPTag] = self._parse_tags(config.get('tags', []))
        self._lock = asyncio.Lock()
    
    def _parse_tags(self, tag_configs: List[Dict]) -> List[EIPTag]:
        """Parse tag configuration into EIPTag objects"""
        tags = []
        for tc in tag_configs:
            tags.append(EIPTag(
                name=tc.get('name', tc.get('plc_tag', f'tag_{len(tags)}')),
                plc_tag=tc.get('plc_tag', tc.get('name', f'tag_{len(tags)}')),
                data_type=tc.get('data_type', 'auto'),
                array_index=tc.get('array_index'),
                bit=tc.get('bit')
            ))
        return tags
    
    async def connect(self) -> bool:
        """Connect to Allen-Bradley PLC"""
        try:
            loop = asyncio.get_event_loop()
            
            def _connect():
                if self.plc_type.lower() == 'slc':
                    driver = SLCDriver(self.host)
                else:
                    driver = LogixDriver(self.host, slot=self.slot)
                driver.open()
                return driver
            
            self.client = await loop.run_in_executor(None, _connect)
            return True
            
        except Exception as e:
            self.logger.error(f"EtherNet/IP connection error: {e}")
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
            try:
                loop = asyncio.get_event_loop()
                
                # Build list of PLC tags to read
                plc_tags = []
                for tag in self.tags:
                    tag_str = tag.plc_tag
                    if tag.array_index is not None:
                        tag_str += f'[{tag.array_index}]'
                    if tag.bit is not None:
                        tag_str += f'.{tag.bit}'
                    plc_tags.append(tag_str)
                
                # Read all tags at once (more efficient)
                def _read():
                    return self.client.read(*plc_tags)
                
                results = await loop.run_in_executor(None, _read)
                
                # Handle single tag result
                if not isinstance(results, list):
                    results = [results]
                
                # Map results back to tag names
                for tag, result in zip(self.tags, results):
                    if result.error is None:
                        values[tag.name] = result.value
                    else:
                        self.logger.warning(f"Tag {tag.name} error: {result.error}")
                
            except CommError as e:
                self.logger.error(f"Communication error: {e}")
                self.connected = False
            except Exception as e:
                self.logger.error(f"Read error: {e}")
        
        return values
    
    async def write_tag(self, tag_name: str, value: Any) -> bool:
        """Write a value to a tag"""
        tag = next((t for t in self.tags if t.name == tag_name), None)
        if not tag:
            self.logger.error(f"Tag not found: {tag_name}")
            return False
        
        async with self._lock:
            try:
                loop = asyncio.get_event_loop()
                
                # Build tag string
                tag_str = tag.plc_tag
                if tag.array_index is not None:
                    tag_str += f'[{tag.array_index}]'
                
                def _write():
                    return self.client.write(tag_str, value)
                
                result = await loop.run_in_executor(None, _write)
                
                if result.error is None:
                    return True
                else:
                    self.logger.error(f"Write error for {tag_name}: {result.error}")
                    return False
                
            except Exception as e:
                self.logger.error(f"Write exception for {tag_name}: {e}")
                return False
    
    async def get_tag_list(self) -> List[str]:
        """Get list of all tags from the PLC (Logix only)"""
        if not self.client or self.plc_type.lower() != 'logix':
            return []
        
        try:
            loop = asyncio.get_event_loop()
            
            def _get_tags():
                return self.client.get_tag_list()
            
            tag_list = await loop.run_in_executor(None, _get_tags)
            return [t['tag_name'] for t in tag_list]
            
        except Exception as e:
            self.logger.error(f"Failed to get tag list: {e}")
            return []
    
    async def discover_tags(self) -> Dict[str, Any]:
        """Discover all tags and their info from the PLC"""
        if not self.client or self.plc_type.lower() != 'logix':
            return {}
        
        try:
            loop = asyncio.get_event_loop()
            
            def _discover():
                tag_list = self.client.get_tag_list()
                return {
                    t['tag_name']: {
                        'type': t.get('data_type_name', 'unknown'),
                        'dimensions': t.get('dimensions', []),
                        'description': t.get('description', '')
                    }
                    for t in tag_list
                }
            
            return await loop.run_in_executor(None, _discover)
            
        except Exception as e:
            self.logger.error(f"Failed to discover tags: {e}")
            return {}
