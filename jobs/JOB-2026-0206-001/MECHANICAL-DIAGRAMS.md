# Demo Conveyor - Mechanical Build Diagrams

**Job:** JOB-2026-0206-001  
**Purpose:** YC Demo Conveyor with VFD Control

---

## 1. FRAME ASSEMBLY - TOP VIEW

```
                         48" (Side Rails)
    ←─────────────────────────────────────────────→
    
    ┌─────────────────────────────────────────────┐
    │░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░│ ← Side Rail (Superstrut)
    │                                             │
    │    ┌───┐                         ┌───┐     │
    │    │   │    HEAD ROLLER          │   │     │  14"
    │    │   │    (Drive End)          │   │     │  Width
    │    └───┘                         └───┘     │
    │      ↑                             ↑       │
    │      Cross Brace                   Cross   │
    │                                    Brace   │
    │                                            │
    │                                            │
    │    ┌───┐                         ┌───┐    │
    │    │   │    TAIL ROLLER          │   │    │
    │    │   │    (Idler End)          │   │    │
    │    └───┘                         └───┘    │
    │                                           │
    │░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░│ ← Side Rail (Superstrut)
    └───────────────────────────────────────────┘
    
    ▼   ▼                               ▼   ▼
   Leg  Leg                            Leg  Leg
```

---

## 2. FRAME ASSEMBLY - SIDE VIEW

```
                    48" Total Length
    ←───────────────────────────────────────────→
    
         HEAD END                    TAIL END
         (Motor)                     (Idler)
            
    ┌────────────────────────────────────────────┐
    │▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓│ ← BELT (on top)
    ├────────────────────────────────────────────┤
    │            SIDE RAIL (48")                 │ ← Superstrut Channel
    ├────────────────────────────────────────────┤
    
       ◯                                    ◯      ← Rollers (12" pipe)
      ╱│╲                                  ╱│╲
     ╱ │ ╲                                ╱ │ ╲
    ║  │  ║                              ║  │  ║   ← Pillow Block Bearings
    ║  │  ║                              ║  │  ║
    ║  │  ║                              ║  │  ║
    ║  │  ║ ← LEG                        ║  │  ║
    ║  │  ║   (36")                      ║  │  ║
    ║  │  ║                              ║  │  ║
    ║  │  ║                              ║  │  ║
    ╚══╧══╝                              ╚══╧══╝
       ▲                                    ▲
    Floor                                Floor
    Flange                               Flange
    
    ├──────────────── ~42" ────────────────┤
              (Between Rollers)
```

---

## 3. ROLLER DETAIL - CROSS SECTION

```
                    14" (Frame Width)
         ←─────────────────────────────────→
         
    ┌─────────────────────────────────────────┐
    │░░░░░░░░░░░│             │░░░░░░░░░░░░░░░│  ← Side Rails
    │           │             │               │
    │  ┌────┐   │             │   ┌────┐      │
    │  │////│   │             │   │////│      │  ← Pillow Block
    │  │////│   │             │   │////│      │    Bearings (UCP201)
    │  └──┬─┘   │             │   └──┬─┘      │
    │     │     │             │      │        │
    ╠═════╪═════╪═════════════╪══════╪════════╣  ← 5/8" Steel Shaft
    │     │     │             │      │        │    (12" long)
    │  ┌──┴─┐   │             │   ┌──┴─┐      │
    │  │    │   │             │   │    │      │
    │  │    │   │    ROLLER   │   │    │      │
    │  │    │   │  (1-1/4"    │   │    │      │  ← 1-1/4" Black Pipe
    │  │    │   │   pipe)     │   │    │      │    (sleeved on shaft)
    │  │    │   │             │   │    │      │
    │  └────┘   │             │   └────┘      │
    │           │             │               │
    └───────────┴─────────────┴───────────────┘
    
    Note: Shaft collars lock pipe in place on shaft
```

---

## 4. DRIVE SYSTEM - HEAD END DETAIL

```
                MOTOR MOUNT (Side View)
    
                        ┌─────────┐
                        │  MOTOR  │
                        │  1.5HP  │
                        │ 3-Phase │
                        └────┬────┘
                             │
                             │ Motor Shaft (5/8")
                             │
                        ┌────┴────┐
                        │ 2" Small│ ← Drive Pulley
                        │ Pulley  │   (on motor)
                        └────┬────┘
                             │
                    ═════════╪═════════  ← V-Belt (3L)
                             │
                        ┌────┴────┐
                        │ 6" Large│ ← Driven Pulley
                        │ Pulley  │   (on roller shaft)
                        └────┬────┘
                             │
    ════════════════════════╪════════════════════════
                   HEAD ROLLER SHAFT
    
    
    Pulley Ratio: 6:2 = 3:1 reduction
    Motor: 1725 RPM → Roller: ~575 RPM
    Belt Speed: ~15 ft/min (adjustable via VFD)
```

---

## 5. DRIVE SYSTEM - TOP VIEW

```
         ┌─────────────────────────────────────┐
         │          CONVEYOR FRAME             │
         │                                     │
    ┌────┼──────────◯──────────────────────────┤
    │    │      HEAD ROLLER                    │
    │    │          │                          │
    │    │    ┌─────┴─────┐                    │
    │    │    │ 6" Pulley │                    │
    │    │    └─────┬─────┘                    │
    │    │          │                          │
    │    │     V-Belt (3L)                     │
    │    │          │                          │
    │    │    ┌─────┴─────┐                    │
    │    │    │ 2" Pulley │                    │
    │    │    └─────┬─────┘                    │
    │    │          │                          │
    │    │    ┌─────┴─────┐                    │
    │    │    │   MOTOR   │ ← Mounted to frame │
    │    │    │           │   with L-bracket   │
    │    │    └───────────┘                    │
    │    │                                     │
    └────┼─────────────────────────────────────┤
         └─────────────────────────────────────┘
```

---

## 6. BELT TENSIONING SYSTEM

```
    HEAD END                              TAIL END
    (Fixed)                               (Adjustable)
    
    ════════╦════════════════════════════════╦════════
            ║                                ║
       ┌────╨────┐                      ┌────╨────┐
       │ Bearing │                      │ Bearing │
       │ (fixed) │                      │ (slots) │ ← Slotted holes
       └─────────┘                      └────┬────┘   allow adjustment
                                             │
                                        ◄────┴────►
                                        Adjust for
                                        belt tension
    
    ADJUSTMENT DETAIL (Tail End):
    ┌─────────────────┐
    │  ═══════════    │ ← Slotted mounting hole
    │       ◯         │   in cross brace
    │  ═══════════    │
    │       ↑         │
    │   Bearing       │
    │   bolt slides   │
    │   in slot       │
    └─────────────────┘
```

---

## 7. COMPLETE ASSEMBLY - ISOMETRIC VIEW

```
                              ╱╲
                             ╱  ╲
                            ╱ M  ╲ ← Motor
                           ╱  O   ╲
                          ╱   T    ╲
                         ╱    O     ╲
                        ╱     R      ╲
                       ╱_______________╲
                            │ │
                       ┌────┴─┴────┐
                       │  Pulley   │
                       └─────┬─────┘
                             │ Belt
    ┌────────────────────────┼──────────────────────────┐
    │░░░░░░░░░░░░░░░░░░░░░░░░│░░░░░░░░░░░░░░░░░░░░░░░░░░│
    │▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓│ ← Belt Surface
    ├──────◯─────────────────────────────────────◯──────┤
    │    HEAD                                  TAIL    │
    │   ROLLER                                ROLLER   │
    ║      ║                                    ║      ║
    ║      ║ ← Legs (36")                       ║      ║
    ║      ║                                    ║      ║
    ╚══════╝                                    ╚══════╝
      ████                                        ████
    Floor Flanges                            Floor Flanges
    
    
    OVERALL DIMENSIONS:
    • Length: 48"
    • Width: 14" (frame) / 6" (belt)
    • Height: 36" (to belt surface)
```

---

## 8. CUT LIST REMINDER

| Piece | Material | Length | Qty |
|-------|----------|--------|-----|
| Side Rails | Superstrut | 48" | 2 |
| Cross Braces | Superstrut | 14" | 4 |
| Legs | Superstrut | 36" | 4 |
| Roller Shafts | 5/8" Steel Rod | 12" | 2 |
| Roller Tubes | 1-1/4" Black Pipe | ~10" | 2 |

---

## 9. ASSEMBLY SEQUENCE

1. **Build the rectangular top frame** (2 side rails + 4 cross braces)
2. **Attach legs** at four corners with 90° fittings
3. **Install floor flanges** on leg bottoms
4. **Mount pillow block bearings** on cross braces (head & tail)
5. **Assemble rollers** (shaft through pipe, shaft collars to lock)
6. **Install rollers** into pillow blocks
7. **Mount motor** with L-bracket at head end
8. **Install pulleys** (small on motor, large on head roller shaft)
9. **Install V-belt** and tension
10. **Install belt material** over rollers, join ends
11. **Adjust tail roller** for proper belt tension

---

**Ready for electrical diagrams when you approve! ⚡**
