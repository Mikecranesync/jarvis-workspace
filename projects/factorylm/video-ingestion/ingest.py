#!/usr/bin/env python3
"""
Video Ingestion Pipeline for FactoryLM

Transforms video recordings into searchable knowledge bases.
- Extracts smart keyframes (skip blur, duplicates)
- Transcribes audio for context
- Runs vision AI on each unique frame
- Outputs structured, indexed knowledge

Usage:
    python ingest.py --input video.mp4 --output ./kb/
    python ingest.py --input video.mp4 --transcribe --fps 2
"""

import os
import sys
import json
import argparse
import hashlib
import subprocess
import asyncio
import aiohttp
from pathlib import Path
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
import base64

# Try imports, install if missing
try:
    import cv2
    import numpy as np
except ImportError:
    print("Installing opencv-python...")
    subprocess.run([sys.executable, "-m", "pip", "install", "opencv-python", "-q"])
    import cv2
    import numpy as np

try:
    import google.generativeai as genai
except ImportError:
    print("Installing google-generativeai...")
    subprocess.run([sys.executable, "-m", "pip", "install", "google-generativeai", "-q"])
    import google.generativeai as genai

# ============================================================================
# CONFIG
# ============================================================================

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "AIzaSyAGRt1kKdBygARiiCv7TiA_tpf4hUjtkJI")
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "")
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")

# Model selection: "gemini" | "deepseek" | "ollama" | "auto"
# Auto = try ollama first (free), fallback to deepseek (cheap), then gemini
MODEL_PROVIDER = os.getenv("MODEL_PROVIDER", "auto")

genai.configure(api_key=GEMINI_API_KEY)

# Thresholds
BLUR_THRESHOLD = 100  # Laplacian variance below this = blurry
SIMILARITY_THRESHOLD = 0.95  # Hash similarity above this = duplicate
MIN_FRAME_INTERVAL = 0.5  # Minimum seconds between frames

# Vision models by provider
gemini_model = genai.GenerativeModel("gemini-2.0-flash-exp")

# ============================================================================
# FRAME EXTRACTION
# ============================================================================

def extract_frames(video_path: str, output_dir: str, fps: float = 1.0) -> list:
    """Extract frames from video at specified FPS."""
    
    frames_dir = Path(output_dir) / "frames"
    frames_dir.mkdir(parents=True, exist_ok=True)
    
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise ValueError(f"Cannot open video: {video_path}")
    
    video_fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = total_frames / video_fps if video_fps > 0 else 0
    
    print(f"📹 Video: {video_path}")
    print(f"   Duration: {duration:.1f}s | FPS: {video_fps:.1f} | Total frames: {total_frames}")
    
    # Calculate frame interval
    frame_interval = int(video_fps / fps) if fps > 0 else int(video_fps)
    
    extracted = []
    frame_count = 0
    saved_count = 0
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        if frame_count % frame_interval == 0:
            timestamp = frame_count / video_fps
            frame_path = frames_dir / f"frame_{saved_count:04d}.jpg"
            cv2.imwrite(str(frame_path), frame)
            extracted.append({
                "path": str(frame_path),
                "timestamp": timestamp,
                "frame_num": frame_count
            })
            saved_count += 1
        
        frame_count += 1
    
    cap.release()
    print(f"   Extracted: {saved_count} frames at {fps} fps")
    
    return extracted


def calculate_blur(image_path: str) -> float:
    """Calculate blur score using Laplacian variance. Higher = sharper."""
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        return 0
    return cv2.Laplacian(img, cv2.CV_64F).var()


def calculate_hash(image_path: str) -> str:
    """Calculate perceptual hash for duplicate detection."""
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        return ""
    # Resize to 8x8 and compute hash
    resized = cv2.resize(img, (8, 8))
    mean = resized.mean()
    bits = (resized > mean).flatten()
    return ''.join(['1' if b else '0' for b in bits])


def hash_similarity(hash1: str, hash2: str) -> float:
    """Calculate similarity between two hashes (0-1)."""
    if not hash1 or not hash2 or len(hash1) != len(hash2):
        return 0
    matches = sum(a == b for a, b in zip(hash1, hash2))
    return matches / len(hash1)


def filter_frames(frames: list, blur_threshold: float = BLUR_THRESHOLD, 
                  similarity_threshold: float = SIMILARITY_THRESHOLD) -> list:
    """Filter out blurry and duplicate frames."""
    
    print(f"🔍 Filtering {len(frames)} frames...")
    
    filtered = []
    last_hash = None
    
    for frame in frames:
        path = frame["path"]
        
        # Check blur
        blur_score = calculate_blur(path)
        if blur_score < blur_threshold:
            print(f"   ❌ Skipping blurry frame: {Path(path).name} (blur={blur_score:.0f})")
            continue
        
        # Check duplicate
        current_hash = calculate_hash(path)
        if last_hash:
            similarity = hash_similarity(current_hash, last_hash)
            if similarity > similarity_threshold:
                print(f"   ❌ Skipping duplicate: {Path(path).name} (sim={similarity:.2f})")
                continue
        
        frame["blur_score"] = blur_score
        frame["hash"] = current_hash
        filtered.append(frame)
        last_hash = current_hash
    
    print(f"   ✅ Kept {len(filtered)}/{len(frames)} frames")
    return filtered


# ============================================================================
# AUDIO TRANSCRIPTION
# ============================================================================

def transcribe_audio(video_path: str, output_dir: str) -> str:
    """Extract and transcribe audio from video."""
    
    audio_path = Path(output_dir) / "audio.wav"
    transcript_path = Path(output_dir) / "transcript.txt"
    
    # Extract audio with FFmpeg
    print("🎤 Extracting audio...")
    cmd = [
        "ffmpeg", "-i", video_path, "-vn", "-acodec", "pcm_s16le",
        "-ar", "16000", "-ac", "1", "-y", str(audio_path)
    ]
    subprocess.run(cmd, capture_output=True)
    
    if not audio_path.exists():
        print("   ⚠️ No audio track found")
        return ""
    
    # Transcribe with Gemini
    print("🎤 Transcribing audio...")
    try:
        with open(audio_path, "rb") as f:
            audio_data = f.read()
        
        response = model.generate_content([
            "Transcribe this audio. Include speaker context if multiple voices. "
            "Format as plain text with timestamps if possible.",
            {"mime_type": "audio/wav", "data": audio_data}
        ])
        
        transcript = response.text
        transcript_path.write_text(transcript)
        print(f"   ✅ Transcription saved: {transcript_path}")
        
        # Cleanup
        audio_path.unlink()
        
        return transcript
    except Exception as e:
        print(f"   ❌ Transcription failed: {e}")
        return ""


# ============================================================================
# VISION AI ANALYSIS
# ============================================================================

EXTRACTION_PROMPT = """Analyze this image from an industrial/technical context.

Extract ALL information visible:

1. **Text Content**: Every word, number, label, warning, spec you can read
2. **Document Type**: Manual page? Electrical print? Nameplate? Equipment photo?
3. **Key Information**: 
   - Equipment names/models
   - Part numbers
   - Specifications (voltage, current, pressure, etc.)
   - Warnings/cautions
   - Procedures/steps
4. **Visual Elements**: Diagrams, symbols, indicators, connections
5. **Context Clues**: What is this about? What equipment? What process?

Output as structured JSON:
{
    "document_type": "manual_page|electrical_print|nameplate|equipment|other",
    "title": "if visible",
    "text_content": "all readable text",
    "key_specs": {"name": "value"},
    "warnings": ["list of warnings/cautions"],
    "procedures": ["numbered steps if present"],
    "equipment_mentioned": ["list"],
    "summary": "one-line summary of what this shows"
}
"""


async def analyze_with_ollama(image_path: str, prompt: str) -> str:
    """Analyze image with local Ollama (LLaVA)."""
    try:
        with open(image_path, "rb") as f:
            image_b64 = base64.b64encode(f.read()).decode()
        
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{OLLAMA_URL}/api/generate",
                json={
                    "model": "llava",  # or llava:13b for better quality
                    "prompt": prompt,
                    "images": [image_b64],
                    "stream": False
                },
                timeout=aiohttp.ClientTimeout(total=60)
            ) as resp:
                if resp.status == 200:
                    result = await resp.json()
                    return result.get("response", "")
    except Exception as e:
        print(f"   Ollama failed: {e}")
    return None


async def analyze_with_deepseek(image_path: str, prompt: str) -> str:
    """Analyze image with DeepSeek VL."""
    try:
        with open(image_path, "rb") as f:
            image_b64 = base64.b64encode(f.read()).decode()
        
        async with aiohttp.ClientSession() as session:
            async with session.post(
                "https://api.deepseek.com/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "deepseek-chat",  # Use vision model when available
                    "messages": [
                        {
                            "role": "user",
                            "content": [
                                {"type": "text", "text": prompt},
                                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_b64}"}}
                            ]
                        }
                    ],
                    "max_tokens": 2000
                },
                timeout=aiohttp.ClientTimeout(total=60)
            ) as resp:
                if resp.status == 200:
                    result = await resp.json()
                    return result["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"   DeepSeek failed: {e}")
    return None


async def analyze_with_gemini(image_path: str, prompt: str) -> str:
    """Analyze image with Gemini."""
    try:
        with open(image_path, "rb") as f:
            image_data = f.read()
        
        response = gemini_model.generate_content([
            prompt,
            {"mime_type": "image/jpeg", "data": image_data}
        ])
        return response.text
    except Exception as e:
        print(f"   Gemini failed: {e}")
    return None


async def analyze_frame(frame: dict, output_dir: str, provider: str = None) -> dict:
    """Analyze a single frame with vision AI (multi-provider)."""
    
    path = frame["path"]
    extracted_dir = Path(output_dir) / "extracted"
    extracted_dir.mkdir(exist_ok=True)
    
    provider = provider or MODEL_PROVIDER
    text = None
    used_provider = None
    
    try:
        # Try providers in order based on setting
        if provider == "auto":
            # Try free first, then cheap, then premium
            text = await analyze_with_ollama(path, EXTRACTION_PROMPT)
            if text:
                used_provider = "ollama"
            else:
                text = await analyze_with_deepseek(path, EXTRACTION_PROMPT)
                if text:
                    used_provider = "deepseek"
                else:
                    text = await analyze_with_gemini(path, EXTRACTION_PROMPT)
                    used_provider = "gemini"
        elif provider == "ollama":
            text = await analyze_with_ollama(path, EXTRACTION_PROMPT)
            used_provider = "ollama"
        elif provider == "deepseek":
            text = await analyze_with_deepseek(path, EXTRACTION_PROMPT)
            used_provider = "deepseek"
        else:  # gemini or fallback
            text = await analyze_with_gemini(path, EXTRACTION_PROMPT)
            used_provider = "gemini"
        
        if not text:
            return {"error": "All providers failed", "source_frame": Path(path).name}
        
        # Try to extract JSON
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0]
        elif "```" in text:
            text = text.split("```")[1].split("```")[0]
        
        try:
            result = json.loads(text)
        except:
            result = {"raw_text": text, "parse_error": True}
        
        # Add metadata
        result["source_frame"] = Path(path).name
        result["timestamp"] = frame.get("timestamp", 0)
        result["provider"] = used_provider
        
        # Save
        output_path = extracted_dir / f"{Path(path).stem}.json"
        with open(output_path, "w") as f:
            json.dump(result, f, indent=2)
        
        return result
        
    except Exception as e:
        print(f"   ❌ Analysis failed for {Path(path).name}: {e}")
        return {"error": str(e), "source_frame": Path(path).name}


async def analyze_all_frames(frames: list, output_dir: str, max_concurrent: int = 5) -> list:
    """Analyze all frames with rate limiting."""
    
    print(f"🧠 Analyzing {len(frames)} frames (provider: {MODEL_PROVIDER})...")
    
    results = []
    for i, frame in enumerate(frames):
        print(f"   Processing {i+1}/{len(frames)}: {Path(frame['path']).name}")
        result = await analyze_frame(frame, output_dir)
        results.append(result)
        
        # Rate limiting
        if i < len(frames) - 1:
            await asyncio.sleep(0.5)
    
    print(f"   ✅ Analyzed {len(results)} frames")
    return results


# ============================================================================
# OUTPUT GENERATION
# ============================================================================

def generate_summary(results: list, transcript: str, output_dir: str) -> dict:
    """Generate summary and index from extraction results."""
    
    output_path = Path(output_dir)
    
    # Build summary
    summary = {
        "generated_at": datetime.now().isoformat(),
        "total_frames_processed": len(results),
        "document_types": {},
        "equipment_found": set(),
        "warnings_found": [],
        "all_text": []
    }
    
    for r in results:
        # Count document types
        doc_type = r.get("document_type", "unknown")
        summary["document_types"][doc_type] = summary["document_types"].get(doc_type, 0) + 1
        
        # Collect equipment
        for eq in r.get("equipment_mentioned", []):
            summary["equipment_found"].add(eq)
        
        # Collect warnings
        summary["warnings_found"].extend(r.get("warnings", []))
        
        # Collect text
        if r.get("text_content"):
            summary["all_text"].append(r["text_content"])
    
    summary["equipment_found"] = list(summary["equipment_found"])
    
    # Save index
    index_path = output_path / "index.json"
    with open(index_path, "w") as f:
        json.dump({
            "summary": summary,
            "frames": results,
            "transcript": transcript
        }, f, indent=2)
    
    # Generate markdown summary
    md_lines = [
        "# Video Ingestion Summary",
        f"\n*Generated: {summary['generated_at']}*\n",
        f"## Overview",
        f"- **Frames processed:** {summary['total_frames_processed']}",
        f"- **Document types found:** {summary['document_types']}",
        f"- **Equipment mentioned:** {', '.join(summary['equipment_found']) or 'None identified'}",
        f"\n## Warnings/Cautions Found",
    ]
    
    for w in summary["warnings_found"][:20]:  # Limit to 20
        md_lines.append(f"- ⚠️ {w}")
    
    if transcript:
        md_lines.extend([
            f"\n## Audio Transcript",
            f"```",
            transcript[:2000] + ("..." if len(transcript) > 2000 else ""),
            f"```"
        ])
    
    md_lines.extend([
        f"\n## Extracted Content",
        f"See `extracted/` folder for per-frame JSON files.",
        f"\n## Full Text Content",
        "```"
    ])
    
    for text in summary["all_text"][:10]:  # First 10
        md_lines.append(text[:500])
        md_lines.append("---")
    
    md_lines.append("```")
    
    summary_path = output_path / "summary.md"
    summary_path.write_text("\n".join(md_lines))
    
    print(f"📄 Summary saved: {summary_path}")
    print(f"📄 Index saved: {index_path}")
    
    return summary


# ============================================================================
# MAIN
# ============================================================================

async def ingest_video(input_path: str, output_dir: str, fps: float = 1.0, 
                       transcribe: bool = False) -> dict:
    """Main ingestion pipeline."""
    
    print("=" * 60)
    print("VIDEO INGESTION PIPELINE")
    print("=" * 60)
    
    # Ensure output dir exists
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    # 1. Extract frames
    frames = extract_frames(input_path, output_dir, fps)
    
    # 2. Filter frames
    filtered_frames = filter_frames(frames)
    
    # 3. Transcribe audio (optional)
    transcript = ""
    if transcribe:
        transcript = transcribe_audio(input_path, output_dir)
    
    # 4. Analyze frames with vision AI
    results = await analyze_all_frames(filtered_frames, output_dir)
    
    # 5. Generate summary
    summary = generate_summary(results, transcript, output_dir)
    
    print("\n" + "=" * 60)
    print("✅ INGESTION COMPLETE")
    print("=" * 60)
    print(f"Output: {output_dir}")
    print(f"Frames processed: {len(results)}")
    print(f"Equipment found: {len(summary['equipment_found'])}")
    print(f"Warnings found: {len(summary['warnings_found'])}")
    
    return summary


def main():
    parser = argparse.ArgumentParser(description="Video Ingestion Pipeline for FactoryLM")
    parser.add_argument("--input", "-i", required=True, help="Input video file")
    parser.add_argument("--output", "-o", default="./output", help="Output directory")
    parser.add_argument("--fps", type=float, default=1.0, help="Frames per second to extract")
    parser.add_argument("--transcribe", "-t", action="store_true", help="Transcribe audio")
    parser.add_argument("--provider", "-p", default="auto", 
                       choices=["auto", "ollama", "deepseek", "gemini"],
                       help="AI provider: auto (free→cheap→premium), ollama (free), deepseek (cheap), gemini")
    
    args = parser.parse_args()
    
    global MODEL_PROVIDER
    MODEL_PROVIDER = args.provider
    
    if not os.path.exists(args.input):
        print(f"Error: Input file not found: {args.input}")
        sys.exit(1)
    
    asyncio.run(ingest_video(args.input, args.output, args.fps, args.transcribe))


if __name__ == "__main__":
    main()
