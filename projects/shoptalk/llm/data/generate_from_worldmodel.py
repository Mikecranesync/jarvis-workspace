#!/usr/bin/env python3
"""
Generate LLM training data from World Model simulations.
This creates realistic sensor trajectories with labeled fault scenarios.
"""

import sys
import json
from pathlib import Path
from datetime import datetime

# Add shoptalk src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from model.world_model import WorldModel, EquipmentState, create_conveyor_model
from inference.engine import SimulatedDataSource

OUTPUT_DIR = Path(__file__).parent


def generate_trajectory_data(scenario: str, n_samples: int = 100) -> list:
    """Generate a time-series of readings for a scenario."""
    source = SimulatedDataSource(scenario)
    trajectory = []
    
    for i in range(n_samples):
        data = source()
        trajectory.append({
            "timestamp": i,
            "readings": data,
            "scenario": scenario,
            "phase": "normal" if i < source.fault_start else "fault"
        })
    
    return trajectory


def trajectory_to_training_sample(trajectory: list, scenario: str) -> dict:
    """Convert a trajectory to a training conversation."""
    
    # Find the fault transition point
    fault_start = None
    for i, t in enumerate(trajectory):
        if t["phase"] == "fault":
            fault_start = i
            break
    
    if fault_start is None:
        # Normal operation
        readings = trajectory[-1]["readings"]
        readings_str = ", ".join([f"{k}: {v:.1f}" for k, v in readings.items() if isinstance(v, (int, float))])
        
        return {
            "instruction": f"Check the conveyor system status. Current readings: {readings_str}",
            "input": "",
            "output": f"The conveyor system is operating normally. All readings are within expected ranges.\n\nCurrent status:\n- Motor speed: {readings.get('motor_speed', 0):.0f} RPM (normal: 1400-1600)\n- Motor current: {readings.get('motor_current', 0):.1f}A (normal: 3.5-5.5)\n- Temperature: {readings.get('temperature', 0):.1f}°C (normal: 40-55)\n\nNo action required. Continue normal monitoring."
        }
    
    # Fault scenario - get readings at peak fault
    fault_readings = trajectory[-1]["readings"]
    normal_readings = trajectory[fault_start - 5]["readings"] if fault_start > 5 else trajectory[0]["readings"]
    
    fault_str = ", ".join([f"{k}: {v:.1f}" for k, v in fault_readings.items() if isinstance(v, (int, float))])
    
    # Generate diagnosis based on scenario
    diagnoses = {
        "jam": {
            "diagnosis": "Belt Jam Detected",
            "explanation": "High motor current combined with low belt and motor speed indicates mechanical obstruction preventing belt movement.",
            "actions": [
                "STOP the conveyor immediately using E-stop",
                "Follow lockout/tagout procedure before approaching",
                "Inspect belt for product accumulation or debris",
                "Check for objects caught in rollers or pulleys",
                "Clear any obstruction found",
                "Verify belt tension and alignment",
                "Test at low speed before resuming full operation"
            ]
        },
        "overload": {
            "diagnosis": "Motor Overload Condition",
            "explanation": "Elevated current draw and rising temperature suggest the motor is working harder than designed, possibly due to excessive load or mechanical resistance.",
            "actions": [
                "Reduce load on conveyor if possible",
                "Check for product pile-up or uneven loading",
                "Inspect motor cooling fan operation",
                "Verify belt tension is not too tight",
                "Check bearings for signs of wear",
                "Monitor temperature - shutdown if exceeds 70°C"
            ]
        },
        "bearing_failure": {
            "diagnosis": "Possible Bearing Failure",
            "explanation": "High temperature with normal current suggests friction from worn bearings rather than electrical overload.",
            "actions": [
                "Schedule immediate bearing inspection",
                "Check lubrication levels on all bearings",
                "Listen for unusual grinding or squealing sounds",
                "Monitor vibration if sensor available",
                "Plan bearing replacement during next maintenance window",
                "Reduce speed to extend bearing life until replacement"
            ]
        }
    }
    
    diag = diagnoses.get(scenario, diagnoses["jam"])
    actions_str = "\n".join([f"{i+1}. {a}" for i, a in enumerate(diag["actions"])])
    
    return {
        "instruction": f"The conveyor alarm triggered. Current readings: {fault_str}. Diagnose the problem.",
        "input": f"Equipment: Conveyor System\nPrevious normal readings: Motor current: {normal_readings.get('motor_current', 4.5):.1f}A, Motor speed: {normal_readings.get('motor_speed', 1500):.0f} RPM",
        "output": f"""**Diagnosis: {diag['diagnosis']}**

{diag['explanation']}

**Key Abnormal Readings:**
- Motor current: {fault_readings.get('motor_current', 0):.1f}A (normal: 3.5-5.5A) {'⚠️ HIGH' if fault_readings.get('motor_current', 0) > 6 else ''}
- Motor speed: {fault_readings.get('motor_speed', 0):.0f} RPM (normal: 1400-1600) {'⚠️ LOW' if fault_readings.get('motor_speed', 0) < 1300 else ''}
- Belt speed: {fault_readings.get('conveyor_speed', 0):.0f}% (normal: 75-85%) {'⚠️ LOW' if fault_readings.get('conveyor_speed', 0) < 60 else ''}
- Temperature: {fault_readings.get('temperature', 0):.1f}°C (normal: 40-55°C) {'⚠️ HIGH' if fault_readings.get('temperature', 0) > 55 else ''}

**Required Actions:**
{actions_str}

**Safety Note:** Always follow lockout/tagout procedures before any physical inspection or maintenance."""
    }


def generate_dataset(n_per_scenario: int = 50) -> list:
    """Generate complete dataset from all scenarios."""
    scenarios = ["normal", "jam", "overload", "bearing_failure"]
    dataset = []
    
    for scenario in scenarios:
        print(f"Generating {n_per_scenario} samples for: {scenario}")
        
        for i in range(n_per_scenario):
            # Vary the trajectory length
            n_samples = 100 + (i * 2)  # 100-200 samples
            trajectory = generate_trajectory_data(scenario, n_samples)
            sample = trajectory_to_training_sample(trajectory, scenario)
            sample["scenario"] = scenario
            sample["trajectory_id"] = f"{scenario}_{i:03d}"
            dataset.append(sample)
    
    return dataset


if __name__ == "__main__":
    print("Generating training data from World Model simulations...")
    
    dataset = generate_dataset(n_per_scenario=100)
    
    # Save in Alpaca format
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = OUTPUT_DIR / f"worldmodel_train_{timestamp}.json"
    
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
    scenarios = Counter(d["scenario"] for d in dataset)
    print(f"\nBy scenario: {dict(scenarios)}")
