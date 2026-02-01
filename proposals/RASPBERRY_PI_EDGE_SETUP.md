# Raspberry Pi 4 Edge Gateway Setup

**Replaces:** BeagleBone Black (deceased 2026-02-01)  
**Role:** Industrial Edge Gateway + Modbus Bridge

---

## Hardware Requirements

| Component | Spec | Notes |
|-----------|------|-------|
| **Raspberry Pi 4** | 4GB or 8GB RAM | 8GB preferred |
| **Power Supply** | 5V 3A USB-C | Official recommended |
| **SD Card** | 32GB+ Class 10 | Samsung EVO recommended |
| **Ethernet** | Direct to PLC network | 192.168.1.x |
| **Case** | With fan/heatsink | Industrial use = heat |

---

## Network Configuration

```
NEW TOPOLOGY:
                                         
PLC Laptop (100.72.2.99)                 
    │ Ethernet                           
    ▼                                    
Raspberry Pi 4 (192.168.1.100)           
    │ Modbus TCP (port 502)              
    ▼                                    
Allen-Bradley Micro 820 PLC              
```

**Pi Static IP:** 192.168.1.100 (same as BeagleBone was)  
**Tailscale:** Install for VPS direct access

---

## Software Stack

```bash
# Base OS
- Raspberry Pi OS Lite (64-bit)
- SSH enabled by default

# Industrial Stack
- Python 3.11+
- pymodbus (Modbus TCP client)
- influxdb-client (metrics)
- Tailscale (VPN to mesh)

# FactoryLM Edge Agent
- /opt/factorylm-edge/
- Syncs via Syncthing
- Runs edge data collector
```

---

## Setup Steps (Claude Code Prompt)

```
You are setting up a Raspberry Pi 4 as the FactoryLM Edge Gateway.

## Network Config
1. Set static IP: 192.168.1.100/24
2. Gateway: 192.168.1.1 (or router)
3. DNS: 8.8.8.8

## Install Tailscale
curl -fsSL https://tailscale.com/install.sh | sh
sudo tailscale up

## Install Industrial Stack
sudo apt update && sudo apt install -y python3-pip python3-venv
python3 -m venv /opt/factorylm-edge/venv
source /opt/factorylm-edge/venv/bin/activate
pip install pymodbus influxdb-client requests

## Install Syncthing
curl -s https://syncthing.net/release-key.txt | sudo apt-key add -
echo "deb https://apt.syncthing.net/ syncthing stable" | sudo tee /etc/apt/sources.list.d/syncthing.list
sudo apt update && sudo apt install -y syncthing
sudo systemctl enable syncthing@pi
sudo systemctl start syncthing@pi

## Test Modbus Connection (when PLC connected)
python3 -c "from pymodbus.client import ModbusTcpClient; c=ModbusTcpClient('192.168.1.100'); print(c.connect())"

## Report back:
- Tailscale IP
- SSH access confirmed
- Syncthing device ID
```

---

## Advantages Over BeagleBone

| Feature | BeagleBone Black | Raspberry Pi 4 |
|---------|------------------|----------------|
| RAM | 512 MB | 4-8 GB |
| CPU | 1 GHz single | 1.5 GHz quad |
| USB | USB 2.0 | USB 3.0 |
| Ethernet | 100 Mbps | 1 Gbps |
| Community | Small | Massive |
| OS Support | Limited | Excellent |
| GPIO | 65 pins | 40 pins |
| Price | ~$55 | ~$55-75 |

**Verdict:** Pi 4 is better for this use case.

---

## FactoryLM Edge Agent

Once Pi is online, deploy:

```python
# /opt/factorylm-edge/modbus_collector.py

from pymodbus.client import ModbusTcpClient
from influxdb_client import InfluxDBClient, Point
import time

PLC_IP = "192.168.1.100"  # Or actual PLC IP
INFLUX_URL = "http://100.68.120.99:8086"
INFLUX_TOKEN = "factorylm-influx-token-2026"

def collect_and_send():
    # Connect to PLC
    client = ModbusTcpClient(PLC_IP, port=502)
    client.connect()
    
    # Read registers (example)
    result = client.read_holding_registers(0, 10)
    
    # Send to InfluxDB
    influx = InfluxDBClient(url=INFLUX_URL, token=INFLUX_TOKEN, org="factorylm")
    write_api = influx.write_api()
    
    for i, val in enumerate(result.registers):
        point = Point("plc_register").tag("register", i).field("value", val)
        write_api.write(bucket="sensors", record=point)
    
    client.close()

if __name__ == "__main__":
    while True:
        collect_and_send()
        time.sleep(1)  # 1 second polling
```

---

## Checklist

- [ ] Flash Raspberry Pi OS to SD card
- [ ] Boot Pi, connect Ethernet
- [ ] SSH in (default: pi@raspberrypi.local)
- [ ] Set static IP 192.168.1.100
- [ ] Install Tailscale
- [ ] Install Python + pymodbus
- [ ] Install Syncthing, pair with VPS
- [ ] Deploy edge agent
- [ ] Connect to PLC
- [ ] Verify data flowing to InfluxDB

---

*Pi > BeagleBone for this use case. RIP BBB.*
