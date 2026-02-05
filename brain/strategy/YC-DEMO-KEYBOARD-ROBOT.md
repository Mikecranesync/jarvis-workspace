# YC Demo: Keyboard Robot
*"Control a Real Machine From Your Phone"*

**Created:** 2026-02-05
**Deadline:** 4 days (2026-02-09)
**Status:** SPEC DRAFT

---

## The Magic Moment

A YC partner, from their personal phone, controls a REAL pneumatic machine through the same interface any maintenance tech would use. This proves FactoryLM can bridge phone → cloud → PLC → physical action.

---

## Demo Flow

### 1. Entry Point
- Reviewer clicks link in YC application
- Opens demo webpage with:
  - Live camera feed of keyboard robot
  - QR code visible (simulated motor nameplate)
  - Brief intro text explaining the demo

### 2. Phone Connection
- Reviewer scans QR code with their phone
- QR code opens Telegram bot (FactoryLM demo bot)
- Bot detects VIP demo mode via QR payload
- Reviewer is now connected to the live demo

### 3. VIP Welcome
```
🤖 "Welcome to FactoryLM. 

You're now connected to a real industrial control system - 
a Micro820 PLC controlling pneumatic actuators.

This is exactly how a maintenance technician would connect 
to their equipment. Same interface, same capabilities.

Let's demonstrate. This machine can play music.
Pick a song:"

🎵 [Chopsticks]
🎵 [Mary Had a Little Lamb]  
🎵 [Twinkle Twinkle]
🎵 [Hot Cross Buns]
🎵 [Ode to Joy (Simple)]
🎵 [Happy Birthday]
```

### 4. The Performance
- User selects song
- Bot sends command to Micro820 via Modbus/EtherNet-IP
- PLC executes ladder logic sequence
- Pneumatic cylinders fire in sequence
- Casio keyboard plays the song
- Live on camera feed
- User hears it through camera audio

### 5. The Education
After the song, the bot continues:
```
🤖 "That was fun. But here's what FactoryLM actually does:

In real industrial settings, that PLC would be monitoring 
a motor, a conveyor, or a pump. When something goes wrong, 
a maintenance tech can:

📸 Take a photo of the equipment nameplate
🔍 Get instant AI identification
📋 Generate a work order automatically  
🔧 Access troubleshooting guides
📦 Order replacement parts
📊 Track everything in the CMMS

Want to see the full workflow? Let me walk you through 
how maintenance SHOULD work..."
```

### 6. Maintenance Workflow Demo
Walk through:
1. Equipment identification (photo → AI)
2. Work order creation (automatic)
3. Parts lookup and ordering
4. Documentation and history
5. Predictive maintenance (sensor data → predictions)
6. The air-gapped security model

### 7. Technical Deep Dive (Optional)
For curious reviewers:
- IO-Link sensor integration
- Edge computing architecture
- LLM cascade for cost optimization
- Data flywheel for training

---

## Hardware Specification

### Pneumatic System

**Cylinders:**
- 5x Bimba flat-1 or similar compact cylinders
- Stroke length: ~1" (25mm) - enough to press a key
- Bore: 3/4" to 1" for sufficient force
- Spring return preferred (simpler control)

**Alternative:** SMC CD55 series compact cylinders

**Solenoid Valves:**
- 5x 3-way or 5/2 solenoid valves
- 24VDC coil (matches Micro820 outputs)
- Flow rate sufficient for quick response
- Options: SMC SY series, Festo MH series

**Air Supply:**
- Home compressor (Mike has this)
- Regulator set to ~40-60 PSI
- Small reservoir tank for consistent pressure

**Mounting:**
- Aluminum extrusion frame (80/20 or similar)
- Adjustable cylinder mounts for key alignment
- Casio keyboard on fixed platform

### Cycle Time Analysis

**Typical pneumatic cylinder cycle time:**
- Fast cylinders: 50-100ms extend, 50-100ms retract
- Total cycle: 100-200ms per note
- Maximum tempo: ~150-300 BPM possible

**Song Selection Criteria:**
- Maximum 5 simultaneous notes (5 fingers)
- Tempo: 60-120 BPM to be safe
- Simple melodies without fast runs
- Songs should be recognizable

### Suggested Songs (5 Fingers)

| Song | Notes Needed | Max Fingers | Tempo | Feasibility |
|------|--------------|-------------|-------|-------------|
| Mary Had a Little Lamb | E D C D E E E | 3 | Slow | ✓ Easy |
| Twinkle Twinkle | C C G G A A G | 4 | Slow | ✓ Easy |
| Hot Cross Buns | E D C, E D C | 3 | Slow | ✓ Easy |
| Chopsticks | F G, F G (repeat) | 2 | Medium | ✓ Easy |
| Ode to Joy (Simple) | E E F G G F E D | 4 | Medium | ✓ Doable |
| Happy Birthday | C C D C F E | 4 | Slow | ✓ Doable |

### PLC Configuration

**Micro820:**
- 5 digital outputs → solenoid valves
- 1 digital input (optional) → start signal from web
- Modbus TCP for remote control
- Ladder logic programs for each song

**Ladder Logic Structure:**
```
Program: SONG_MARY_LAMB
- Sequence timer (200ms per step)
- Output pattern: 
  Step 1: O:0.2 (E)
  Step 2: O:0.1 (D)
  Step 3: O:0.0 (C)
  Step 4: O:0.1 (D)
  ... etc
```

### Camera System

**Option A: Canon DSLR Tethering**
- gPhoto2 on Raspberry Pi/Linux
- Live view streaming via HDMI capture or USB
- OBS for stream processing

**Option B: Webcam (Simpler)**
- Logitech C920 or similar
- Direct USB to streaming PC
- OBS → RTMP → Web player

**Recommended: Start with webcam, upgrade to DSLR if time permits**

---

## Software Components

### 1. Demo Landing Page
```
/demo/keyboard-robot/

- Live video player (HLS/WebRTC)
- QR code display
- Brief instructions
- Queue status indicator
- "Currently playing: [song]" display
```

### 2. Telegram Bot (Demo Mode)
```python
# Demo mode detection
if qr_payload.startswith("DEMO_VIP_"):
    user.demo_mode = True
    user.priority = "VIP"
    await send_welcome_demo(user)
```

### 3. PLC Control API
```python
# FastAPI endpoint
@app.post("/api/play-song")
async def play_song(song_id: str, session_id: str):
    # Verify user is in active demo session
    # Send Modbus command to Micro820
    # Return acknowledgment
```

### 4. Queue System
```python
class DemoQueue:
    def __init__(self):
        self.current_user = None
        self.queue = []
        self.vip_queue = []  # YC reviewers jump here
    
    def add_user(self, user, is_vip=False):
        if is_vip:
            self.vip_queue.append(user)
        else:
            self.queue.append(user)
```

---

## 4-Day Build Plan

### Day 1 (Today/Tomorrow)
- [ ] Source Bimba cylinders and solenoid valves
- [ ] Design mounting frame
- [ ] Set up Micro820 with Modbus TCP
- [ ] Write ladder logic for one test song

### Day 2
- [ ] Assemble pneumatic system
- [ ] Test individual cylinder firing
- [ ] Align cylinders over keyboard
- [ ] Write all 6 song programs

### Day 3
- [ ] Set up camera and streaming
- [ ] Build demo landing page
- [ ] Integrate bot with PLC control API
- [ ] Test full loop: phone → bot → PLC → keyboard

### Day 4
- [ ] Polish and bug fixes
- [ ] Write educational bot script
- [ ] Record backup video (in case live fails)
- [ ] Full dress rehearsal

---

## Risk Mitigation

**Risk: Hardware doesn't arrive in time**
- Mitigation: Source locally (Grainger, MSC, Amazon)
- Backup: Factory I/O simulation demo

**Risk: Live stream fails during demo**
- Mitigation: Pre-recorded backup video
- Secondary camera/stream ready

**Risk: PLC connection drops**
- Mitigation: Local fallback mode
- Status monitoring on landing page

**Risk: Song sounds bad**
- Mitigation: Test extensively, tune timing
- Pick forgiving songs (slow tempo)

---

## Bill of Materials (Estimated)

| Item | Qty | Est. Cost | Source |
|------|-----|-----------|--------|
| Bimba cylinders | 5 | $100-150 | Grainger/Amazon |
| Solenoid valves 24VDC | 5 | $75-100 | Amazon/SMC |
| Fittings/tubing | lot | $30-50 | Home Depot |
| 80/20 extrusion | 4ft | $20-30 | Amazon |
| Casio keyboard | 1 | $20-40 | Thrift/Amazon |
| Webcam (if needed) | 1 | $50-80 | Amazon |
| **Total** | | **~$300-450** | |

Note: Mike likely has some of this already

---

## Success Criteria

1. YC reviewer can control the machine from their phone
2. Song plays recognizably (they know what it is)
3. Live camera shows it happening in real-time
4. Bot provides educational walkthrough
5. Full loop completes in <5 minutes
6. Zero crashes during demo window

---

## The Pitch

"You just controlled a real industrial machine from your phone. A Micro820 PLC, pneumatic actuators, and a Casio keyboard - all through a Telegram bot.

Now imagine that same interface connected to every motor, pump, and conveyor in a factory. That's FactoryLM.

The maintenance tech's phone becomes the control room. AI identifies equipment. Predictive analytics prevent failures. Parts order themselves.

We're not building software. We're building the operating system for industrial maintenance."

---

*This demo will be unforgettable.*
