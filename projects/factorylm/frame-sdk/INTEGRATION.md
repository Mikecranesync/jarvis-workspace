# FactoryLM × Frame Integration Architecture

## Overview

Frame glasses + Claude multimodal + global expert network = hands-free industrial diagnostics.

## The Flow

```
┌─────────────────────────────────────────────────────────────────┐
│  TECHNICIAN IN FIELD                                            │
│  ┌─────────┐                                                    │
│  │  Frame  │ ── Bluetooth ──> Phone/Edge Device                 │
│  │ Glasses │                       │                            │
│  └─────────┘                       │                            │
│       │                            ▼                            │
│  [Photo/Audio]              FactoryLM Backend                   │
│                                    │                            │
│                    ┌───────────────┼───────────────┐            │
│                    ▼               ▼               ▼            │
│               Claude API     Atlas CMMS     Expert Network      │
│              (Multimodal)    (Work Orders)  (Remote Support)    │
│                    │               │               │            │
│                    └───────────────┼───────────────┘            │
│                                    ▼                            │
│                          Response to Frame                      │
│                         (Display + Audio)                       │
└─────────────────────────────────────────────────────────────────┘
```

## Core Use Cases

### 1. Nameplate OCR + Instant Diagnosis
```python
# Technician taps Frame, says "What is this?"
photo = await frame.camera.take_photo(autofocus_seconds=2)
result = await claude.analyze(photo, "Read nameplate, identify equipment, list common faults")
await frame.display.show_text(result.equipment_name)
await frame.display.scroll_text(result.diagnosis)
```

### 2. Voice-Activated Troubleshooting
```python
# Technician asks "Why is the motor overheating?"
audio = await frame.microphone.record_audio(max_length=30)
transcription = await whisper.transcribe(audio)
context = await atlas_cmms.get_equipment_history(equipment_id)
solution = await claude.troubleshoot(transcription, context, photo)
await frame.display.scroll_text(solution)
```

### 3. Remote Expert "Puppet Master" Mode
```python
# Expert sees what technician sees in real-time
async def puppet_master_session(frame, expert_websocket):
    while session_active:
        photo = await frame.camera.take_photo()
        await expert_websocket.send(photo)
        
        # Expert can send instructions
        instruction = await expert_websocket.receive()
        await frame.display.show_text(instruction)
        
        # Expert can draw on screen (highlight components)
        if instruction.type == "highlight":
            await frame.display.draw_rect(
                instruction.x, instruction.y,
                instruction.width, instruction.height,
                PaletteColors.RED
            )
```

### 4. Automatic Work Order Creation
```python
# After diagnosis, auto-create WO
diagnosis = await get_diagnosis()
work_order = await atlas_cmms.create_work_order(
    title=f"Repair: {diagnosis.equipment_name}",
    description=diagnosis.recommendation,
    priority=diagnosis.severity,
    photos=[photo]
)
await frame.display.show_text(f"WO #{work_order.id} created")
```

## Technical Components

### Frame App (Python)
```
factorylm-frame/
├── main.py              # Entry point
├── connection.py        # Frame Bluetooth management
├── camera.py            # Photo capture + preprocessing
├── audio.py             # Voice commands + playback
├── display.py           # UI rendering on Frame
├── claude_client.py     # Claude API integration
├── cmms_client.py       # Atlas CMMS API
└── expert_session.py    # WebSocket to expert network
```

### Backend Services
```
factorylm-backend/
├── api/
│   ├── diagnose.py      # Claude multimodal endpoint
│   ├── transcribe.py    # Whisper STT endpoint
│   ├── expert.py        # Expert matching + WebSocket
│   └── cmms.py          # Atlas CMMS proxy
├── knowledge/
│   ├── equipment_db.py  # Equipment specs + fault codes
│   ├── prompts/         # Domain-specific prompts (THE MOAT)
│   └── cost_models.py   # Repair cost estimation
└── billing/
    └── usage.py         # Track API usage per customer
```

## MVP Feature Set (v0.1)

| Feature | Priority | Complexity |
|---------|----------|------------|
| Nameplate OCR | P0 | Low |
| Equipment identification | P0 | Low |
| Fault code lookup | P0 | Low |
| Voice commands | P1 | Medium |
| Work order creation | P1 | Medium |
| Expert video call | P2 | High |
| Real-time annotations | P2 | High |

## Hardware Requirements

- Frame glasses ($349)
- Android phone (Bluetooth host) OR
- Raspberry Pi (edge deployment)
- Internet connection (for Claude API)

## API Costs (per session)

| Action | Cost |
|--------|------|
| Photo analysis (Claude) | ~$0.02-0.05 |
| Voice transcription (Whisper) | ~$0.006/min |
| Text response (Claude) | ~$0.01 |
| **Total per diagnosis** | **~$0.05-0.10** |

At $99/month subscription with avg 200 diagnoses = $10-20 API cost = 80-90% margin.

## Development Phases

### Phase 1: Mock Development (Weeks 1-4, while waiting for glasses)
- [ ] Build Telegram bot that mimics Frame workflow
- [ ] User sends photo → Claude analyzes → bot responds
- [ ] Voice messages → Whisper → Claude → text response
- [ ] Test all prompts and refine

### Phase 2: Frame Integration (Weeks 5-6)
- [ ] Port Telegram bot logic to Frame SDK
- [ ] Test camera capture + display
- [ ] Test microphone + voice commands
- [ ] Optimize for latency (<3 sec response)

### Phase 3: Expert Network (Weeks 7-8)
- [ ] Build expert dashboard (web)
- [ ] WebSocket for real-time photo streaming
- [ ] Expert annotation tools
- [ ] Billing integration

### Phase 4: Pilot (Weeks 9-12)
- [ ] Deploy to first customer
- [ ] Collect feedback
- [ ] Iterate
- [ ] Video case study

## Key Differentiators

1. **$349 hardware** vs $3,000+ competitors
2. **Claude multimodal** for instant AI diagnosis
3. **Global expert network** at $100/hr (not $500/hr)
4. **Open platform** — developers can build on top
5. **Industrial focus** — not generic enterprise AR

## Risk Mitigation

| Risk | Mitigation |
|------|------------|
| Frame hardware issues | Test extensively in pilot before scale |
| Claude API costs spike | Implement caching, batch processing |
| Expert quality varies | Rating system, certification program |
| Competitor copies | Speed to market, brand, relationships |

---

*Last updated: 2026-01-28*
