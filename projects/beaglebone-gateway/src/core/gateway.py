#!/usr/bin/env python3
"""
Industrial Protocol Gateway - Core Application
Supports: Modbus TCP/RTU, Siemens S7, Allen-Bradley EtherNet/IP, OPC UA, Mitsubishi MELSEC

Copyright 2026 FactoryLM / Mike Harper
"""

import asyncio
import logging
import yaml
import signal
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional
from dataclasses import dataclass, field
from collections import defaultdict

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('gateway')


@dataclass
class TagValue:
    """Represents a single tag value with metadata"""
    value: Any
    timestamp: datetime = field(default_factory=datetime.now)
    quality: str = "good"
    source: str = ""
    
    def to_dict(self) -> Dict:
        return {
            'value': self.value,
            'timestamp': self.timestamp.isoformat(),
            'quality': self.quality,
            'source': self.source
        }


class TagDatabase:
    """Unified tag database for all protocol adapters"""
    
    def __init__(self):
        self._tags: Dict[str, TagValue] = {}
        self._subscribers: Dict[str, list] = defaultdict(list)
        self._lock = asyncio.Lock()
    
    async def write(self, tag_name: str, value: Any, source: str = "", quality: str = "good"):
        """Write a value to a tag"""
        async with self._lock:
            self._tags[tag_name] = TagValue(
                value=value,
                timestamp=datetime.now(),
                quality=quality,
                source=source
            )
            # Notify subscribers
            for callback in self._subscribers.get(tag_name, []):
                try:
                    await callback(tag_name, self._tags[tag_name])
                except Exception as e:
                    logger.error(f"Subscriber callback error: {e}")
    
    async def read(self, tag_name: str) -> Optional[TagValue]:
        """Read a tag value"""
        async with self._lock:
            return self._tags.get(tag_name)
    
    async def read_all(self) -> Dict[str, Dict]:
        """Read all tags"""
        async with self._lock:
            return {name: tv.to_dict() for name, tv in self._tags.items()}
    
    def subscribe(self, tag_name: str, callback):
        """Subscribe to tag changes"""
        self._subscribers[tag_name].append(callback)
    
    def get_tag_names(self) -> list:
        """Get all tag names"""
        return list(self._tags.keys())


class ProtocolAdapter:
    """Base class for protocol adapters"""
    
    def __init__(self, name: str, config: Dict, tag_db: TagDatabase):
        self.name = name
        self.config = config
        self.tag_db = tag_db
        self.running = False
        self.connected = False
        self.logger = logging.getLogger(f'adapter.{name}')
    
    async def connect(self) -> bool:
        """Connect to the device"""
        raise NotImplementedError
    
    async def disconnect(self):
        """Disconnect from the device"""
        raise NotImplementedError
    
    async def read_tags(self) -> Dict[str, Any]:
        """Read all configured tags"""
        raise NotImplementedError
    
    async def write_tag(self, tag_name: str, value: Any) -> bool:
        """Write a value to a tag"""
        raise NotImplementedError
    
    async def run(self):
        """Main polling loop"""
        self.running = True
        scan_rate = self.config.get('scan_rate', 1.0)
        retry_delay = self.config.get('retry_delay', 5.0)
        
        while self.running:
            try:
                if not self.connected:
                    self.logger.info(f"Connecting to {self.config.get('host', 'device')}...")
                    self.connected = await self.connect()
                    if self.connected:
                        self.logger.info("Connected successfully")
                    else:
                        self.logger.warning(f"Connection failed, retrying in {retry_delay}s")
                        await asyncio.sleep(retry_delay)
                        continue
                
                # Read all tags
                values = await self.read_tags()
                for tag_name, value in values.items():
                    await self.tag_db.write(tag_name, value, source=self.name)
                
                await asyncio.sleep(scan_rate)
                
            except Exception as e:
                self.logger.error(f"Error in polling loop: {e}")
                self.connected = False
                await asyncio.sleep(retry_delay)
    
    def stop(self):
        """Stop the adapter"""
        self.running = False


class Gateway:
    """Main gateway application"""
    
    def __init__(self, config_path: str = "config/gateway.yaml"):
        self.config_path = Path(config_path)
        self.config = {}
        self.tag_db = TagDatabase()
        self.adapters: Dict[str, ProtocolAdapter] = {}
        self.running = False
        
    def load_config(self):
        """Load configuration from YAML file"""
        if self.config_path.exists():
            with open(self.config_path) as f:
                self.config = yaml.safe_load(f)
            logger.info(f"Loaded configuration from {self.config_path}")
        else:
            logger.warning(f"Config file not found: {self.config_path}, using defaults")
            self.config = self._default_config()
    
    def _default_config(self) -> Dict:
        """Return default configuration"""
        return {
            'gateway': {
                'name': 'Industrial Gateway',
                'log_level': 'INFO'
            },
            'web': {
                'host': '0.0.0.0',
                'port': 8080
            },
            'opcua': {
                'enabled': True,
                'endpoint': 'opc.tcp://0.0.0.0:4840',
                'name': 'IndustrialGateway'
            },
            'devices': []
        }
    
    def create_adapter(self, device_config: Dict) -> Optional[ProtocolAdapter]:
        """Create a protocol adapter based on device configuration"""
        protocol = device_config.get('protocol', '').lower()
        name = device_config.get('name', f'device_{len(self.adapters)}')
        
        # Import adapters lazily to handle missing dependencies gracefully
        try:
            if protocol == 'modbus_tcp':
                from adapters.modbus_adapter import ModbusTCPAdapter
                return ModbusTCPAdapter(name, device_config, self.tag_db)
            elif protocol == 'modbus_rtu':
                from adapters.modbus_adapter import ModbusRTUAdapter
                return ModbusRTUAdapter(name, device_config, self.tag_db)
            elif protocol == 's7':
                from adapters.s7_adapter import S7Adapter
                return S7Adapter(name, device_config, self.tag_db)
            elif protocol == 'ethernetip':
                from adapters.ethernetip_adapter import EtherNetIPAdapter
                return EtherNetIPAdapter(name, device_config, self.tag_db)
            elif protocol == 'melsec':
                from adapters.melsec_adapter import MelsecAdapter
                return MelsecAdapter(name, device_config, self.tag_db)
            else:
                logger.error(f"Unknown protocol: {protocol}")
                return None
        except ImportError as e:
            logger.error(f"Failed to import adapter for {protocol}: {e}")
            return None
    
    async def start(self):
        """Start the gateway"""
        self.load_config()
        self.running = True
        
        # Set log level
        log_level = self.config.get('gateway', {}).get('log_level', 'INFO')
        logging.getLogger().setLevel(getattr(logging, log_level))
        
        logger.info("Starting Industrial Protocol Gateway")
        
        # Create adapters for each configured device
        for device_config in self.config.get('devices', []):
            adapter = self.create_adapter(device_config)
            if adapter:
                self.adapters[adapter.name] = adapter
                logger.info(f"Created adapter: {adapter.name} ({device_config.get('protocol')})")
        
        # Start all adapter tasks
        tasks = []
        for adapter in self.adapters.values():
            tasks.append(asyncio.create_task(adapter.run()))
        
        # Start OPC UA server if enabled
        if self.config.get('opcua', {}).get('enabled', False):
            from core.opcua_server import OPCUAServer
            opcua_server = OPCUAServer(self.config['opcua'], self.tag_db)
            tasks.append(asyncio.create_task(opcua_server.run()))
        
        # Start web server
        from web.app import create_app
        web_config = self.config.get('web', {})
        app = create_app(self.tag_db, self.adapters, self.config)
        
        # Run web server in background
        from hypercorn.asyncio import serve
        from hypercorn.config import Config as HypercornConfig
        
        hypercorn_config = HypercornConfig()
        hypercorn_config.bind = [f"{web_config.get('host', '0.0.0.0')}:{web_config.get('port', 8080)}"]
        
        tasks.append(asyncio.create_task(serve(app, hypercorn_config)))
        
        logger.info(f"Gateway started with {len(self.adapters)} adapters")
        logger.info(f"Web interface: http://{web_config.get('host', '0.0.0.0')}:{web_config.get('port', 8080)}")
        
        # Wait for all tasks
        try:
            await asyncio.gather(*tasks)
        except asyncio.CancelledError:
            logger.info("Gateway shutdown requested")
    
    def stop(self):
        """Stop the gateway"""
        self.running = False
        for adapter in self.adapters.values():
            adapter.stop()
        logger.info("Gateway stopped")


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Industrial Protocol Gateway')
    parser.add_argument('-c', '--config', default='config/gateway.yaml',
                        help='Path to configuration file')
    args = parser.parse_args()
    
    gateway = Gateway(args.config)
    
    # Handle shutdown signals
    def signal_handler(sig, frame):
        logger.info("Shutdown signal received")
        gateway.stop()
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Run the gateway
    asyncio.run(gateway.start())


if __name__ == '__main__':
    main()
