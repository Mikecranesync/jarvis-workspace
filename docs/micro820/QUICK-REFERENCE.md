# Micro820 Quick Reference for Zero-Shot Connection

## Hardware: Allen-Bradley Micro820 (2080-LC20-20AWB)
- **Ethernet Port:** Built-in, RJ45
- **Default IP:** DHCP (no static IP out of box!)
- **Protocols:** EtherNet/IP (port 44818), Modbus TCP (port 502)

## Critical Pre-requisites (Must be done in CCW first!)

### 1. Set Static IP Address
In CCW:
1. Connect via USB
2. Project Properties → Controller → Ethernet
3. Set IP: `192.168.1.10` (or your choice)
4. Set Subnet: `255.255.255.0`
5. Download to controller

### 2. Enable Modbus TCP Server
In CCW:
1. Project Properties → Protocol Configuration
2. Check "Enable Modbus TCP Server"
3. Note the "Modbus Mapping" tab for register addresses

## Modbus Register Mapping (CCW default)
| Register Type | CCW Name | Modbus Address Range |
|---------------|----------|----------------------|
| Coils | Modbus_Coils | 0-255 |
| Discrete Inputs | Modbus_DI | 0-255 |
| Input Registers | Modbus_IR | 0-255 |
| Holding Registers | Modbus_HR | 0-255 |

## Python Connection Examples

### Using pymodbus (RECOMMENDED for Micro820)
```python
from pymodbus.client import ModbusTcpClient

client = ModbusTcpClient('192.168.1.10', port=502)
client.connect()

# Read holding register 0
result = client.read_holding_registers(0, 1)
if not result.isError():
    print(f"Value: {result.registers[0]}")

# Write to holding register 0
client.write_register(0, 1234)

client.close()
```

### Using pycomm3 (EtherNet/IP - partial support)
```python
from pycomm3 import LogixDriver

# Just use IP, no slot needed for Micro800
with LogixDriver('192.168.1.10') as plc:
    # Auto-detects Micro800 based on product name prefix "2080"
    print(plc.info)  # Get controller info
    
    # Read tag (must match CCW variable name)
    result = plc.read('MyVariable')
    print(result.value)
```

### Using CIPDriver for Discovery
```python
from pycomm3 import CIPDriver

# Discover all devices on network
devices = CIPDriver.discover()
for d in devices:
    print(f"{d['ip_address']}: {d['product_name']}")

# Get identity of specific device
info = CIPDriver.list_identity('192.168.1.10')
print(info)
```

## Troubleshooting

### "Connection refused" on port 502
- Modbus TCP Server not enabled in CCW
- Firewall on PLC (unlikely for Micro820)

### "Connection refused" on port 44818
- Normal - EtherNet/IP might not be enabled
- Try Modbus instead

### "No response" to any connection
- Check IP address is correct
- Check cable connection
- Check PLC is in RUN mode
- Try pinging PLC first

### pycomm3 read fails
- Tag name must EXACTLY match CCW variable name
- Tag must have "External Access" enabled in CCW
- Micro800 has limited pycomm3 support - use Modbus

## CCW Modbus Mapping Reference

To map variables to Modbus registers in CCW:
1. Open "Modbus Mapping" in project
2. Add variable to appropriate register type
3. Note the starting address
4. Use that address in pymodbus read/write

Example mapping:
```
Motor_Speed -> Holding Register 100
Motor_Running -> Coil 0
Temperature -> Input Register 50
```
