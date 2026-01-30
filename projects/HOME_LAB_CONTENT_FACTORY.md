# Project: Home Lab Content Factory

**Created:** 2026-01-29  
**Status:** PROPOSAL  
**Owner:** Mike + Jarvis

---

## The Vision

Turn Mike's home PLC workbench into a **24/7 autonomous content factory** that:
- Creates video tutorials and case studies
- Documents PLC diagnostics and troubleshooting
- Generates marketing content for FactoryLM
- Runs experiments while Mike sleeps

---

## Components

### Hardware (Mike's Home Setup)
- Windows/Mac desktop (always on)
- Connected to PLC workbench (Factory IO + Allen-Bradley Micro 820)
- Screen recording capability
- Webcam (optional, for picture-in-picture)

### Software Stack
| Component | Purpose |
|-----------|---------|
| **Ollama** | Local LLM runtime (DeepSeek, Qwen, Llama) |
| **Open Interpreter** | Natural language → computer control |
| **01 OS Mode** | Desktop automation (screenshots, clicks, typing) |
| **OBS Studio** | Screen recording / streaming |
| **Factory IO** | PLC simulation software |

---

## How It Works

```
┌─────────────────────────────────────────────────────────────────┐
│                    HOME LAB CONTENT FACTORY                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────┐     ┌──────────────┐     ┌──────────────┐    │
│  │    Jarvis    │────▶│    Open      │────▶│   Desktop    │    │
│  │  (VPS/Cloud) │     │  Interpreter │     │   Actions    │    │
│  └──────────────┘     └──────────────┘     └──────────────┘    │
│         │                    │                    │             │
│         │                    ▼                    ▼             │
│         │             ┌──────────────┐     ┌──────────────┐    │
│         │             │   Ollama     │     │   OBS/Screen │    │
│         │             │  (Local LLM) │     │   Recording  │    │
│         │             └──────────────┘     └──────────────┘    │
│         │                    │                    │             │
│         ▼                    ▼                    ▼             │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                    PLC WORKBENCH                          │  │
│  │  Factory IO  ←→  Modbus TCP  ←→  Allen-Bradley Micro820   │  │
│  └──────────────────────────────────────────────────────────┘  │
│                              │                                  │
│                              ▼                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                    OUTPUT                                 │  │
│  │  📹 Video tutorials    📊 Case studies    📝 Blog posts   │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Use Cases

### 1. Automated PLC Tutorial Videos
**Scenario:** "Create a 5-minute tutorial on reading Modbus registers"

**Steps:**
1. Jarvis sends task to Open Interpreter on home machine
2. Open Interpreter launches Factory IO + PLC software
3. Starts OBS screen recording
4. Narrates steps while demonstrating (TTS or pre-recorded)
5. Stops recording, adds captions
6. Uploads to YouTube draft
7. Pings Mike for review

### 2. Case Study Documentation
**Scenario:** "Document how PLC Copilot diagnoses a conveyor fault"

**Steps:**
1. Set up fault condition in Factory IO
2. Trigger PLC Copilot diagnosis
3. Screen record the entire process
4. Generate written case study from recording
5. Create before/after screenshots
6. Package as blog post + video

### 3. Experimental Learning
**Scenario:** "Figure out how to read temperature sensor via EtherNet/IP"

**Steps:**
1. Jarvis researches documentation
2. Open Interpreter tries different approaches on PLC
3. Documents what works / what fails
4. Creates troubleshooting guide from learnings
5. Saves as knowledge base article

---

## Feasibility Assessment

### ✅ Definitely Feasible (Today)
| Capability | How |
|------------|-----|
| Run local LLM | Ollama with DeepSeek/Qwen |
| Control desktop | Open Interpreter OS Mode |
| Take screenshots | Built into Open Interpreter |
| Click/type | Computer API in Open Interpreter |
| Run shell commands | Native Open Interpreter |
| Screen recording | OBS command line control |

### 🟡 Feasible with Work
| Capability | Challenge | Solution |
|------------|-----------|----------|
| Video narration | Need TTS | Use Coqui TTS or ElevenLabs API |
| Edit videos | Complex | FFmpeg scripting or DaVinci CLI |
| Upload to YouTube | Auth required | YouTube API + saved credentials |
| Remote access | Network config | Tailscale VPN (already have skill) |

### ⚠️ Challenges
| Challenge | Mitigation |
|-----------|------------|
| LLM reliability | Use proven models (DeepSeek-R1, Qwen2.5) |
| Desktop state | Clear state between runs, snapshot VM |
| Error recovery | Watchdog script to restart on failure |
| Quality control | All outputs → review queue before publish |

---

## Implementation Plan

### Phase 1: Infrastructure (Week 1)
- [ ] Install Ollama on home machine
- [ ] Pull DeepSeek-R1:14b or Qwen2.5:14b
- [ ] Install Open Interpreter with OS mode
- [ ] Set up Tailscale for remote access
- [ ] Install OBS Studio with CLI control
- [ ] Test basic desktop automation

### Phase 2: Pipeline (Week 2)
- [ ] Create screen recording script
- [ ] Set up TTS for narration
- [ ] Build video processing workflow (FFmpeg)
- [ ] Create YouTube upload automation
- [ ] Build task queue system

### Phase 3: Content Factory (Week 3+)
- [ ] Create first automated tutorial
- [ ] Set up nightly content generation tasks
- [ ] Build review queue for Mike approval
- [ ] Document the system itself (meta-content!)

---

## Task Queue System

```yaml
# ~/.content-factory/tasks.yaml
tasks:
  - id: tutorial-modbus-basics
    type: video-tutorial
    title: "Reading Modbus Registers with Python"
    duration: 5-7 min
    outline:
      - Intro: What is Modbus
      - Demo: Connect to PLC
      - Demo: Read register values
      - Code walkthrough
      - Wrap-up
    status: queued
    
  - id: case-study-conveyor-fault
    type: case-study
    title: "AI Diagnoses Conveyor Motor Fault"
    format: video + blog
    scenario: "Induce thermal overload, show PLC Copilot diagnosis"
    status: queued
```

**Jarvis processes queue → Open Interpreter executes → Output to review**

---

## Remote Control Architecture

```
Mike (anywhere)
    │
    ▼
Telegram → Jarvis (VPS)
    │
    ▼
Tailscale VPN
    │
    ▼
Home Machine → Open Interpreter → Desktop Actions
    │
    ▼
PLC Workbench → Content Creation → YouTube Draft
    │
    ▼
Telegram ← "Tutorial ready for review! 📹"
```

---

## Video Content Ideas (Initial Queue)

### Beginner Series
1. "What is a PLC? 60-Second Explainer"
2. "Setting Up Factory IO for PLC Simulation"
3. "Your First Modbus Connection in Python"
4. "Reading and Writing PLC Registers"

### PLC Copilot Demos
5. "AI Reads Your PLC Fault Codes"
6. "Predictive Maintenance Demo: Motor Temperature"
7. "Natural Language PLC Diagnostics"

### FactoryLM Platform
8. "CMMS That Actually Gets Used"
9. "From Fault Code to Work Order in 30 Seconds"
10. "Smart Glasses for Maintenance Technicians (Preview)"

---

## Cost Analysis

| Item | Cost | Notes |
|------|------|-------|
| Ollama | Free | Open source |
| Open Interpreter | Free | Open source |
| DeepSeek-R1 | Free | Open weights |
| OBS Studio | Free | Open source |
| Tailscale | Free tier | Up to 100 devices |
| ElevenLabs TTS | $5-22/mo | Optional, for narration |
| YouTube | Free | For hosting |
| **Total** | **$0-22/mo** | Mostly free! |

---

## Security Considerations

- [ ] Tailscale for encrypted remote access (no port forwarding)
- [ ] Separate user account for automation
- [ ] No credentials stored in scripts
- [ ] Review queue prevents auto-publish of bad content
- [ ] Watchdog to kill runaway processes

---

## Success Metrics

| Metric | Target (Month 1) |
|--------|------------------|
| Videos produced | 10 |
| Videos published | 5 (after review) |
| YouTube views | 500 |
| Leads generated | 5 |
| Hours saved | 20+ |

---

## Next Steps

1. **Mike approves plan** ← YOU ARE HERE
2. Install Ollama + Open Interpreter on home machine
3. Set up Tailscale connection
4. Test basic automation
5. Create first tutorial (manual supervision)
6. Automate and scale

---

*"The best marketing is demonstrating your product solving real problems. The second best is doing it on autopilot."*
