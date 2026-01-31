# PLC Auto-Connect Research
**Date:** 2026-01-31
**Priority:** Critical Path for ShopTalk
**Goal:** Plug-and-play PLC connection without manual configuration

---

## Executive Summary

**Feasibility: 7/10** - Auto-discovery is achievable for most common scenarios. The key is scanning the network for devices speaking industrial protocols, then auto-detecting register maps.

---

## Three Approaches to Auto-Connect

### Approach 1: Modbus TCP Network Scan
**Feasibility: 8/10** | **Complexity: Low**

**How it works:**
1. Scan local network for port 502 (Modbus TCP default)
2. For each IP responding on 502, enumerate slave IDs (1-247)
3. For each slave, read device identification (function 0x2B)
4. Auto-populate register map based on device type

**Tools/Libraries:**
- **nmap** with `modbus-discover.nse` script
- **pymodbus** Python library
- **modbustcp-scanner** (GitHub: T-6891/modbustcp-scanner)

**Code approach:**
```python
import socket
from pymodbus.client import ModbusTcpClient

def scan_network_for_plcs(network_prefix="192.168.1"):
    """Scan network for Modbus devices"""
    devices = []
    for i in range(1, 255):
        ip = f"{network_prefix}.{i}"
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.5)
            result = sock.connect_ex((ip, 502))
            if result == 0:
                devices.append(ip)
            sock.close()
        except:
            pass
    return devices

def identify_plc(ip):
    """Get device identification"""
    client = ModbusTcpClient(ip)
    client.connect()
    # Read device ID using Modbus function 0x2B (43)
    result = client.read_device_information()
    client.close()
    return result
```

**Limitations:**
- Only works for Modbus TCP devices
- Doesn't auto-detect register meanings
- Some PLCs need explicit configuration to enable Modbus

---

### Approach 2: Device Fingerprinting + Template Library
**Feasibility: 9/10** | **Complexity: Medium**

**How it works:**
1. After discovery, read device identification registers
2. Match against a library of known device templates
3. Auto-load register map for that device type

**Device Templates (JSON):**
```json
{
  "schneider_m340": {
    "vendor": "Schneider Electric",
    "model_pattern": "M340.*",
    "registers": {
      "40001": {"name": "motor_speed", "unit": "RPM", "type": "uint16"},
      "40002": {"name": "motor_current", "unit": "A", "type": "float32"},
      "40003": {"name": "temperature", "unit": "C", "type": "int16"}
    }
  },
  "allen_bradley_micro800": {
    "vendor": "Allen-Bradley",
    "model_pattern": "Micro8[0-9]{2}",
    "registers": {...}
  }
}
```

**Strategy:**
1. Build a template library for top 20 most common PLCs
2. Crowdsource templates from users
3. Use AI to suggest mappings for unknown devices

**GitHub Resources:**
- Template libraries don't exist yet - this is our opportunity!
- We could build the "device profile" database

---

### Approach 3: EtherNet/IP CIP Discovery (Allen-Bradley)
**Feasibility: 7/10** | **Complexity: Medium**

**How it works:**
EtherNet/IP uses CIP (Common Industrial Protocol) which has built-in device discovery via UDP broadcast.

1. Send UDP broadcast to port 44818
2. Devices respond with identity information
3. Connect and enumerate tags automatically

**Libraries:**
- **pycomm3** - Python library for Allen-Bradley PLCs
- Supports tag enumeration natively

```python
from pycomm3 import LogixDriver

def discover_allen_bradley():
    # Auto-discover on network
    with LogixDriver('192.168.1.1') as plc:
        # Get all tags automatically!
        tags = plc.get_tag_list()
        for tag in tags:
            print(f"{tag['tag_name']}: {tag['data_type']}")
```

**Advantage:** Allen-Bradley PLCs can enumerate ALL their tags automatically - no manual register mapping needed!

**GitHub:** https://github.com/ottowayi/pycomm3

---

### Approach 4: OPC-UA Discovery (Siemens, Modern PLCs)
**Feasibility: 8/10** | **Complexity: Medium**

**How it works:**
OPC-UA has built-in discovery services (LDS - Local Discovery Server).

1. Query LDS on port 4840
2. Browse server address space
3. Auto-discover all variables with metadata

```python
from opcua import Client

def discover_opcua():
    client = Client("opc.tcp://192.168.1.1:4840")
    client.connect()
    
    # Browse all nodes automatically
    root = client.get_root_node()
    objects = root.get_child(["0:Objects"])
    
    # Recursively discover all variables
    for node in objects.get_children():
        print(f"Found: {node.get_browse_name()}")
```

**Libraries:**
- **opcua** / **asyncua** (Python)
- **node-opcua** (Node.js)

**Advantage:** Full metadata including units, data types, descriptions

---

## Recommended Implementation Strategy

### Phase 1: Quick Win (Day 1)
```
1. Network scan for port 502 (Modbus TCP)
2. Enumerate slave IDs
3. Read first 100 holding registers
4. Display values and let user label them
```

### Phase 2: Template Library (Week 1)
```
1. Build JSON templates for common PLCs:
   - Allen-Bradley MicroLogix/CompactLogix
   - Siemens S7-1200/1500
   - Schneider M340/M580
   - Modicon
   - Automation Direct
   
2. Auto-match discovered device to template
3. Pre-populate register meanings
```

### Phase 3: AI-Assisted Mapping (Week 2+)
```
1. For unknown devices, read registers
2. Use LLM to guess register meanings based on:
   - Value ranges
   - Value patterns (oscillating = temp/speed)
   - Register addresses (common conventions)
3. User confirms/corrects
4. Save as new template
```

---

## GitHub Repos That Help

1. **modbustcp-scanner** (T-6891)
   - Network scanning for Modbus devices
   - License: CC-BY-NC (need commercial license)

2. **pycomm3** (ottowayi)
   - Allen-Bradley auto-tag discovery
   - License: MIT ✅

3. **opcua-asyncio** / **python-opcua**
   - OPC-UA discovery and browsing
   - License: LGPL ✅

4. **nmap modbus-discover.nse**
   - Network-level PLC discovery
   - License: Nmap Public Source License

5. **pymodbus** (riptideio)
   - Core Modbus library
   - License: BSD ✅

---

## The "Magic" UX Flow

```
┌─────────────────────────────────────────┐
│  ShopTalk Auto-Connect                  │
├─────────────────────────────────────────┤
│                                         │
│  🔍 Scanning network...                 │
│  ████████████████░░░░ 75%               │
│                                         │
│  Found 3 devices:                       │
│                                         │
│  ✅ 192.168.1.10 - Allen-Bradley 1769   │
│     └─ 47 tags discovered               │
│                                         │
│  ✅ 192.168.1.15 - Schneider M340       │
│     └─ Using template: conveyor_line    │
│                                         │
│  ⚠️ 192.168.1.20 - Unknown Modbus       │
│     └─ 12 registers found, need mapping │
│                                         │
│  [Connect All]  [Configure Unknown]     │
│                                         │
└─────────────────────────────────────────┘
```

---

## Action Items

1. [ ] Build Modbus network scanner in Python
2. [ ] Integrate pycomm3 for Allen-Bradley support
3. [ ] Create device template JSON format
4. [ ] Build 5 initial templates for common PLCs
5. [ ] Add AI-assisted register mapping
6. [ ] Test with Factory I/O + BeagleBone

---

## Key Insight

> **"The real unlock is the template library."**
> 
> Once we have profiles for common PLCs, ShopTalk becomes:
> "Plug in → Auto-detect → Already knows your equipment"
>
> This is our moat. Build the largest industrial device profile database.
