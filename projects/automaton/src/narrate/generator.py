#!/usr/bin/env python3
"""
Narration Generator for The Automaton
Generates audio narration from scripts using TTS
"""

import subprocess
import os
import json
from pathlib import Path
from datetime import datetime
from typing import Optional

# Paths
AUTOMATON_DIR = Path("/root/jarvis-workspace/projects/automaton")
QUEUE_DIR = AUTOMATON_DIR / "queue"
OUTPUT_DIR = AUTOMATON_DIR / "output"
QUEUE_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


class NarrationGenerator:
    """Generate audio narration from text scripts."""
    
    def __init__(self, voice: str = "alloy", speed: float = 1.0):
        """Initialize generator.
        
        Args:
            voice: TTS voice to use
            speed: Speech speed multiplier
        """
        self.voice = voice
        self.speed = speed
        
    def generate(self, text: str, output_path: str = None) -> str:
        """Generate audio narration from text.
        
        Uses Clawdbot's TTS integration if available,
        falls back to edge-tts or espeak.
        
        Args:
            text: Script text to narrate
            output_path: Optional output file path
            
        Returns:
            Path to generated audio file
        """
        if not output_path:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = str(QUEUE_DIR / f"narration_{timestamp}.mp3")
        
        # Try different TTS methods in order of preference
        
        # Method 1: edge-tts (Microsoft Azure voices, free)
        if self._try_edge_tts(text, output_path):
            return output_path
            
        # Method 2: espeak (basic, always available)
        if self._try_espeak(text, output_path):
            return output_path
        
        # Method 3: Save as text for manual TTS
        text_path = output_path.replace('.mp3', '.txt')
        with open(text_path, 'w') as f:
            f.write(text)
        print(f"TTS unavailable. Script saved to: {text_path}")
        return text_path
    
    def _try_edge_tts(self, text: str, output_path: str) -> bool:
        """Try generating with edge-tts."""
        try:
            # Map simple voice names to edge-tts voices
            voice_map = {
                "alloy": "en-US-GuyNeural",
                "male": "en-US-GuyNeural", 
                "female": "en-US-JennyNeural",
                "british": "en-GB-RyanNeural",
                "spanish": "es-MX-JorgeNeural",
            }
            
            edge_voice = voice_map.get(self.voice, "en-US-GuyNeural")
            
            cmd = [
                "edge-tts",
                "--voice", edge_voice,
                "--text", text,
                "--write-media", output_path
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            
            if result.returncode == 0 and os.path.exists(output_path):
                print(f"Generated with edge-tts: {output_path}")
                return True
                
        except (FileNotFoundError, subprocess.TimeoutExpired):
            pass
            
        return False
    
    def _try_espeak(self, text: str, output_path: str) -> bool:
        """Try generating with espeak."""
        try:
            wav_path = output_path.replace('.mp3', '.wav')
            
            cmd = [
                "espeak",
                "-w", wav_path,
                "-s", str(int(150 * self.speed)),  # Words per minute
                text
            ]
            
            subprocess.run(cmd, capture_output=True, timeout=30)
            
            if os.path.exists(wav_path):
                # Convert to MP3 if ffmpeg available
                try:
                    ffmpeg_cmd = [
                        "ffmpeg", "-y",
                        "-i", wav_path,
                        "-acodec", "libmp3lame",
                        "-q:a", "2",
                        output_path
                    ]
                    subprocess.run(ffmpeg_cmd, capture_output=True, timeout=30)
                    os.remove(wav_path)
                    print(f"Generated with espeak: {output_path}")
                    return True
                except:
                    # Keep WAV if MP3 conversion fails
                    print(f"Generated with espeak: {wav_path}")
                    return True
                    
        except (FileNotFoundError, subprocess.TimeoutExpired):
            pass
            
        return False
    
    def generate_segments(self, segments: list, output_dir: str = None) -> list:
        """Generate audio for multiple script segments.
        
        Args:
            segments: List of {"name": str, "text": str} dicts
            output_dir: Directory for output files
            
        Returns:
            List of output file paths
        """
        if not output_dir:
            output_dir = str(QUEUE_DIR)
        
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        outputs = []
        for i, segment in enumerate(segments):
            name = segment.get("name", f"segment_{i:03d}")
            text = segment.get("text", "")
            
            if text.strip():
                output_path = str(output_dir / f"{name}.mp3")
                result = self.generate(text, output_path)
                outputs.append(result)
                
        return outputs


def install_edge_tts():
    """Install edge-tts if not present."""
    try:
        subprocess.run(["edge-tts", "--version"], capture_output=True)
        print("edge-tts already installed")
    except FileNotFoundError:
        print("Installing edge-tts...")
        subprocess.run(["pip3", "install", "edge-tts"], check=True)
        print("edge-tts installed successfully")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "install":
            install_edge_tts()
        elif sys.argv[1] == "test":
            generator = NarrationGenerator()
            text = "This is a test of the narration generator. Working perfectly."
            output = generator.generate(text)
            print(f"Test audio: {output}")
        else:
            # Generate from provided text
            text = " ".join(sys.argv[1:])
            generator = NarrationGenerator()
            output = generator.generate(text)
            print(f"Generated: {output}")
    else:
        print("Usage:")
        print("  generator.py install     - Install edge-tts")
        print("  generator.py test        - Generate test audio")
        print("  generator.py <text>      - Generate narration for text")
