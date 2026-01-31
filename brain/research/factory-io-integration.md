# Factory I/O Integration Research
**Date:** 2026-01-31

## Overview

Factory I/O is a 3D factory simulation that connects to PLCs via:
- **Modbus TCP** (primary for our use case)
- **OPC UA Client** (alternative)
- **OPC DA** (legacy)

## Connection Architecture

```
┌─────────────┐     Modbus TCP     ┌─────────────┐
│ Factory I/O │◄──────────────────►│ Allen-Bradley│
│ (Simulation)│     Port 502       │  Micro 820   │
└─────────────┘                    └──────┬───────┘
                                          │ Ethernet
                                   ┌──────▼───────┐
                                   │  BeagleBone  │
                                   │  (Data Cap)  │
                                   └──────────────┘
```

## Modbus Register Mapping

Factory I/O uses standard Modbus addressing:
- **Coils (0xxxx):** Digital outputs
- **Discrete Inputs (1xxxx):** Digital inputs  
- **Input Registers (3xxxx):** Analog inputs
- **Holding Registers (4xxxx):** Analog outputs

## Data Collection Approach

1. **Direct from PLC:** BeagleBone reads Modbus registers
2. **Sample Rate:** 10-100ms intervals
3. **Data Format:** CSV with timestamps
4. **Labels:** Scenario name embedded in filename

## Key Resources

- Factory I/O Docs: https://docs.factoryio.com/manual/drivers/
- Modbus Driver: https://docs.factoryio.com/manual/drivers/modbus-tcp-ip-server/
- OPC UA Driver: https://docs.factoryio.com/manual/drivers/opc/

## For Saturday

Mike connects:
1. Factory I/O → PLC via Modbus TCP
2. PLC → BeagleBone via Ethernet
3. Run `collect.py --host <PLC_IP> --scenario normal`
4. Capture 5 scenarios

## Notes

- Factory I/O acts as Modbus SERVER, PLC is CLIENT
- BeagleBone reads as secondary CLIENT
- No special API needed - just Modbus registers
