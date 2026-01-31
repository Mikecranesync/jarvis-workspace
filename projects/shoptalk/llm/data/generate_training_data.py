#!/usr/bin/env python3
"""
Synthetic Training Data Generator for ShopTalk LLM
Generates conversation pairs for fine-tuning on industrial diagnostics.

This creates the "domain expertise" moat - teaching an LLM to think like
an experienced maintenance technician.
"""

import json
import random
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Tuple

OUTPUT_DIR = Path(__file__).parent
OUTPUT_DIR.mkdir(exist_ok=True)

# Equipment types and their characteristics
EQUIPMENT = {
    "conveyor": {
        "sensors": ["motor_speed", "motor_current", "belt_speed", "temperature", "vibration"],
        "normal_ranges": {
            "motor_speed": (1400, 1600, "RPM"),
            "motor_current": (3.5, 5.5, "A"),
            "belt_speed": (75, 85, "%"),
            "temperature": (40, 55, "°C"),
            "vibration": (0.5, 2.0, "mm/s")
        },
        "faults": [
            {
                "name": "belt_jam",
                "symptoms": {"motor_current": "high", "belt_speed": "low", "motor_speed": "low"},
                "diagnosis": "Belt jam detected. High motor current with low belt speed indicates mechanical obstruction.",
                "actions": ["Stop conveyor immediately", "Check for debris or product accumulation", "Inspect belt tension", "Clear obstruction before restart"]
            },
            {
                "name": "motor_overload",
                "symptoms": {"motor_current": "high", "temperature": "high"},
                "diagnosis": "Motor overload condition. Elevated current and temperature suggest excessive load or cooling issue.",
                "actions": ["Reduce load on conveyor", "Check motor cooling fan", "Verify belt tension is not too tight", "Inspect motor bearings"]
            },
            {
                "name": "belt_slip",
                "symptoms": {"motor_speed": "normal", "belt_speed": "low"},
                "diagnosis": "Belt slippage detected. Motor running but belt not moving at expected speed.",
                "actions": ["Check belt tension", "Inspect drive pulley for wear", "Look for oil or debris on belt", "Adjust tensioner"]
            },
            {
                "name": "bearing_failure",
                "symptoms": {"vibration": "high", "temperature": "high"},
                "diagnosis": "Possible bearing failure. High vibration and temperature indicate mechanical wear.",
                "actions": ["Schedule immediate bearing inspection", "Check lubrication levels", "Listen for unusual noise", "Plan bearing replacement"]
            }
        ]
    },
    "pump": {
        "sensors": ["flow_rate", "inlet_pressure", "outlet_pressure", "motor_current", "temperature"],
        "normal_ranges": {
            "flow_rate": (80, 120, "GPM"),
            "inlet_pressure": (10, 20, "PSI"),
            "outlet_pressure": (50, 80, "PSI"),
            "motor_current": (15, 25, "A"),
            "temperature": (35, 50, "°C")
        },
        "faults": [
            {
                "name": "cavitation",
                "symptoms": {"flow_rate": "low", "inlet_pressure": "low", "vibration": "high"},
                "diagnosis": "Pump cavitation detected. Low inlet pressure causing vapor bubbles.",
                "actions": ["Check suction line for blockage", "Verify inlet valve is fully open", "Check fluid level in supply tank", "Inspect impeller for damage"]
            },
            {
                "name": "seal_leak",
                "symptoms": {"flow_rate": "low", "outlet_pressure": "low"},
                "diagnosis": "Possible mechanical seal leak. Pressure loss indicates fluid escaping.",
                "actions": ["Inspect seal area for leaks", "Check seal faces for wear", "Verify proper seal installation", "Replace seal if damaged"]
            }
        ]
    },
    "compressor": {
        "sensors": ["discharge_pressure", "suction_pressure", "oil_pressure", "temperature", "motor_current"],
        "normal_ranges": {
            "discharge_pressure": (100, 150, "PSI"),
            "suction_pressure": (20, 40, "PSI"),
            "oil_pressure": (40, 60, "PSI"),
            "temperature": (60, 90, "°C"),
            "motor_current": (30, 50, "A")
        },
        "faults": [
            {
                "name": "low_oil",
                "symptoms": {"oil_pressure": "low", "temperature": "high"},
                "diagnosis": "Low oil pressure with elevated temperature. Risk of bearing damage.",
                "actions": ["Check oil level immediately", "Inspect for oil leaks", "Verify oil pump operation", "Add oil if low"]
            },
            {
                "name": "valve_failure",
                "symptoms": {"discharge_pressure": "low", "suction_pressure": "high", "temperature": "high"},
                "diagnosis": "Possible valve failure. Abnormal pressure differential indicates internal leakage.",
                "actions": ["Inspect discharge valves", "Check suction valves", "Look for valve plate damage", "Plan valve replacement"]
            }
        ]
    }
}

# Conversation templates
TEMPLATES = {
    "status_query": [
        "What's the status of the {equipment}?",
        "How is the {equipment} running?",
        "Check the {equipment} for me.",
        "Is the {equipment} operating normally?",
        "Give me a status report on the {equipment}.",
    ],
    "status_query_spanish": [
        "¿Cuál es el estado del {equipment}?",
        "¿Cómo está funcionando el {equipment}?",
        "Revisa el {equipment} por favor.",
        "¿El {equipment} está operando normalmente?",
        "Dame un informe del {equipment}.",
    ],
    "anomaly_query": [
        "The {equipment} seems off. What's wrong?",
        "I'm seeing issues with the {equipment}. Diagnose it.",
        "The {equipment} alarm went off. What happened?",
        "Something's wrong with the {equipment}. Help!",
        "Diagnose the {equipment} problem.",
    ],
    "normal_response": [
        "The {equipment} is operating normally. All readings within expected ranges: {readings}",
        "{equipment} status: Normal operation. {readings}",
        "Everything looks good on the {equipment}. Current readings: {readings}",
    ],
    "fault_response": [
        "{diagnosis}\n\nCurrent readings: {readings}\n\nRecommended actions:\n{actions}",
        "⚠️ {diagnosis}\n\nSensor data: {readings}\n\nImmediate steps:\n{actions}",
    ]
}


def generate_reading(sensor: str, range_info: Tuple, condition: str = "normal") -> str:
    """Generate a sensor reading based on condition."""
    min_val, max_val, unit = range_info
    
    if condition == "normal":
        value = random.uniform(min_val, max_val)
    elif condition == "high":
        value = random.uniform(max_val * 1.2, max_val * 1.5)
    elif condition == "low":
        value = random.uniform(min_val * 0.3, min_val * 0.7)
    else:
        value = random.uniform(min_val, max_val)
    
    return f"{sensor}: {value:.1f} {unit}"


def generate_readings(equipment_type: str, fault: Dict = None) -> str:
    """Generate a set of sensor readings."""
    config = EQUIPMENT[equipment_type]
    readings = []
    
    for sensor in config["sensors"]:
        if sensor in config["normal_ranges"]:
            condition = "normal"
            if fault and sensor in fault.get("symptoms", {}):
                condition = fault["symptoms"][sensor]
            readings.append(generate_reading(sensor, config["normal_ranges"][sensor], condition))
    
    return ", ".join(readings)


def generate_conversation(equipment_type: str, scenario: str = "normal", language: str = "en") -> Dict:
    """Generate a single conversation pair."""
    config = EQUIPMENT[equipment_type]
    
    if scenario == "normal":
        # Normal operation query
        if language == "es":
            query_templates = TEMPLATES["status_query_spanish"]
        else:
            query_templates = TEMPLATES["status_query"]
        
        query = random.choice(query_templates).format(equipment=equipment_type)
        readings = generate_readings(equipment_type)
        response = random.choice(TEMPLATES["normal_response"]).format(
            equipment=equipment_type.title(),
            readings=readings
        )
    else:
        # Fault scenario
        fault = random.choice(config["faults"])
        query = random.choice(TEMPLATES["anomaly_query"]).format(equipment=equipment_type)
        readings = generate_readings(equipment_type, fault)
        actions = "\n".join([f"• {a}" for a in fault["actions"]])
        response = random.choice(TEMPLATES["fault_response"]).format(
            diagnosis=fault["diagnosis"],
            readings=readings,
            actions=actions
        )
    
    return {
        "instruction": query,
        "input": f"Equipment: {equipment_type}\nReadings: {readings}" if scenario != "normal" else "",
        "output": response,
        "equipment": equipment_type,
        "scenario": scenario,
        "language": language
    }


def generate_dataset(n_samples: int = 1000) -> List[Dict]:
    """Generate a complete training dataset."""
    dataset = []
    
    equipment_types = list(EQUIPMENT.keys())
    scenarios = ["normal", "fault"]
    languages = ["en", "es"]
    
    for _ in range(n_samples):
        equipment = random.choice(equipment_types)
        scenario = random.choice(scenarios)
        # 70% English, 30% Spanish
        language = "en" if random.random() > 0.3 else "es"
        
        conversation = generate_conversation(equipment, scenario, language)
        dataset.append(conversation)
    
    return dataset


def save_dataset(dataset: List[Dict], format: str = "alpaca"):
    """Save dataset in specified format."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    if format == "alpaca":
        # Alpaca format for fine-tuning
        output = [
            {
                "instruction": d["instruction"],
                "input": d["input"],
                "output": d["output"]
            }
            for d in dataset
        ]
        filename = OUTPUT_DIR / f"shoptalk_train_{timestamp}.json"
        with open(filename, 'w') as f:
            json.dump(output, f, indent=2, ensure_ascii=False)
        print(f"Saved Alpaca format: {filename}")
        
    elif format == "sharegpt":
        # ShareGPT format
        output = [
            {
                "conversations": [
                    {"from": "human", "value": d["instruction"] + ("\n" + d["input"] if d["input"] else "")},
                    {"from": "gpt", "value": d["output"]}
                ]
            }
            for d in dataset
        ]
        filename = OUTPUT_DIR / f"shoptalk_sharegpt_{timestamp}.json"
        with open(filename, 'w') as f:
            json.dump(output, f, indent=2, ensure_ascii=False)
        print(f"Saved ShareGPT format: {filename}")
    
    return filename


def generate_knowledge_base() -> Dict:
    """Generate a structured knowledge base for RAG."""
    kb = {
        "equipment": EQUIPMENT,
        "general_knowledge": {
            "safety_first": "Always follow lockout/tagout procedures before any maintenance.",
            "documentation": "Log all maintenance activities in the CMMS.",
            "escalation": "If unsure, escalate to senior technician or engineer."
        },
        "fault_patterns": [],
        "best_practices": [
            "Check oil levels weekly on rotating equipment",
            "Inspect belts for wear monthly",
            "Monitor vibration trends to predict bearing failure",
            "Keep motor cooling fins clean",
            "Document all repairs with photos when possible"
        ]
    }
    
    # Extract all fault patterns
    for eq_type, config in EQUIPMENT.items():
        for fault in config["faults"]:
            kb["fault_patterns"].append({
                "equipment": eq_type,
                "fault_name": fault["name"],
                "symptoms": fault["symptoms"],
                "diagnosis": fault["diagnosis"],
                "actions": fault["actions"]
            })
    
    return kb


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Generate ShopTalk training data")
    parser.add_argument("--samples", type=int, default=1000, help="Number of samples")
    parser.add_argument("--format", choices=["alpaca", "sharegpt", "both"], default="both")
    args = parser.parse_args()
    
    print(f"Generating {args.samples} training samples...")
    dataset = generate_dataset(args.samples)
    
    if args.format in ["alpaca", "both"]:
        save_dataset(dataset, "alpaca")
    if args.format in ["sharegpt", "both"]:
        save_dataset(dataset, "sharegpt")
    
    # Also save knowledge base
    kb = generate_knowledge_base()
    kb_file = OUTPUT_DIR / "knowledge_base.json"
    with open(kb_file, 'w') as f:
        json.dump(kb, f, indent=2, ensure_ascii=False)
    print(f"Saved knowledge base: {kb_file}")
    
    print(f"\nDataset stats:")
    print(f"  Total samples: {len(dataset)}")
    print(f"  Normal scenarios: {sum(1 for d in dataset if d['scenario'] == 'normal')}")
    print(f"  Fault scenarios: {sum(1 for d in dataset if d['scenario'] == 'fault')}")
    print(f"  English: {sum(1 for d in dataset if d['language'] == 'en')}")
    print(f"  Spanish: {sum(1 for d in dataset if d['language'] == 'es')}")
