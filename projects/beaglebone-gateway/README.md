# 🏭 Industrial Protocol Gateway

**The USB of PLC adapters** — A sub-$500 universal industrial protocol gateway built on BeagleBone.

Competes with:
- Ewon Flexy 205 ($1,200+)
- Siemens SCALANCE ($2,000+)
- HMS Anybus ($500-800)

## 📡 Supported Protocols

| Protocol | PLCs/Devices | Library |
|----------|--------------|---------|
| **Modbus TCP** | Any Modbus TCP device | pymodbus |
| **Modbus RTU** | RS-485 serial devices | pymodbus |
| **Siemens S7** | S7-300, S7-400, S7-1200, S7-1500 | python-snap7 |
| **EtherNet/IP** | Allen-Bradley CompactLogix, ControlLogix | pycomm3 |
| **MELSEC** | Mitsubishi Q, L, iQ-R, iQ-L series | pymcprotocol |
| **OPC UA** | Server exposing all tags | asyncua |

## 🔧 Hardware Requirements

| Component | Cost | Notes |
|-----------|------|-------|
| BeagleBone Black/AI | $55-150 | AM3358 or AM5729 processor |
| USB Wi-Fi Adapter | $15-30 | Linux-compatible, use with extension cable |
| 5V 2A Power Supply | $15-25 | Barrel jack, DIN rail mountable |
| RS-485 Cape (optional) | $30-50 | For Modbus RTU |
| **Total** | **~$115-255** | |

## 🚀 Quick Start

### 1. Flash BeagleBone
Download latest Debian image from [beagleboard.org](https://beagleboard.org/latest-images)

### 2. Install Gateway
```bash
# SSH into BeagleBone
ssh debian@beaglebone.local

# Clone repository
git clone https://github.com/your-org/beaglebone-gateway.git
cd beaglebone-gateway

# Run installer
sudo ./scripts/install.sh
```

### 3. Configure
Edit `/opt/industrial-gateway/config/gateway.yaml`:
```yaml
devices:
  - name: "my_plc"
    protocol: "s7"
    host: "192.168.1.50"
    rack: 0
    slot: 1
    tags:
      - name: "motor_speed"
        area: "DB"
        db_number: 1
        offset: 0
        data_type: "real"
```

### 4. Start
```bash
sudo systemctl start industrial-gateway
```

### 5. Access
- **Web UI:** http://beaglebone.local:8080
- **OPC UA:** opc.tcp://beaglebone.local:4840
- **REST API:** http://beaglebone.local:8080/api/tags

## 🌐 Wi-Fi Access Point Mode

Create a direct Wi-Fi connection from your laptop:
```bash
sudo ./scripts/setup_wifi_ap.sh "MyGateway" "SecurePassword123"
```

Then connect laptop to "MyGateway" network and access at http://192.168.50.1:8080

## 📖 API Reference

### Get All Tags
```bash
curl http://gateway:8080/api/tags
```

### Get Single Tag
```bash
curl http://gateway:8080/api/tags/motor_speed
```

### Write Tag
```bash
curl -X POST http://gateway:8080/api/tags/setpoint \
  -H "Content-Type: application/json" \
  -d '{"value": 75.5}'
```

### Gateway Status
```bash
curl http://gateway:8080/api/status
```

## 📁 Project Structure

```
beaglebone-gateway/
├── src/
│   ├── core/
│   │   ├── gateway.py      # Main application
│   │   └── opcua_server.py # OPC UA server
│   ├── adapters/
│   │   ├── modbus_adapter.py
│   │   ├── s7_adapter.py
│   │   ├── ethernetip_adapter.py
│   │   └── melsec_adapter.py
│   └── web/
│       └── app.py          # Web interface
├── config/
│   └── gateway.yaml        # Configuration
├── scripts/
│   ├── install.sh          # Installation script
│   └── setup_wifi_ap.sh    # Wi-Fi AP setup
├── tests/
├── docs/
├── requirements.txt
└── README.md
```

## 🔒 Security

- Configure firewall rules for PLC networks
- Use strong Wi-Fi passwords
- Enable OPC UA authentication for production
- Follow IEC 62443 guidelines

## 📄 License

MIT License - See LICENSE file

## 🏢 About

Built by [FactoryLM](https://factorylm.com) — Industrial AI for Maintenance Teams

---

*The sub-$500 alternative to $2,000+ commercial gateways*
