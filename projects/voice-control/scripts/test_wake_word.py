#!/usr/bin/env python3
"""
Test wake word detection with Picovoice Porcupine.

Usage:
    export PICOVOICE_ACCESS_KEY="your-key"
    python test_wake_word.py

Say "Hey Jarvis" to test detection.
Press Ctrl+C to exit.
"""

import os
import sys
import struct

try:
    import pvporcupine
    import pyaudio
except ImportError as e:
    print(f"Missing dependency: {e}")
    print("\nInstall with:")
    print("  pip install pvporcupine pyaudio")
    sys.exit(1)


def main():
    access_key = os.environ.get("PICOVOICE_ACCESS_KEY")
    
    if not access_key:
        print("❌ PICOVOICE_ACCESS_KEY not set")
        print("\nGet a free key at: https://console.picovoice.ai/")
        print("Then run: export PICOVOICE_ACCESS_KEY='your-key'")
        sys.exit(1)
    
    print("🎤 Initializing wake word detector...")
    
    # Create Porcupine instance with built-in "jarvis" keyword
    porcupine = pvporcupine.create(
        access_key=access_key,
        keywords=["jarvis"],  # Built-in keyword
        sensitivities=[0.7]   # Adjust sensitivity (0-1)
    )
    
    # Set up audio stream
    pa = pyaudio.PyAudio()
    audio_stream = pa.open(
        rate=porcupine.sample_rate,
        channels=1,
        format=pyaudio.paInt16,
        input=True,
        frames_per_buffer=porcupine.frame_length
    )
    
    print(f"✅ Ready! Say 'Hey Jarvis' (or just 'Jarvis')")
    print(f"   Sample rate: {porcupine.sample_rate}Hz")
    print(f"   Frame length: {porcupine.frame_length}")
    print("\nPress Ctrl+C to exit\n")
    
    detections = 0
    
    try:
        while True:
            # Read audio frame
            pcm = audio_stream.read(porcupine.frame_length, exception_on_overflow=False)
            pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)
            
            # Check for wake word
            keyword_index = porcupine.process(pcm)
            
            if keyword_index >= 0:
                detections += 1
                print(f"🎯 [{detections}] Wake word detected! 'Jarvis' heard")
                
    except KeyboardInterrupt:
        print(f"\n\n👋 Exiting. Total detections: {detections}")
    finally:
        audio_stream.close()
        pa.terminate()
        porcupine.delete()


if __name__ == "__main__":
    main()
