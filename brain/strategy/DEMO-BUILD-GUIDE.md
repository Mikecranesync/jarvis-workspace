# Demo Conveyor Build Guide
*Father-Son Robot Factory Night - Feb 5, 2026*

---

## Overview
Build a working VFD-controlled conveyor connected to Micro820 PLC, mirrored in Factory I/O, with AI computer vision watching both.

---

## PHASE 1: Wiring (30 min)

### VFD Input Power (220V)
```
Dryer Outlet (NEMA 14-30) → VFD Input
├── L1 (Hot 1)  → VFD Terminal L1
├── L2 (Hot 2)  → VFD Terminal L2
├── Neutral    → (not used on 220V VFD)
└── Ground     → VFD Ground Terminal
```

### VFD Output to Motor
```
VFD Output → Motor
├── U (T1) → Motor Lead 1
├── V (T2) → Motor Lead 2
├── W (T3) → Motor Lead 3
└── Ground → Motor Frame Ground
```

**For Single-Phase Motor (dryer motor):**
Connect motor to U and V only (2 of 3 phases). Set VFD to single-phase output mode.

### VFD Control from Micro820
```
Micro820 Digital Outputs → VFD Control Terminals
├── DO1 → VFD "FWD" (Run Forward)
├── DO2 → VFD "REV" (Run Reverse) [optional]
├── DO3 → VFD "STOP" or "Reset"
└── COM → VFD "DCM" (Digital Common)

Micro820 Analog Output → VFD Speed Reference
├── AO1 → VFD "VI" (0-10V speed reference)
└── COM → VFD "ACM" (Analog Common)
```

---

## PHASE 2: VFD Programming (15 min)

### Essential Parameters (GS11N-20P5)
| Param | Name | Value | Notes |
|-------|------|-------|-------|
| P00 | Motor HP | 0.5 | Match your motor |
| P01 | Motor Voltage | 230 | |
| P02 | Motor Amps | Check nameplate | |
| P03 | Base Freq | 60 | Hz |
| P04 | Max Freq | 60 | Hz |
| P05 | Accel Time | 5 | Seconds |
| P06 | Decel Time | 5 | Seconds |
| P07 | Source Select | 1 | Terminal control |
| P08 | Frequency Source | 1 | Terminal (VI input) |

### For Single-Phase Motor
Set P42 (if available) for single-phase output mode.

---

## PHASE 3: PLC Program (20 min)

### Ladder Logic Outline
```
RUNG 1: Start Button
[Start_PB]----[/Stop_PB]----[/Fault]----(Conveyor_Run)----

RUNG 2: Run Forward Output  
[Conveyor_Run]----(DO1_FWD)----

RUNG 3: Speed Control
[Conveyor_Run]----[MOV Speed_Setpoint → AO1]----

RUNG 4: Fault Detection
[VFD_Fault_Input]----(Fault_Latch)----
```

### I/O Map
| Address | Description | Wire To |
|---------|-------------|---------|
| I:0/0 | Start Button | Pushbutton NO |
| I:0/1 | Stop Button | Pushbutton NC |
| I:0/2 | VFD Fault | VFD fault relay |
| O:0/0 | Run Forward | VFD FWD terminal |
| O:0/1 | Run Reverse | VFD REV terminal |
| AO:0 | Speed Ref | VFD VI (0-10V) |

---

## PHASE 4: Factory I/O Setup (15 min)

### Recommended Scene
**"Sorting by Height (Basic)"** or **"From A to B"**
- Simple conveyor with sensors
- Easy to map to physical I/O

### Driver Setup
1. Open Factory I/O
2. File → Drivers → Allen-Bradley Logix/Micro800
3. Configure:
   - IP: Micro820's IP address
   - Mode: Client
4. Map I/O tags to match your PLC program

### Digital Twin Mapping
| Factory I/O | Micro820 | Physical |
|-------------|----------|----------|
| Conveyor Start | O:0/0 | VFD FWD |
| Sensor 1 | I:0/3 | (future) |
| Speed | AO:0 | VFD VI |

---

## PHASE 5: Computer Vision AI (Optional Tonight)

### Setup on PLC Laptop
1. Open browser to Factory I/O window
2. Position camera/screen recording on physical conveyor
3. Run computer use model with prompt:
   ```
   Watch both the Factory I/O simulation and the physical 
   conveyor. Note any differences in timing or behavior.
   Suggest I/O mappings between virtual and physical.
   ```

### Tools Needed
- Screen capture of Factory I/O
- Camera/phone pointed at physical conveyor
- Claude computer use or similar model

---

## Quick Start Sequence

### Tonight's Minimum Viable Demo:

1. **Wire VFD power** (220V in)
2. **Wire motor** (if you have one) - or skip and demo VFD panel only
3. **Wire VFD control** from Micro820 DO1 to FWD terminal
4. **Program PLC** with simple Start/Stop logic
5. **Test** - Toggle DO1 from CCW, motor should run
6. **Open Factory I/O** with matching scene
7. **Connect Factory I/O** to Micro820
8. **Watch both run in sync!**

---

## Safety Reminders ⚠️

- **220V is dangerous** - double-check wiring before power-on
- **Motor can spin unexpectedly** - keep hands clear
- **VFD can store charge** - wait 5 min after power-off before touching
- **Teach your son** - this is real industrial equipment!

---

## Help Commands

When you're ready, message me with:
- "Ready to wire" → I'll walk through connections
- "VFD parameters" → I'll guide programming
- "PLC help" → I'll help with ladder logic
- "Factory I/O stuck" → Troubleshooting

Let's build! 🏭🤖
