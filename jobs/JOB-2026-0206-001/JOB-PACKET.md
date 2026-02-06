# JOB PACKET: VFD Conveyor Demo Build
**Job #:** 2026-0206-001
**Customer:** FactoryLM (Internal Demo)
**Site:** Lake Wales, FL (Home Lab)
**Tech Assigned:** Mike Harp
**Date Issued:** 2026-02-06
**Target Completion:** 2026-02-09

---

## 📋 SCOPE OF WORK

Build a VFD-controlled conveyor system that mirrors Factory I/O "Sorting by Height (Basic)" scene. System includes:
- 3-phase motor on VFD
- Micro820 PLC control
- Start/Stop/Speed control via PLC
- Digital twin running in Factory I/O
- Optional: Brake motor, sensors for sorting

---

## 🔧 MOTOR SPECIFICATION

### Required Motor

| Spec | Value |
|------|-------|
| **Frame** | 56C (C-Face, removable base) |
| **HP** | 1/2 HP |
| **Phase** | 3-Phase |
| **Voltage** | 208-230/460V |
| **RPM** | 1725-1800 (4-pole) |
| **Duty** | Inverter Duty (REQUIRED) |
| **Insulation** | Class F minimum |
| **Enclosure** | TEFC (Totally Enclosed Fan Cooled) |
| **Service Factor** | 1.15 |

### Recommended Part Numbers (in order of preference)

1. **Marathon G581** - Amazon, ~$180
   - 56C, 1/2HP, 3PH, 230/460V, Inverter Duty 10:1 CT
   - https://www.amazon.com/dp/B007ZQLAA6

2. **WorldWide Electric ODP12-36-56CB** - ~$150
   - Premium efficiency, inverter duty
   - https://worldwideelectric.com

3. **NAT12-18-56CB** - compressor-source.com, ~$160
   - TEFC, Class F, 1.15 SF, inverter rated

### Local Purchase Options (Lake Wales/Orlando Area)

| Store | Address | Phone | Opens |
|-------|---------|-------|-------|
| **Grainger** | 2900 Titan Row, Orlando | (407) 857-3780 | 7 AM |
| **Motion Industries** | 1050 Sunshine Blvd, Orlando | (407) 898-4641 | 7 AM |
| **Bearing & Drive Solutions** | Winter Haven | (863) 294-5593 | 8 AM |
| **Electric Motor Repair** | Lakeland | (863) 682-0167 | 8 AM |

**Tell them:** "I need a 56C frame, half horse, 3-phase, inverter duty motor. TEFC. 230V or dual voltage."

### Brake Motor (Nice to Have)
If available, a motor with electromagnetic brake adds:
- Precise stopping (no coasting)
- Holding torque when stopped
- Adds ~$100-150 to cost
- Part example: Marathon 56T17F5348 (brake motor)

---

## 🏭 FACTORY I/O SCENE: "Sorting by Height (Basic)"

### Why This Scene
- Simple conveyor with height sensors
- Pusher mechanisms for sorting
- Easy I/O mapping
- Matches real industrial sorting applications

### Scene I/O Map

| Factory I/O Tag | Type | Description |
|-----------------|------|-------------|
| Conveyor | Digital OUT | Main belt run/stop |
| Sensor 1 (Entry) | Digital IN | Part detected at entry |
| Sensor 2 (High) | Digital IN | Tall part detected |
| Sensor 3 (Low) | Digital IN | Short part detected |
| Pusher 1 | Digital OUT | Push tall parts |
| Pusher 2 | Digital OUT | Push short parts |
| Conveyor Speed | Analog OUT | Belt speed 0-100% |

---

## 📐 MECHANICAL DRAWINGS

### Conveyor Frame Assembly

```
TOP VIEW
┌─────────────────────────────────────────────────┐
│  MOTOR          BELT SURFACE              IDLER │
│   ██═══════════════════════════════════════██   │
│   ║                                         ║   │
│   ║    ← ← ← DIRECTION OF TRAVEL ← ← ←    ║   │
│   ║                                         ║   │
│   ██═══════════════════════════════════════██   │
└─────────────────────────────────────────────────┘
     ↑                                        ↑
  DRIVE END                              TAIL END

SIDE VIEW
                    SENSOR BRACKET
                         │
    MOTOR    GUARD       ▼         IDLER
      █▓▓▓▓▓██████████████████████████▓▓▓▓█
      ╔══════════════════════════════════╗ ←── BELT
      ║▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒║
    ┌─╨─┐                              ┌─╨─┐
    │   │                              │   │
    │   │ ← FRAME (UNISTRUT OR ANGLE) │   │
    └───┘                              └───┘
      ▲                                  ▲
   36" HEIGHT                         ADJUSTABLE
   (WORKING HEIGHT)                   TENSIONER
```

### Dimensions

| Component | Dimension | Notes |
|-----------|-----------|-------|
| Overall Length | 48" - 72" | Match Factory I/O belt |
| Belt Width | 6" - 12" | Standard for small parts |
| Working Height | 36" | Ergonomic for standing |
| Frame Material | Unistrut or 1.5" angle iron | |
| Belt Material | PVC or rubber flat belt | |

### Motor Mounting Detail

```
56C FACE MOUNT DETAIL
                    
    ┌──────────────────┐
    │   GEARBOX/       │
    │   REDUCER        │
    │   (if needed)    │
    │                  │
    │    ████████      │◄── MOTOR 56C FACE
    │    ████████      │    4-BOLT PATTERN
    │    ████████      │    PILOT: 4.5" DIA
    │                  │
    └──────────────────┘
           ║
           ║◄── 5/8" SHAFT TO DRIVE PULLEY
           ▼
```

### Pulley/Sprocket Sizing

For 1800 RPM motor, typical conveyor speed 50-100 FPM:
- **Motor Pulley:** 2" diameter
- **Driven Pulley:** 8-10" diameter (gives 4:1 to 5:1 reduction)
- **Belt Speed:** ~90 FPM at full VFD output

OR use gear reducer:
- **Ratio:** 10:1 or 15:1
- **Output:** 120-180 RPM
- **Direct drive** to conveyor roller

---

## ⚡ ELECTRICAL PRINTS

### Single Line Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    POWER DISTRIBUTION                        │
└─────────────────────────────────────────────────────────────┘

MAIN PANEL (200A)                                              
    │                                                          
    ├──► 30A 2-POLE ──► DISCONNECT ──► VFD INPUT (L1, L2)     
    │    BREAKER           SW-1         GS11N-20P5             
    │                                       │                  
    │                                       ▼                  
    │                               ┌───────────────┐          
    │                               │     VFD       │          
    │                               │  GS11N-20P5   │          
    │                               │               │          
    │                               │ U  V  W  PE   │          
    │                               └─┬──┬──┬──┬────┘          
    │                                 │  │  │  │               
    │                                 ▼  ▼  ▼  ▼               
    │                               ┌───────────────┐          
    │                               │   MOTOR       │          
    │                               │  1/2 HP 3PH   │          
    │                               │   56C TEFC    │          
    │                               └───────────────┘          
    │                                                          
    └──► 15A 1-POLE ──► 24VDC SUPPLY ──► MICRO820 + I/O       
         BREAKER           PS-1              PLC               
```

### VFD Control Wiring

```
MICRO820                          VFD CONTROL TERMINALS
┌──────────┐                      ┌──────────────────┐
│          │                      │                  │
│  DO1 ────┼──────────────────────┼──► FWD (Run)     │
│          │                      │                  │
│  DO2 ────┼──────────────────────┼──► REV (Reverse) │
│          │                      │                  │
│  DO3 ────┼──────────────────────┼──► STOP/Reset    │
│          │                      │                  │
│  COM ────┼──────────────────────┼──► DCM (Common)  │
│          │                      │                  │
│  AO1 ────┼──────────────────────┼──► VI (0-10V)    │
│          │                      │                  │
│  AGND ───┼──────────────────────┼──► ACM (A. Com)  │
│          │                      │                  │
│  DI1 ◄───┼──────────────────────┼─── FAULT OUTPUT  │
│          │                      │                  │
└──────────┘                      └──────────────────┘
```

### Sensor Wiring (Future Expansion)

```
PROXIMITY SENSORS (NPN, 3-WIRE)
┌────────────────┐
│  24VDC SUPPLY  │
│    (+) ────────┼───► SENSOR BROWN (V+)
│    (-) ────────┼───► SENSOR BLUE (V-)
└────────────────┘
                 
MICRO820 INPUT
┌────────────────┐
│   DI2 ◄────────┼─── SENSOR BLACK (SIGNAL)
│   COM ─────────┼─── SENSOR BLUE (COMMON)
└────────────────┘
```

---

## 📦 BILL OF MATERIALS

### Electrical

| Qty | Part | Description | Est. Cost | Source |
|-----|------|-------------|-----------|--------|
| 1 | Motor | 56C, 1/2HP, 3PH, Inverter Duty | $150-200 | Local/Amazon |
| 1 | VFD | GS11N-20P5 (Already have?) | $0 | On-hand |
| 1 | Micro820 | 2080-LC30-48QWB (Already have) | $0 | On-hand |
| 1 | 24VDC PSU | 2A minimum | $25 | Amazon |
| 1 | Disconnect | 30A, non-fused | $20 | Home Depot |
| 50ft | THHN 10AWG | VFD power wiring | $30 | Home Depot |
| 25ft | 18/4 Cable | Control wiring | $15 | Home Depot |
| 1 | Junction Box | 8x8x4" NEMA | $15 | Home Depot |
| 10 | Wire terminals | Fork and ring | $10 | Amazon |

**Electrical Subtotal:** ~$265-315

### Mechanical

| Qty | Part | Description | Est. Cost | Source |
|-----|------|-------------|-----------|--------|
| 20ft | Unistrut | 1-5/8" channel, 12ga | $60 | Home Depot |
| 8 | Unistrut fittings | Corners, angles | $25 | Home Depot |
| 1 | Drive Pulley | 2" V-belt pulley, 5/8" bore | $15 | Amazon |
| 1 | Driven Pulley | 8" V-belt pulley | $25 | Amazon |
| 1 | V-Belt | 3L or A section, size to fit | $10 | Amazon |
| 2 | Pillow Block | 5/8" bore, UCP201-8 | $20 | Amazon |
| 1 | Conveyor Roller | 2" OD, 12" wide | $40 | Amazon |
| 1 | Belt Material | PVC, 6" x 60" | $30 | Amazon |
| 1 | Idler Roller | 1.5" OD, 12" wide | $25 | Amazon |
| Misc | Hardware | Bolts, nuts, washers | $30 | Home Depot |

**Mechanical Subtotal:** ~$280

### Optional/Future

| Qty | Part | Description | Est. Cost |
|-----|------|-------------|-----------|
| 3 | Prox Sensors | M12, NPN, 24VDC | $30 |
| 2 | Pneumatic Cylinders | Pusher actuators | $60 |
| 1 | Air Solenoid Valve | 5/2, 24VDC coil | $25 |
| 1 | FRL Unit | Filter/regulator/lubricator | $40 |

---

## 🔌 VFD PARAMETER SHEET

### GS11N-20P5 (AutomationDirect GS1 Series)

| Param | Name | Set Value | Notes |
|-------|------|-----------|-------|
| P00 | Motor HP | 0.5 | Match motor |
| P01 | Motor Voltage | 230 | Or 208 |
| P02 | Motor Amps | 2.4 | Per nameplate |
| P03 | Base Frequency | 60 | Hz |
| P04 | Max Frequency | 60 | Hz |
| P05 | Accel Time | 3 | Seconds |
| P06 | Decel Time | 3 | Seconds |
| P07 | Source Select | 1 | Terminal control |
| P08 | Freq Source | 1 | VI terminal (0-10V) |
| P12 | Multi-Speed 1 | 30 | Hz (50% speed preset) |
| P40 | Motor Control | 0 | V/F control |

### Terminal Configuration

| Terminal | Function | Wire From |
|----------|----------|-----------|
| L1, L2 | AC Input | 220V supply |
| U, V, W | Motor Output | Motor leads |
| FWD | Run Forward | Micro820 DO1 |
| REV | Run Reverse | Micro820 DO2 |
| DCM | Digital Common | Micro820 COM |
| VI | Speed Input | Micro820 AO1 |
| ACM | Analog Common | Micro820 AGND |
| FA, FB | Fault Relay | Micro820 DI |

---

## 📝 PLC PROGRAM OUTLINE

### I/O Assignment (Micro820)

| Address | Type | Description |
|---------|------|-------------|
| _IO_EM_DI_00 | Input | Start Button |
| _IO_EM_DI_01 | Input | Stop Button (NC) |
| _IO_EM_DI_02 | Input | E-Stop (NC) |
| _IO_EM_DI_03 | Input | VFD Fault |
| _IO_EM_DI_04 | Input | Sensor 1 - Entry |
| _IO_EM_DI_05 | Input | Sensor 2 - High |
| _IO_EM_DI_06 | Input | Sensor 3 - Low |
| _IO_EM_DO_00 | Output | VFD FWD |
| _IO_EM_DO_01 | Output | VFD REV |
| _IO_EM_DO_02 | Output | Indicator Light |
| _IO_EM_AO_00 | Analog Out | Speed Reference (0-10V) |

### Ladder Logic Rungs

```
RUNG 1: START/STOP SEAL-IN
[Start]──[/Stop]──[/EStop]──[/Fault]──(Run_Latch)──
                                           │
         [Run_Latch]───────────────────────┘

RUNG 2: RUN FORWARD OUTPUT
[Run_Latch]──(VFD_FWD)──

RUNG 3: SPEED CONTROL
[Run_Latch]──[MOV: Speed_SP → AO_00]──

RUNG 4: FAULT DETECTION
[VFD_Fault]──(TON: Fault_Timer)──
[Fault_Timer.DN]──(System_Fault)──

RUNG 5: PILOT LIGHT
[Run_Latch]──(Pilot_Light)──
```

---

## ✅ COMMISSIONING CHECKLIST

### Pre-Power Checks
- [ ] Verify all wiring matches prints
- [ ] Check motor nameplate vs VFD settings
- [ ] Confirm rotation direction needed
- [ ] Tighten all connections
- [ ] Verify ground continuity
- [ ] Check belt tension and alignment

### Power-Up Sequence
1. [ ] Turn on 24VDC supply
2. [ ] Verify PLC powers up
3. [ ] Turn on VFD disconnect
4. [ ] Verify VFD displays no faults
5. [ ] Jog motor briefly at low speed
6. [ ] Check rotation (reverse if needed)
7. [ ] Run at 50% speed for 2 minutes
8. [ ] Check for vibration or noise
9. [ ] Run at 100% speed
10. [ ] Verify all controls work

### Factory I/O Integration
- [ ] Connect Factory I/O to Micro820
- [ ] Map all I/O tags
- [ ] Start physical conveyor
- [ ] Verify Factory I/O belt moves in sync
- [ ] Test stop/start synchronization
- [ ] Record video of both running

---

## 📞 SUPPORT CONTACTS

| Role | Name | Phone |
|------|------|-------|
| Service Manager | Jarvis AI | (Telegram) |
| Motor Supplier | Grainger Orlando | (407) 857-3780 |
| VFD Support | AutomationDirect | (800) 633-0405 |
| PLC Support | Rockwell | (440) 646-3434 |

---

## 📎 ATTACHMENTS

1. Motor spec sheet (download from Amazon listing)
2. VFD GS11N manual (AutomationDirect website)
3. Micro820 I/O wiring diagram (CCW project file)
4. Factory I/O scene file (export from app)

---

**Job Packet Prepared By:** Jarvis AI Service Manager
**Date:** 2026-02-06 14:36 UTC
**Revision:** 1.0

---

*"A good service manager gives the tech everything they need to succeed. Now go build something.*"
