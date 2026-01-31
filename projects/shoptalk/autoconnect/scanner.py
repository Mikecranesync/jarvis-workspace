#!/usr/bin/env python3
"""
ShopTalk Auto-Connect Scanner
Automatically discovers PLCs and industrial devices on the network.

Usage:
    python scanner.py                    # Scan local network
    python scanner.py --network 192.168.1.0/24  # Scan specific network
    python scanner.py --ip 192.168.1.10  # Scan specific IP
"""

import socket
import json
import argparse
import ipaddress
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
from concurrent.futures import ThreadPoolExecutor, as_completed
import logging

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

# Try to import pymodbus
try:
    from pymodbus.client import ModbusTcpClient
    from pymodbus.exceptions import ModbusException
    HAS_PYMODBUS = True
except ImportError:
    HAS_PYMODBUS = False
    logger.warning("pymodbus not installed. Install with: pip install pymodbus")

# Load device profiles
PROFILES_PATH = Path(__file__).parent.parent.parent.parent / "knowledge" / "devices" / "modbus_profiles.json"


@dataclass
class DiscoveredDevice:
    """Represents a discovered industrial device."""
    ip: str
    port: int
    protocol: str
    slave_id: Optional[int] = None
    vendor: Optional[str] = None
    product: Optional[str] = None
    profile_match: Optional[str] = None
    registers_found: int = 0
    tags: List[str] = None
    
    def __post_init__(self):
        if self.tags is None:
            self.tags = []


class NetworkScanner:
    """Scans network for industrial devices."""
    
    # Common industrial ports
    INDUSTRIAL_PORTS = {
        502: "modbus_tcp",
        102: "s7comm",
        44818: "ethernet_ip",
        4840: "opcua",
        2222: "ethernet_ip_explicit",
        47808: "bacnet"
    }
    
    def __init__(self, timeout: float = 1.0, max_workers: int = 50):
        self.timeout = timeout
        self.max_workers = max_workers
        self.profiles = self._load_profiles()
    
    def _load_profiles(self) -> Dict:
        """Load device profiles from knowledge base."""
        if PROFILES_PATH.exists():
            with open(PROFILES_PATH) as f:
                return json.load(f).get("profiles", {})
        return {}
    
    def scan_port(self, ip: str, port: int) -> Optional[str]:
        """Check if a port is open on an IP."""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(self.timeout)
            result = sock.connect_ex((ip, port))
            sock.close()
            if result == 0:
                return self.INDUSTRIAL_PORTS.get(port, "unknown")
        except:
            pass
        return None
    
    def scan_ip(self, ip: str) -> List[DiscoveredDevice]:
        """Scan a single IP for industrial devices."""
        devices = []
        
        for port, protocol in self.INDUSTRIAL_PORTS.items():
            result = self.scan_port(ip, port)
            if result:
                device = DiscoveredDevice(
                    ip=ip,
                    port=port,
                    protocol=protocol
                )
                
                # If Modbus, try to get more info
                if protocol == "modbus_tcp" and HAS_PYMODBUS:
                    self._probe_modbus(device)
                
                devices.append(device)
        
        return devices
    
    def _probe_modbus(self, device: DiscoveredDevice):
        """Probe a Modbus device for more information."""
        try:
            client = ModbusTcpClient(device.ip, port=device.port, timeout=self.timeout)
            if not client.connect():
                return
            
            # Try common slave IDs
            for slave_id in [1, 2, 3, 0]:
                try:
                    # Try reading first holding register
                    result = client.read_holding_registers(0, 1, slave=slave_id)
                    if not result.isError():
                        device.slave_id = slave_id
                        
                        # Count readable registers
                        for start in range(0, 100, 10):
                            try:
                                r = client.read_holding_registers(start, 10, slave=slave_id)
                                if not r.isError():
                                    device.registers_found += 10
                            except:
                                break
                        
                        # Try device identification
                        try:
                            # Function 0x2B - Read Device Identification
                            from pymodbus.mei_message import ReadDeviceInformationRequest
                            req = ReadDeviceInformationRequest(slave=slave_id)
                            response = client.execute(req)
                            if not response.isError() and hasattr(response, 'information'):
                                info = response.information
                                device.vendor = info.get(0, b'').decode('utf-8', errors='ignore')
                                device.product = info.get(1, b'').decode('utf-8', errors='ignore')
                        except:
                            pass
                        
                        # Match to profile
                        device.profile_match = self._match_profile(device)
                        break
                        
                except:
                    continue
            
            client.close()
            
        except Exception as e:
            logger.debug(f"Modbus probe error for {device.ip}: {e}")
    
    def _match_profile(self, device: DiscoveredDevice) -> Optional[str]:
        """Match device to a known profile."""
        for profile_name, profile in self.profiles.items():
            if profile.get("protocol") != device.protocol:
                continue
            
            # Check vendor match
            if device.vendor and profile.get("vendor"):
                if profile["vendor"].lower() in device.vendor.lower():
                    return profile_name
            
            # Check product pattern
            if device.product and profile.get("identification", {}).get("product_code_pattern"):
                import re
                pattern = profile["identification"]["product_code_pattern"]
                if re.match(pattern, device.product):
                    return profile_name
        
        return None
    
    def scan_network(self, network: str) -> List[DiscoveredDevice]:
        """Scan an entire network for devices."""
        try:
            net = ipaddress.ip_network(network, strict=False)
        except ValueError as e:
            logger.error(f"Invalid network: {e}")
            return []
        
        all_devices = []
        hosts = list(net.hosts())
        
        logger.info(f"Scanning {len(hosts)} hosts on {network}...")
        
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = {executor.submit(self.scan_ip, str(ip)): ip for ip in hosts}
            
            completed = 0
            for future in as_completed(futures):
                completed += 1
                if completed % 50 == 0:
                    logger.info(f"  Progress: {completed}/{len(hosts)}")
                
                try:
                    devices = future.result()
                    all_devices.extend(devices)
                except Exception as e:
                    logger.debug(f"Scan error: {e}")
        
        return all_devices
    
    def get_local_network(self) -> str:
        """Detect local network."""
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            local_ip = s.getsockname()[0]
            s.close()
            
            # Assume /24 network
            parts = local_ip.split('.')
            return f"{parts[0]}.{parts[1]}.{parts[2]}.0/24"
        except:
            return "192.168.1.0/24"


def main():
    parser = argparse.ArgumentParser(description="ShopTalk Auto-Connect Scanner")
    parser.add_argument("--network", help="Network to scan (e.g., 192.168.1.0/24)")
    parser.add_argument("--ip", help="Single IP to scan")
    parser.add_argument("--timeout", type=float, default=1.0, help="Connection timeout")
    parser.add_argument("--output", "-o", help="Output file (JSON)")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    scanner = NetworkScanner(timeout=args.timeout)
    
    print("=" * 50)
    print("🔍 ShopTalk Auto-Connect Scanner")
    print("=" * 50)
    
    if args.ip:
        print(f"\nScanning {args.ip}...")
        devices = scanner.scan_ip(args.ip)
    else:
        network = args.network or scanner.get_local_network()
        print(f"\nScanning network: {network}")
        devices = scanner.scan_network(network)
    
    print(f"\n{'=' * 50}")
    print(f"📡 Found {len(devices)} industrial device(s)")
    print("=" * 50)
    
    for device in devices:
        print(f"\n✅ {device.ip}:{device.port}")
        print(f"   Protocol: {device.protocol}")
        if device.slave_id is not None:
            print(f"   Slave ID: {device.slave_id}")
        if device.vendor:
            print(f"   Vendor: {device.vendor}")
        if device.product:
            print(f"   Product: {device.product}")
        if device.profile_match:
            print(f"   Profile: {device.profile_match} ✨")
        if device.registers_found:
            print(f"   Registers: {device.registers_found} found")
    
    if args.output:
        output_data = {
            "scan_results": [asdict(d) for d in devices],
            "total_devices": len(devices)
        }
        with open(args.output, 'w') as f:
            json.dump(output_data, f, indent=2)
        print(f"\n💾 Results saved to {args.output}")
    
    return devices


if __name__ == "__main__":
    main()
