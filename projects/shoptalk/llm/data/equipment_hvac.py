#!/usr/bin/env python3
"""
HVAC Equipment Training Data
Extends ShopTalk to chillers, air handlers, and cooling systems.
"""

import json
import random
from pathlib import Path
from datetime import datetime

OUTPUT_DIR = Path(__file__).parent

HVAC_CONFIG = {
    "chiller": {
        "description": "Industrial water chiller",
        "sensors": ["supply_temp", "return_temp", "compressor_amps", "discharge_pressure", "suction_pressure", "oil_pressure"],
        "normal_ranges": {
            "supply_temp": (42, 46, "°F"),
            "return_temp": (52, 56, "°F"),
            "compressor_amps": (80, 120, "A"),
            "discharge_pressure": (180, 220, "PSI"),
            "suction_pressure": (35, 45, "PSI"),
            "oil_pressure": (45, 65, "PSI")
        },
        "faults": [
            {
                "name": "low_refrigerant",
                "symptoms": {"suction_pressure": "low", "discharge_pressure": "low", "supply_temp": "high"},
                "diagnosis": "Low refrigerant charge. System unable to achieve setpoint.",
                "actions": ["Check for refrigerant leaks", "Inspect sight glass for bubbles", "Check evaporator superheat", "Call certified technician for recharge"]
            },
            {
                "name": "condenser_fouling",
                "symptoms": {"discharge_pressure": "high", "compressor_amps": "high"},
                "diagnosis": "High head pressure indicates restricted heat rejection. Likely fouled condenser.",
                "actions": ["Inspect condenser coils for debris", "Check condenser fan operation", "Clean coils with approved cleaner", "Verify airflow is not blocked"]
            },
            {
                "name": "compressor_overload",
                "symptoms": {"compressor_amps": "high", "discharge_pressure": "high", "oil_pressure": "low"},
                "diagnosis": "Compressor approaching overload. May trip on thermal protection.",
                "actions": ["Check condenser for fouling", "Verify cooling water flow", "Check for non-condensables in system", "Inspect oil level and condition"]
            }
        ]
    },
    "ahu": {
        "description": "Air Handling Unit",
        "sensors": ["supply_air_temp", "return_air_temp", "fan_speed", "filter_dp", "coil_valve_position", "discharge_static"],
        "normal_ranges": {
            "supply_air_temp": (52, 58, "°F"),
            "return_air_temp": (72, 76, "°F"),
            "fan_speed": (70, 100, "%"),
            "filter_dp": (0.3, 0.8, "inWC"),
            "coil_valve_position": (20, 80, "%"),
            "discharge_static": (1.0, 1.5, "inWC")
        },
        "faults": [
            {
                "name": "filter_clogged",
                "symptoms": {"filter_dp": "high", "fan_speed": "high", "discharge_static": "low"},
                "diagnosis": "High filter differential pressure indicates clogged filters. Reduced airflow.",
                "actions": ["Replace air filters immediately", "Check filter rack for bypass", "Verify filter size is correct", "Consider upgrading filter change schedule"]
            },
            {
                "name": "frozen_coil",
                "symptoms": {"supply_air_temp": "low", "coil_valve_position": "high", "filter_dp": "high"},
                "diagnosis": "Possible frozen cooling coil. Ice restricting airflow.",
                "actions": ["Stop unit and let ice melt", "Check for low airflow causes", "Verify refrigerant charge", "Check freeze stat setting"]
            },
            {
                "name": "belt_failure",
                "symptoms": {"fan_speed": "low", "discharge_static": "low"},
                "diagnosis": "Fan belt may be slipping or broken. Reduced airflow.",
                "actions": ["Inspect fan belts for wear or breakage", "Check belt tension", "Look for belt debris in unit", "Replace belts if worn"]
            }
        ]
    },
    "cooling_tower": {
        "description": "Evaporative cooling tower",
        "sensors": ["water_temp_out", "water_temp_in", "fan_status", "water_level", "conductivity", "vibration"],
        "normal_ranges": {
            "water_temp_out": (78, 85, "°F"),
            "water_temp_in": (90, 100, "°F"),
            "water_level": (80, 100, "%"),
            "conductivity": (800, 1500, "µS/cm"),
            "vibration": (0.5, 2.0, "mm/s")
        },
        "faults": [
            {
                "name": "scale_buildup",
                "symptoms": {"conductivity": "high", "water_temp_out": "high"},
                "diagnosis": "High conductivity indicates mineral buildup. Reduced heat transfer efficiency.",
                "actions": ["Increase blowdown rate", "Check water treatment chemical levels", "Inspect fill media for scale", "Consider chemical cleaning"]
            },
            {
                "name": "fan_bearing_failure",
                "symptoms": {"vibration": "high"},
                "diagnosis": "High vibration indicates fan bearing degradation.",
                "actions": ["Inspect fan bearings", "Check lubrication", "Listen for unusual noise", "Plan bearing replacement before failure"]
            },
            {
                "name": "low_water_level",
                "symptoms": {"water_level": "low", "water_temp_out": "high"},
                "diagnosis": "Low basin water level. Risk of pump cavitation and reduced cooling.",
                "actions": ["Check makeup water supply", "Inspect float valve operation", "Look for basin leaks", "Verify blowdown is not excessive"]
            }
        ]
    }
}


def generate_hvac_sample(equipment_type: str, scenario: str = "normal") -> dict:
    """Generate a training sample for HVAC equipment."""
    config = HVAC_CONFIG[equipment_type]
    
    if scenario == "normal":
        readings = {}
        for sensor, (min_val, max_val, unit) in config["normal_ranges"].items():
            value = random.uniform(min_val, max_val)
            readings[sensor] = f"{value:.1f} {unit}"
        
        readings_str = ", ".join([f"{k}: {v}" for k, v in readings.items()])
        
        instruction = f"Check the {config['description']} status. Readings: {readings_str}"
        output = f"The {config['description']} is operating normally.\n\n**Current Readings:**\n" + "\n".join([f"- {k}: {v}" for k, v in readings.items()]) + "\n\n✅ All parameters within normal range. No action required."
        
    else:
        fault = random.choice(config["faults"])
        
        readings = {}
        for sensor, (min_val, max_val, unit) in config["normal_ranges"].items():
            symptom = fault["symptoms"].get(sensor, "normal")
            if symptom == "high":
                value = random.uniform(max_val * 1.15, max_val * 1.4)
            elif symptom == "low":
                value = random.uniform(min_val * 0.4, min_val * 0.7)
            else:
                value = random.uniform(min_val, max_val)
            readings[sensor] = f"{value:.1f} {unit}"
        
        readings_str = ", ".join([f"{k}: {v}" for k, v in readings.items()])
        actions_str = "\n".join([f"{i+1}. {a}" for i, a in enumerate(fault["actions"])])
        
        instruction = f"The {config['description']} has an alarm. Readings: {readings_str}. What's wrong?"
        output = f"""**Diagnosis: {fault['name'].replace('_', ' ').title()}**

{fault['diagnosis']}

**Abnormal Readings:**
""" + "\n".join([f"- {k}: {v}" + (" ⚠️" if fault["symptoms"].get(k.split()[0] if ' ' in k else k) else "") for k, v in readings.items()]) + f"""

**Recommended Actions:**
{actions_str}"""
    
    return {
        "instruction": instruction,
        "input": "",
        "output": output,
        "equipment": equipment_type,
        "scenario": scenario
    }


def generate_hvac_dataset(n_per_type: int = 50) -> list:
    """Generate HVAC training data."""
    dataset = []
    
    for eq_type in HVAC_CONFIG.keys():
        print(f"Generating samples for: {eq_type}")
        for _ in range(n_per_type):
            dataset.append(generate_hvac_sample(eq_type, "normal"))
            dataset.append(generate_hvac_sample(eq_type, "fault"))
    
    return dataset


if __name__ == "__main__":
    print("Generating HVAC Training Data...")
    
    dataset = generate_hvac_dataset(n_per_type=60)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = OUTPUT_DIR / f"hvac_train_{timestamp}.json"
    
    with open(output_file, 'w') as f:
        json.dump([{"instruction": d["instruction"], "input": d["input"], "output": d["output"]} for d in dataset], f, indent=2)
    
    print(f"Generated {len(dataset)} samples → {output_file}")
