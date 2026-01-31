#!/usr/bin/env python3
"""
ShopTalk Edge AI - Main Entry Point
Industrial equipment diagnostics that run anywhere.

Usage:
    # Run with simulated data (demo mode)
    python main.py --simulate
    
    # Run with real PLC
    python main.py --host 192.168.1.100
    
    # Run API server
    python main.py --api --simulate
    
    # Spanish voice
    python main.py --simulate --language es
"""

import argparse
import asyncio
import time
import sys
from pathlib import Path

# Ensure src is in path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from model.world_model import WorldModel, EquipmentState, create_conveyor_model
from inference.engine import InferenceEngine, SimulatedDataSource, InferenceResult
from voice.tts import VoiceInterface, DiagnosticAnnouncer


def run_demo(args):
    """Run interactive demo."""
    print("=" * 50)
    print("  ShopTalk Edge AI - Demo Mode")
    print("=" * 50)
    print()
    
    # Create model
    print("📊 Creating world model...")
    model = create_conveyor_model()
    
    # Create inference engine
    engine = InferenceEngine(model, sample_interval=0.05)
    
    # Setup data source
    source = SimulatedDataSource(args.scenario)
    engine.set_data_source(source)
    print(f"📡 Data source: Simulation ({args.scenario})")
    
    # Setup voice
    voice = VoiceInterface(language=args.language)
    announcer = DiagnosticAnnouncer(voice, cooldown=10.0)
    print(f"🔊 Voice: {args.language}")
    
    # Train on initial data
    print("\n🎓 Training on normal operation...")
    training_data = []
    for i in range(100):
        data = source()
        state = EquipmentState(
            timestamp=float(i),
            sensors={k: v for k, v in data.items() if isinstance(v, (int, float))},
            controls={},
            discrete={k: v for k, v in data.items() if isinstance(v, bool)}
        )
        training_data.append(state)
    model.train(training_data)
    print("✅ Training complete!")
    
    # Reset scenario for demo
    source.set_scenario(args.scenario)
    
    # Setup callbacks
    def on_anomaly(result: InferenceResult):
        print(f"\n🚨 ANOMALY DETECTED!")
        print(f"   Diagnosis: {result.diagnosis}")
        for a in result.anomalies:
            print(f"   - {a['feature']}: {a['direction']} (z={a['z_score']:.2f})")
        
        # Announce
        if args.voice:
            announcer.announce(result.diagnosis, result.anomalies)
    
    engine.set_on_anomaly(on_anomaly)
    
    # Announce start
    if args.voice:
        start_msg = voice.get_template("check_complete") + " ready."
        voice.speak(start_msg)
    
    # Run monitoring
    print(f"\n📈 Starting monitoring (scenario: {args.scenario})...")
    print("-" * 50)
    
    try:
        for i in range(args.samples):
            data = source()
            result = engine.process_sample(data)
            
            if i % 20 == 0:
                status = "⚠️ ANOMALY" if result.is_anomaly else "✅ Normal"
                print(f"[{i:3d}] {status} | Speed: {data['motor_speed']:.0f} RPM | "
                      f"Current: {data['motor_current']:.1f}A | Temp: {data['temperature']:.1f}°C")
            
            time.sleep(args.interval)
            
    except KeyboardInterrupt:
        print("\n\nStopped by user")
    
    # Final stats
    stats = engine.get_stats()
    print("\n" + "=" * 50)
    print("📊 Summary")
    print(f"   Total samples: {stats['total_samples']}")
    print(f"   Anomalies: {stats['total_anomalies']}")
    print(f"   Anomaly rate: {stats['anomaly_rate']*100:.1f}%")
    
    # Save model
    model_path = Path(__file__).parent / "data" / "trained_model.json"
    model.save(str(model_path))
    print(f"\n💾 Model saved to {model_path}")


def run_api(args):
    """Run API server."""
    from api.server import main as api_main
    
    # Override sys.argv for API server
    sys.argv = [
        "server.py",
        "--host", args.api_host,
        "--port", str(args.api_port),
        "--language", args.language
    ]
    
    if args.simulate:
        sys.argv.append("--simulate")
        sys.argv.extend(["--scenario", args.scenario])
    else:
        sys.argv.extend(["--plc-host", args.host])
        sys.argv.extend(["--plc-port", str(args.port)])
    
    api_main()


def main():
    parser = argparse.ArgumentParser(
        description="ShopTalk Edge AI - Industrial Equipment Diagnostics",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py --simulate                    # Demo with normal operation
  python main.py --simulate --scenario jam     # Demo with conveyor jam
  python main.py --simulate --language es      # Demo with Spanish voice
  python main.py --api --simulate              # Run API server
  python main.py --host 192.168.1.100          # Connect to real PLC
        """
    )
    
    # Mode
    parser.add_argument("--api", action="store_true",
                       help="Run as API server")
    parser.add_argument("--simulate", action="store_true",
                       help="Use simulated data")
    
    # Data source
    parser.add_argument("--host", default="192.168.1.100",
                       help="PLC IP address")
    parser.add_argument("--port", type=int, default=502,
                       help="Modbus port")
    parser.add_argument("--scenario", default="normal",
                       choices=["normal", "jam", "overload", "bearing_failure"],
                       help="Simulation scenario")
    
    # Voice
    parser.add_argument("--language", "-l", default="en",
                       choices=["en", "es", "pt", "de", "fr"],
                       help="Voice language")
    parser.add_argument("--voice", action="store_true",
                       help="Enable voice announcements")
    
    # Demo settings
    parser.add_argument("--samples", type=int, default=200,
                       help="Number of samples to process")
    parser.add_argument("--interval", type=float, default=0.05,
                       help="Sample interval (seconds)")
    
    # API settings
    parser.add_argument("--api-host", default="0.0.0.0",
                       help="API server host")
    parser.add_argument("--api-port", type=int, default=8080,
                       help="API server port")
    
    args = parser.parse_args()
    
    if args.api:
        run_api(args)
    else:
        run_demo(args)


if __name__ == "__main__":
    main()
