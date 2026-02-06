# Dorner Gearbox Compatibility Report
**Job #:** 2026-0206-001  
**Date:** 2026-02-06  
**Prepared by:** Jarvis AI

---

## YOUR GEARBOX

| Field | Value |
|-------|-------|
| **Manufacturer** | Dorner Mfg. Corp. |
| **Location** | Hartland, WI USA |
| **Model Number** | 32M020HS |
| **Serial Number** | 516338-002-001-001 |
| **Gear Ratio** | 20:1 |
| **Motor Mount** | NEMA 56C |
| **Tech Support** | 800-397-8664 |

---

## MODEL NUMBER BREAKDOWN

**32M020HS** decodes as:
- **32** = Dorner 3200 Series conveyor system
- **M** = Motor drive package
- **020** = 20:1 gear ratio
- **H** = Heavy duty / High torque
- **S** = Standard mounting (56C)

---

## MOTOR REQUIREMENTS

### Must Have:
| Spec | Required Value | Why |
|------|----------------|-----|
| **Frame Size** | 56C | C-face mount to gearbox |
| **Shaft Diameter** | 5/8" (0.625") | Standard 56C shaft |
| **Shaft Length** | 1.875" min | Engages gearbox coupler |
| **Pilot Diameter** | 4.5" (4.500") | Registers in gearbox bore |
| **Bolt Circle** | 6.72" | 4-bolt pattern |
| **Voltage** | 208-230V or 460V | Match your VFD |
| **Phase** | 3-Phase | For VFD control |

### Recommended:
| Spec | Recommended | Why |
|------|-------------|-----|
| **HP** | 1/4 to 1/2 HP | Matches gearbox capacity |
| **RPM** | 1725-1800 | Standard 4-pole |
| **Duty** | Inverter Duty | VFD compatible |
| **Insulation** | Class F | Heat resistant |
| **Enclosure** | TEFC | Dust/moisture protection |

---

## OUTPUT CALCULATIONS

With a 1/2 HP, 1800 RPM motor + 20:1 gearbox:

| Parameter | Value |
|-----------|-------|
| **Input Speed** | 1800 RPM |
| **Gear Ratio** | 20:1 |
| **Output Speed** | **90 RPM** |
| **Input Torque** | ~18 in-lb (at 1/2 HP) |
| **Output Torque** | ~340 in-lb (minus efficiency loss) |

**90 RPM is ideal for small parts conveyors!**

With VFD speed control (10-60 Hz):
- Min speed: ~15 RPM
- Max speed: ~90 RPM
- Full range control from your PLC

---

## NEMA 56C FRAME DIMENSIONS

```
         ┌─────────────────────────┐
         │                         │
         │    ○           ○        │  ← Bolt holes (4x)
         │         ┌───┐           │
         │         │   │           │  ← Pilot (4.5" dia)
         │         │ ● │           │  ← Shaft (5/8" dia)
         │         │   │           │
         │         └───┘           │
         │    ○           ○        │
         │                         │
         └─────────────────────────┘

Dimensions:
- Bolt Circle (BC): 6.72"
- Bolt Size: 3/8-16
- Pilot Diameter: 4.500"
- Shaft Diameter: 0.625"
- Shaft Length: 1.875"
- Key: 3/16" x 3/16"
```

---

## COMPATIBLE MOTORS (Examples)

### Best Match - Marathon G581
- **Part #:** 5K49MN4065
- **HP:** 1/2
- **RPM:** 1800
- **Voltage:** 208-230/460V
- **Frame:** 56C
- **Duty:** Inverter, 10:1 CT
- **Price:** ~$180
- **Source:** Amazon, Grainger

### Alternative - WorldWide Electric
- **Part #:** AT12-18-56CB
- **HP:** 1/2
- **RPM:** 1800
- **Voltage:** 208-230/460V
- **Frame:** 56C
- **Duty:** Inverter rated
- **Price:** ~$150
- **Source:** Grainger, Motion

### Budget Option - Leeson/Regal
- **HP:** 1/2
- **Frame:** 56C
- **Look for:** "Inverter Duty" or "Vector Duty"
- **Price:** ~$120-150

---

## INSTALLATION NOTES

### Before Installing Motor:

1. **Clean the gearbox input bore** - Remove any rust/debris from the 4.5" pilot area
2. **Check shaft coupler** - Ensure the internal coupler isn't damaged
3. **Inspect o-ring/seal** - Replace if cracked
4. **Apply anti-seize** - Light coat on pilot surface

### Mounting Procedure:

1. Align motor shaft with gearbox coupler
2. Slide motor into pilot bore
3. Rotate shaft slightly to engage coupler splines
4. Insert 4x 3/8-16 bolts through motor flange
5. Torque to 15-20 ft-lb in cross pattern
6. Verify shaft rotates freely by hand

### Wiring:

- Connect motor leads to VFD output (U, V, W)
- Ground motor frame to VFD ground
- DO NOT connect motor directly to line power when using VFD

---

## GEARBOX MAINTENANCE

### Oil Check:
- Type: SAE 90 gear oil (or synthetic equivalent)
- Level: Fill to bottom of check plug
- Change interval: Every 2500 hours or annually

### Inspection Points:
- Output shaft seal (check for leaks)
- Input shaft bearing (listen for noise)
- Mounting bolts (check torque)

---

## DORNER SUPPORT

| Contact | Info |
|---------|------|
| **Tech Support** | 800-397-8664 |
| **Website** | www.dornerconveyors.com |
| **Parts** | parts@dornerconveyors.com |
| **Hours** | M-F 7 AM - 5 PM CT |

---

## SUMMARY

✅ **Your Dorner 32M020HS gearbox accepts any standard NEMA 56C motor**

**Go buy:**
> "56C frame, half horse, 3-phase, inverter duty motor"

**It will bolt right on.** No adapters needed.

---

*Report generated from Dorner documentation and NEMA standards*
