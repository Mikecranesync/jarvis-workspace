#!/usr/bin/env python3
"""
Motor and Drive Equipment Training Data
Extends ShopTalk coverage to electric motors, VFDs, and drive systems.
"""

import json
import random
from pathlib import Path
from datetime import datetime

OUTPUT_DIR = Path(__file__).parent

# Motor and Drive Equipment Configuration
MOTORS_CONFIG = {
    "induction_motor": {
        "description": "3-phase AC induction motor",
        "sensors": ["current_l1", "current_l2", "current_l3", "speed", "temperature", "vibration"],
        "normal_ranges": {
            "current_l1": (10, 15, "A"),
            "current_l2": (10, 15, "A"),
            "current_l3": (10, 15, "A"),
            "speed": (1750, 1800, "RPM"),
            "temperature": (40, 65, "°C"),
            "vibration": (0.5, 2.5, "mm/s")
        },
        "faults": [
            {
                "name": "phase_imbalance",
                "symptoms": {"current_l1": "high", "current_l2": "normal", "current_l3": "low"},
                "diagnosis": "Phase current imbalance detected. One phase drawing significantly more current than others.",
                "causes": ["Loose connection", "Damaged winding", "Power supply issue"],
                "actions": ["Check all phase connections at motor terminals", "Measure voltage at each phase", "Inspect contactor contacts for pitting", "Megger test motor windings"]
            },
            {
                "name": "overheating",
                "symptoms": {"temperature": "high", "current_l1": "high", "current_l2": "high", "current_l3": "high"},
                "diagnosis": "Motor overheating with elevated current draw. May indicate overload or cooling issue.",
                "causes": ["Overload condition", "Blocked cooling fan", "High ambient temperature", "Bearing friction"],
                "actions": ["Reduce load immediately", "Check cooling fan operation", "Clean motor fins and vents", "Verify motor is correctly sized for application"]
            },
            {
                "name": "bearing_wear",
                "symptoms": {"vibration": "high", "temperature": "high"},
                "diagnosis": "Elevated vibration and temperature suggest bearing degradation.",
                "causes": ["Lack of lubrication", "Misalignment", "End of bearing life", "Contamination"],
                "actions": ["Listen for grinding or squealing", "Check lubrication points", "Measure vibration spectrum if possible", "Plan bearing replacement"]
            },
            {
                "name": "insulation_breakdown",
                "symptoms": {"current_l1": "erratic", "temperature": "high"},
                "diagnosis": "Possible winding insulation degradation. Risk of ground fault.",
                "causes": ["Age and thermal cycling", "Moisture ingress", "Voltage spikes", "Contamination"],
                "actions": ["STOP motor immediately", "Perform megger/insulation resistance test", "Check for moisture in junction box", "Plan motor rewind or replacement"]
            }
        ]
    },
    "vfd": {
        "description": "Variable Frequency Drive",
        "sensors": ["output_frequency", "output_voltage", "dc_bus_voltage", "heatsink_temp", "output_current"],
        "normal_ranges": {
            "output_frequency": (0, 60, "Hz"),
            "output_voltage": (0, 480, "V"),
            "dc_bus_voltage": (650, 700, "VDC"),
            "heatsink_temp": (30, 55, "°C"),
            "output_current": (0, 100, "%FLA")
        },
        "faults": [
            {
                "name": "dc_bus_overvoltage",
                "symptoms": {"dc_bus_voltage": "high"},
                "diagnosis": "DC bus overvoltage fault. Usually caused by regenerative energy from decelerating load.",
                "causes": ["Deceleration too fast", "Overhauling load", "Incoming voltage spike", "Brake resistor failure"],
                "actions": ["Increase deceleration time", "Check brake resistor if equipped", "Verify incoming voltage stability", "Consider adding dynamic braking"]
            },
            {
                "name": "drive_overtemp",
                "symptoms": {"heatsink_temp": "high", "output_current": "high"},
                "diagnosis": "VFD heatsink overtemperature. Drive may derate or trip.",
                "causes": ["Blocked cooling fan", "High ambient temperature", "Overload condition", "Enclosure ventilation issue"],
                "actions": ["Check VFD cooling fan operation", "Clean heatsink fins", "Verify enclosure ventilation", "Reduce load or add cooling"]
            },
            {
                "name": "output_phase_loss",
                "symptoms": {"output_current": "erratic", "output_voltage": "low"},
                "diagnosis": "Output phase loss detected. Motor may run rough or stall.",
                "causes": ["Loose output connection", "Damaged output cable", "Motor winding open", "IGBT failure"],
                "actions": ["Check output terminal connections", "Inspect cable from VFD to motor", "Megger test motor", "If connections OK, drive may need repair"]
            }
        ]
    },
    "servo_motor": {
        "description": "Servo motor with encoder feedback",
        "sensors": ["position_error", "velocity", "torque_percent", "temperature", "encoder_status"],
        "normal_ranges": {
            "position_error": (0, 10, "counts"),
            "velocity": (0, 3000, "RPM"),
            "torque_percent": (0, 80, "%"),
            "temperature": (30, 60, "°C")
        },
        "faults": [
            {
                "name": "following_error",
                "symptoms": {"position_error": "high", "torque_percent": "high"},
                "diagnosis": "Servo following error - motor cannot reach commanded position.",
                "causes": ["Mechanical binding", "Undersized motor", "Gain tuning issue", "Encoder problem"],
                "actions": ["Check for mechanical obstruction", "Verify motor sizing for application", "Review servo tuning parameters", "Check encoder cable and connections"]
            },
            {
                "name": "encoder_fault",
                "symptoms": {"position_error": "erratic", "encoder_status": "fault"},
                "diagnosis": "Encoder communication error. Position feedback unreliable.",
                "causes": ["Encoder cable damage", "EMI interference", "Encoder failure", "Loose connector"],
                "actions": ["Inspect encoder cable for damage", "Check cable routing away from power cables", "Verify encoder connector is secure", "Test with known good encoder if available"]
            }
        ]
    }
}


def generate_motor_sample(equipment_type: str, scenario: str = "normal", language: str = "en") -> dict:
    """Generate a training sample for motor/drive equipment."""
    config = MOTORS_CONFIG[equipment_type]
    
    if scenario == "normal":
        # Generate normal readings
        readings = {}
        for sensor, (min_val, max_val, unit) in config["normal_ranges"].items():
            value = random.uniform(min_val, max_val)
            readings[sensor] = f"{value:.1f} {unit}"
        
        readings_str = ", ".join([f"{k}: {v}" for k, v in readings.items()])
        
        instruction = f"Check the {config['description']} status."
        output = f"The {config['description']} is operating normally.\n\nCurrent readings:\n" + "\n".join([f"- {k}: {v}" for k, v in readings.items()]) + "\n\nNo issues detected. Continue normal monitoring."
        
    else:
        # Generate fault scenario
        fault = random.choice(config["faults"])
        
        readings = {}
        for sensor, (min_val, max_val, unit) in config["normal_ranges"].items():
            symptom = fault["symptoms"].get(sensor, "normal")
            if symptom == "high":
                value = random.uniform(max_val * 1.2, max_val * 1.5)
            elif symptom == "low":
                value = random.uniform(min_val * 0.3, min_val * 0.7)
            elif symptom == "erratic":
                value = random.uniform(min_val * 0.5, max_val * 1.3)
            else:
                value = random.uniform(min_val, max_val)
            readings[sensor] = f"{value:.1f} {unit}"
        
        readings_str = ", ".join([f"{k}: {v}" for k, v in readings.items()])
        
        instruction = f"The {config['description']} alarm triggered. Readings: {readings_str}. Diagnose the problem."
        
        actions_str = "\n".join([f"{i+1}. {a}" for i, a in enumerate(fault["actions"])])
        causes_str = ", ".join(fault["causes"])
        
        output = f"""**Diagnosis: {fault['name'].replace('_', ' ').title()}**

{fault['diagnosis']}

**Possible Causes:** {causes_str}

**Current Readings:**
""" + "\n".join([f"- {k}: {v}" for k, v in readings.items()]) + f"""

**Recommended Actions:**
{actions_str}

**Safety Note:** Follow lockout/tagout procedures before any electrical work on motors or drives."""
    
    return {
        "instruction": instruction,
        "input": f"Equipment: {config['description']}",
        "output": output,
        "equipment": equipment_type,
        "scenario": scenario
    }


def generate_motor_dataset(n_per_type: int = 50) -> list:
    """Generate training data for all motor/drive types."""
    dataset = []
    
    for eq_type in MOTORS_CONFIG.keys():
        print(f"Generating {n_per_type * 2} samples for: {eq_type}")
        
        # Normal samples
        for _ in range(n_per_type):
            sample = generate_motor_sample(eq_type, "normal")
            dataset.append(sample)
        
        # Fault samples
        for _ in range(n_per_type):
            sample = generate_motor_sample(eq_type, "fault")
            dataset.append(sample)
    
    return dataset


if __name__ == "__main__":
    print("Generating Motor/Drive Training Data...")
    
    dataset = generate_motor_dataset(n_per_type=75)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = OUTPUT_DIR / f"motors_train_{timestamp}.json"
    
    alpaca_format = [
        {"instruction": d["instruction"], "input": d["input"], "output": d["output"]}
        for d in dataset
    ]
    
    with open(output_file, 'w') as f:
        json.dump(alpaca_format, f, indent=2)
    
    print(f"\nGenerated {len(dataset)} samples")
    print(f"Saved to: {output_file}")
    
    # Stats
    from collections import Counter
    equipment = Counter(d["equipment"] for d in dataset)
    scenarios = Counter(d["scenario"] for d in dataset)
    print(f"\nBy equipment: {dict(equipment)}")
    print(f"By scenario: {dict(scenarios)}")
