#!/usr/bin/env python3
"""
ShopTalk Inference Engine
Real-time equipment monitoring and anomaly detection.
"""

import asyncio
import time
import logging
from typing import Dict, Optional, Callable, List
from dataclasses import dataclass
from pathlib import Path

# Add parent to path for imports
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from model.world_model import WorldModel, EquipmentState

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("InferenceEngine")


@dataclass
class InferenceResult:
    """Result from inference engine."""
    timestamp: float
    is_anomaly: bool
    anomalies: List[Dict]
    diagnosis: str
    prediction: Dict[str, float]
    z_scores: Dict[str, float]
    raw_state: Dict


class InferenceEngine:
    """
    Real-time inference engine for equipment monitoring.
    
    Connects to data sources, runs world model predictions,
    and triggers callbacks on anomalies.
    """
    
    def __init__(self, model: WorldModel, 
                 sample_interval: float = 0.1,
                 alert_cooldown: float = 30.0):
        """
        Initialize inference engine.
        
        Args:
            model: Trained world model
            sample_interval: Time between samples (seconds)
            alert_cooldown: Minimum time between alerts (seconds)
        """
        self.model = model
        self.sample_interval = sample_interval
        self.alert_cooldown = alert_cooldown
        
        # Callbacks
        self.on_anomaly: Optional[Callable[[InferenceResult], None]] = None
        self.on_update: Optional[Callable[[InferenceResult], None]] = None
        
        # State
        self.running = False
        self.last_alert_time = 0.0
        self.total_samples = 0
        self.total_anomalies = 0
        
        # Data source
        self.data_source: Optional[Callable[[], Dict]] = None
        
    def set_data_source(self, source: Callable[[], Dict]):
        """
        Set data source function.
        
        Args:
            source: Function that returns current sensor readings
        """
        self.data_source = source
        
    def set_on_anomaly(self, callback: Callable[[InferenceResult], None]):
        """Set callback for anomaly events."""
        self.on_anomaly = callback
        
    def set_on_update(self, callback: Callable[[InferenceResult], None]):
        """Set callback for all updates."""
        self.on_update = callback
    
    def process_sample(self, data: Dict) -> InferenceResult:
        """
        Process a single data sample.
        
        Args:
            data: Dict with sensor/control values
            
        Returns:
            InferenceResult with predictions and anomalies
        """
        timestamp = time.time()
        
        # Convert to EquipmentState
        sensors = {}
        controls = {}
        discrete = {}
        
        for key, value in data.items():
            if isinstance(value, bool):
                discrete[key] = value
            elif key.startswith('ctrl_'):
                controls[key] = float(value)
            else:
                sensors[key] = float(value)
        
        state = EquipmentState(
            timestamp=timestamp,
            sensors=sensors,
            controls=controls,
            discrete=discrete
        )
        
        # Run through model
        result = self.model.update(state)
        
        # Generate diagnosis if anomaly
        diagnosis = ""
        if result.get("is_anomaly"):
            diagnosis = self.model.diagnose(result.get("anomalies", []))
        
        # Create result
        inference_result = InferenceResult(
            timestamp=timestamp,
            is_anomaly=result.get("is_anomaly", False),
            anomalies=result.get("anomalies", []),
            diagnosis=diagnosis,
            prediction=result.get("prediction", {}),
            z_scores=result.get("z_scores", {}),
            raw_state=data
        )
        
        # Update counters
        self.total_samples += 1
        if inference_result.is_anomaly:
            self.total_anomalies += 1
        
        return inference_result
    
    async def run_async(self):
        """Run inference loop asynchronously."""
        if self.data_source is None:
            raise ValueError("No data source configured")
        
        self.running = True
        logger.info("Inference engine started")
        
        try:
            while self.running:
                start_time = time.time()
                
                # Get data
                try:
                    data = self.data_source()
                except Exception as e:
                    logger.error(f"Data source error: {e}")
                    await asyncio.sleep(self.sample_interval)
                    continue
                
                # Process
                result = self.process_sample(data)
                
                # Callbacks
                if self.on_update:
                    try:
                        self.on_update(result)
                    except Exception as e:
                        logger.error(f"Update callback error: {e}")
                
                if result.is_anomaly and self.on_anomaly:
                    # Check cooldown
                    if time.time() - self.last_alert_time > self.alert_cooldown:
                        try:
                            self.on_anomaly(result)
                            self.last_alert_time = time.time()
                        except Exception as e:
                            logger.error(f"Anomaly callback error: {e}")
                
                # Wait for next sample
                elapsed = time.time() - start_time
                sleep_time = max(0, self.sample_interval - elapsed)
                await asyncio.sleep(sleep_time)
                
        except asyncio.CancelledError:
            logger.info("Inference engine stopped")
        finally:
            self.running = False
    
    def run(self):
        """Run inference loop (blocking)."""
        asyncio.run(self.run_async())
    
    def stop(self):
        """Stop inference loop."""
        self.running = False
    
    def get_stats(self) -> Dict:
        """Get engine statistics."""
        return {
            "total_samples": self.total_samples,
            "total_anomalies": self.total_anomalies,
            "anomaly_rate": self.total_anomalies / max(1, self.total_samples),
            "running": self.running
        }


class SimulatedDataSource:
    """
    Simulated data source for testing.
    Generates realistic equipment data with optional fault injection.
    """
    
    def __init__(self, scenario: str = "normal"):
        """
        Initialize simulator.
        
        Args:
            scenario: "normal", "jam", "overload", "bearing_failure"
        """
        self.scenario = scenario
        self.sample_count = 0
        self.fault_start = 100  # Sample when fault starts
        
        # Base values
        self.base_speed = 1500
        self.base_current = 4.5
        self.base_conveyor = 80
        self.base_temp = 45
        
    def __call__(self) -> Dict:
        """Generate next data sample."""
        import numpy as np
        
        self.sample_count += 1
        
        # Normal operation with noise
        speed = self.base_speed + np.random.normal(0, 20)
        current = self.base_current + np.random.normal(0, 0.2)
        conveyor = self.base_conveyor + np.random.normal(0, 2)
        temp = self.base_temp + np.random.normal(0, 1)
        
        # Apply fault patterns after fault_start
        if self.sample_count > self.fault_start:
            progress = (self.sample_count - self.fault_start) / 50.0
            progress = min(progress, 1.0)
            
            if self.scenario == "jam":
                # Jam: current spikes, speed drops
                current += 4.0 * progress
                speed -= 300 * progress
                conveyor -= 50 * progress
                temp += 7 * progress
                
            elif self.scenario == "overload":
                # Overload: gradual current increase
                current += 2.0 * progress
                temp += 10 * progress
                
            elif self.scenario == "bearing_failure":
                # Bearing: vibration and temperature increase
                temp += 15 * progress
                # Add noise to simulate vibration
                speed += np.random.normal(0, 50) * progress
                
        return {
            "motor_speed": speed,
            "motor_current": current,
            "conveyor_speed": conveyor,
            "temperature": temp,
            "sensor_1": np.random.random() > 0.3,
            "sensor_2": np.random.random() > 0.5,
            "sensor_3": np.random.random() > 0.5,
            "sensor_4": np.random.random() > 0.7
        }
    
    def set_scenario(self, scenario: str):
        """Change scenario and reset."""
        self.scenario = scenario
        self.sample_count = 0


def create_modbus_data_source(host: str, port: int = 502) -> Callable[[], Dict]:
    """
    Create a data source that reads from Modbus TCP.
    
    Args:
        host: PLC IP address
        port: Modbus TCP port
        
    Returns:
        Callable data source function
    """
    try:
        from pymodbus.client import ModbusTcpClient
    except ImportError:
        logger.error("pymodbus not installed")
        return None
    
    client = ModbusTcpClient(host, port=port)
    
    def read_data() -> Dict:
        if not client.connected:
            client.connect()
        
        # Read registers (adjust addresses for your PLC)
        holding = client.read_holding_registers(0, 10)
        inputs = client.read_input_registers(0, 10)
        coils = client.read_coils(0, 8)
        
        return {
            "motor_speed": inputs.registers[0] * 0.1 if not inputs.isError() else 0,
            "motor_current": inputs.registers[1] * 0.01 if not inputs.isError() else 0,
            "conveyor_speed": inputs.registers[2] if not inputs.isError() else 0,
            "temperature": inputs.registers[3] * 0.1 if not inputs.isError() else 0,
            "sensor_1": coils.bits[0] if not coils.isError() else False,
            "sensor_2": coils.bits[1] if not coils.isError() else False,
            "sensor_3": coils.bits[2] if not coils.isError() else False,
            "sensor_4": coils.bits[3] if not coils.isError() else False,
        }
    
    return read_data


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--simulate", action="store_true", help="Use simulated data")
    parser.add_argument("--scenario", default="normal", help="Simulation scenario")
    parser.add_argument("--host", default="192.168.1.100", help="PLC host")
    parser.add_argument("--samples", type=int, default=200, help="Number of samples")
    args = parser.parse_args()
    
    # Create model
    from model.world_model import create_conveyor_model
    model = create_conveyor_model()
    
    # Create engine
    engine = InferenceEngine(model, sample_interval=0.05)
    
    # Setup data source
    if args.simulate:
        source = SimulatedDataSource(args.scenario)
        engine.set_data_source(source)
    else:
        source = create_modbus_data_source(args.host)
        if source:
            engine.set_data_source(source)
        else:
            print("Falling back to simulation")
            source = SimulatedDataSource(args.scenario)
            engine.set_data_source(source)
    
    # Setup callbacks
    def on_anomaly(result: InferenceResult):
        print(f"\n🚨 ANOMALY DETECTED!")
        print(f"   Diagnosis: {result.diagnosis}")
        for a in result.anomalies:
            print(f"   - {a['feature']}: {a['direction']} (z={a['z_score']:.2f})")
    
    engine.set_on_anomaly(on_anomaly)
    
    # Train on initial samples
    print("Training on normal operation...")
    training_data = []
    for i in range(100):
        data = source()
        state = EquipmentState(
            timestamp=float(i),
            sensors={k: v for k, v in data.items() if isinstance(v, (int, float)) and not k.startswith('sensor_')},
            controls={},
            discrete={k: v for k, v in data.items() if isinstance(v, bool)}
        )
        training_data.append(state)
    
    model.train(training_data)
    print("Training complete. Starting monitoring...\n")
    
    # Run inference
    for i in range(args.samples):
        data = source()
        result = engine.process_sample(data)
        
        if i % 10 == 0:
            status = "⚠️ ANOMALY" if result.is_anomaly else "✅ Normal"
            print(f"[{i:3d}] {status} | Speed: {data['motor_speed']:.0f} | Current: {data['motor_current']:.1f}A | Temp: {data['temperature']:.1f}°C")
        
        time.sleep(0.02)
    
    print(f"\n📊 Stats: {engine.get_stats()}")
