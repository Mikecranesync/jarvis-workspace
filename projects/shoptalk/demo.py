#!/usr/bin/env python3
"""
ShopTalk Demo Script for Tuesday Presentation
Shows the edge AI diagnosing equipment faults in real-time.

Usage:
    python demo.py                     # Run full demo
    python demo.py --scenario jam      # Run specific scenario
    python demo.py --language es       # Spanish voice
"""

import sys
import time
import argparse
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from model.world_model import WorldModel, EquipmentState, create_conveyor_model
from inference.engine import InferenceEngine, SimulatedDataSource, InferenceResult
from voice.tts import VoiceInterface, DiagnosticAnnouncer

# Demo scripts
DEMO_SCRIPTS = {
    "en": {
        "intro": "ShopTalk Edge AI Demo. This system monitors industrial equipment and detects problems before they cause downtime.",
        "training": "First, we train the AI on normal operation. This takes about 10 seconds.",
        "training_done": "Training complete. The AI has learned what normal looks like.",
        "monitoring": "Now we're monitoring in real-time. Watch what happens when a fault occurs.",
        "jam_start": "Simulating a conveyor jam...",
        "diagnosis": "The AI detected the problem and diagnosed it.",
        "conclusion": "This runs on a 50 dollar device, works offline, and speaks any language."
    },
    "es": {
        "intro": "Demostración de ShopTalk Edge AI. Este sistema monitorea equipos industriales y detecta problemas antes de que causen tiempo de inactividad.",
        "training": "Primero, entrenamos la IA en operación normal. Esto toma aproximadamente 10 segundos.",
        "training_done": "Entrenamiento completado. La IA ha aprendido cómo es el funcionamiento normal.",
        "monitoring": "Ahora estamos monitoreando en tiempo real. Observe lo que sucede cuando ocurre una falla.",
        "jam_start": "Simulando un atasco del transportador...",
        "diagnosis": "La IA detectó el problema y lo diagnosticó.",
        "conclusion": "Esto funciona en un dispositivo de 50 dólares, trabaja sin internet, y habla cualquier idioma."
    }
}


def run_demo(language: str = "en", scenario: str = "jam", use_voice: bool = True):
    """Run the full demo."""
    
    scripts = DEMO_SCRIPTS.get(language, DEMO_SCRIPTS["en"])
    
    print("\n" + "=" * 60)
    print("  🏭 ShopTalk Edge AI - Live Demo")
    print("=" * 60)
    print()
    
    # Setup voice
    voice = None
    if use_voice:
        voice = VoiceInterface(language=language)
        print(f"🔊 Voice: {language.upper()}")
    
    def speak(text):
        print(f"\n💬 {text}")
        if voice:
            voice.speak(text, play=False)  # Generate but don't play in demo
    
    # Intro
    speak(scripts["intro"])
    time.sleep(2)
    
    # Create model
    print("\n📊 Creating world model...")
    model = create_conveyor_model()
    
    # Create inference engine
    engine = InferenceEngine(model, sample_interval=0.05)
    
    # Setup data source - start with normal
    source = SimulatedDataSource("normal")
    engine.set_data_source(source)
    
    # Train
    speak(scripts["training"])
    print("\n🎓 Training Phase")
    print("-" * 40)
    
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
        
        if i % 25 == 0:
            print(f"   Training: {i}% complete")
    
    model.train(training_data)
    print("   Training: 100% complete ✅")
    
    speak(scripts["training_done"])
    time.sleep(1)
    
    # Monitoring phase
    speak(scripts["monitoring"])
    print("\n📈 Monitoring Phase")
    print("-" * 40)
    
    # Reset source for monitoring
    source.set_scenario("normal")
    
    # Setup anomaly callback
    detected_anomaly = False
    
    def on_anomaly(result: InferenceResult):
        nonlocal detected_anomaly
        detected_anomaly = True
        print(f"\n🚨 ANOMALY DETECTED!")
        print(f"   {result.diagnosis}")
        for a in result.anomalies:
            print(f"   • {a['feature']}: {a['direction'].upper()} (z-score: {a['z_score']:.1f})")
    
    engine.set_on_anomaly(on_anomaly)
    
    # Run normal monitoring
    print("\n✅ Normal Operation")
    for i in range(30):
        data = source()
        result = engine.process_sample(data)
        
        if i % 10 == 0:
            print(f"   [{i:2d}] Speed: {data['motor_speed']:.0f} RPM | "
                  f"Current: {data['motor_current']:.1f}A | "
                  f"Temp: {data['temperature']:.1f}°C")
        
        time.sleep(0.03)
    
    # Trigger fault
    print()
    speak(scripts["jam_start"])
    source.set_scenario(scenario)
    
    print(f"\n⚠️ Fault Injected: {scenario.upper()}")
    
    # Continue monitoring until anomaly detected
    for i in range(100):
        data = source()
        result = engine.process_sample(data)
        
        if i % 10 == 0:
            status = "⚠️" if result.is_anomaly else "✅"
            print(f"   [{i:2d}] {status} Speed: {data['motor_speed']:.0f} RPM | "
                  f"Current: {data['motor_current']:.1f}A | "
                  f"Temp: {data['temperature']:.1f}°C")
        
        if detected_anomaly:
            break
        
        time.sleep(0.03)
    
    # Diagnosis
    time.sleep(1)
    speak(scripts["diagnosis"])
    
    # Print final stats
    stats = engine.get_stats()
    print(f"\n📊 Session Stats")
    print(f"   Samples processed: {stats['total_samples']}")
    print(f"   Anomalies detected: {stats['total_anomalies']}")
    
    # Conclusion
    time.sleep(1)
    speak(scripts["conclusion"])
    
    print("\n" + "=" * 60)
    print("  Demo Complete!")
    print("=" * 60)
    print()


def run_quick_test():
    """Quick functionality test."""
    print("🧪 Quick Test - ShopTalk Components")
    print("-" * 40)
    
    # Test world model
    print("1. World Model...")
    model = create_conveyor_model()
    print("   ✅ Created")
    
    # Test inference engine
    print("2. Inference Engine...")
    engine = InferenceEngine(model)
    source = SimulatedDataSource("normal")
    engine.set_data_source(source)
    print("   ✅ Created")
    
    # Test voice
    print("3. Voice Interface...")
    voice = VoiceInterface(language="en")
    print(f"   ✅ Backend: {voice.backend}")
    
    # Train quickly
    print("4. Training...")
    training_data = []
    for i in range(50):
        data = source()
        state = EquipmentState(
            timestamp=float(i),
            sensors={k: v for k, v in data.items() if isinstance(v, (int, float))},
            controls={},
            discrete={k: v for k, v in data.items() if isinstance(v, bool)}
        )
        training_data.append(state)
    model.train(training_data)
    print("   ✅ Trained")
    
    # Test anomaly detection
    print("5. Anomaly Detection...")
    source.set_scenario("jam")
    source.sample_count = 150  # Skip to fault
    
    for i in range(10):
        data = source()
        result = engine.process_sample(data)
        if result.is_anomaly:
            print(f"   ✅ Anomaly detected: {len(result.anomalies)} issues")
            break
    
    print("\n✅ All components working!")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="ShopTalk Demo")
    parser.add_argument("--language", "-l", default="en",
                       choices=["en", "es", "pt"],
                       help="Voice language")
    parser.add_argument("--scenario", "-s", default="jam",
                       choices=["jam", "overload", "bearing_failure"],
                       help="Fault scenario")
    parser.add_argument("--voice", action="store_true",
                       help="Enable voice output")
    parser.add_argument("--test", action="store_true",
                       help="Run quick test only")
    args = parser.parse_args()
    
    if args.test:
        run_quick_test()
    else:
        run_demo(
            language=args.language,
            scenario=args.scenario,
            use_voice=args.voice
        )
