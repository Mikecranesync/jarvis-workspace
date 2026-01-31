#!/usr/bin/env python3
"""
PLC and Industrial Automation Training Data
Covers PLCs, HMIs, sensors, and control system diagnostics.
"""

import json
import random
from pathlib import Path
from datetime import datetime

OUTPUT_DIR = Path(__file__).parent

PLC_CONFIG = {
    "plc_controller": {
        "description": "Programmable Logic Controller",
        "sensors": ["cpu_load", "memory_used", "scan_time", "io_status", "battery_status", "comm_status"],
        "normal_ranges": {
            "cpu_load": (15, 45, "%"),
            "memory_used": (30, 70, "%"),
            "scan_time": (5, 25, "ms"),
            "battery_status": (80, 100, "%")
        },
        "faults": [
            {
                "name": "cpu_overload",
                "symptoms": {"cpu_load": "high", "scan_time": "high"},
                "diagnosis": "PLC CPU overloaded. Scan time increasing, may cause missed I/O updates.",
                "actions": ["Review program for inefficient code", "Check for excessive interrupt routines", "Consider program optimization", "Verify no infinite loops in logic"]
            },
            {
                "name": "memory_full",
                "symptoms": {"memory_used": "high"},
                "diagnosis": "PLC memory nearly full. Risk of program malfunction.",
                "actions": ["Archive and clear fault logs", "Remove unused program blocks", "Check for data table overflow", "Consider memory upgrade if available"]
            },
            {
                "name": "battery_low",
                "symptoms": {"battery_status": "low"},
                "diagnosis": "PLC backup battery low. Risk of program/data loss on power failure.",
                "actions": ["Replace battery during next maintenance window", "Backup program immediately", "Order replacement battery", "Schedule replacement within 30 days"]
            },
            {
                "name": "io_fault",
                "symptoms": {"io_status": "fault"},
                "diagnosis": "I/O module communication fault. Field devices may not respond.",
                "actions": ["Check I/O module LEDs for fault indication", "Verify field wiring connections", "Check for 24VDC power to I/O", "Reseat I/O module if safe to do so"]
            }
        ]
    },
    "hmi_panel": {
        "description": "Human Machine Interface Panel",
        "sensors": ["screen_status", "plc_comm", "alarm_count", "cpu_temp", "memory_free"],
        "normal_ranges": {
            "cpu_temp": (35, 55, "°C"),
            "memory_free": (30, 80, "%"),
            "alarm_count": (0, 5, "active")
        },
        "faults": [
            {
                "name": "comm_loss",
                "symptoms": {"plc_comm": "fault"},
                "diagnosis": "HMI lost communication with PLC. Displays may show stale data.",
                "actions": ["Check Ethernet/serial cable connection", "Verify PLC is running", "Check IP address configuration", "Restart HMI communication driver"]
            },
            {
                "name": "screen_freeze",
                "symptoms": {"cpu_temp": "high", "memory_free": "low"},
                "diagnosis": "HMI may be freezing due to high CPU temp or low memory.",
                "actions": ["Check panel ventilation", "Clear alarm history logs", "Restart HMI if safe", "Check for memory leaks in scripts"]
            }
        ]
    },
    "proximity_sensor": {
        "description": "Inductive proximity sensor",
        "sensors": ["output_state", "target_distance", "supply_voltage", "temperature"],
        "normal_ranges": {
            "target_distance": (0, 8, "mm"),
            "supply_voltage": (22, 26, "VDC"),
            "temperature": (10, 50, "°C")
        },
        "faults": [
            {
                "name": "no_detection",
                "symptoms": {"output_state": "stuck_off", "target_distance": "high"},
                "diagnosis": "Sensor not detecting target. May be misaligned or failed.",
                "actions": ["Check sensor alignment to target", "Verify target is metal (for inductive)", "Clean sensor face", "Check sensing distance specification"]
            },
            {
                "name": "false_trigger",
                "symptoms": {"output_state": "stuck_on"},
                "diagnosis": "Sensor stuck in triggered state. May be sensing unintended target.",
                "actions": ["Check for metal debris near sensor", "Verify mounting bracket is non-metallic", "Check for EMI interference", "Replace sensor if internal failure"]
            },
            {
                "name": "intermittent",
                "symptoms": {"output_state": "erratic"},
                "diagnosis": "Intermittent sensor operation. Loose wiring or failing sensor.",
                "actions": ["Check wiring connections at sensor", "Inspect cable for damage", "Verify supply voltage is stable", "Swap with known good sensor to test"]
            }
        ]
    },
    "level_transmitter": {
        "description": "Ultrasonic level transmitter",
        "sensors": ["level_percent", "signal_strength", "temperature", "output_ma"],
        "normal_ranges": {
            "level_percent": (10, 90, "%"),
            "signal_strength": (70, 100, "%"),
            "temperature": (0, 60, "°C"),
            "output_ma": (4, 20, "mA")
        },
        "faults": [
            {
                "name": "weak_signal",
                "symptoms": {"signal_strength": "low", "level_percent": "erratic"},
                "diagnosis": "Weak return signal. Foam, dust, or obstructions may be affecting measurement.",
                "actions": ["Check for foam on liquid surface", "Clean transmitter face", "Verify no obstructions in beam path", "Check mounting angle"]
            },
            {
                "name": "output_saturated",
                "symptoms": {"output_ma": "high", "level_percent": "high"},
                "diagnosis": "Transmitter output at maximum. Tank may be overfull or sensor misconfigured.",
                "actions": ["Verify actual tank level visually", "Check high level alarm operation", "Review transmitter span configuration", "Inspect for buildup on sensor"]
            }
        ]
    }
}


def generate_plc_sample(equipment_type: str, scenario: str = "normal") -> dict:
    """Generate training sample for PLC/automation equipment."""
    config = PLC_CONFIG[equipment_type]
    
    if scenario == "normal":
        readings = {}
        for sensor, (min_val, max_val, unit) in config["normal_ranges"].items():
            value = random.uniform(min_val, max_val)
            readings[sensor] = f"{value:.1f} {unit}"
        
        instruction = f"Check {config['description']} status."
        if readings:
            instruction += f" Readings: {', '.join([f'{k}: {v}' for k, v in readings.items()])}"
        
        output = f"The {config['description']} is operating normally.\n\n" + "\n".join([f"- {k}: {v} ✓" for k, v in readings.items()]) + "\n\nNo issues detected."
    else:
        fault = random.choice(config["faults"])
        readings = {}
        
        for sensor, (min_val, max_val, unit) in config["normal_ranges"].items():
            symptom = fault["symptoms"].get(sensor, "normal")
            if symptom == "high":
                value = random.uniform(max_val * 1.2, max_val * 1.5)
            elif symptom == "low":
                value = random.uniform(min_val * 0.2, min_val * 0.5)
            elif symptom in ["fault", "stuck_on", "stuck_off", "erratic"]:
                value = symptom.upper()
            else:
                value = random.uniform(min_val, max_val)
            
            if isinstance(value, float):
                readings[sensor] = f"{value:.1f} {unit}"
            else:
                readings[sensor] = value
        
        instruction = f"{config['description']} alarm. Status: {', '.join([f'{k}: {v}' for k, v in readings.items()])}. Diagnose."
        
        actions_str = "\n".join([f"{i+1}. {a}" for i, a in enumerate(fault["actions"])])
        output = f"""**{fault['name'].replace('_', ' ').title()}**

{fault['diagnosis']}

**Status:**
{chr(10).join([f'- {k}: {v}' for k, v in readings.items()])}

**Actions:**
{actions_str}"""
    
    return {"instruction": instruction, "input": "", "output": output, "equipment": equipment_type, "scenario": scenario}


def generate_plc_dataset(n_per_type: int = 50) -> list:
    """Generate PLC/automation training data."""
    dataset = []
    for eq_type in PLC_CONFIG.keys():
        print(f"Generating samples for: {eq_type}")
        for _ in range(n_per_type):
            dataset.append(generate_plc_sample(eq_type, "normal"))
            dataset.append(generate_plc_sample(eq_type, "fault"))
    return dataset


if __name__ == "__main__":
    print("Generating PLC/Automation Training Data...")
    dataset = generate_plc_dataset(n_per_type=50)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = OUTPUT_DIR / f"plc_train_{timestamp}.json"
    
    with open(output_file, 'w') as f:
        json.dump([{"instruction": d["instruction"], "input": d["input"], "output": d["output"]} for d in dataset], f, indent=2)
    
    print(f"Generated {len(dataset)} samples → {output_file}")
