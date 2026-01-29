# Video Ingestion Pipeline

**"Capture Once, Index Forever"**

Transform video walkthroughs into searchable knowledge bases. Record manuals, equipment, electrical prints — AI extracts and indexes everything.

## Quick Start

```bash
# 1. Record video on phone (manual pages, equipment walkthrough, etc.)
# 2. Send video to this pipeline
# 3. Get structured knowledge base output

python ingest.py --input video.mp4 --output ./knowledge-base/
```

## Features

- **Smart Frame Extraction** — Only keeps unique, non-blurry frames
- **Audio Transcription** — Voice narration becomes searchable context  
- **OCR + Vision AI** — Extracts text, diagrams, specs from every frame
- **Duplicate Detection** — Skips redundant content automatically
- **Batch Processing** — Handles long videos efficiently

## Usage

### Basic: Process a Video
```bash
python ingest.py --input manual_flipthrough.mp4
```

### With Audio Context
```bash
python ingest.py --input walkthrough.mp4 --transcribe
```

### Specify Output Location
```bash
python ingest.py --input video.mp4 --output ./kb/stardust-racers/
```

### Adjust Frame Rate
```bash
# More frames = more detail, higher cost
python ingest.py --input video.mp4 --fps 2

# Fewer frames = faster, cheaper
python ingest.py --input video.mp4 --fps 0.5
```

## Output Structure

```
output/
├── frames/              # Extracted keyframes
│   ├── frame_001.jpg
│   ├── frame_002.jpg
│   └── ...
├── extracted/           # AI-extracted content
│   ├── frame_001.json   # {text, objects, context}
│   ├── frame_002.json
│   └── ...
├── transcript.txt       # Audio transcription (if --transcribe)
├── summary.md           # Human-readable summary
└── index.json           # Searchable index
```

## Requirements

- Python 3.10+
- FFmpeg (for video processing)
- Gemini API key (set in environment)

## API Costs

| Video Length | Frames (1fps) | Estimated Cost |
|--------------|---------------|----------------|
| 1 minute     | ~30 frames    | ~$0.03         |
| 5 minutes    | ~100 frames   | ~$0.10         |
| 30 minutes   | ~500 frames   | ~$0.50         |

*After duplicate/blur filtering, actual frames processed is typically 30-50% less*

## Integration

This pipeline feeds into:
- **Puppeteer** (AR glasses assistant)
- **FactoryLM** (industrial AI platform)
- **RideView** (equipment inspection)

All extracted knowledge is queryable by any system.
