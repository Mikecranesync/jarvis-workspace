#!/usr/bin/env python3
"""
Test Deepgram speech-to-text.

Usage:
    export DEEPGRAM_API_KEY="your-key"
    python test_deepgram.py

Records 5 seconds of audio and transcribes it.
"""

import os
import sys
import wave
import struct
import asyncio
import tempfile

try:
    import pyaudio
except ImportError:
    print("Missing pyaudio. Install with: pip install pyaudio")
    sys.exit(1)

try:
    from deepgram import DeepgramClient, PrerecordedOptions, FileSource
except ImportError:
    print("Missing deepgram-sdk. Install with: pip install deepgram-sdk")
    sys.exit(1)


def record_audio(duration: float = 5.0, sample_rate: int = 16000) -> bytes:
    """Record audio from microphone."""
    print(f"🎤 Recording for {duration} seconds... Speak now!")
    
    pa = pyaudio.PyAudio()
    stream = pa.open(
        rate=sample_rate,
        channels=1,
        format=pyaudio.paInt16,
        input=True,
        frames_per_buffer=1024
    )
    
    frames = []
    for _ in range(int(sample_rate * duration / 1024)):
        data = stream.read(1024, exception_on_overflow=False)
        frames.append(data)
    
    stream.stop_stream()
    stream.close()
    pa.terminate()
    
    print("✅ Recording complete!")
    return b''.join(frames)


def save_wav(audio_data: bytes, filepath: str, sample_rate: int = 16000):
    """Save audio to WAV file."""
    with wave.open(filepath, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(audio_data)


async def transcribe(filepath: str, api_key: str) -> str:
    """Transcribe audio file using Deepgram."""
    print("📝 Transcribing with Deepgram...")
    
    client = DeepgramClient(api_key)
    
    with open(filepath, 'rb') as f:
        buffer_data = f.read()
    
    payload: FileSource = {
        "buffer": buffer_data,
    }
    
    options = PrerecordedOptions(
        model="nova-2",
        language="en",
        smart_format=True,
        punctuate=True,
    )
    
    response = await client.listen.asyncrest.v("1").transcribe_file(payload, options)
    
    transcript = response.results.channels[0].alternatives[0].transcript
    confidence = response.results.channels[0].alternatives[0].confidence
    
    return transcript, confidence


async def main():
    api_key = os.environ.get("DEEPGRAM_API_KEY")
    
    if not api_key:
        print("❌ DEEPGRAM_API_KEY not set")
        print("\nGet $200 free credit at: https://deepgram.com/")
        print("Then run: export DEEPGRAM_API_KEY='your-key'")
        sys.exit(1)
    
    print("🚀 Deepgram STT Test")
    print("=" * 40)
    
    # Record audio
    audio_data = record_audio(duration=5.0)
    
    # Save to temp file
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
        save_wav(audio_data, f.name)
        temp_path = f.name
    
    try:
        # Transcribe
        transcript, confidence = await transcribe(temp_path, api_key)
        
        print("\n" + "=" * 40)
        print("📝 TRANSCRIPTION:")
        print(f"   {transcript}")
        print(f"\n   Confidence: {confidence:.1%}")
        print("=" * 40)
        
        if not transcript.strip():
            print("\n⚠️  Empty transcription. Make sure you spoke clearly.")
        else:
            print("\n✅ Deepgram is working!")
            
    finally:
        os.unlink(temp_path)


if __name__ == "__main__":
    asyncio.run(main())
