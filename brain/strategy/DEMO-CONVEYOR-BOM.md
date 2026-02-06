# YC Demo Conveyor System - Bill of Materials
*Small conveyor matching Factory IO simulation style*

**Goal:** Build a functional conveyor demo that can be controlled by the Micro820 PLC, demonstrating real industrial automation on a budget.

---

## 🔌 VFD (Variable Frequency Drive) - ORDER TONIGHT

### Recommended: ATO 1HP VFD 110V Input
- **Amazon:** https://www.amazon.com/Single-Output-Variable-Frequency-Control/dp/B0897B6CRR
- **Price:** ~$90-110
- **Specs:** 110V single phase input → 220V 3-phase output
- **Why this one:** 
  - Designed for 110V household outlets
  - Has Modbus RS485 for PLC integration
  - Can control speed 0-400Hz
  - 1HP is plenty for a small demo conveyor

### Alternative: Generic 750W VFD
- **Amazon:** https://www.amazon.com/Generic-110-220V-Variable-Frequency-Converter/dp/B0D53Z7RZ5
- **Price:** ~$50-70
- **Specs:** 110-220V input, 750W
- **Cheaper but less reliable brand**

### VFD Integration Notes:
- Most have RS485 Modbus - can control from Micro820
- Need a small 3-phase motor OR use VFD single-phase output mode
- Set parameters: motor voltage, frequency, accel/decel times

---

## 🛒 Home Depot / Lowe's Parts List

### Frame (Aluminum/Wood)
| Item | Qty | Est. Price | Notes |
|------|-----|------------|-------|
| 1x4 Pine board, 6ft | 2 | $8 | Side rails |
| 2x4 Pine, 8ft | 1 | $6 | Base/supports |
| Aluminum angle 1"x1", 4ft | 2 | $20 | Optional: more rigid |
| Wood screws assorted | 1 box | $8 | Assembly |
| **Subtotal** | | **~$42** | |

### Rollers (PVC Method)
| Item | Qty | Est. Price | Notes |
|------|-----|------------|-------|
| 1" PVC pipe, 10ft | 1 | $5 | Cut into rollers |
| 1" PVC caps | 6 | $6 | End caps for rollers |
| 608 bearings (skateboard) | 6 | $12 | Amazon - pack of 10 |
| 5/16" threaded rod, 3ft | 1 | $5 | Axles through bearings |
| Nuts & washers 5/16" | 1 pack | $5 | Secure axles |
| **Subtotal** | | **~$33** | |

### Belt Material
| Item | Qty | Est. Price | Notes |
|------|-----|------------|-------|
| Canvas drop cloth, 4x12ft | 1 | $15 | Cut to width, sew loop |
| OR: Rubber mat (thin) | 1 | $20 | Alternative belt material |
| OR: Wide rubber band/belt | 1 | $15 | Amazon - easier option |
| **Subtotal** | | **~$15-20** | |

### Motor Options (if not using VFD + 3-phase)

**Option A: DC Gear Motor (simpler)**
| Item | Qty | Est. Price | Notes |
|------|-----|------------|-------|
| 12V/24V DC gear motor | 1 | $25 | Amazon - 30-60 RPM |
| 12V power supply | 1 | $15 | Or 24V matching motor |
| PWM speed controller | 1 | $10 | Simple speed control |
| **Subtotal** | | **~$50** | |

**Option B: Small AC Motor + VFD (industrial demo)**
| Item | Qty | Est. Price | Notes |
|------|-----|------------|-------|
| Small 3-phase motor | 1 | $80-150 | Amazon/eBay - 1/4-1/2 HP |
| VFD (from above) | 1 | $90-110 | ATO 1HP recommended |
| **Subtotal** | | **~$180-260** | |

### Drive Mechanism
| Item | Qty | Est. Price | Notes |
|------|-----|------------|-------|
| V-belt pulley, 2" | 2 | $12 | Motor to roller |
| V-belt, size A | 1 | $8 | Match pulley distance |
| Motor mount plate | 1 | $10 | Or fabricate from wood |
| **Subtotal** | | **~$30** | |

---

## 📦 Amazon Orders (Order Tonight)

### Must-Have for VFD Demo
1. **ATO 1HP VFD 110V Input** - $100
   - https://www.amazon.com/dp/B0897B6CRR

2. **Small 3-Phase Motor 1/4HP** - $80
   - Search: "1/4 HP 3 phase motor 220V"
   - Or: Use a standard AC motor in single-phase VFD mode

3. **608 Bearings (10-pack)** - $10
   - Essential for smooth rollers

4. **12V DC Gear Motor 30RPM (backup)** - $20
   - Simpler option if VFD integration is tricky

### Nice-to-Have
- Photoelectric sensors (through-beam) - $30/pair
- Proximity sensors (inductive) - $15 each
- Mini conveyor belt kit (pre-made) - $50-80

---

## 💰 Total Cost Estimates

### Budget Build (DC Motor)
| Category | Cost |
|----------|------|
| Frame | $42 |
| Rollers | $33 |
| Belt | $20 |
| DC Motor + Controller | $50 |
| Misc (wire, connectors) | $20 |
| **TOTAL** | **~$165** |

### Full Industrial Demo (VFD + 3-Phase)
| Category | Cost |
|----------|------|
| Frame | $42 |
| Rollers | $33 |
| Belt | $20 |
| VFD | $100 |
| 3-Phase Motor | $80 |
| Drive (pulleys, belt) | $30 |
| Misc (wire, connectors) | $30 |
| **TOTAL** | **~$335** |

---

## ⏱️ Build Time Estimate

| Phase | Time | Notes |
|-------|------|-------|
| Shopping (Home Depot) | 2 hrs | One trip for wood/PVC |
| Frame construction | 3 hrs | Cut, drill, assemble |
| Roller assembly | 2 hrs | PVC + bearings |
| Belt fabrication | 1 hr | Cut canvas, sew loop |
| Motor mounting | 1 hr | Align, tension |
| Wiring + VFD setup | 2 hrs | Parameters, test |
| PLC integration | 2 hrs | Modbus to Micro820 |
| **TOTAL** | **~13 hours** | 2 solid days |

---

## 🎯 Factory IO Scene Match

This matches the **"Sorting by Height"** and **"From A to B"** Factory IO scenes:
- Single conveyor belt
- Start/stop control from PLC
- Variable speed via VFD
- Can add sensors for object detection

For the YC demo:
1. Conveyor moves small boxes/objects
2. Telegram bot shows "Conveyor: RUNNING / STOPPED"
3. Reviewer can control via bot: "Start conveyor" / "Stop conveyor"
4. Speed control: "Set speed 50%"

---

## 🛒 Tonight's Order (Before Bed)

**Amazon Cart:**
1. ATO 1HP VFD 110V - ~$100
2. 608 Bearings 10-pack - ~$10
3. 12V DC Gear Motor 30RPM (backup) - ~$20
4. Small 3-phase motor 1/4HP - ~$80 (optional)

**Total Amazon Order: ~$130-210**

**Tomorrow at Home Depot:**
- 1x4 pine (2x 6ft)
- 2x4 pine (1x 8ft)  
- 1" PVC pipe (10ft)
- 1" PVC caps (6)
- 5/16" threaded rod
- Nuts, washers, screws
- Canvas drop cloth

**Est. Home Depot: ~$50-60**

---

*Created: 2026-02-05 | Demo deadline: 4 days*
