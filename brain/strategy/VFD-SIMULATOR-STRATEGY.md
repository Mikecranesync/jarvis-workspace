# VFD Simulator Strategy
*FactoryLM Demo System - February 2026*

---

## Goal
Create a VFD simulator that inputs/outputs real-world data, connects to your Micro820 PLC, and mirrors your physical DURApulse GS11N VFD for the demo.

---

## Architecture Overview

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│  Micro820 PLC   │────▶│  VFD Simulator   │────▶│  Factory I/O    │
│  (Real Hardware)│     │  (Software)      │     │  (3D Sim)       │
└─────────────────┘     └──────────────────┘     └─────────────────┘
        │                        │                        │
        ▼                        ▼                        ▼
   Digital I/O             Modbus/TCP              Motor Animation
   Analog 0-10V            OPC-UA                  Speed Display
```

---

## Component Strategy

### 1. Yaskawa V1000 Simulator (Download Now)
**Purpose:** Learn VFD parameter programming  
**Link:** https://www.yaskawa.com/downloads/search-index/details?showType=details&docnum=SW.V1000.01

**Use For:**
- Practice VFD parameter setup
- Understand digital operator interface
- Test frequency/speed relationships
- Learn fault codes and responses

### 2. Modbus VFD Emulator (Build This)
**Purpose:** Let PLC think it's talking to real VFD

**Python Libraries:**
- `pymodbus` - Modbus server/client
- `minimalmodbus` - Simple serial Modbus

**Key Registers to Emulate:**
| Register | Function | R/W |
|----------|----------|-----|
| 40001 | Command Word (Run/Stop) | R/W |
| 40002 | Speed Reference (0-10000) | R/W |
| 40003 | Status Word | R |
| 40004 | Output Frequency (Hz x 10) | R |
| 40005 | Output Current (A x 10) | R |
| 40006 | DC Bus Voltage | R |

### 3. OPC-UA Bridge (Optional)
**Purpose:** Industry-standard data exchange

**Libraries:**
- `opcua-asyncio` - Python OPC-UA
- `open62541` - C-based OPC-UA

### 4. Factory I/O Integration
**Purpose:** 3D visualization matching VFD state

**Connection:** Allen-Bradley driver → Micro820 → Simulator → Factory I/O

---

## Implementation Steps

### Phase 1: Tonight (30 min)
1. Download Yaskawa V1000 Simulator
2. Practice basic parameter programming
3. Understand Run/Stop, Speed Reference

### Phase 2: Tomorrow (2 hours)
1. Install pymodbus: `pip install pymodbus`
2. Create basic Modbus TCP server
3. Map registers to VFD functions
4. Connect Micro820 via Modbus TCP

### Phase 3: Integration (1 hour)
1. Link simulator output to Factory I/O
2. Test PLC → Simulator → 3D Animation loop
3. Add fault injection for demo

---

## Quick Start Code

```python
# vfd_simulator.py
from pymodbus.server import StartTcpServer
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext
from pymodbus.datastore import ModbusSequentialDataBlock

# Initialize registers
store = ModbusSlaveContext(
    hr=ModbusSequentialDataBlock(0, [0]*100)  # Holding registers
)
context = ModbusServerContext(slaves=store, single=True)

# Register map
COMMAND_WORD = 0    # 40001: Bit 0 = Run
SPEED_REF = 1       # 40002: 0-10000 = 0-60Hz
STATUS_WORD = 2     # 40003: Bit 0 = Running
OUTPUT_FREQ = 3     # 40004: Hz x 10

# Start server on port 502
StartTcpServer(context, address=("0.0.0.0", 502))
```

---

## Downloads & Links

| Item | Link |
|------|------|
| Yaskawa V1000 Simulator | [Download](https://www.yaskawa.com/downloads/search-index/details?showType=details&docnum=SW.V1000.01) |
| PyModbus Docs | [Docs](https://pymodbus.readthedocs.io/) |
| Factory I/O | [Website](https://factoryio.com/) |
| DURApulse Manual | [AutomationDirect](https://www.automationdirect.com/adc/shopping/catalog/drives_-a-_soft_starters/ac_variable_frequency_drives_(vfd)/gs1_series) |

---

## Your VFD: DURApulse GS11N-20P5

**Modbus Address:** Default 1  
**Baud Rate:** 9600 (RS-485)  
**Protocol:** Modbus RTU

**Key Parameters:**
- P04.00: Modbus address
- P04.01: Baud rate
- P04.02: Data format

---

## Next Steps for Mike

1. **Right Now:** Click the Yaskawa link, download simulator
2. **While Downloading:** Review the register map above
3. **Tonight:** Play with Yaskawa simulator, learn parameters
4. **Tomorrow:** I'll have Python Modbus emulator ready to deploy

---

*Created by Jarvis for FactoryLM Demo*
