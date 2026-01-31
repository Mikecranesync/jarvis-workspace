#!/usr/bin/env python3
"""
Data Collection Script for BeagleBone Edge Gateway
Collects PLC data from Factory I/O via Modbus TCP

Usage:
    python3 collect.py --host 192.168.1.100 --scenario normal --duration 1800
"""

import argparse
import csv
import json
import time
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any

# Try to import pymodbus
try:
    from pymodbus.client import ModbusTcpClient
    MODBUS_AVAILABLE = True
except ImportError:
    MODBUS_AVAILABLE = False
    print("Warning: pymodbus not installed. Install with: pip install pymodbus")

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Data directory
DATA_DIR = Path("/opt/factorylm/data")
DATA_DIR.mkdir(parents=True, exist_ok=True)


class PLCDataCollector:
    """Collects data from PLC via Modbus TCP."""
    
    # Default register mapping (adjust for your PLC/Factory I/O setup)
    DEFAULT_REGISTERS = {
        # Holding Registers (read/write)
        "motor_speed_setpoint": {"address": 0, "type": "holding", "scale": 0.1},
        "conveyor_speed": {"address": 1, "type": "holding", "scale": 1.0},
        
        # Input Registers (read-only, from sensors)
        "motor_current": {"address": 0, "type": "input", "scale": 0.01},
        "motor_speed_actual": {"address": 1, "type": "input", "scale": 0.1},
        "temperature": {"address": 2, "type": "input", "scale": 0.1},
        
        # Coils (digital outputs)
        "motor_run": {"address": 0, "type": "coil"},
        "conveyor_run": {"address": 1, "type": "coil"},
        "alarm_active": {"address": 2, "type": "coil"},
        
        # Discrete Inputs (digital inputs from sensors)
        "sensor_1": {"address": 0, "type": "discrete"},
        "sensor_2": {"address": 1, "type": "discrete"},
        "sensor_3": {"address": 2, "type": "discrete"},
        "sensor_4": {"address": 3, "type": "discrete"},
        "sensor_5": {"address": 4, "type": "discrete"},
        "sensor_6": {"address": 5, "type": "discrete"},
        "sensor_7": {"address": 6, "type": "discrete"},
        "sensor_8": {"address": 7, "type": "discrete"},
        "emergency_stop": {"address": 8, "type": "discrete"},
    }
    
    def __init__(self, host: str, port: int = 502, 
                 registers: Dict = None, unit_id: int = 1):
        """Initialize the collector.
        
        Args:
            host: PLC IP address
            port: Modbus TCP port (default 502)
            registers: Custom register mapping
            unit_id: Modbus unit/slave ID
        """
        self.host = host
        self.port = port
        self.registers = registers or self.DEFAULT_REGISTERS
        self.unit_id = unit_id
        self.client = None
        
    def connect(self) -> bool:
        """Connect to the PLC."""
        if not MODBUS_AVAILABLE:
            logger.error("pymodbus not available")
            return False
            
        self.client = ModbusTcpClient(self.host, port=self.port)
        if self.client.connect():
            logger.info(f"Connected to PLC at {self.host}:{self.port}")
            return True
        else:
            logger.error(f"Failed to connect to PLC at {self.host}:{self.port}")
            return False
    
    def disconnect(self):
        """Disconnect from the PLC."""
        if self.client:
            self.client.close()
            logger.info("Disconnected from PLC")
    
    def read_all(self) -> Dict[str, Any]:
        """Read all configured registers.
        
        Returns:
            Dictionary with register names and values
        """
        if not self.client:
            return {}
            
        data = {
            "timestamp": datetime.now().isoformat(),
            "unix_ms": int(time.time() * 1000),
        }
        
        for name, config in self.registers.items():
            try:
                addr = config["address"]
                reg_type = config["type"]
                scale = config.get("scale", 1.0)
                
                if reg_type == "holding":
                    result = self.client.read_holding_registers(addr, 1, slave=self.unit_id)
                    if not result.isError():
                        data[name] = result.registers[0] * scale
                        
                elif reg_type == "input":
                    result = self.client.read_input_registers(addr, 1, slave=self.unit_id)
                    if not result.isError():
                        data[name] = result.registers[0] * scale
                        
                elif reg_type == "coil":
                    result = self.client.read_coils(addr, 1, slave=self.unit_id)
                    if not result.isError():
                        data[name] = result.bits[0]
                        
                elif reg_type == "discrete":
                    result = self.client.read_discrete_inputs(addr, 1, slave=self.unit_id)
                    if not result.isError():
                        data[name] = result.bits[0]
                        
            except Exception as e:
                logger.warning(f"Error reading {name}: {e}")
                data[name] = None
                
        return data
    
    def collect(self, duration: int, interval: float = 0.1,
                scenario: str = "default", output_format: str = "csv") -> str:
        """Collect data for a specified duration.
        
        Args:
            duration: Collection duration in seconds
            interval: Sampling interval in seconds
            scenario: Scenario name for labeling
            output_format: "csv" or "jsonl"
            
        Returns:
            Path to output file
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = DATA_DIR / f"{scenario}_{timestamp}.{output_format}"
        
        logger.info(f"Starting collection: {scenario}")
        logger.info(f"Duration: {duration}s, Interval: {interval}s")
        logger.info(f"Output: {filename}")
        
        samples = []
        start_time = time.time()
        sample_count = 0
        
        try:
            while (time.time() - start_time) < duration:
                data = self.read_all()
                data["scenario"] = scenario
                data["sample_id"] = sample_count
                samples.append(data)
                sample_count += 1
                
                if sample_count % 100 == 0:
                    logger.info(f"Collected {sample_count} samples...")
                
                time.sleep(interval)
                
        except KeyboardInterrupt:
            logger.info("Collection interrupted by user")
        
        # Save data
        if output_format == "csv":
            self._save_csv(samples, filename)
        else:
            self._save_jsonl(samples, filename)
            
        logger.info(f"Collection complete: {sample_count} samples saved to {filename}")
        return str(filename)
    
    def _save_csv(self, samples: List[Dict], filename: Path):
        """Save samples to CSV file."""
        if not samples:
            return
            
        with open(filename, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=samples[0].keys())
            writer.writeheader()
            writer.writerows(samples)
    
    def _save_jsonl(self, samples: List[Dict], filename: Path):
        """Save samples to JSONL file."""
        with open(filename, 'w') as f:
            for sample in samples:
                f.write(json.dumps(sample) + '\n')


def simulate_collection(duration: int, interval: float, 
                       scenario: str) -> str:
    """Simulate data collection for testing without PLC.
    
    Returns:
        Path to output file with simulated data
    """
    import random
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = DATA_DIR / f"{scenario}_{timestamp}_simulated.csv"
    
    logger.info(f"SIMULATION MODE - No PLC connected")
    logger.info(f"Generating simulated data for scenario: {scenario}")
    
    samples = []
    start_time = time.time()
    sample_count = 0
    
    # Simulation parameters based on scenario
    if scenario == "normal":
        motor_speed_base = 1500
        variance = 50
    elif scenario == "overload":
        motor_speed_base = 1800
        variance = 100
    elif scenario == "jam":
        motor_speed_base = 1500
        variance = 200
    else:
        motor_speed_base = 1500
        variance = 50
    
    while (time.time() - start_time) < duration:
        # Generate realistic-looking data
        sample = {
            "timestamp": datetime.now().isoformat(),
            "unix_ms": int(time.time() * 1000),
            "sample_id": sample_count,
            "scenario": scenario,
            "motor_speed_actual": motor_speed_base + random.uniform(-variance, variance),
            "motor_current": 4.0 + random.uniform(-0.5, 0.5),
            "conveyor_speed": 80 + random.uniform(-5, 5),
            "temperature": 45 + random.uniform(-2, 2),
            "motor_run": True,
            "conveyor_run": True,
            "alarm_active": False,
            "sensor_1": random.random() > 0.3,
            "sensor_2": random.random() > 0.5,
            "sensor_3": random.random() > 0.5,
            "sensor_4": random.random() > 0.7,
            "emergency_stop": False,
        }
        
        # Add scenario-specific anomalies
        if scenario == "jam" and sample_count > duration / interval / 2:
            sample["motor_current"] = 8.0 + random.uniform(0, 2)
            sample["conveyor_speed"] = 20 + random.uniform(-10, 10)
            sample["alarm_active"] = True
            
        samples.append(sample)
        sample_count += 1
        
        if sample_count % 100 == 0:
            logger.info(f"Generated {sample_count} samples...")
        
        time.sleep(interval)
    
    # Save to CSV
    with open(filename, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=samples[0].keys())
        writer.writeheader()
        writer.writerows(samples)
    
    logger.info(f"Simulation complete: {sample_count} samples saved to {filename}")
    return str(filename)


def main():
    parser = argparse.ArgumentParser(description="Collect PLC data for world model training")
    parser.add_argument("--host", default="192.168.1.100", help="PLC IP address")
    parser.add_argument("--port", type=int, default=502, help="Modbus TCP port")
    parser.add_argument("--scenario", default="normal", help="Scenario name for labeling")
    parser.add_argument("--duration", type=int, default=300, help="Collection duration in seconds")
    parser.add_argument("--interval", type=float, default=0.1, help="Sampling interval in seconds")
    parser.add_argument("--simulate", action="store_true", help="Simulate data (no PLC needed)")
    parser.add_argument("--format", choices=["csv", "jsonl"], default="csv", help="Output format")
    
    args = parser.parse_args()
    
    if args.simulate:
        output = simulate_collection(args.duration, args.interval, args.scenario)
    else:
        collector = PLCDataCollector(args.host, args.port)
        if collector.connect():
            try:
                output = collector.collect(
                    duration=args.duration,
                    interval=args.interval,
                    scenario=args.scenario,
                    output_format=args.format
                )
            finally:
                collector.disconnect()
        else:
            logger.error("Could not connect to PLC. Use --simulate for testing.")
            return
    
    print(f"\nOutput file: {output}")


if __name__ == "__main__":
    main()
