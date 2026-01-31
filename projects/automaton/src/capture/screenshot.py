#!/usr/bin/env python3
"""
Screenshot Capture Module for The Automaton
Captures screenshots and creates comparison images
"""

import subprocess
import os
from datetime import datetime
from pathlib import Path
from typing import Optional, Tuple

CAPTURE_DIR = Path("/root/jarvis-workspace/projects/automaton/queue")
CAPTURE_DIR.mkdir(parents=True, exist_ok=True)


def capture_url(url: str, name: str = None, 
                width: int = 1920, height: int = 1080) -> str:
    """Capture screenshot of a URL using headless browser.
    
    Args:
        url: URL to capture
        name: Optional name for the file
        width: Screenshot width
        height: Screenshot height
        
    Returns:
        Path to screenshot file
    """
    if not name:
        name = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    filename = CAPTURE_DIR / f"screenshot_{name}.png"
    
    # Try using Playwright/Puppeteer via Node, or fallback to cutycapt
    try:
        # Try with chrome headless
        cmd = [
            "google-chrome", "--headless", "--disable-gpu",
            f"--window-size={width},{height}",
            f"--screenshot={filename}",
            url
        ]
        subprocess.run(cmd, check=True, capture_output=True)
    except (FileNotFoundError, subprocess.CalledProcessError):
        try:
            # Try chromium
            cmd = [
                "chromium-browser", "--headless", "--disable-gpu",
                f"--window-size={width},{height}",
                f"--screenshot={filename}",
                url
            ]
            subprocess.run(cmd, check=True, capture_output=True)
        except (FileNotFoundError, subprocess.CalledProcessError):
            print(f"No headless browser available. Cannot capture {url}")
            return None
    
    return str(filename)


def capture_terminal_output(command: str, name: str = None) -> str:
    """Capture terminal output as an image.
    
    Args:
        command: Command to run
        name: Optional name for the file
        
    Returns:
        Path to image file
    """
    if not name:
        name = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    filename = CAPTURE_DIR / f"terminal_{name}.png"
    txt_file = CAPTURE_DIR / f"terminal_{name}.txt"
    
    # Run command and capture output
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    output = result.stdout + result.stderr
    
    # Save text output
    with open(txt_file, 'w') as f:
        f.write(f"$ {command}\n")
        f.write(output)
    
    # Convert to image using imagemagick if available
    try:
        cmd = [
            "convert",
            "-font", "DejaVu-Sans-Mono",
            "-pointsize", "14",
            "-background", "black",
            "-fill", "white",
            f"label:@{txt_file}",
            str(filename)
        ]
        subprocess.run(cmd, check=True)
        os.remove(txt_file)
    except (FileNotFoundError, subprocess.CalledProcessError):
        # Keep text file as fallback
        print(f"ImageMagick not available. Text saved to {txt_file}")
        return str(txt_file)
    
    return str(filename)


def create_comparison(before: str, after: str, 
                      output: str = None, 
                      layout: str = "horizontal") -> str:
    """Create a before/after comparison image.
    
    Args:
        before: Path to before image
        after: Path to after image
        output: Optional output path
        layout: "horizontal" or "vertical"
        
    Returns:
        Path to comparison image
    """
    if not output:
        output = CAPTURE_DIR / f"comparison_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    
    append_flag = "+append" if layout == "horizontal" else "-append"
    
    cmd = [
        "convert",
        before, after,
        append_flag,
        str(output)
    ]
    
    try:
        subprocess.run(cmd, check=True)
    except (FileNotFoundError, subprocess.CalledProcessError):
        print("ImageMagick not available for comparison")
        return None
    
    return str(output)


def add_text_overlay(image: str, text: str, 
                     position: str = "bottom",
                     output: str = None) -> str:
    """Add text overlay to an image.
    
    Args:
        image: Path to image
        text: Text to add
        position: "top", "bottom", "center"
        output: Optional output path
        
    Returns:
        Path to output image
    """
    if not output:
        output = image.replace(".png", "_labeled.png")
    
    gravity = {
        "top": "North",
        "bottom": "South",
        "center": "Center"
    }.get(position, "South")
    
    cmd = [
        "convert", image,
        "-gravity", gravity,
        "-pointsize", "24",
        "-fill", "white",
        "-stroke", "black",
        "-strokewidth", "1",
        "-annotate", "+0+10", text,
        output
    ]
    
    try:
        subprocess.run(cmd, check=True)
    except (FileNotFoundError, subprocess.CalledProcessError):
        print("ImageMagick not available for text overlay")
        return image
    
    return output


def list_screenshots() -> list:
    """List all screenshots in the queue."""
    screenshots = []
    for ext in ["*.png", "*.jpg", "*.jpeg"]:
        for f in CAPTURE_DIR.glob(ext):
            stat = f.stat()
            screenshots.append({
                "name": f.stem,
                "path": str(f),
                "size": stat.st_size,
                "created": datetime.fromtimestamp(stat.st_ctime).isoformat()
            })
    return screenshots


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        
        if cmd == "url":
            url = sys.argv[2]
            name = sys.argv[3] if len(sys.argv) > 3 else None
            result = capture_url(url, name)
            print(f"Captured: {result}")
            
        elif cmd == "terminal":
            command = " ".join(sys.argv[2:])
            result = capture_terminal_output(command)
            print(f"Captured: {result}")
            
        elif cmd == "compare":
            before = sys.argv[2]
            after = sys.argv[3]
            result = create_comparison(before, after)
            print(f"Created: {result}")
            
        elif cmd == "list":
            for s in list_screenshots():
                print(f"{s['name']}: {s['path']}")
    else:
        print("Usage:")
        print("  screenshot.py url <url> [name]      - Capture URL")
        print("  screenshot.py terminal <command>    - Capture terminal output")
        print("  screenshot.py compare <before> <after> - Create comparison")
        print("  screenshot.py list                  - List screenshots")
