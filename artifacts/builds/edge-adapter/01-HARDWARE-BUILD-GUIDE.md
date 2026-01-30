# Industrial Edge Adapter — Hardware Build Guide

**Project:** Network Ninja Passive Tap  
**Hardware:** BeagleBone Black Industrial  
**Date:** 2026-01-29

---

## Bill of Materials

| # | Item | Required | Notes |
|---|------|----------|-------|
| 1 | BeagleBone Black Industrial | ✅ Yes | The brain |
| 2 | USB-to-Ethernet Adapter | ✅ Yes | Second NIC for WireGuard |
| 3 | MicroSD Card (8GB+) | ⚠️ Optional | If not using eMMC |
| 4 | 5V 2A DC Power Supply | ✅ Yes | Barrel jack 5.5x2.1mm |
| 5 | Ethernet Cable #1 | ✅ Yes | To PLC network switch |
| 6 | Ethernet Cable #2 | ✅ Yes | To internet (or use WiFi/4G) |
| 7 | USB-A to Mini-USB Cable | ⚠️ Optional | For serial console/power |
| 8 | Enclosure | ⚠️ Optional | DIN-rail box for production |

---

## BeagleBone Black Industrial Specs

```
┌─────────────────────────────────────────────────────────┐
│                 BEAGLEBONE BLACK INDUSTRIAL             │
├─────────────────────────────────────────────────────────┤
│ Processor    │ AM3358 1GHz ARM Cortex-A8               │
│ RAM          │ 512MB DDR3                               │
│ Storage      │ 4GB eMMC + MicroSD slot                  │
│ Ethernet     │ 10/100 Mbps (built-in)                   │
│ USB          │ 1x USB Host, 1x Mini-USB (client)        │
│ PRU          │ 2x 200MHz real-time coprocessors         │
│ Power        │ 5V DC barrel OR USB                      │
│ Temp Range   │ -40°C to 85°C (Industrial)               │
│ Size         │ 86.4mm x 54.6mm                          │
└─────────────────────────────────────────────────────────┘
```

---

## Port Identification

```
        ┌──────────────────────────────────┐
        │      BeagleBone Black            │
        │                                  │
   ┌────┤ [ETHERNET]  ← PLC Network        │
   │    │                                  │
   │    │ [USB HOST]  ← USB-Ethernet       │
   │    │              (WireGuard NIC)     │
   │    │                                  │
   │    │ [MINI-USB]  ← Power + Console    │
   │    │                                  │
   │    │ [5V BARREL] ← Main Power         │
   │    │                                  │
   │    │ [MICROSD]   ← OS (optional)      │
   │    └──────────────────────────────────┘
   │
   └───► To PLC switch (stealth capture)
```

---

## Physical Assembly

### Step 1: Unbox and Inspect
```
□ BeagleBone board is clean, no damage
□ All ports accessible
□ No bent pins on headers
```

### Step 2: Insert MicroSD (If Using)
```
□ Insert MicroSD card with Debian image
□ Card clicks into slot
□ Note: Can use eMMC instead (already has Linux)
```

### Step 3: Connect USB-Ethernet Adapter
```
□ Plug USB-Ethernet into USB HOST port
□ This becomes your second NIC (for WireGuard)
□ Adapter should have activity LEDs
```

### Step 4: Connect Power
```
Option A: 5V Barrel Jack (Recommended)
□ Use 5V 2A DC adapter
□ Center-positive barrel 5.5x2.1mm
□ Blue power LED illuminates

Option B: USB Power
□ Connect Mini-USB to computer/charger
□ 5V 1A minimum
□ May brownout under load - barrel preferred
```

### Step 5: Connect Ethernet Cables

**Cable 1: PLC Network (Stealth Interface)**
```
□ Connect built-in Ethernet to PLC network switch
□ Find an empty port on the industrial switch
□ This is your CAPTURE interface (eth0)
□ Link LED should light up
```

**Cable 2: Internet/WireGuard (Secure Interface)**
```
□ Connect USB-Ethernet to your internet source
□ Options:
  - Office/home router
  - Dedicated 4G/LTE modem
  - Mobile hotspot
□ This is your TUNNEL interface (eth1/usb0)
```

---

## Network Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        PLANT NETWORK                            │
│                                                                 │
│  ┌─────────┐    ┌─────────┐    ┌─────────┐                     │
│  │  PLC 1  │    │  PLC 2  │    │  HMI    │                     │
│  │ Modbus  │    │ OPC UA  │    │         │                     │
│  └────┬────┘    └────┬────┘    └────┬────┘                     │
│       │              │              │                           │
│       └──────────────┼──────────────┘                           │
│                      │                                          │
│               ┌──────┴──────┐                                   │
│               │   SWITCH    │                                   │
│               └──────┬──────┘                                   │
│                      │                                          │
│                      │ ← You plug in here (empty port)          │
│                      │                                          │
│               ┌──────┴──────┐                                   │
│               │ BeagleBone  │ (STEALTH - no IP)                 │
│               │   eth0      │                                   │
│               └──────┬──────┘                                   │
│                      │                                          │
└──────────────────────┼──────────────────────────────────────────┘
                       │
              ┌────────┴────────┐
              │ BeagleBone      │
              │ USB-Ethernet    │ (Has IP - WireGuard)
              └────────┬────────┘
                       │
                       │ Internet (Encrypted Tunnel)
                       ▼
              ┌─────────────────┐
              │   Your VPS     │
              │  72.60.175.144 │
              └────────┬───────┘
                       │
                       ▼
              ┌─────────────────┐
              │ Your Phone     │
              │  (Telegram)    │
              └─────────────────┘
```

---

## LED Status Guide

| LED | Color | Meaning |
|-----|-------|---------|
| PWR | Blue | Power on |
| USR0 | Green | Heartbeat (blinking = alive) |
| USR1 | Green | MicroSD activity |
| USR2 | Green | CPU activity |
| USR3 | Green | eMMC activity |
| ETH LINK | Green | Network connected |
| ETH ACT | Yellow | Network activity |

---

## First Boot Checklist

```
□ Power connected (blue LED on)
□ USR0 starts blinking after ~30 seconds
□ Ethernet LINK LED is green
□ Wait 60-90 seconds for full boot
□ Can ping 192.168.7.2 via USB (if connected to computer)
```

---

## Connecting via USB Serial (Debugging)

If you need console access:

```bash
# On Mac/Linux
screen /dev/ttyUSB0 115200

# On Windows
# Use PuTTY, COM port, 115200 baud
```

Default login:
- Username: `debian`
- Password: `temppwd`

---

## Production Enclosure Options

### Option 1: DIN-Rail Mount ($20-40)
```
Good for: Control cabinet installation
Products: 
- Hammond 1591xxBK series
- Phoenix Contact ME series
- Search: "BeagleBone DIN rail enclosure"
```

### Option 2: Project Box ($10-20)
```
Good for: Bench/desktop use
Products:
- Hammond 1591xxCL (clear lid)
- Any ~100x60x25mm ABS box
- Drill holes for cables
```

### Option 3: 3D Printed
```
Good for: Custom fit
Files: Search Thingiverse "BeagleBone Black case"
Material: PETG for heat resistance
```

---

## Heat Management

The Industrial variant handles -40°C to 85°C but:
```
□ Ensure ventilation holes if enclosed
□ Don't stack on hot equipment
□ Passive cooling is usually sufficient
□ Optional: Add small heatsink to processor
```

---

## Grounding & ESD

Industrial environments have electrical noise:
```
□ Use shielded Ethernet cables in noisy environments
□ Ground enclosure if metal
□ Avoid running cables parallel to power lines
□ Consider surge protection on Ethernet
```

---

## Hardware Verification Checklist

Before moving to software:

```
□ BeagleBone powers on (blue LED)
□ Heartbeat LED blinking (USR0)
□ Built-in Ethernet shows LINK
□ USB-Ethernet adapter recognized (LED activity)
□ Can access via USB serial OR SSH
□ Both Ethernet cables connected to their networks
```

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| No power LED | Check power supply voltage (must be 5V) |
| No heartbeat | Wait longer, or reflash OS |
| No Ethernet link | Check cable, try different switch port |
| USB-Ethernet not seen | Try different adapter, check USB port |
| Overheating | Add ventilation, reduce ambient temp |

---

## Next Steps

Once hardware is assembled and powered:
→ Proceed to **02-SOFTWARE-BUILD-GUIDE.md**

---

*Hardware build complete. Time to make it invisible.*
