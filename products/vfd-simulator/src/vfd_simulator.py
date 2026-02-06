#!/usr/bin/env python3
"""
VFD Modbus Simulator
====================
Emulates a Variable Frequency Drive for PLC integration and testing.
Supports Modbus TCP protocol with realistic VFD behavior.

Author: Jarvis Agent for FactoryLM
Created: 2026-02-06
Issue: #27
"""

import asyncio
import logging
import time
import math
from dataclasses import dataclass, field
from typing import Optional, Callable
from enum import IntEnum, IntFlag

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("VFD-Simulator")


class VFDCommand(IntFlag):
    """VFD Command Word Bits"""
    RUN = 0x0001
    DIRECTION = 0x0002  # 0=Forward, 1=Reverse
    FAULT_RESET = 0x0004
    EXTERNAL_FAULT = 0x0008
    ENABLE = 0x0010


class VFDStatus(IntFlag):
    """VFD Status Word Bits"""
    READY = 0x0001
    RUNNING = 0x0002
    DIRECTION = 0x0004  # 0=Forward, 1=Reverse
    FAULT = 0x0008
    AT_SPEED = 0x0010
    VOLTAGE_OK = 0x0020
    CURRENT_LIMIT = 0x0040
    THERMAL_WARNING = 0x0080


class VFDFault(IntEnum):
    """VFD Fault Codes"""
    NO_FAULT = 0
    OVERCURRENT = 1
    OVERVOLTAGE = 2
    UNDERVOLTAGE = 3
    OVERTEMPERATURE = 4
    GROUND_FAULT = 5
    MOTOR_OVERLOAD = 6
    COMMUNICATION_LOSS = 7


@dataclass
class VFDParameters:
    """VFD Configuration Parameters"""
    # Motor Parameters
    motor_hp: float = 0.5
    motor_voltage: int = 230
    motor_amps: float = 2.0
    motor_rpm: int = 1725
    motor_poles: int = 4
    
    # Drive Parameters
    base_frequency: float = 60.0
    max_frequency: float = 60.0
    min_frequency: float = 0.0
    accel_time: float = 5.0  # seconds
    decel_time: float = 5.0  # seconds
    
    # Communication
    modbus_address: int = 1
    
    # Scaling
    speed_ref_max: int = 10000  # 0-10000 = 0-max_frequency


@dataclass
class VFDState:
    """Real-time VFD State"""
    # Command inputs
    command_word: int = 0
    speed_reference: int = 0  # 0-10000
    
    # Status outputs
    status_word: int = VFDStatus.READY | VFDStatus.VOLTAGE_OK
    output_frequency: float = 0.0  # Hz
    output_current: float = 0.0  # Amps
    output_voltage: float = 0.0  # Volts
    dc_bus_voltage: float = 325.0  # Volts (rectified 230VAC)
    motor_rpm: float = 0.0
    motor_torque: float = 0.0  # %
    
    # Internal state
    target_frequency: float = 0.0
    is_running: bool = False
    fault_code: int = VFDFault.NO_FAULT
    run_time: float = 0.0  # Total run hours
    
    # Timestamps
    last_update: float = field(default_factory=time.time)


class VFDSimulator:
    """
    Variable Frequency Drive Simulator
    
    Simulates realistic VFD behavior including:
    - Acceleration/deceleration ramps
    - V/Hz control
    - Current draw based on load
    - Fault injection
    """
    
    def __init__(self, params: Optional[VFDParameters] = None):
        self.params = params or VFDParameters()
        self.state = VFDState()
        self._running = False
        self._callbacks: list[Callable] = []
        
        # Calculate derived values
        self._sync_speed = (120 * self.params.base_frequency) / self.params.motor_poles
        self._slip = (self._sync_speed - self.params.motor_rpm) / self._sync_speed
        
        logger.info(f"VFD Simulator initialized: {self.params.motor_hp}HP, {self.params.motor_voltage}V")
    
    def add_callback(self, callback: Callable):
        """Add state change callback"""
        self._callbacks.append(callback)
    
    def _notify_callbacks(self):
        """Notify all callbacks of state change"""
        for cb in self._callbacks:
            try:
                cb(self.state)
            except Exception as e:
                logger.error(f"Callback error: {e}")
    
    def write_command(self, command_word: int):
        """Write command word from PLC"""
        self.state.command_word = command_word
        
        # Process run command
        run_requested = bool(command_word & VFDCommand.RUN)
        enable = bool(command_word & VFDCommand.ENABLE) if command_word & VFDCommand.ENABLE else True
        
        if run_requested and enable and not self.state.is_running:
            if self.state.fault_code == VFDFault.NO_FAULT:
                self.state.is_running = True
                self.state.status_word |= VFDStatus.RUNNING
                logger.info("VFD Started")
        elif not run_requested and self.state.is_running:
            self.state.is_running = False
            self.state.status_word &= ~VFDStatus.RUNNING
            logger.info("VFD Stopped")
        
        # Process fault reset
        if command_word & VFDCommand.FAULT_RESET:
            self.reset_fault()
        
        # Process direction
        if command_word & VFDCommand.DIRECTION:
            self.state.status_word |= VFDStatus.DIRECTION
        else:
            self.state.status_word &= ~VFDStatus.DIRECTION
        
        self._notify_callbacks()
    
    def write_speed_reference(self, speed_ref: int):
        """Write speed reference from PLC (0-10000)"""
        self.state.speed_reference = max(0, min(speed_ref, self.params.speed_ref_max))
        self.state.target_frequency = (
            self.state.speed_reference / self.params.speed_ref_max
        ) * self.params.max_frequency
        self._notify_callbacks()
    
    def read_status(self) -> int:
        """Read status word"""
        return self.state.status_word
    
    def read_frequency(self) -> int:
        """Read output frequency (Hz * 10)"""
        return int(self.state.output_frequency * 10)
    
    def read_current(self) -> int:
        """Read output current (Amps * 10)"""
        return int(self.state.output_current * 10)
    
    def read_voltage(self) -> int:
        """Read output voltage"""
        return int(self.state.output_voltage)
    
    def read_dc_bus(self) -> int:
        """Read DC bus voltage"""
        return int(self.state.dc_bus_voltage)
    
    def read_rpm(self) -> int:
        """Read motor RPM"""
        return int(self.state.motor_rpm)
    
    def inject_fault(self, fault_code: VFDFault):
        """Inject a fault for testing"""
        self.state.fault_code = fault_code
        self.state.status_word |= VFDStatus.FAULT
        self.state.is_running = False
        self.state.status_word &= ~VFDStatus.RUNNING
        logger.warning(f"Fault injected: {fault_code.name}")
        self._notify_callbacks()
    
    def reset_fault(self):
        """Reset fault condition"""
        if self.state.fault_code != VFDFault.NO_FAULT:
            logger.info(f"Fault reset: {VFDFault(self.state.fault_code).name}")
            self.state.fault_code = VFDFault.NO_FAULT
            self.state.status_word &= ~VFDStatus.FAULT
            self._notify_callbacks()
    
    def update(self, dt: float = 0.1):
        """
        Update VFD simulation state
        
        Args:
            dt: Time step in seconds
        """
        now = time.time()
        self.state.last_update = now
        
        if self.state.is_running:
            # Calculate frequency ramp
            freq_diff = self.state.target_frequency - self.state.output_frequency
            
            if freq_diff > 0:
                # Accelerating
                max_change = (self.params.max_frequency / self.params.accel_time) * dt
                self.state.output_frequency += min(freq_diff, max_change)
            elif freq_diff < 0:
                # Decelerating
                max_change = (self.params.max_frequency / self.params.decel_time) * dt
                self.state.output_frequency -= min(-freq_diff, max_change)
            
            # Check if at speed
            if abs(freq_diff) < 0.1:
                self.state.status_word |= VFDStatus.AT_SPEED
            else:
                self.state.status_word &= ~VFDStatus.AT_SPEED
            
            # Update run time
            self.state.run_time += dt / 3600  # Convert to hours
        else:
            # Coast to stop when not running
            if self.state.output_frequency > 0:
                max_change = (self.params.max_frequency / self.params.decel_time) * dt
                self.state.output_frequency = max(0, self.state.output_frequency - max_change)
            
            self.state.status_word &= ~VFDStatus.AT_SPEED
        
        # Calculate V/Hz output voltage
        if self.state.output_frequency > 0:
            volts_per_hz = self.params.motor_voltage / self.params.base_frequency
            self.state.output_voltage = min(
                self.state.output_frequency * volts_per_hz,
                self.params.motor_voltage
            )
        else:
            self.state.output_voltage = 0
        
        # Calculate motor RPM (with slip)
        sync_speed_at_freq = (120 * self.state.output_frequency) / self.params.motor_poles
        self.state.motor_rpm = sync_speed_at_freq * (1 - self._slip)
        
        # Simulate current draw (simplified)
        if self.state.is_running and self.state.output_frequency > 0:
            # Base current proportional to frequency
            base_current = (self.state.output_frequency / self.params.base_frequency) * self.params.motor_amps
            # Add some noise
            noise = 0.1 * math.sin(now * 10)
            self.state.output_current = max(0, base_current + noise)
        else:
            self.state.output_current = 0
        
        # Simulate DC bus voltage (slight variation)
        self.state.dc_bus_voltage = 325 + 5 * math.sin(now * 2)
        
        self._notify_callbacks()
    
    async def run_async(self, interval: float = 0.1):
        """Run simulation loop asynchronously"""
        self._running = True
        logger.info("VFD Simulation started")
        
        while self._running:
            self.update(interval)
            await asyncio.sleep(interval)
        
        logger.info("VFD Simulation stopped")
    
    def stop(self):
        """Stop simulation loop"""
        self._running = False
    
    def get_state_dict(self) -> dict:
        """Get current state as dictionary"""
        return {
            "command_word": self.state.command_word,
            "speed_reference": self.state.speed_reference,
            "status_word": self.state.status_word,
            "output_frequency_hz": round(self.state.output_frequency, 1),
            "output_current_a": round(self.state.output_current, 2),
            "output_voltage_v": round(self.state.output_voltage, 1),
            "dc_bus_voltage_v": round(self.state.dc_bus_voltage, 1),
            "motor_rpm": round(self.state.motor_rpm, 0),
            "is_running": self.state.is_running,
            "at_speed": bool(self.state.status_word & VFDStatus.AT_SPEED),
            "fault_code": self.state.fault_code,
            "fault_name": VFDFault(self.state.fault_code).name,
            "run_time_hours": round(self.state.run_time, 2),
        }


# Modbus Register Map
class ModbusRegisters:
    """Modbus holding register addresses"""
    COMMAND_WORD = 0      # 40001
    SPEED_REF = 1         # 40002
    STATUS_WORD = 2       # 40003
    OUTPUT_FREQ = 3       # 40004
    OUTPUT_CURRENT = 4    # 40005
    OUTPUT_VOLTAGE = 5    # 40006
    DC_BUS_VOLTAGE = 6    # 40007
    MOTOR_RPM = 7         # 40008
    FAULT_CODE = 8        # 40009
    RUN_TIME_H = 9        # 40010 (hours, high word)
    RUN_TIME_L = 10       # 40011 (hours, low word x100)


if __name__ == "__main__":
    # Quick test
    vfd = VFDSimulator()
    
    print("Testing VFD Simulator...")
    print(f"Initial state: {vfd.get_state_dict()}")
    
    # Start VFD
    vfd.write_command(VFDCommand.RUN | VFDCommand.ENABLE)
    vfd.write_speed_reference(5000)  # 50% speed = 30Hz
    
    # Simulate for a few seconds
    for i in range(50):
        vfd.update(0.1)
        if i % 10 == 0:
            state = vfd.get_state_dict()
            print(f"t={i*0.1:.1f}s: {state['output_frequency_hz']}Hz, {state['motor_rpm']}RPM, {state['output_current_a']}A")
    
    print(f"Final state: {vfd.get_state_dict()}")
