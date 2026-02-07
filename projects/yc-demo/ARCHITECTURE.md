# 🎬 YC Demo Director - Architecture

> "14 cameras, dynamic switching, phones as displays, real PLC I/O, force functions, Hollywood-level direction"
> — Mike, 2026-02-05

---

## Overview

A fully automated multi-camera demo system that:
1. Streams Factory I/O simulation to audience phones
2. Cuts to real PLC I/O changes in sync
3. Allows interactive force functions
4. Shows code changes in real-time
5. Auto-directs like a Hollywood production

---

## System Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        DEMO DIRECTOR (Celery Conductor)                 │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ┌─────────────┐   ┌─────────────┐   ┌─────────────┐   ┌─────────────┐  │
│  │  🎥 Camera   │   │  📺 Scene   │   │  🔌 PLC     │   │  📱 Phone   │  │
│  │   Brigade    │   │  Director   │   │  Bridge     │   │  Streamer   │  │
│  └──────┬──────┘   └──────┬──────┘   └──────┬──────┘   └──────┬──────┘  │
│         │                 │                 │                 │          │
│         v                 v                 v                 v          │
│  ┌──────────────────────────────────────────────────────────────────┐   │
│  │                      OBS WebSocket Bridge                         │   │
│  │              (Scene switching, source control)                    │   │
│  └──────────────────────────────────────────────────────────────────┘   │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘

         │                                           │
         v                                           v
┌─────────────────────┐                 ┌─────────────────────┐
│   PLC Laptop        │                 │   Phone Viewers     │
│   100.72.2.99       │                 │   WebRTC Stream     │
│                     │                 │                     │
│   • Factory I/O     │<───Sync────────>│   • Live sim view   │
│   • Micro820 PLC    │                 │   • Force buttons   │
│   • ShowUI          │                 │   • I/O status      │
│   • OBS             │                 │                     │
└─────────────────────┘                 └─────────────────────┘
```

---

## Camera Positions (14 Angles)

| ID | Name | Source | Purpose |
|----|------|--------|---------|
| CAM-1 | Factory I/O Overview | Screen Capture | Full sim view |
| CAM-2 | Factory I/O Closeup | Screen Capture | Detail view |
| CAM-3 | PLC Physical | Webcam 1 | Real Micro820 |
| CAM-4 | PLC I/O LEDs | Webcam 2 | Status lights |
| CAM-5 | Code Editor | Screen Region | Live code |
| CAM-6 | Mermaid Diagram | Browser | I/O visualization |
| CAM-7 | Presenter Wide | Canon | Mike talking |
| CAM-8 | Presenter Close | Webcam 3 | Reaction shots |
| CAM-9 | Phone Demo | Webcam 4 | Audience POV |
| CAM-10 | Terminal | Screen Region | CLI actions |
| CAM-11 | Network Traffic | Screen Region | Data flow |
| CAM-12 | Browser UI | Screen Region | Web interface |
| CAM-13 | Split: Sim+PLC | Composite | Side-by-side |
| CAM-14 | Outro | Static | End card |

---

## Demo Script Engine

```python
# demo_script.yaml - Scene-by-scene breakdown

scenes:
  - name: "intro"
    duration: 30
    cameras: [CAM-7]  # Presenter wide
    narration: "Welcome to FactoryLM..."
    actions: []
    
  - name: "show_factory_io"
    duration: 45
    cameras: [CAM-1, CAM-13]  # Overview, then split
    narration: "This is a factory simulation..."
    actions:
      - type: obs_transition
        scene: "factory_overview"
      - type: highlight
        target: "conveyor_belt"
        
  - name: "connect_plc"
    duration: 60
    cameras: [CAM-3, CAM-4, CAM-13]
    narration: "Now watch the real PLC..."
    actions:
      - type: plc_read
        address: "I:0/0"
        highlight: true
      - type: mermaid_update
        show_io: true
        
  - name: "phone_interaction"
    duration: 90
    cameras: [CAM-9, CAM-6]
    narration: "Audience, open your phones..."
    actions:
      - type: qr_display
        url: "${PHONE_VIEWER_URL}"
      - type: wait_for_connections
        min_clients: 1
      - type: enable_force_buttons
        
  - name: "force_demo"
    duration: 120
    cameras: [CAM-9, CAM-4, CAM-13]
    narration: "Try forcing that output..."
    actions:
      - type: plc_force
        address: "O:0/0"
        value: 1
        show_code: true
```

---

## Worker Army Hierarchy

```
                    ┌──────────────────┐
                    │    FOREMAN       │
                    │  (Celery Beat)   │
                    └────────┬─────────┘
                             │
           ┌─────────────────┼─────────────────┐
           │                 │                 │
           v                 v                 v
    ┌──────────────┐  ┌──────────────┐  ┌──────────────┐
    │   DIVISION:  │  │   DIVISION:  │  │   DIVISION:  │
    │   CONTENT    │  │   TECHNICAL  │  │   QA         │
    └──────┬───────┘  └──────┬───────┘  └──────┬───────┘
           │                 │                 │
           v                 v                 v
    ┌──────────────┐  ┌──────────────┐  ┌──────────────┐
    │  GENERAL:    │  │  GENERAL:    │  │  GENERAL:    │
    │  VideoMaster │  │  CodeForge   │  │  Hammurabi   │
    └──────┬───────┘  └──────┬───────┘  └──────┬───────┘
           │                 │                 │
    ┌──────┴──────┐   ┌──────┴──────┐   ┌──────┴──────┐
    │             │   │             │   │             │
    v             v   v             v   v             v
┌────────┐  ┌────────┐┌────────┐┌────────┐┌────────┐┌────────┐
│Script  │  │Scene   ││OBS     ││PLC     ││Judge   ││Polish  │
│Writer  │  │Builder ││Control ││Bridge  ││Worker  ││Worker  │
└────────┘  └────────┘└────────┘└────────┘└────────┘└────────┘
```

---

## Iteration Definition (Celery)

```python
# An "iteration" in our Celery system:

class IterationCycle:
    """
    One complete quality improvement cycle.
    
    ITERATION = Execute → Judge → (Polish if fail) → Repeat
    
    Max iterations: 5 (configurable)
    Pass threshold: 0.85 score
    
    If artifact doesn't pass after max_iterations:
    → Flag for human review
    → DO NOT ship garbage
    """
    
    def run_iteration(self, task, input_data, iteration_num):
        # 1. EXECUTE: Run the worker task
        artifact = task.execute(input_data)
        
        # 2. JUDGE: Hammurabi evaluates
        judgment = self.hammurabi.judge(artifact, spec=task.spec)
        
        # 3. RECORD: Save to Prometheus (training data)
        self.prometheus.record(input_data, artifact, judgment, iteration_num)
        
        if judgment.passed:
            return artifact, "PASSED"
        
        if iteration_num >= self.max_iterations:
            return artifact, "NEEDS_REVIEW"
        
        # 4. POLISH: Improve based on feedback
        polished = self.polish(artifact, judgment.suggestions)
        
        # 5. RECURSE: Try again
        return self.run_iteration(task, polished, iteration_num + 1)
```

---

## LLM Judge Spec: Demo Quality

```python
# Quality criteria for YC demo content

class DemoContentSpec(BaseModel):
    """What makes demo content 'knock their socks off'."""
    
    # VISUAL IMPACT
    visual_clarity: float = Field(ge=0, le=1, description="Clear, not cluttered")
    professional_polish: float = Field(ge=0, le=1, description="Looks expensive")
    wow_factor: float = Field(ge=0, le=1, description="Makes them say 'damn'")
    
    # TECHNICAL ACCURACY
    plc_accuracy: float = Field(ge=0, le=1, description="Real PLC behavior shown")
    code_clarity: float = Field(ge=0, le=1, description="Code is readable on screen")
    sync_quality: float = Field(ge=0, le=1, description="Video/PLC in sync")
    
    # STORYTELLING
    narrative_flow: float = Field(ge=0, le=1, description="Story makes sense")
    pacing: float = Field(ge=0, le=1, description="Not too fast/slow")
    hook_strength: float = Field(ge=0, le=1, description="Grabs attention early")
    
    # ACCESSIBILITY
    eleven_year_old_test: float = Field(ge=0, le=1, description="A kid could follow")
    jargon_free: float = Field(ge=0, le=1, description="No unnecessary tech speak")
    
    @property
    def overall_score(self) -> float:
        """Weighted overall score."""
        weights = {
            'visual_clarity': 1.0,
            'professional_polish': 1.5,  # Extra important
            'wow_factor': 2.0,  # MOST important
            'plc_accuracy': 1.2,
            'code_clarity': 0.8,
            'sync_quality': 1.0,
            'narrative_flow': 1.0,
            'pacing': 1.0,
            'hook_strength': 1.5,
            'eleven_year_old_test': 1.5,
            'jargon_free': 0.8,
        }
        
        total_weight = sum(weights.values())
        weighted_sum = sum(
            getattr(self, field) * weight 
            for field, weight in weights.items()
        )
        
        return weighted_sum / total_weight
    
    @property
    def passes(self) -> bool:
        """Must score 0.85+ to ship."""
        return self.overall_score >= 0.85
```

---

## Fallback: Hollywood Director Mode

If live demo doesn't work, we film it. The system becomes a virtual director:

```
┌─────────────────────────────────────────────────────────────┐
│                    DIRECTOR MODE                             │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  🎬 "Scene 1, Take 3. Camera 7. Action!"                     │
│                                                              │
│  Director Agent provides:                                    │
│  • Shot list for each scene                                  │
│  • Camera angles to use                                      │
│  • Timing cues for cuts                                      │
│  • Script for Mike to follow                                 │
│  • Post-production edit notes                                │
│                                                              │
│  Output: Final cut video with professional editing           │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## Implementation Phases

### Phase 1: OBS Integration (Today)
- [ ] Install obsws-python on PLC laptop
- [ ] Create scene collection with 14 sources
- [ ] Test WebSocket scene switching from VPS
- [ ] Basic demo_director.py Celery task

### Phase 2: Phone Viewer (Tomorrow)  
- [ ] WebRTC stream from Factory I/O
- [ ] Force button UI (HTML/JS)
- [ ] Deploy to phones via QR code
- [ ] PLC read-back to show changes

### Phase 3: Script Engine (Day 3)
- [ ] Demo script YAML parser
- [ ] Scene transition automation
- [ ] Mermaid diagram sync
- [ ] Narration timing

### Phase 4: Worker Army (Day 4)
- [ ] Deploy content workers
- [ ] Deploy QA/judge workers
- [ ] Iteration loop testing
- [ ] Quality threshold tuning

### Phase 5: Full Rehearsal (Day 5)
- [ ] End-to-end run-through
- [ ] Edge case handling
- [ ] Fallback video recording
- [ ] Final polish

---

## Files to Create

```
/opt/master_of_puppets/
├── workers/
│   ├── demo_director_tasks.py      # Main orchestrator
│   ├── obs_controller_tasks.py     # OBS WebSocket control
│   ├── phone_streamer_tasks.py     # WebRTC to phones
│   └── plc_sync_tasks.py           # PLC I/O sync
│
├── specs/
│   └── demo_content_spec.py        # Pydantic quality specs
│
└── scripts/
    └── demo_script.yaml            # Scene-by-scene script

/root/jarvis-workspace/projects/yc-demo/
├── ARCHITECTURE.md                 # This file
├── phone-viewer/                   # Phone web app
│   ├── index.html
│   └── app.js
└── scenes/                         # OBS scene configs
    └── yc_demo_collection.json
```

---

## Let's Build This Army 🤖⚔️
