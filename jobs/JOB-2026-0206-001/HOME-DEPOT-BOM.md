# Demo Conveyor Build - Bill of Materials

**Job ID:** JOB-2026-0206-001  
**Purpose:** YC Demo - VFD-controlled conveyor with FactoryLM edge integration  
**Estimated Total:** ~$350 (Home Depot) + ~$37 (Amazon)

---

## 🏗️ FRAME (Electrical Aisle - Unistrut)

| Item | Qty | Unit Price | Total |
|------|-----|------------|-------|
| Superstrut 10ft channel | 4 | $18 | $72 |
| 90° angle fittings | 8 | $4 | $32 |
| Flat plate fittings | 4 | $3 | $12 |
| Box 3/8" strut bolts | 1 | $15 | $15 |
| Floor flanges (feet) | 4 | $6 | $24 |

**Subtotal:** $155

---

## 🔄 ROLLERS (Plumbing)

| Item | Qty | Unit Price | Total |
|------|-----|------------|-------|
| 1-1/4" black pipe, 12" long | 2 | $8 | $16 |
| 1-1/4" floor flanges | 2 | $8 | $16 |
| 5/8" x 12" steel rod (Metals dept) | 2 | $6 | $12 |

**Subtotal:** $44

---

## 🎢 BELT (Flooring/Outdoor)

| Item | Qty | Unit Price | Total |
|------|-----|------------|-------|
| Rubber stall mat or doormat | 1 | $25-45 | ~$35 |
| Contact cement | 1 | $8 | $8 |

**Subtotal:** ~$43

---

## ⚙️ DRIVE (Automotive)

| Item | Qty | Unit Price | Total |
|------|-----|------------|-------|
| 2" V-belt pulley 5/8" bore | 1 | $12 | $12 |
| 6" V-belt pulley 5/8" bore | 1 | $18 | $18 |
| 3L V-belt | 1 | $8 | $8 |

**Subtotal:** $38

---

## 🔩 HARDWARE

| Item | Qty | Unit Price | Total |
|------|-----|------------|-------|
| 1/4-20 bolts, nuts, washers assortment | 1 | $20 | $20 |
| Shaft collars, Loctite, misc | 1 | $20 | $20 |

**Subtotal:** $40

---

## 📦 AMAZON ORDER (not available at Home Depot)

| Item | Qty | Unit Price | Total |
|------|-----|------------|-------|
| Pillow block bearings UCP201-8 | 2 | $6 | $12 |
| PVC conveyor belt 6"x72" | 1 | $25 | $25 |

**Subtotal:** $37

---

## ✂️ CUT LIST

Cut from 10ft Superstrut channels:

| Piece | Length | Qty | Purpose |
|-------|--------|-----|---------|
| Side rails | 48" | 2 | Main frame sides |
| Cross braces | 14" | 4 | Frame width support |
| Legs | 36" | 4 | Vertical supports |

**Cutting notes:**
- Side rails: 2x 48" = 96" (fits on one 10ft channel)
- Cross braces: 4x 14" = 56" (fits on one 10ft channel)  
- Legs: 4x 36" = 144" (needs two 10ft channels)
- Total channels needed: 4 ✓

---

## 🔌 NOT INCLUDED (Already Have / Separate Purchase)

- VFD (Variable Frequency Drive) - PowerFlex 525 ~$200 used
- Motor - 1/4 HP 3-phase
- Micro820 PLC
- FactoryLM Edge Device

---

## 📐 Assembly Notes

1. Build frame first - test squareness
2. Install roller shafts with pillow blocks
3. Mount motor and VFD
4. Install belt and tension
5. Wire to Micro820 + FactoryLM edge
6. Test speed control via AI

**Target completion:** Before Feb 9 YC deadline
