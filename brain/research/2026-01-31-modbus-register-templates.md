# Modbus Register Templates Research

**Date:** 2026-01-31
**Request:** Research registers to parameterize, learn, and template for ShopTalk

---

## Key Finding: Modbus Data Model (Universal)

All Modbus devices follow this 4-type structure:

| Type | Address Range | Access | Use Case |
|------|---------------|--------|----------|
| **Coils** (0x) | 00000-09999 | R/W bits | Outputs: relays, actuators, on/off |
| **Discrete Inputs** (1x) | 10000-19999 | Read-only bits | Inputs: switches, status flags |
| **Input Registers** (3x) | 30000-39999 | Read-only 16-bit | Analog sensors: temp, pressure, flow |
| **Holding Registers** (4x) | 40000-49999 | R/W 16-bit | Config, setpoints, commands |

---

## Common Register Categories (Template)

### 1. Status Registers
- Run/Stop status
- Fault/Alarm active
- Ready/Enabled state
- Operating mode

### 2. Control Registers
- Run command (forward/reverse/jog)
- Speed/frequency reference
- Start/Stop commands
- Reset fault

### 3. Feedback Registers
- Actual speed/frequency
- Motor current (amps)
- Motor voltage
- Power (kW)
- Torque

### 4. Diagnostic Registers
- Fault codes
- Warning codes
- Runtime hours
- Temperature (motor, drive)

### 5. Configuration Registers
- Acceleration time
- Deceleration time
- Min/Max frequency
- Motor parameters

---

## VFD Example: Yaskawa GA500

| Register | Description | Unit |
|----------|-------------|------|
| 4x0002 | Run Command (bits) | - |
| 4x0003 | Frequency Reference | 0.01 Hz |
| 4x0004 | Output Frequency | 0.01 Hz |
| 4x0005 | Output Current | 0.01 A |
| 4x0006 | Output Voltage | 0.1 V |
| 4x0007 | DC Bus Voltage | 0.1 V |
| 4x0020 | Fault Code | - |

**Run Command Bits (4x0002):**
- Bit 0: Forward Run
- Bit 1: Reverse Run
- Bit 2: External Fault Reset
- Bit 3: Fault Reset

---

## Manufacturer Documentation Sources

| Manufacturer | Equipment | Register Map Location |
|--------------|-----------|----------------------|
| **Yaskawa** | VFDs (GA500, etc) | Manual Chapter on Modbus |
| **Danfoss** | VFDs (FC102, etc) | [ccontrols.com/support/dp/DanfossFC102.xls](https://www.ccontrols.com/support/dp/DanfossFC102.xls) |
| **ABB** | VFDs, Breakers | [library.e.abb.com](https://library.e.abb.com) |
| **Siemens** | PLCs, VFDs | [cache.industry.siemens.com](https://cache.industry.siemens.com) |
| **Allen-Bradley** | VFDs (PowerFlex) | Rockwell Knowledgebase |
| **Daikin** | Chillers, AHUs | [tahoeweb.daikinapplied.com](https://tahoeweb.daikinapplied.com) |
| **Mitsubishi** | PLCs, VFDs | [dl.mitsubishielectric.com](https://dl.mitsubishielectric.com) |
| **Johnson Controls** | HVAC, VFDs | [docs.johnsoncontrols.com](https://docs.johnsoncontrols.com) |
| **Cummins** | Generators | [ccontrols.com/support/dp/modbus2300.pdf](https://www.ccontrols.com/support/dp/modbus2300.pdf) |

---

## ShopTalk Template Strategy

### Device Profile JSON Structure
```json
{
  "device_type": "vfd",
  "manufacturer": "yaskawa",
  "model": "ga500",
  "protocol": "modbus_rtu",
  "registers": {
    "status": {
      "run_status": {"address": 40001, "type": "uint16", "bits": {"running": 0, "fault": 1}},
      "fault_code": {"address": 40020, "type": "uint16"}
    },
    "control": {
      "run_command": {"address": 40002, "type": "uint16", "bits": {"forward": 0, "reverse": 1}},
      "speed_ref": {"address": 40003, "type": "uint16", "scale": 0.01, "unit": "Hz"}
    },
    "feedback": {
      "actual_speed": {"address": 40004, "type": "uint16", "scale": 0.01, "unit": "Hz"},
      "current": {"address": 40005, "type": "uint16", "scale": 0.01, "unit": "A"},
      "voltage": {"address": 40006, "type": "uint16", "scale": 0.1, "unit": "V"}
    },
    "diagnostics": {
      "motor_temp": {"address": 40030, "type": "int16", "scale": 0.1, "unit": "°C"},
      "runtime_hours": {"address": 40040, "type": "uint32"}
    }
  }
}
```

### Auto-Discovery Approach
1. **Scan common addresses** - Try known register locations
2. **Read device ID** - Modbus function 43/14 (Read Device ID)
3. **Pattern match** - Compare responses to known profiles
4. **Learn mode** - Record all register values over time, detect patterns

---

## Next Steps

1. **Build device profile library** - Start with top 10 VFD brands
2. **Create scanner** - Auto-detect devices on network
3. **Template generator** - Export discovered registers as JSON
4. **World model integration** - Feed register definitions to anomaly detection

---

## References

- [Modbus Organization](https://modbus.org) - Official protocol specs
- [Maple Systems VFD Tutorial](https://maplesystems.com/how-to-control-vfd-with-plc-and-hmi/)
- [Modbus Protocol Guide](https://maplesystems.com/modbus-protocol/)
