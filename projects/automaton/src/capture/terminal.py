#!/usr/bin/env python3
"""
Terminal Capture Module for The Automaton
Captures terminal sessions using asciinema and converts to video
"""

import subprocess
import os
import json
from datetime import datetime
from pathlib import Path

CAPTURE_DIR = Path("/root/jarvis-workspace/projects/automaton/queue")
CAPTURE_DIR.mkdir(parents=True, exist_ok=True)


def start_recording(name: str = None) -> str:
    """Start a new terminal recording session.
    
    Args:
        name: Optional name for the recording
        
    Returns:
        Path to the recording file
    """
    if not name:
        name = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    filename = CAPTURE_DIR / f"terminal_{name}.cast"
    
    # Start asciinema recording
    cmd = [
        "asciinema", "rec",
        "--stdin",  # Record stdin
        "--overwrite",
        str(filename)
    ]
    
    print(f"Starting recording: {filename}")
    print("Run your commands, then type 'exit' to stop recording")
    
    subprocess.run(cmd)
    
    return str(filename)


def record_command(command: str, name: str = None) -> str:
    """Record a single command execution.
    
    Args:
        command: Command to execute and record
        name: Optional name for the recording
        
    Returns:
        Path to the recording file
    """
    if not name:
        name = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    filename = CAPTURE_DIR / f"terminal_{name}.cast"
    
    # Use asciinema rec with command
    cmd = [
        "asciinema", "rec",
        "--command", command,
        "--overwrite",
        str(filename)
    ]
    
    print(f"Recording command: {command}")
    subprocess.run(cmd)
    
    return str(filename)


def convert_to_gif(cast_file: str, output: str = None) -> str:
    """Convert asciinema recording to GIF.
    
    Args:
        cast_file: Path to .cast file
        output: Optional output path
        
    Returns:
        Path to GIF file
    """
    if not output:
        output = cast_file.replace(".cast", ".gif")
    
    # Use agg if available, otherwise svg-term
    try:
        # Try agg (asciinema gif generator)
        cmd = ["agg", cast_file, output]
        subprocess.run(cmd, check=True)
    except FileNotFoundError:
        # Fallback: convert via svg
        print("agg not found, using fallback method")
        svg_file = cast_file.replace(".cast", ".svg")
        subprocess.run(["asciinema", "cat", cast_file], 
                      stdout=open(svg_file, 'w'))
        # Would need imagemagick for svg->gif
        return svg_file
    
    return output


def convert_to_mp4(cast_file: str, output: str = None, 
                   width: int = 1920, height: int = 1080) -> str:
    """Convert asciinema recording to MP4 using ffmpeg.
    
    Args:
        cast_file: Path to .cast file
        output: Optional output path
        width: Video width
        height: Video height
        
    Returns:
        Path to MP4 file
    """
    if not output:
        output = cast_file.replace(".cast", ".mp4")
    
    # First convert to GIF, then to MP4
    gif_file = convert_to_gif(cast_file)
    
    cmd = [
        "ffmpeg", "-y",
        "-i", gif_file,
        "-movflags", "faststart",
        "-pix_fmt", "yuv420p",
        "-vf", f"scale={width}:{height}:force_original_aspect_ratio=decrease,pad={width}:{height}:(ow-iw)/2:(oh-ih)/2",
        output
    ]
    
    subprocess.run(cmd, check=True)
    
    # Cleanup GIF
    os.remove(gif_file)
    
    return output


def list_recordings() -> list:
    """List all recordings in the queue."""
    recordings = []
    for f in CAPTURE_DIR.glob("*.cast"):
        stat = f.stat()
        recordings.append({
            "name": f.stem,
            "path": str(f),
            "size": stat.st_size,
            "created": datetime.fromtimestamp(stat.st_ctime).isoformat()
        })
    return recordings


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        
        if cmd == "record":
            name = sys.argv[2] if len(sys.argv) > 2 else None
            start_recording(name)
            
        elif cmd == "run":
            command = " ".join(sys.argv[2:])
            record_command(command)
            
        elif cmd == "list":
            for r in list_recordings():
                print(f"{r['name']}: {r['path']}")
                
        elif cmd == "convert":
            cast_file = sys.argv[2]
            convert_to_mp4(cast_file)
    else:
        print("Usage:")
        print("  terminal.py record [name]  - Start interactive recording")
        print("  terminal.py run <command>  - Record a command")
        print("  terminal.py list           - List recordings")
        print("  terminal.py convert <file> - Convert .cast to .mp4")
