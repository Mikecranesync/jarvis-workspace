#!/usr/bin/env python3
"""
ShopTalk CLI - Interactive command-line interface for testing.
"""

import argparse
import json
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

def cmd_status(args):
    """Show current sensor status."""
    from src.inference.engine import InferenceEngine, SimulatedDataSource
    
    source = SimulatedDataSource(args.scenario)
    engine = InferenceEngine(source)
    
    status = engine.get_stats()
    
    print("\n📊 ShopTalk Status")
    print("=" * 40)
    print(f"Equipment: Conveyor System")
    print(f"Scenario: {args.scenario}")
    print(f"\nStats:")
    for key, value in status.items():
        if isinstance(value, float):
            print(f"  • {key}: {value:.2f}")
        else:
            print(f"  • {key}: {value}")
    
    # Get current readings from source
    readings = source()
    print(f"\nCurrent Readings:")
    for key, value in readings.items():
        if isinstance(value, (int, float)):
            print(f"  • {key}: {value:.2f}")


def cmd_diagnose(args):
    """Run diagnosis on current or simulated readings."""
    from src.model.world_model import WorldModel, EquipmentState, create_conveyor_model
    
    model = create_conveyor_model()
    
    # Parse readings from args or use defaults
    if args.readings:
        readings = json.loads(args.readings)
    else:
        # Simulate fault readings
        scenarios = {
            "jam": {"motor_current": 9.0, "motor_speed": 400, "conveyor_speed": 15, "temperature": 58},
            "overload": {"motor_current": 7.5, "motor_speed": 1350, "conveyor_speed": 65, "temperature": 68},
            "bearing": {"motor_current": 5.0, "motor_speed": 1450, "conveyor_speed": 75, "temperature": 72},
            "normal": {"motor_current": 4.5, "motor_speed": 1500, "conveyor_speed": 80, "temperature": 48}
        }
        readings = scenarios.get(args.scenario, scenarios["normal"])
    
    state = EquipmentState(
        timestamp=0,
        sensors=readings,
        controls={},
        discrete={}
    )
    
    # Update model with state (returns analysis)
    result = model.update(state)
    anomalies = result.get('anomalies', [])
    diagnosis = model.diagnose(anomalies)
    
    print("\n🔧 ShopTalk Diagnosis")
    print("=" * 40)
    print(f"Scenario: {args.scenario}")
    print(f"\nReadings:")
    for k, v in readings.items():
        print(f"  • {k}: {v}")
    
    print(f"\n📋 Diagnosis:")
    print(f"  {diagnosis}")
    
    if anomalies:
        print(f"\n⚠️  Anomalies Detected:")
        for a in anomalies:
            print(f"  • {a['feature']}: {a['deviation']:.1f}σ deviation ({a['severity']})")


def cmd_ask(args):
    """Ask a question (requires Ollama)."""
    try:
        from llm.serve.ollama_serve import OllamaShopTalk
        
        client = OllamaShopTalk(model=args.model)
        
        print(f"\n💬 Question: {args.question}")
        print("-" * 40)
        
        response = client.ask(args.question, language=args.lang)
        print(response)
        
    except Exception as e:
        print(f"Error: {e}")
        print("\nMake sure Ollama is running: ollama serve")


def cmd_train_info(args):
    """Show training data statistics."""
    data_dir = Path(__file__).parent / "llm" / "data"
    
    print("\n📚 Training Data Statistics")
    print("=" * 40)
    
    total = 0
    for json_file in sorted(data_dir.glob("*.json")):
        if "benchmark" in json_file.name or "knowledge" in json_file.name:
            continue
        try:
            with open(json_file) as f:
                data = json.load(f)
            if isinstance(data, list):
                count = len(data)
                total += count
                print(f"  {json_file.name}: {count:,} samples")
        except:
            pass
    
    print(f"\n  Total: {total:,} samples")
    
    # Check merged
    merged_dir = data_dir / "merged"
    if merged_dir.exists():
        print(f"\n📦 Merged Datasets:")
        for f in merged_dir.glob("*.json"):
            with open(f) as fp:
                data = json.load(fp)
            print(f"  {f.name}: {len(data):,} samples")


def cmd_demo(args):
    """Run interactive demo."""
    print("\n🔧 ShopTalk Interactive Demo")
    print("=" * 40)
    print("Commands: status, diagnose, ask <question>, quit")
    print("Scenarios: normal, jam, overload, bearing")
    print()
    
    scenario = "normal"
    
    while True:
        try:
            cmd = input(f"[{scenario}] > ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break
        
        if not cmd:
            continue
        
        parts = cmd.split(maxsplit=1)
        action = parts[0].lower()
        
        if action in ("quit", "exit", "q"):
            print("Goodbye!")
            break
        elif action == "status":
            args.scenario = scenario
            cmd_status(args)
        elif action == "diagnose":
            args.scenario = scenario
            args.readings = None
            cmd_diagnose(args)
        elif action in ("normal", "jam", "overload", "bearing"):
            scenario = action
            print(f"Scenario set to: {scenario}")
        elif action == "ask" and len(parts) > 1:
            args.question = parts[1]
            args.model = "qwen2:1.5b"
            args.lang = "en"
            cmd_ask(args)
        else:
            print("Unknown command. Try: status, diagnose, ask <question>, or scenario name")


def main():
    parser = argparse.ArgumentParser(
        description="ShopTalk CLI - Industrial AI Assistant",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  shoptalk status --scenario jam
  shoptalk diagnose --scenario overload
  shoptalk ask "What causes high motor current?"
  shoptalk demo
  shoptalk train-info
        """
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    # Status command
    status_parser = subparsers.add_parser("status", help="Show sensor status")
    status_parser.add_argument("--scenario", default="normal", 
                               choices=["normal", "jam", "overload", "bearing_failure"])
    
    # Diagnose command
    diag_parser = subparsers.add_parser("diagnose", help="Run diagnosis")
    diag_parser.add_argument("--scenario", default="normal",
                            choices=["normal", "jam", "overload", "bearing"])
    diag_parser.add_argument("--readings", help="JSON readings (optional)")
    
    # Ask command
    ask_parser = subparsers.add_parser("ask", help="Ask a question")
    ask_parser.add_argument("question", help="Question to ask")
    ask_parser.add_argument("--model", default="qwen2:1.5b", help="Ollama model")
    ask_parser.add_argument("--lang", default="en", choices=["en", "es"])
    
    # Train info
    subparsers.add_parser("train-info", help="Show training data stats")
    
    # Demo
    subparsers.add_parser("demo", help="Interactive demo mode")
    
    args = parser.parse_args()
    
    if args.command == "status":
        cmd_status(args)
    elif args.command == "diagnose":
        cmd_diagnose(args)
    elif args.command == "ask":
        cmd_ask(args)
    elif args.command == "train-info":
        cmd_train_info(args)
    elif args.command == "demo":
        cmd_demo(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
