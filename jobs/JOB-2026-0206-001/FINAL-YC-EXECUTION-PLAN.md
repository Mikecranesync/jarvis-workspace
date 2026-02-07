# 🚀 FACTORYLM YC DEMO - FINAL EXECUTION PLAN
## Deadline: Feb 9, 2026 11:59 PM EST

**Time Remaining: ~2 days, 11 hours**

---

## 📋 EXECUTIVE SUMMARY

**What we're building:** A VFD-controlled conveyor demonstrating FactoryLM's maintenance copilot

**The YC thesis:** "You don't need more AI. You need less chaos."

**The demo proves:**
1. Real hardware controlled by PLC
2. FactoryLM predicts/prevents failures
3. 98% of intelligence is FREE (logic, not LLM)

---

## ✅ ALREADY DONE

### Materials (Cut & Ready)
- [x] PVC: 2x 14" (rollers)
- [x] Dowel: 2x 16" (shafts)  
- [x] 2x4: 2x 48" (rails) + 4x 14" (braces) + 4x 30" (legs)
- [x] Threaded rod: 2x 18"
- [x] Plywood: 1x 12"x12" (motor mount)
- [x] Belt: 6" x 120" rubber shelf liner

### Infrastructure
- [x] Hetzner VPS migrated (8GB RAM, all services running)
- [x] CMMS (Atlas) running
- [x] YC application drafted
- [x] Pitch deck core thesis written
- [x] Architecture diagrams created

### Equipment (On Hand)
- [x] VFD (ordered/arrived?)
- [x] Motor (ordered/arrived?)
- [x] Micro820 PLC
- [x] Basic tools, screws, etc.

---

## 🔧 BUILD SCHEDULE

### DAY 1: TODAY (Feb 7) - BUILD THE CONVEYOR

| Time | Task | Duration | Checkpoint |
|------|------|----------|------------|
| NOW | Set up video capture (Google Photos backup ON) | 5 min | ✓ |
| +5 min | **PHASE 1: Frame Base** | 30 min | 📸 Photo |
| +35 min | **PHASE 2: Attach Legs** | 15 min | 📸 Photo |
| +50 min | **PHASE 3: Build Rollers** | 20 min | 📸 Photo |
| +70 min | **PHASE 4: Mount Rollers** | 15 min | 📸 Photo |
| +85 min | **PHASE 5: Motor Mount** | 15 min | 📸 Photo |
| +100 min | **PHASE 6: Belt Install** | 10 min | 📸 Photo |
| +110 min | **PHASE 7: Wire VFD + Test** | 30 min | 🎥 VIDEO! |
| **~2.5 hrs** | **CONVEYOR RUNNING** | | 🎉 |

---

## 🔨 BUILD INSTRUCTIONS (DETAILED)

### PHASE 1: Frame Base (30 min)

```
        ←─────────── 48" ───────────→
        
    ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
    ┃        2x4 SIDE RAIL              ┃
    ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
        ┃           ┃           ┃
        ┃  14"      ┃   14"     ┃  14"     ← Cross braces
        ┃  BRACE    ┃   BRACE   ┃  BRACE
        ┃           ┃           ┃
    ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
    ┃        2x4 SIDE RAIL              ┃
    ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
    
    Frame inside width: 14"
```

**Steps:**
1. Lay two 48" 2x4s parallel on ground
2. Space them 14" apart (inside edge to inside edge)
3. Place 14" cross braces at both ends, flush with rail ends
4. Add 2 more braces evenly spaced in middle
5. Pre-drill, then drive 2x 3" deck screws per joint
6. Check square with speed square

**📸 PHOTO: Frame assembled flat on ground**

---

### PHASE 2: Attach Legs (15 min)

```
    SIDE VIEW:
    
    ┌─────────────────────────────────────────┐
    │▓▓▓▓▓▓▓▓▓▓▓▓▓ FRAME TOP ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓│
    └──┬─────────────────────────────────┬────┘
       │                                 │
       │                                 │
       │  30" LEG                        │  30" LEG
       │                                 │
       │                                 │
       ▼                                 ▼
    ════════════════════════════════════════════
                    FLOOR
    
    Working height: ~32" (comfortable)
```

**Steps:**
1. Flip frame right-side up (or have helper hold)
2. Position 30" legs at all 4 corners, on OUTSIDE of frame
3. Drive 2-3 angled screws per leg into frame
4. Check all legs touch floor evenly
5. Verify frame is level

**📸 PHOTO: Frame standing on legs**

---

### PHASE 3: Build Rollers (20 min)

```
    ROLLER CROSS-SECTION:
    
              ←────── 16" wooden dowel ──────→
              
    ══════════●━━━━━━━━━━━━━━━━━━━━━●══════════
              │                     │
              │    14" PVC PIPE     │
              │◄───────────────────►│
              │                     │
            1" overhang          1" overhang
            each side            each side
```

**Steps:**
1. Take 14" PVC pipe
2. Slide 16" wooden dowel through center
3. Center it so 1" sticks out each side
4. Drill small pilot hole through PVC into dowel
5. Drive short screw to lock dowel in place (prevents spinning)
6. **Repeat for second roller**

**📸 PHOTO: Both rollers assembled**

---

### PHASE 4: Mount Rollers (15 min)

```
    TOP VIEW - Roller positions:
    
    ┌──────────────────────────────────────────┐
    │                                          │
    │    ═══════════════════════  HEAD ROLLER  │  ← Motor connects here
    │            ▲                             │
    │         U-notch                          │
    │         in brace                         │
    │                                          │
    │         (belt travels →)                 │
    │                                          │
    │            ▼                             │
    │    ═══════════════════════  TAIL ROLLER  │  ← Idler (free spinning)
    │                                          │
    └──────────────────────────────────────────┘
```

**Steps:**
1. At HEAD end (motor side): cut U-shaped notches in cross brace
   - Notch width = dowel diameter + tiny clearance
   - Notch depth = ~1" (so roller sits in it)
2. At TAIL end: same notches
3. Drop rollers into notches - dowel ends rest in U-notches
4. Spin by hand - should rotate freely
5. Add small wood block screwed above each notch to keep roller from popping up

**📸 PHOTO: Rollers mounted, spinning freely**

---

### PHASE 5: Motor Mount (15 min)

```
    HEAD END DETAIL:
    
              ┌────────────┐
              │   12"x12"  │
              │  PLYWOOD   │
              │            │
              │   MOTOR    │
              │    ⚙️      │
              └─────┬──────┘
                    │
                    │  shaft
                    ▼
    ═══════════════════════════  HEAD ROLLER
    
    Motor shaft → Coupler or Pulley → Roller shaft
```

**Steps:**
1. Position 12"x12" plywood at head end of frame
2. Screw plywood to frame (4+ screws)
3. Hold motor in position to mark mounting holes
4. Drill holes, bolt motor down
5. Align motor shaft with roller shaft
6. Connect via:
   - Direct coupling (if shafts match), OR
   - Pulley + belt system

**📸 PHOTO: Motor mounted and aligned**

---

### PHASE 6: Belt Install (10 min)

```
    SIDE VIEW - Belt path:
    
              ┌───────────────────────────────┐
    ──────────┤  BELT ON TOP (carrying side)  ├──────────
              │                               │
            ◯─┘                               └─◯
          HEAD                                TAIL
         ROLLER                              ROLLER
            │                                  │
            └──────────────────────────────────┘
                   BELT UNDERNEATH (return)
```

**Steps:**
1. Drape 6"x120" rubber shelf liner over both rollers
2. Pull ends underneath
3. Tension: snug but not super tight
4. Join ends:
   - Option A: Overlap 2-3" and staple heavily
   - Option B: Contact cement the overlap
   - Option C: Use belt lacing if you have it
5. Test by spinning roller by hand - belt should move smoothly

**📸 PHOTO: Belt installed and tensioned**

---

### PHASE 7: Wire & Test (30 min)

```
    ELECTRICAL:
    
    ┌──────────┐      ┌──────────┐      ┌──────────┐
    │  120V    │──────│   VFD    │──────│  MOTOR   │
    │  OUTLET  │      │          │      │          │
    └──────────┘      └──────────┘      └──────────┘
                           │
                      Speed Control
                      Start/Stop
```

**Steps:**
1. **POWER OFF** - verify outlet is off
2. Wire VFD input to 120V (follow VFD manual for terminals)
3. Wire VFD output to motor (U, V, W or T1, T2, T3)
4. Set VFD parameters:
   - Motor voltage
   - Motor Hz (60Hz for US)
   - Usually has auto-tune feature
5. **TEST AT LOW SPEED FIRST**
6. Increase speed gradually
7. Listen for unusual sounds
8. Watch belt tracking

**🎥 VIDEO: Record the first run! Multiple angles!**

---

## 📹 VIDEO CAPTURE PLAN

### Setup (Before Building)
1. Turn ON Google Photos backup on Pixel 9a
2. Position phone(s) to capture work area
3. Good lighting (natural or shop lights)

### During Build
- Photo at each phase completion
- Short video clips of key moments
- Final glamour shots of completed conveyor

### The Money Shot 🎬
- 30-60 second video of conveyor RUNNING
- Show VFD speed control
- Show belt moving smoothly
- Voiceover explaining what FactoryLM does

---

## 🎯 YC DEMO SCRIPT

### The Problem (10 sec)
"Maintenance teams waste 30% of their time on paperwork and hunting for information."

### The Solution (20 sec)
"FactoryLM is an AI copilot for maintenance - but here's the twist: 98% of answers come from logic, not expensive AI calls."

### The Demo (30 sec)
*[Show conveyor running]*
"This conveyor is controlled by a PLC. FactoryLM monitors it, predicts failures, and guides technicians - but every time AI answers a question, that answer hardens into a rule. The system gets smarter by needing LESS AI."

### The Ask (10 sec)
"We're looking for $500K to deploy at 10 beta sites. Our first customer is ready."

---

## 📊 YC APPLICATION CHECKLIST

- [x] Company description
- [x] Problem statement
- [x] Solution (Layer 0-3 architecture)
- [x] Traction (Mike's 30 years + brother as beta user)
- [x] Market size ($15B CMMS market)
- [x] Team (Mike = IS the customer)
- [ ] **Demo video** ← BUILD THIS TODAY
- [ ] Final review and submit

---

## ⏰ REMAINING SCHEDULE

### Feb 7 (Today)
- [ ] Build conveyor (2-3 hours)
- [ ] Film demo video
- [ ] Upload to YouTube/Google Drive

### Feb 8 (Tomorrow)
- [ ] Review YC application
- [ ] Polish demo video if needed
- [ ] Prepare any additional materials
- [ ] **REST** - don't burn out before deadline

### Feb 9 (Deadline Day)
- [ ] Final review 
- [ ] Submit before 11:59 PM EST
- [ ] 🎉 Celebrate

---

## 🆘 IF THINGS GO WRONG

### Motor won't spin
- Check VFD error codes
- Verify wiring (U-V-W order matters)
- Try reversing two motor leads

### Belt slips
- Increase tension
- Add friction (sandpaper on rollers)
- Check roller alignment

### Rollers won't turn
- Notches too tight - widen them
- Add grease/wax to dowel
- Check for obstructions

### VFD trips
- Reduce acceleration time
- Check motor current vs VFD rating
- Verify parameters

---

## 📞 CONTACTS

- **Jarvis (VPS):** Always here
- **Local electrical supply:** Graybar Lake Wales 863-XXX-XXXX
- **Hardware store:** Home Depot, Walmart

---

## 💡 REMEMBER

> "You don't need more AI. You need less chaos."

> "LLMs are encyclopedias. Maintenance needs a diary."

> "Every AI answer hardens into a rule. The system gets smarter by needing LESS intelligence."

---

**LET'S BUILD! 🏭🔧**

*Last updated: 2026-02-07 13:24 UTC*
