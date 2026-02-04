# FactoryLM Edge Configurator - Product Vision

*Created: Feb 3, 2026*
*Author: Mike Harper*
*Status: VISION → Implementation*

---

## The Concept

A revolutionary product page featuring the FactoryLM Edge adapter as the center of an industrial connectivity universe.

### Visual Design (Apple-Style)

```
                    ┌─────────────┐
                    │   Glasses   │ ← Click to explore
                    │   (Halo)    │
                    └─────────────┘
                          │
    ┌───────────┐         │         ┌───────────┐
    │  Analog   │─────────┼─────────│  Serial   │
    │  Pack     │         │         │  Pack     │
    └───────────┘         │         └───────────┘
                          │
              ╔═══════════════════════╗
              ║                       ║
              ║   FactoryLM Edge      ║  ← Central black box
              ║   [ADAPTER]           ║    Rotates in 3D
              ║                       ║
              ╚═══════════════════════╝
                          │
    ┌───────────┐         │         ┌───────────┐
    │ Pneumatic │─────────┼─────────│  Remote   │
    │  Pack     │         │         │   I/O     │
    └───────────┘         │         └───────────┘
                          │
                    ┌─────────────┐
                    │   Legacy    │
                    │   Adapters  │
                    └─────────────┘
```

### Key Features

1. **The Black Box (Hero)**
   - FactoryLM Edge adapter rendered in 3D
   - Sleek, minimal, on its edge (like a monolith)
   - User can rotate/spin it
   - Shows ports and connections as you rotate

2. **Orbital Products**
   - Accessories orbit around the central device
   - Brilliant Labs Halo glasses
   - Analog Packs (AP-4, AP-8)
   - Pneumatic Pack (PP-1)
   - Remote I/O (IO-8)
   - Serial Pack (SP-2)
   - Legacy adapters (RS-232, RS-485, etc.)

3. **Click to Explore**
   - Each orbiting product is clickable
   - Opens detailed product page
   - Shows compatibility, specs, pricing

4. **Product Configurator Wizard**
   - "Pick Your System" button
   - Step 1: What PLC brand? (Allen-Bradley, Siemens, etc.)
   - Step 2: What fieldbus? (EtherNet/IP, Modbus, Profinet, etc.)
   - Step 3: What I/O needs? (Analog, Digital, Pneumatic)
   - Result: Recommended bundle + accessories
   - One-click purchase

---

## Legacy Technology Support

**Goal:** Connect back to the most basic industrial networks (even what's running in Venezuela!)

### Supported Protocols (Past → Present)

| Era | Protocol | Adapter Needed |
|-----|----------|----------------|
| 1970s | 4-20mA Current Loop | Analog Pack |
| 1980s | RS-232 Serial | SP-2 |
| 1980s | RS-485 Multidrop | SP-2 |
| 1990s | Modbus RTU | Built-in |
| 1990s | DeviceNet | CAN adapter |
| 2000s | Modbus TCP | Built-in |
| 2000s | EtherNet/IP | Built-in |
| 2010s | Profinet | Adapter |
| 2020s | MQTT/REST | Built-in |

**Message:** "From 1970s current loops to modern AI - one adapter connects it all."

---

## Page Structure

```
factorylm.com/edge
├── /edge (Hero + 3D orbit)
├── /edge/glasses (Brilliant Labs Halo)
├── /edge/analog (AP-4, AP-8)
├── /edge/pneumatic (PP-1)
├── /edge/io (IO-8)
├── /edge/serial (SP-2)
├── /edge/legacy (RS-232, RS-485, 4-20mA history)
└── /edge/configurator (Pick your system wizard)
```

---

## Technical Implementation

### Phase 1: Static MVP
- Hero section with Edge product image
- Grid of orbiting products (CSS animations)
- Click through to product pages
- Simple configurator form

### Phase 2: 3D Interactive
- Three.js or Spline for 3D model
- Rotate/zoom on the Edge adapter
- Animated orbits
- Product hotspots

### Phase 3: Full Configurator
- Database of PLC systems
- Compatibility matrix
- Dynamic bundle builder
- Stripe checkout integration

---

## Inspirations

- Apple product pages (iPhone, AirPods)
- Tesla vehicle configurator
- Figma's 3D product reveals

---

## Files to Create

1. `/edge/index.html` - Main hero + orbit
2. `/edge/configurator.html` - Pick your system wizard
3. `/edge/products/*.html` - Individual product pages
4. `/assets/3d/edge-adapter.glb` - 3D model (later)
5. `/assets/images/products/` - Product photography

---

*This is the future of industrial hardware shopping.*
