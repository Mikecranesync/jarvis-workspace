# VFD Simulator

**Variable Frequency Drive Emulator for FactoryLM Demo**

A Python-based VFD simulator that provides Modbus TCP communication for PLC integration and a web UI for monitoring and control.

## Features

- ✅ **Modbus TCP Server** - Connect your PLC via Modbus TCP on port 502
- ✅ **Realistic VFD Behavior** - Acceleration ramps, V/Hz control, current simulation
- ✅ **Web UI** - Real-time monitoring with animated motor visualization
- ✅ **Fault Injection** - Test fault handling and recovery
- ✅ **Zero Dependencies** - Runs on Python 3.8+ with no external packages

## Quick Start

```bash
# Navigate to source directory
cd products/vfd-simulator/src

# Run the simulator (requires root for port 502, or use --modbus-port 5020)
sudo python3 main.py

# Or with custom ports (no root needed)
python3 main.py --modbus-port 5020 --web-port 8080
```

## Accessing the Simulator

- **Web UI:** http://localhost:8080
- **Modbus TCP:** localhost:502 (or your custom port)

## Modbus Register Map

| Register | Address | Description | R/W |
|----------|---------|-------------|-----|
| 40001 | 0 | Command Word | R/W |
| 40002 | 1 | Speed Reference (0-10000) | R/W |
| 40003 | 2 | Status Word | R |
| 40004 | 3 | Output Frequency (Hz × 10) | R |
| 40005 | 4 | Output Current (A × 10) | R |
| 40006 | 5 | Output Voltage | R |
| 40007 | 6 | DC Bus Voltage | R |
| 40008 | 7 | Motor RPM | R |
| 40009 | 8 | Fault Code | R |

### Command Word Bits (40001)

| Bit | Function |
|-----|----------|
| 0 | Run (1 = Start) |
| 1 | Direction (0 = Forward, 1 = Reverse) |
| 2 | Fault Reset |
| 3 | External Fault |
| 4 | Enable |

### Status Word Bits (40003)

| Bit | Function |
|-----|----------|
| 0 | Ready |
| 1 | Running |
| 2 | Direction |
| 3 | Fault |
| 4 | At Speed |
| 5 | Voltage OK |

## Command Line Options

```
--modbus-port PORT    Modbus TCP port (default: 502)
--web-port PORT       Web UI port (default: 8080)
--motor-hp HP         Motor horsepower (default: 0.5)
--motor-voltage V     Motor voltage (default: 230)
--motor-amps A        Motor full load amps (default: 2.0)
--base-freq HZ        Base frequency (default: 60)
--max-freq HZ         Maximum frequency (default: 60)
--accel-time SEC      Acceleration time (default: 5)
--decel-time SEC      Deceleration time (default: 5)
```

## PLC Connection (Micro820)

1. Add Modbus TCP Client instruction in CCW
2. Configure:
   - IP Address: VPS or PC running simulator
   - Port: 502 (or custom)
   - Unit ID: 1
3. Read/Write registers per the map above

## Integration with Factory I/O

1. Run VFD Simulator on your PC
2. Configure Factory I/O scene with conveyor
3. Connect Micro820 to both:
   - VFD Simulator (Modbus TCP)
   - Factory I/O (Allen-Bradley driver)
4. PLC program controls both simultaneously!

## Architecture

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│  Micro820 PLC   │────▶│  VFD Simulator   │────▶│  Factory I/O    │
│  (Real Hardware)│     │  (This Software) │     │  (3D Sim)       │
└─────────────────┘     └──────────────────┘     └─────────────────┘
                               │
                               ▼
                        ┌──────────────┐
                        │   Web UI     │
                        │  (Monitor)   │
                        └──────────────┘
```

## Project Structure

```
vfd-simulator/
├── README.md
├── requirements.txt
└── src/
    ├── main.py           # Entry point
    ├── vfd_simulator.py  # Core VFD logic
    ├── modbus_server.py  # Modbus TCP server
    └── web_ui.py         # Web interface
```

## License

MIT License - FactoryLM Project

---

Created by Jarvis Agent for FactoryLM YC Demo
GitHub Issue: #27
