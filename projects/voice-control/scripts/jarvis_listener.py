#!/usr/bin/env python3
"""
Jarvis Voice Listener

Main script that:
1. Listens for "Hey Jarvis" wake word (Porcupine)
2. Records speech after wake word
3. Transcribes via Deepgram
4. Sends to Jarvis via webhook/Telegram
5. Plays audio response

Usage:
    python jarvis_listener.py [--offline] [--debug]

Environment Variables:
    PICOVOICE_ACCESS_KEY  - Picovoice API key
    DEEPGRAM_API_KEY      - Deepgram API key  
    JARVIS_WEBHOOK_URL    - Webhook URL for transcribed text
    TELEGRAM_BOT_TOKEN    - (optional) Direct Telegram bot token
    TELEGRAM_CHAT_ID      - (optional) Your Telegram chat ID
"""

import os
import sys
import time
import wave
import struct
import logging
import argparse
import tempfile
import threading
from pathlib import Path
from typing import Optional, Callable

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger(__name__)

# Optional imports with graceful degradation
try:
    import pvporcupine
    PORCUPINE_AVAILABLE = True
except ImportError:
    PORCUPINE_AVAILABLE = False
    logger.warning("pvporcupine not installed. Wake word detection disabled.")

try:
    import pyaudio
    PYAUDIO_AVAILABLE = True
except ImportError:
    PYAUDIO_AVAILABLE = False
    logger.warning("pyaudio not installed. Audio capture disabled.")

try:
    from deepgram import Deepgram
    DEEPGRAM_AVAILABLE = True
except ImportError:
    try:
        from deepgram import DeepgramClient
        DEEPGRAM_AVAILABLE = True
    except ImportError:
        DEEPGRAM_AVAILABLE = False
        logger.warning("deepgram-sdk not installed. Cloud STT disabled.")

try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False
    logger.warning("requests not installed. Webhook disabled.")


class WakeWordDetector:
    """Picovoice Porcupine wake word detection."""
    
    def __init__(self, access_key: str, keywords: list = None, sensitivities: list = None):
        if not PORCUPINE_AVAILABLE:
            raise RuntimeError("pvporcupine not installed")
        
        self.access_key = access_key
        # Use built-in "jarvis" keyword or custom ppn file
        self.keywords = keywords or ["jarvis"]
        self.sensitivities = sensitivities or [0.7]
        self.porcupine = None
        
    def start(self):
        """Initialize Porcupine engine."""
        self.porcupine = pvporcupine.create(
            access_key=self.access_key,
            keywords=self.keywords,
            sensitivities=self.sensitivities
        )
        logger.info(f"Wake word detector started. Keywords: {self.keywords}")
        return self.porcupine.frame_length, self.porcupine.sample_rate
    
    def process(self, audio_frame) -> int:
        """Process audio frame. Returns keyword index if detected, -1 otherwise."""
        if self.porcupine is None:
            return -1
        return self.porcupine.process(audio_frame)
    
    def stop(self):
        """Clean up Porcupine engine."""
        if self.porcupine:
            self.porcupine.delete()
            self.porcupine = None


class AudioCapture:
    """PyAudio-based audio capture."""
    
    def __init__(self, sample_rate: int = 16000, frame_length: int = 512):
        if not PYAUDIO_AVAILABLE:
            raise RuntimeError("pyaudio not installed")
        
        self.sample_rate = sample_rate
        self.frame_length = frame_length
        self.pa = None
        self.stream = None
        
    def start(self):
        """Start audio stream."""
        self.pa = pyaudio.PyAudio()
        self.stream = self.pa.open(
            rate=self.sample_rate,
            channels=1,
            format=pyaudio.paInt16,
            input=True,
            frames_per_buffer=self.frame_length
        )
        logger.info(f"Audio capture started. Rate: {self.sample_rate}Hz")
        
    def read(self):
        """Read one frame of audio."""
        pcm = self.stream.read(self.frame_length, exception_on_overflow=False)
        return struct.unpack_from("h" * self.frame_length, pcm)
    
    def read_raw(self, num_frames: int = 1):
        """Read raw bytes."""
        return self.stream.read(num_frames * self.frame_length, exception_on_overflow=False)
    
    def stop(self):
        """Stop audio stream."""
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
        if self.pa:
            self.pa.terminate()


class SpeechRecorder:
    """Records speech after wake word detection."""
    
    def __init__(self, audio_capture: AudioCapture, 
                 max_duration: float = 10.0,
                 silence_threshold: int = 500,
                 silence_duration: float = 1.5):
        self.audio = audio_capture
        self.max_duration = max_duration
        self.silence_threshold = silence_threshold
        self.silence_duration = silence_duration
        
    def record(self) -> bytes:
        """Record speech until silence or max duration."""
        logger.info("🎤 Listening... (speak now)")
        
        frames = []
        silence_frames = 0
        silence_limit = int(self.silence_duration * self.audio.sample_rate / self.audio.frame_length)
        max_frames = int(self.max_duration * self.audio.sample_rate / self.audio.frame_length)
        
        for _ in range(max_frames):
            frame = self.audio.read()
            frames.append(struct.pack("h" * len(frame), *frame))
            
            # Check for silence (simple RMS threshold)
            rms = sum(abs(s) for s in frame) / len(frame)
            if rms < self.silence_threshold:
                silence_frames += 1
                if silence_frames >= silence_limit:
                    logger.info("🔇 Silence detected, stopping recording")
                    break
            else:
                silence_frames = 0
        
        audio_data = b''.join(frames)
        duration = len(audio_data) / (2 * self.audio.sample_rate)  # 2 bytes per sample
        logger.info(f"📼 Recorded {duration:.1f}s of audio")
        
        return audio_data
    
    def save_wav(self, audio_data: bytes, filepath: str):
        """Save audio data to WAV file."""
        with wave.open(filepath, 'wb') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(self.audio.sample_rate)
            wf.writeframes(audio_data)


class DeepgramTranscriber:
    """Deepgram speech-to-text."""
    
    def __init__(self, api_key: str):
        if not DEEPGRAM_AVAILABLE:
            raise RuntimeError("deepgram-sdk not installed")
        
        self.api_key = api_key
        
    async def transcribe_async(self, audio_data: bytes) -> str:
        """Transcribe audio using Deepgram (async)."""
        try:
            from deepgram import DeepgramClient, PrerecordedOptions
            
            client = DeepgramClient(self.api_key)
            options = PrerecordedOptions(
                model="nova-2",
                language="en",
                smart_format=True,
                punctuate=True
            )
            
            response = await client.listen.prerecorded.v("1").transcribe_file(
                {"buffer": audio_data, "mimetype": "audio/wav"},
                options
            )
            
            transcript = response.results.channels[0].alternatives[0].transcript
            return transcript
            
        except Exception as e:
            logger.error(f"Deepgram error: {e}")
            return ""
    
    def transcribe(self, audio_data: bytes) -> str:
        """Transcribe audio using Deepgram (sync wrapper)."""
        import asyncio
        return asyncio.run(self.transcribe_async(audio_data))


class JarvisWebhook:
    """Send transcribed text to Jarvis webhook."""
    
    def __init__(self, webhook_url: str = None, 
                 telegram_token: str = None,
                 telegram_chat_id: str = None):
        self.webhook_url = webhook_url
        self.telegram_token = telegram_token
        self.telegram_chat_id = telegram_chat_id
        
    def send(self, text: str, metadata: dict = None) -> bool:
        """Send text to Jarvis."""
        if not text.strip():
            logger.warning("Empty text, not sending")
            return False
        
        # Try webhook first
        if self.webhook_url:
            return self._send_webhook(text, metadata)
        
        # Fall back to Telegram
        if self.telegram_token and self.telegram_chat_id:
            return self._send_telegram(text)
        
        logger.error("No webhook or Telegram configured")
        return False
    
    def _send_webhook(self, text: str, metadata: dict = None) -> bool:
        """Send to n8n/custom webhook."""
        try:
            payload = {
                "text": text,
                "source": "voice",
                "timestamp": time.time(),
                **(metadata or {})
            }
            response = requests.post(self.webhook_url, json=payload, timeout=10)
            response.raise_for_status()
            logger.info(f"✅ Sent to webhook: {text[:50]}...")
            return True
        except Exception as e:
            logger.error(f"Webhook error: {e}")
            return False
    
    def _send_telegram(self, text: str) -> bool:
        """Send directly to Telegram bot."""
        try:
            url = f"https://api.telegram.org/bot{self.telegram_token}/sendMessage"
            payload = {
                "chat_id": self.telegram_chat_id,
                "text": f"🎤 Voice: {text}"
            }
            response = requests.post(url, json=payload, timeout=10)
            response.raise_for_status()
            logger.info(f"✅ Sent to Telegram: {text[:50]}...")
            return True
        except Exception as e:
            logger.error(f"Telegram error: {e}")
            return False


class JarvisVoiceListener:
    """Main voice listener that orchestrates all components."""
    
    def __init__(self, 
                 picovoice_key: str,
                 deepgram_key: str = None,
                 webhook_url: str = None,
                 telegram_token: str = None,
                 telegram_chat_id: str = None,
                 offline_mode: bool = False):
        
        self.wake_detector = WakeWordDetector(picovoice_key)
        self.audio = None
        self.recorder = None
        self.transcriber = None
        self.webhook = None
        self.offline_mode = offline_mode
        self.running = False
        
        # Set up transcriber
        if not offline_mode and deepgram_key:
            self.transcriber = DeepgramTranscriber(deepgram_key)
        
        # Set up webhook
        self.webhook = JarvisWebhook(
            webhook_url=webhook_url,
            telegram_token=telegram_token,
            telegram_chat_id=telegram_chat_id
        )
    
    def start(self):
        """Start the voice listener."""
        logger.info("🚀 Starting Jarvis Voice Listener...")
        
        # Initialize wake word detector
        frame_length, sample_rate = self.wake_detector.start()
        
        # Initialize audio capture
        self.audio = AudioCapture(sample_rate=sample_rate, frame_length=frame_length)
        self.audio.start()
        
        # Initialize speech recorder
        self.recorder = SpeechRecorder(self.audio)
        
        self.running = True
        logger.info("✅ Ready! Say 'Hey Jarvis' to activate...")
        
    def run(self):
        """Main loop - listen for wake word and process commands."""
        try:
            while self.running:
                # Read audio frame
                frame = self.audio.read()
                
                # Check for wake word
                keyword_index = self.wake_detector.process(frame)
                
                if keyword_index >= 0:
                    logger.info("🎯 Wake word detected!")
                    self._handle_command()
                    
        except KeyboardInterrupt:
            logger.info("\n👋 Interrupted by user")
        finally:
            self.stop()
    
    def _handle_command(self):
        """Handle a voice command after wake word detection."""
        # Record speech
        audio_data = self.recorder.record()
        
        if len(audio_data) < 1000:
            logger.warning("Recording too short, ignoring")
            return
        
        # Save to temp file for transcription
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
            self.recorder.save_wav(audio_data, f.name)
            temp_path = f.name
        
        try:
            # Transcribe
            if self.transcriber:
                # Read WAV file for Deepgram
                with open(temp_path, 'rb') as f:
                    wav_data = f.read()
                
                text = self.transcriber.transcribe(wav_data)
                logger.info(f"📝 Transcription: {text}")
                
                if text.strip():
                    # Send to Jarvis
                    self.webhook.send(text)
            else:
                logger.warning("No transcriber configured (offline mode)")
                # In offline mode, could use local Whisper here
                
        finally:
            # Clean up temp file
            Path(temp_path).unlink(missing_ok=True)
        
        logger.info("✅ Ready for next command...")
    
    def stop(self):
        """Stop the voice listener."""
        self.running = False
        self.wake_detector.stop()
        if self.audio:
            self.audio.stop()
        logger.info("🛑 Jarvis Voice Listener stopped")


def main():
    parser = argparse.ArgumentParser(description="Jarvis Voice Listener")
    parser.add_argument("--offline", action="store_true", help="Offline mode (no cloud STT)")
    parser.add_argument("--debug", action="store_true", help="Enable debug logging")
    args = parser.parse_args()
    
    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Get configuration from environment
    picovoice_key = os.environ.get("PICOVOICE_ACCESS_KEY")
    deepgram_key = os.environ.get("DEEPGRAM_API_KEY")
    webhook_url = os.environ.get("JARVIS_WEBHOOK_URL")
    telegram_token = os.environ.get("TELEGRAM_BOT_TOKEN")
    telegram_chat_id = os.environ.get("TELEGRAM_CHAT_ID")
    
    if not picovoice_key:
        logger.error("PICOVOICE_ACCESS_KEY not set")
        logger.info("Get a free key at: https://console.picovoice.ai/")
        sys.exit(1)
    
    if not args.offline and not deepgram_key:
        logger.warning("DEEPGRAM_API_KEY not set - transcription will be disabled")
        logger.info("Get $200 free credit at: https://deepgram.com/")
    
    if not webhook_url and not (telegram_token and telegram_chat_id):
        logger.warning("No webhook or Telegram configured - commands will be logged only")
    
    # Create and run listener
    listener = JarvisVoiceListener(
        picovoice_key=picovoice_key,
        deepgram_key=deepgram_key,
        webhook_url=webhook_url,
        telegram_token=telegram_token,
        telegram_chat_id=telegram_chat_id,
        offline_mode=args.offline
    )
    
    listener.start()
    listener.run()


if __name__ == "__main__":
    main()
