#!/usr/bin/env python3
"""
OPC UA Server
Exposes all gateway tags via OPC UA protocol
"""

import asyncio
import logging
from typing import Dict, Any
from datetime import datetime

try:
    from opcua import Server, ua
    from opcua.common.node import Node
    OPCUA_AVAILABLE = True
except ImportError:
    try:
        from asyncua import Server, ua
        from asyncua.common.node import Node
        ASYNCUA_AVAILABLE = True
        OPCUA_AVAILABLE = False
    except ImportError:
        OPCUA_AVAILABLE = False
        ASYNCUA_AVAILABLE = False

import sys
sys.path.append('..')
from core.gateway import TagDatabase

logger = logging.getLogger('opcua_server')


class OPCUAServer:
    """OPC UA Server exposing gateway tags"""
    
    def __init__(self, config: Dict, tag_db: TagDatabase):
        self.config = config
        self.tag_db = tag_db
        self.server = None
        self.nodes: Dict[str, Node] = {}
        self.running = False
        
        if not OPCUA_AVAILABLE and not ASYNCUA_AVAILABLE:
            raise ImportError("opcua or asyncua is required. Install with: pip install opcua")
    
    async def run(self):
        """Start the OPC UA server"""
        self.running = True
        endpoint = self.config.get('endpoint', 'opc.tcp://0.0.0.0:4840')
        name = self.config.get('name', 'IndustrialGateway')
        
        logger.info(f"Starting OPC UA server at {endpoint}")
        
        # Create server
        self.server = Server()
        await self.server.init()
        
        self.server.set_endpoint(endpoint)
        self.server.set_server_name(name)
        
        # Set up namespace
        uri = f"urn:{name}"
        idx = await self.server.register_namespace(uri)
        
        # Create objects folder for our tags
        objects = self.server.nodes.objects
        tags_folder = await objects.add_folder(idx, "Tags")
        
        # Start server
        async with self.server:
            logger.info("OPC UA server started")
            
            # Main loop - update tag values
            while self.running:
                try:
                    await self._update_nodes(tags_folder, idx)
                    await asyncio.sleep(0.5)  # Update rate
                except Exception as e:
                    logger.error(f"OPC UA update error: {e}")
                    await asyncio.sleep(1)
    
    async def _update_nodes(self, folder: Node, idx: int):
        """Update OPC UA nodes from tag database"""
        all_tags = await self.tag_db.read_all()
        
        for tag_name, tag_data in all_tags.items():
            try:
                if tag_name not in self.nodes:
                    # Create new node
                    value = tag_data.get('value', 0)
                    variant_type = self._get_variant_type(value)
                    
                    node = await folder.add_variable(
                        idx, tag_name, value, variant_type
                    )
                    await node.set_writable()
                    self.nodes[tag_name] = node
                    logger.debug(f"Created OPC UA node: {tag_name}")
                else:
                    # Update existing node
                    value = tag_data.get('value', 0)
                    await self.nodes[tag_name].write_value(value)
                    
            except Exception as e:
                logger.error(f"Error updating node {tag_name}: {e}")
    
    def _get_variant_type(self, value: Any) -> ua.VariantType:
        """Get OPC UA variant type for a Python value"""
        if isinstance(value, bool):
            return ua.VariantType.Boolean
        elif isinstance(value, int):
            if value < 0:
                return ua.VariantType.Int32
            elif value > 65535:
                return ua.VariantType.UInt32
            else:
                return ua.VariantType.UInt16
        elif isinstance(value, float):
            return ua.VariantType.Float
        elif isinstance(value, str):
            return ua.VariantType.String
        else:
            return ua.VariantType.Variant
    
    def stop(self):
        """Stop the OPC UA server"""
        self.running = False
        if self.server:
            try:
                asyncio.get_event_loop().run_until_complete(self.server.stop())
            except:
                pass
