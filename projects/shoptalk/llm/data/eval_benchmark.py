#!/usr/bin/env python3
"""
ShopTalk Evaluation Benchmark
Test the LLM's diagnostic accuracy on held-out scenarios.
"""

import json
from pathlib import Path
from typing import List, Dict, Tuple

EVAL_CASES = [
    # Conveyor scenarios
    {
        "id": "conv_jam_01",
        "equipment": "conveyor",
        "input": "Motor current: 8.2A, Belt speed: 25%, Motor speed: 1150 RPM, Temperature: 52°C",
        "expected_fault": "belt_jam",
        "expected_keywords": ["jam", "obstruction", "stop", "lockout"],
        "language": "en"
    },
    {
        "id": "conv_jam_02_es",
        "equipment": "conveyor",
        "input": "Corriente del motor: 8.5A, Velocidad de banda: 20%, Velocidad del motor: 1100 RPM",
        "expected_fault": "belt_jam",
        "expected_keywords": ["atasco", "obstrucción", "detener"],
        "language": "es"
    },
    {
        "id": "conv_bearing_01",
        "equipment": "conveyor",
        "input": "Vibration: 4.5 mm/s, Temperature: 68°C, Motor current: 5.2A",
        "expected_fault": "bearing_failure",
        "expected_keywords": ["bearing", "vibration", "inspect", "lubrication"],
        "language": "en"
    },
    {
        "id": "conv_normal_01",
        "equipment": "conveyor",
        "input": "Motor current: 4.5A, Belt speed: 82%, Motor speed: 1520 RPM, Temperature: 47°C",
        "expected_fault": None,
        "expected_keywords": ["normal", "operating", "good"],
        "language": "en"
    },
    
    # Pump scenarios
    {
        "id": "pump_cavitation_01",
        "equipment": "pump",
        "input": "Flow rate: 42 GPM, Inlet pressure: 6 PSI, Outlet pressure: 55 PSI, rough sound",
        "expected_fault": "cavitation",
        "expected_keywords": ["cavitation", "inlet", "suction", "pressure"],
        "language": "en"
    },
    {
        "id": "pump_seal_01",
        "equipment": "pump",
        "input": "Flow rate: 65 GPM, Outlet pressure: 35 PSI, visible leak near shaft",
        "expected_fault": "seal_leak",
        "expected_keywords": ["seal", "leak", "replace"],
        "language": "en"
    },
    
    # Compressor scenarios
    {
        "id": "comp_oil_01",
        "equipment": "compressor",
        "input": "Oil pressure: 22 PSI, Temperature: 102°C, Discharge pressure: 130 PSI",
        "expected_fault": "low_oil",
        "expected_keywords": ["oil", "pressure", "bearing", "check level"],
        "language": "en"
    },
    
    # Edge cases
    {
        "id": "ambiguous_01",
        "equipment": "conveyor",
        "input": "Motor current: 5.8A, Belt speed: 70%",
        "expected_fault": "borderline",
        "expected_keywords": ["monitor", "watch", "slight"],
        "language": "en"
    }
]


def evaluate_response(response: str, case: Dict) -> Dict:
    """Evaluate a model response against expected output."""
    response_lower = response.lower()
    
    # Check for expected keywords
    keywords_found = []
    keywords_missing = []
    for kw in case["expected_keywords"]:
        if kw.lower() in response_lower:
            keywords_found.append(kw)
        else:
            keywords_missing.append(kw)
    
    keyword_score = len(keywords_found) / len(case["expected_keywords"]) if case["expected_keywords"] else 1.0
    
    # Check fault detection
    fault_detected = False
    if case["expected_fault"]:
        fault_keywords = {
            "belt_jam": ["jam", "obstruction", "atasco"],
            "bearing_failure": ["bearing", "vibration", "rodamiento"],
            "cavitation": ["cavitation", "cavitación", "vapor"],
            "seal_leak": ["seal", "leak", "sello", "fuga"],
            "low_oil": ["oil", "aceite", "lubric"],
            "borderline": ["monitor", "watch", "borderline"]
        }
        for kw in fault_keywords.get(case["expected_fault"], []):
            if kw in response_lower:
                fault_detected = True
                break
    else:
        # Expected normal - check for "normal" or absence of alarm words
        alarm_words = ["critical", "danger", "stop", "emergency", "fault", "failure"]
        fault_detected = not any(w in response_lower for w in alarm_words)
    
    # Check for actionable recommendations
    has_actions = any(phrase in response_lower for phrase in [
        "check", "inspect", "verify", "stop", "replace", "adjust",
        "verificar", "inspeccionar", "detener", "reemplazar"
    ])
    
    # Check for safety mentions
    has_safety = any(phrase in response_lower for phrase in [
        "lockout", "tagout", "safety", "caution",
        "bloqueo", "seguridad", "precaución"
    ])
    
    return {
        "case_id": case["id"],
        "keyword_score": keyword_score,
        "keywords_found": keywords_found,
        "keywords_missing": keywords_missing,
        "fault_detected_correctly": fault_detected,
        "has_actionable_steps": has_actions,
        "mentions_safety": has_safety,
        "passed": keyword_score >= 0.5 and fault_detected
    }


def run_benchmark(model_fn, verbose: bool = True) -> Dict:
    """
    Run benchmark against a model.
    
    Args:
        model_fn: Function that takes (prompt, context) and returns response
        verbose: Print detailed results
        
    Returns:
        Benchmark results dict
    """
    results = []
    
    for case in EVAL_CASES:
        prompt = f"Equipment: {case['equipment']}\nReadings: {case['input']}\n\nDiagnose this equipment and recommend actions."
        
        try:
            response = model_fn(prompt, case.get("language", "en"))
            eval_result = evaluate_response(response, case)
            eval_result["response"] = response[:200] + "..." if len(response) > 200 else response
            results.append(eval_result)
            
            if verbose:
                status = "✅" if eval_result["passed"] else "❌"
                print(f"{status} {case['id']}: keyword={eval_result['keyword_score']:.0%}, fault={'✓' if eval_result['fault_detected_correctly'] else '✗'}")
        
        except Exception as e:
            results.append({
                "case_id": case["id"],
                "error": str(e),
                "passed": False
            })
            if verbose:
                print(f"❌ {case['id']}: ERROR - {e}")
    
    # Calculate summary stats
    passed = sum(1 for r in results if r.get("passed", False))
    total = len(results)
    avg_keyword = sum(r.get("keyword_score", 0) for r in results) / total
    
    summary = {
        "total_cases": total,
        "passed": passed,
        "failed": total - passed,
        "pass_rate": passed / total,
        "avg_keyword_score": avg_keyword,
        "results": results
    }
    
    if verbose:
        print(f"\n📊 Summary: {passed}/{total} passed ({summary['pass_rate']:.0%})")
    
    return summary


def mock_model(prompt: str, language: str = "en") -> str:
    """Mock model for testing the benchmark itself."""
    # Simple rule-based responses for testing
    prompt_lower = prompt.lower()
    
    if "8.2a" in prompt_lower or "8.5a" in prompt_lower:
        if language == "es":
            return "Diagnóstico: Atasco de banda. Obstrucción detectada. Detener el transportador y verificar."
        return "Diagnosis: Belt jam detected. Obstruction causing high current. Stop conveyor and perform lockout/tagout. Check for debris."
    
    if "vibration" in prompt_lower and "4.5" in prompt_lower:
        return "Diagnosis: Possible bearing failure. High vibration and temperature. Inspect bearings and check lubrication. Plan replacement."
    
    if "42 gpm" in prompt_lower:
        return "Diagnosis: Pump cavitation. Low inlet pressure causing vapor bubbles. Check suction line and inlet valve."
    
    if "normal" in prompt_lower or ("4.5a" in prompt_lower and "82%" in prompt_lower):
        return "All systems operating normally. Readings within expected ranges."
    
    return "Unable to diagnose. Please provide more sensor data."


if __name__ == "__main__":
    print("ShopTalk Evaluation Benchmark")
    print("=" * 40)
    print("\nRunning with mock model...\n")
    
    results = run_benchmark(mock_model)
    
    # Save results
    output_path = Path(__file__).parent / "benchmark_results.json"
    with open(output_path, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\nResults saved to {output_path}")
