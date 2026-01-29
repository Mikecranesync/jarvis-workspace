#!/usr/bin/env python3
"""
Telegram Video Handler for FactoryLM

Receives videos via Telegram, processes them, returns results.

Usage:
    1. Send video to Jarvis bot
    2. Say "ingest this" or "process this video"
    3. Get back extracted knowledge
"""

import os
import sys
import asyncio
import tempfile
from pathlib import Path

# Add parent for imports
sys.path.append(str(Path(__file__).parent))

from ingest import ingest_video


async def process_telegram_video(video_path: str, chat_id: str, context: str = "") -> dict:
    """
    Process a video received from Telegram.
    
    Args:
        video_path: Path to downloaded video file
        chat_id: Telegram chat ID for notifications
        context: Optional context (user's message with the video)
    
    Returns:
        Summary dict with extraction results
    """
    
    # Create output directory based on timestamp
    from datetime import datetime
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = Path(f"C:/Users/hharp/clawd/projects/factorylm/knowledge-base/videos/{timestamp}")
    
    # Check if context mentions transcription
    transcribe = any(word in context.lower() for word in ["transcribe", "audio", "voice", "narration"])
    
    # Determine FPS from context
    fps = 1.0
    if "detailed" in context.lower() or "slow" in context.lower():
        fps = 2.0
    elif "fast" in context.lower() or "quick" in context.lower():
        fps = 0.5
    
    # Process video
    try:
        summary = await ingest_video(
            input_path=video_path,
            output_dir=str(output_dir),
            fps=fps,
            transcribe=transcribe
        )
        
        return {
            "success": True,
            "output_dir": str(output_dir),
            "summary": summary,
            "frames_processed": summary.get("total_frames_processed", 0),
            "equipment_found": summary.get("equipment_found", []),
            "warnings_found": len(summary.get("warnings_found", []))
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


# For direct testing
if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        result = asyncio.run(process_telegram_video(sys.argv[1], "test", ""))
        print(result)
