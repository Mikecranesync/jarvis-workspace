#!/usr/bin/env python3
"""
Video Assembler for The Automaton
Combines terminal recordings, screenshots, and audio into final videos
"""

import subprocess
import os
import json
from pathlib import Path
from datetime import datetime
from typing import List, Optional

AUTOMATON_DIR = Path("/root/jarvis-workspace/projects/automaton")
QUEUE_DIR = AUTOMATON_DIR / "queue"
OUTPUT_DIR = AUTOMATON_DIR / "output"
ASSETS_DIR = AUTOMATON_DIR / "assets"

for d in [QUEUE_DIR, OUTPUT_DIR, ASSETS_DIR]:
    d.mkdir(parents=True, exist_ok=True)


class VideoAssembler:
    """Assemble video content from multiple sources."""
    
    def __init__(self, width: int = 1920, height: int = 1080, fps: int = 30):
        self.width = width
        self.height = height
        self.fps = fps
        
    def terminal_to_video(self, cast_file: str, output: str = None,
                          font_size: int = 20) -> str:
        """Convert asciinema recording to video.
        
        Args:
            cast_file: Path to .cast file
            output: Output video path
            font_size: Terminal font size
            
        Returns:
            Path to output video
        """
        if not output:
            output = cast_file.replace('.cast', '.mp4')
        
        # Use asciinema cat + ffmpeg for conversion
        # First, render to raw frames via agg or similar
        
        # Fallback: Create a video from terminal playback
        # This requires a virtual framebuffer on headless systems
        
        temp_dir = QUEUE_DIR / "temp_frames"
        temp_dir.mkdir(exist_ok=True)
        
        # For now, create a placeholder approach
        # Real implementation would use agg or similar
        
        print(f"Converting {cast_file} to video...")
        print("Note: Full terminal-to-video requires agg or VHS")
        
        # Create a simple title card as placeholder
        self._create_title_card(
            "Terminal Recording",
            str(temp_dir / "frame.png")
        )
        
        # Convert to video
        cmd = [
            "ffmpeg", "-y",
            "-loop", "1",
            "-i", str(temp_dir / "frame.png"),
            "-t", "5",
            "-vf", f"scale={self.width}:{self.height}",
            "-pix_fmt", "yuv420p",
            output
        ]
        
        subprocess.run(cmd, capture_output=True)
        return output
    
    def add_audio(self, video: str, audio: str, output: str = None) -> str:
        """Add audio track to video.
        
        Args:
            video: Input video path
            audio: Audio file path
            output: Output video path
            
        Returns:
            Path to output video
        """
        if not output:
            base = Path(video).stem
            output = str(OUTPUT_DIR / f"{base}_with_audio.mp4")
        
        cmd = [
            "ffmpeg", "-y",
            "-i", video,
            "-i", audio,
            "-c:v", "copy",
            "-c:a", "aac",
            "-map", "0:v:0",
            "-map", "1:a:0",
            "-shortest",
            output
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"Added audio: {output}")
            return output
        else:
            print(f"Error adding audio: {result.stderr}")
            return video
    
    def concat_videos(self, videos: List[str], output: str = None) -> str:
        """Concatenate multiple videos.
        
        Args:
            videos: List of video file paths
            output: Output video path
            
        Returns:
            Path to concatenated video
        """
        if not output:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output = str(OUTPUT_DIR / f"concat_{timestamp}.mp4")
        
        # Create concat file
        concat_file = QUEUE_DIR / "concat_list.txt"
        with open(concat_file, 'w') as f:
            for v in videos:
                f.write(f"file '{v}'\n")
        
        cmd = [
            "ffmpeg", "-y",
            "-f", "concat",
            "-safe", "0",
            "-i", str(concat_file),
            "-c", "copy",
            output
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"Concatenated: {output}")
            return output
        else:
            print(f"Error concatenating: {result.stderr}")
            return None
    
    def create_intro(self, title: str, subtitle: str = "",
                     duration: float = 3.0, output: str = None) -> str:
        """Create an intro title card video.
        
        Args:
            title: Main title text
            subtitle: Subtitle text
            duration: Duration in seconds
            output: Output path
            
        Returns:
            Path to intro video
        """
        if not output:
            output = str(ASSETS_DIR / "intro.mp4")
        
        # Create title card image
        title_image = QUEUE_DIR / "title_card.png"
        self._create_title_card(title, str(title_image), subtitle)
        
        # Convert to video
        cmd = [
            "ffmpeg", "-y",
            "-loop", "1",
            "-i", str(title_image),
            "-t", str(duration),
            "-vf", f"scale={self.width}:{self.height},format=yuv420p",
            "-r", str(self.fps),
            output
        ]
        
        subprocess.run(cmd, capture_output=True)
        return output
    
    def create_outro(self, text: str = "Thanks for watching",
                     cta: str = "Follow for more",
                     duration: float = 3.0, output: str = None) -> str:
        """Create an outro card video.
        
        Args:
            text: Main text
            cta: Call to action
            duration: Duration in seconds
            output: Output path
            
        Returns:
            Path to outro video
        """
        if not output:
            output = str(ASSETS_DIR / "outro.mp4")
        
        return self.create_intro(text, cta, duration, output)
    
    def _create_title_card(self, title: str, output: str, 
                           subtitle: str = "") -> bool:
        """Create a title card image using ImageMagick.
        
        Args:
            title: Main title
            output: Output image path
            subtitle: Optional subtitle
            
        Returns:
            True if successful
        """
        # Create with ImageMagick
        text = title
        if subtitle:
            text += f"\n{subtitle}"
        
        cmd = [
            "convert",
            "-size", f"{self.width}x{self.height}",
            "xc:#1a1a2e",  # Dark blue background
            "-font", "DejaVu-Sans-Bold",
            "-pointsize", "72",
            "-fill", "white",
            "-gravity", "center",
            "-annotate", "+0+0", text,
            output
        ]
        
        try:
            subprocess.run(cmd, capture_output=True, check=True)
            return True
        except:
            # Fallback: create blank image
            cmd_fallback = [
                "convert",
                "-size", f"{self.width}x{self.height}",
                "xc:#1a1a2e",
                output
            ]
            subprocess.run(cmd_fallback, capture_output=True)
            return False
    
    def assemble_demo(self, segments: List[dict], output: str = None) -> str:
        """Assemble a complete demo video from segments.
        
        Args:
            segments: List of segment configs:
                {"type": "intro|content|outro", "source": "path", ...}
            output: Final output path
            
        Returns:
            Path to final video
        """
        if not output:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output = str(OUTPUT_DIR / f"demo_{timestamp}.mp4")
        
        videos = []
        
        for seg in segments:
            seg_type = seg.get("type", "content")
            
            if seg_type == "intro":
                v = self.create_intro(
                    seg.get("title", "Demo"),
                    seg.get("subtitle", "")
                )
                videos.append(v)
                
            elif seg_type == "outro":
                v = self.create_outro(
                    seg.get("text", "Thanks for watching"),
                    seg.get("cta", "")
                )
                videos.append(v)
                
            elif seg_type == "content":
                source = seg.get("source")
                if source and os.path.exists(source):
                    videos.append(source)
        
        if videos:
            return self.concat_videos(videos, output)
        
        return None


if __name__ == "__main__":
    import sys
    
    assembler = VideoAssembler()
    
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        
        if cmd == "intro":
            title = sys.argv[2] if len(sys.argv) > 2 else "Demo Video"
            output = assembler.create_intro(title)
            print(f"Created: {output}")
            
        elif cmd == "outro":
            output = assembler.create_outro()
            print(f"Created: {output}")
            
        elif cmd == "concat":
            videos = sys.argv[2:]
            output = assembler.concat_videos(videos)
            print(f"Created: {output}")
            
        elif cmd == "add-audio":
            video = sys.argv[2]
            audio = sys.argv[3]
            output = assembler.add_audio(video, audio)
            print(f"Created: {output}")
    else:
        print("Video Assembler - The Automaton")
        print("")
        print("Usage:")
        print("  assembler.py intro [title]        - Create intro video")
        print("  assembler.py outro                - Create outro video")
        print("  assembler.py concat <v1> <v2> ... - Concatenate videos")
        print("  assembler.py add-audio <video> <audio> - Add audio track")
