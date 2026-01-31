#!/usr/bin/env python3
"""
ShopTalk Voice Interface
Multi-language text-to-speech for industrial diagnostics.
"""

import subprocess
import os
import asyncio
import logging
from pathlib import Path
from typing import Optional, Dict
from dataclasses import dataclass

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("VoiceTTS")

# Output directory
AUDIO_DIR = Path("/tmp/shoptalk_audio")
AUDIO_DIR.mkdir(exist_ok=True)


@dataclass
class VoiceConfig:
    """Voice configuration."""
    language: str = "en"
    voice_id: str = "default"
    speed: float = 1.0
    pitch: float = 1.0


# Language-specific voice mappings for edge-tts
EDGE_VOICES = {
    "en": "en-US-GuyNeural",
    "en-us": "en-US-GuyNeural",
    "en-gb": "en-GB-RyanNeural",
    "es": "es-MX-JorgeNeural",
    "es-mx": "es-MX-JorgeNeural",
    "es-es": "es-ES-AlvaroNeural",
    "pt": "pt-BR-AntonioNeural",
    "pt-br": "pt-BR-AntonioNeural",
    "de": "de-DE-ConradNeural",
    "fr": "fr-FR-HenriNeural",
    "zh": "zh-CN-YunxiNeural",
    "ja": "ja-JP-KeitaNeural",
}

# Diagnostic messages in multiple languages
DIAGNOSTIC_TEMPLATES = {
    "en": {
        "normal": "All systems operating normally.",
        "anomaly_detected": "Anomaly detected.",
        "high_current": "High motor current detected. Possible mechanical overload.",
        "high_temp": "Elevated temperature. Check cooling system.",
        "low_speed": "Motor speed below normal. Check belt tension.",
        "jam": "Conveyor jam detected. Clear obstruction and reset.",
        "check_bearings": "Unusual vibration detected. Inspect bearings.",
        "check_complete": "Equipment check complete. Status is",
    },
    "es": {
        "normal": "Todos los sistemas funcionando normalmente.",
        "anomaly_detected": "Anomalía detectada.",
        "high_current": "Corriente alta del motor detectada. Posible sobrecarga mecánica.",
        "high_temp": "Temperatura elevada. Verifique el sistema de enfriamiento.",
        "low_speed": "Velocidad del motor por debajo de lo normal. Verifique la tensión de la banda.",
        "jam": "Atasco del transportador detectado. Retire la obstrucción y reinicie.",
        "check_bearings": "Vibración inusual detectada. Inspeccione los rodamientos.",
        "check_complete": "Verificación del equipo completada. El estado es",
    },
    "pt": {
        "normal": "Todos os sistemas operando normalmente.",
        "anomaly_detected": "Anomalia detectada.",
        "high_current": "Alta corrente do motor detectada. Possível sobrecarga mecânica.",
        "high_temp": "Temperatura elevada. Verifique o sistema de resfriamento.",
        "low_speed": "Velocidade do motor abaixo do normal. Verifique a tensão da correia.",
        "jam": "Bloqueio do transportador detectado. Remova a obstrução e reinicie.",
        "check_bearings": "Vibração incomum detectada. Inspecione os rolamentos.",
        "check_complete": "Verificação do equipamento concluída. O status é",
    }
}


class VoiceInterface:
    """
    Text-to-speech interface for ShopTalk.
    Supports multiple languages and TTS backends.
    """
    
    def __init__(self, language: str = "en", backend: str = "auto"):
        """
        Initialize voice interface.
        
        Args:
            language: Language code (en, es, pt, de, fr, etc.)
            backend: TTS backend (edge-tts, espeak, piper, auto)
        """
        self.language = language.lower()
        self.backend = backend
        self.config = VoiceConfig(language=self.language)
        
        # Detect available backend
        if backend == "auto":
            self.backend = self._detect_backend()
            
        logger.info(f"Voice interface: {self.backend} / {self.language}")
    
    def _detect_backend(self) -> str:
        """Detect available TTS backend."""
        # Try edge-tts first (best quality)
        try:
            result = subprocess.run(["edge-tts", "--version"], 
                                   capture_output=True, timeout=5)
            if result.returncode == 0:
                return "edge-tts"
        except (subprocess.SubprocessError, FileNotFoundError, OSError):
            pass
        
        # Try piper (fast, good quality)
        try:
            result = subprocess.run(["piper", "--version"], 
                                   capture_output=True, timeout=5)
            if result.returncode == 0:
                return "piper"
        except (subprocess.SubprocessError, FileNotFoundError, OSError):
            pass
        
        # Fallback to espeak (always available on Linux)
        return "espeak"
    
    def speak(self, text: str, output_file: Optional[str] = None,
              play: bool = True) -> Optional[str]:
        """
        Convert text to speech.
        
        Args:
            text: Text to speak
            output_file: Optional output file path
            play: Whether to play the audio
            
        Returns:
            Path to audio file if output_file specified
        """
        if not output_file:
            output_file = str(AUDIO_DIR / f"speech_{os.getpid()}.mp3")
        
        success = False
        
        if self.backend == "edge-tts":
            success = self._speak_edge_tts(text, output_file)
        elif self.backend == "piper":
            success = self._speak_piper(text, output_file)
        else:
            success = self._speak_espeak(text, output_file)
        
        if success and play:
            self._play_audio(output_file)
        
        return output_file if success else None
    
    def _speak_edge_tts(self, text: str, output_file: str) -> bool:
        """Generate speech using edge-tts."""
        voice = EDGE_VOICES.get(self.language, "en-US-GuyNeural")
        
        try:
            cmd = [
                "edge-tts",
                "--voice", voice,
                "--text", text,
                "--write-media", output_file
            ]
            result = subprocess.run(cmd, capture_output=True, timeout=30)
            return result.returncode == 0 and os.path.exists(output_file)
        except Exception as e:
            logger.error(f"edge-tts error: {e}")
            return False
    
    def _speak_piper(self, text: str, output_file: str) -> bool:
        """Generate speech using piper."""
        # Piper model selection based on language
        model_map = {
            "en": "en_US-lessac-medium",
            "es": "es_ES-davefx-medium",
        }
        model = model_map.get(self.language, "en_US-lessac-medium")
        
        try:
            wav_file = output_file.replace('.mp3', '.wav')
            cmd = f'echo "{text}" | piper --model {model} --output_file {wav_file}'
            result = subprocess.run(cmd, shell=True, capture_output=True, timeout=30)
            
            if result.returncode == 0 and os.path.exists(wav_file):
                # Convert to MP3
                subprocess.run(["ffmpeg", "-y", "-i", wav_file, output_file],
                             capture_output=True)
                os.remove(wav_file)
                return os.path.exists(output_file)
            return False
        except Exception as e:
            logger.error(f"piper error: {e}")
            return False
    
    def _speak_espeak(self, text: str, output_file: str) -> bool:
        """Generate speech using espeak."""
        # espeak language codes
        lang_map = {
            "en": "en-us",
            "es": "es",
            "pt": "pt",
            "de": "de",
            "fr": "fr",
        }
        voice = lang_map.get(self.language, "en-us")
        
        try:
            wav_file = output_file.replace('.mp3', '.wav')
            cmd = ["espeak", "-v", voice, "-w", wav_file, text]
            result = subprocess.run(cmd, capture_output=True, timeout=30)
            
            if result.returncode == 0 and os.path.exists(wav_file):
                # Convert to MP3 if ffmpeg available
                try:
                    subprocess.run(["ffmpeg", "-y", "-i", wav_file, output_file],
                                 capture_output=True, timeout=10)
                    os.remove(wav_file)
                    return os.path.exists(output_file)
                except (subprocess.SubprocessError, FileNotFoundError, OSError):
                    # Keep WAV if MP3 conversion fails
                    return True
            return False
        except Exception as e:
            logger.error(f"espeak error: {e}")
            return False
    
    def _play_audio(self, file_path: str):
        """Play audio file."""
        players = ["mpv", "ffplay", "aplay", "paplay"]
        
        for player in players:
            try:
                if player == "ffplay":
                    cmd = [player, "-nodisp", "-autoexit", file_path]
                elif player == "mpv":
                    cmd = [player, "--no-video", file_path]
                else:
                    cmd = [player, file_path]
                
                subprocess.run(cmd, capture_output=True, timeout=60)
                return
            except:
                continue
        
        logger.warning("No audio player available")
    
    def announce_diagnosis(self, diagnosis: str, severity: str = "normal"):
        """
        Announce a diagnosis with appropriate framing.
        
        Args:
            diagnosis: Diagnosis message
            severity: Severity level (normal, warning, critical)
        """
        templates = DIAGNOSTIC_TEMPLATES.get(self.language, DIAGNOSTIC_TEMPLATES["en"])
        
        if severity == "critical":
            prefix = templates.get("anomaly_detected", "Anomaly detected.")
            message = f"{prefix} {diagnosis}"
        elif severity == "warning":
            message = diagnosis
        else:
            message = templates.get("normal", diagnosis)
        
        self.speak(message)
    
    def get_template(self, key: str) -> str:
        """Get a localized template string."""
        templates = DIAGNOSTIC_TEMPLATES.get(self.language, DIAGNOSTIC_TEMPLATES["en"])
        return templates.get(key, key)
    
    def set_language(self, language: str):
        """Change language."""
        self.language = language.lower()
        self.config.language = self.language
        logger.info(f"Language changed to: {self.language}")


class DiagnosticAnnouncer:
    """
    High-level diagnostic announcer that integrates with the inference engine.
    """
    
    def __init__(self, voice: VoiceInterface, cooldown: float = 30.0):
        """
        Initialize announcer.
        
        Args:
            voice: VoiceInterface instance
            cooldown: Minimum seconds between announcements
        """
        self.voice = voice
        self.cooldown = cooldown
        self.last_announcement = 0
        
    def should_announce(self) -> bool:
        """Check if enough time has passed for new announcement."""
        import time
        return time.time() - self.last_announcement > self.cooldown
    
    def announce(self, diagnosis: str, anomalies: list):
        """
        Announce diagnosis if appropriate.
        
        Args:
            diagnosis: Diagnosis string
            anomalies: List of anomaly dicts
        """
        import time
        
        if not self.should_announce():
            return
        
        # Determine severity
        high_severity = any(a.get("severity") == "high" for a in anomalies)
        severity = "critical" if high_severity else "warning" if anomalies else "normal"
        
        self.voice.announce_diagnosis(diagnosis, severity)
        self.last_announcement = time.time()
    
    def announce_status(self, status: str):
        """Announce a status message."""
        self.voice.speak(status)


async def demo_multilingual():
    """Demo of multilingual capabilities."""
    print("ShopTalk Voice Demo - Multilingual")
    print("=" * 40)
    
    for lang in ["en", "es", "pt"]:
        print(f"\n🔊 Language: {lang}")
        voice = VoiceInterface(language=lang)
        
        # Get localized message
        normal = voice.get_template("normal")
        anomaly = voice.get_template("high_current")
        
        print(f"   Normal: {normal}")
        print(f"   Anomaly: {anomaly}")
        
        # Generate audio (don't play in demo)
        voice.speak(normal, play=False)


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--lang", default="en", help="Language code")
    parser.add_argument("--text", default="All systems operating normally.", help="Text to speak")
    parser.add_argument("--demo", action="store_true", help="Run multilingual demo")
    args = parser.parse_args()
    
    if args.demo:
        asyncio.run(demo_multilingual())
    else:
        voice = VoiceInterface(language=args.lang)
        voice.speak(args.text)
