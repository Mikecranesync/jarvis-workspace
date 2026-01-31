# PLC Manufacturer Templates — Status

**Last Updated:** 2026-01-31 09:59 UTC

---

## Template Status

| Manufacturer | Protocol | Template | Documentation Source |
|--------------|----------|----------|---------------------|
| **Allen-Bradley/Rockwell** | EtherNet/IP, Modbus | ⚠️ Basic | literature.rockwellautomation.com |
| **Siemens** | OPC-UA, Modbus | ⚠️ Basic | support.industry.siemens.com |
| **Schneider/Modicon** | Modbus TCP (native) | ✅ Done | se.com |
| **Mitsubishi** | Modbus RTU/TCP | 📋 TODO | dl.mitsubishielectric.com |
| **Omron** | Modbus RTU/TCP | 📋 TODO | industrial.omron.com |
| **ABB** | Modbus RTU/TCP | 📋 TODO | library.abb.com |
| **Beckhoff** | Modbus TCP | 📋 TODO | infosys.beckhoff.com |
| **Delta** | Modbus RTU/TCP | 📋 TODO | deltaww.com |
| **Keyence** | Modbus RTU/TCP | 📋 TODO | plc.keyence.com |
| **Automation Direct** | Modbus (native) | 📋 TODO | automationdirect.com |

---

## VFD/Drive Templates

| Manufacturer | Models | Template | Source |
|--------------|--------|----------|--------|
| **Yaskawa** | GA500, etc | ✅ Documented | Manual Ch. Modbus |
| **Danfoss** | FC102, etc | ✅ Spreadsheet | ccontrols.com |
| **ABB** | ACS series | 📋 TODO | library.abb.com |
| **Siemens** | SINAMICS | 📋 TODO | support.industry.siemens.com |
| **Allen-Bradley** | PowerFlex | 📋 TODO | literature.rockwellautomation.com |

---

## What We Have (modbus_profiles.json)

- ✅ Generic VFD template
- ✅ Schneider M340
- ✅ Allen-Bradley Micro800 (EtherNet/IP)
- ✅ Siemens S7-1200 (OPC-UA)
- ✅ Factory I/O (simulation)

---

## Priority Order for Template Creation

1. **Automation Direct** — Popular in SMB, native Modbus, easy docs
2. **Schneider/Modicon** — Modbus inventors, most documentation
3. **Allen-Bradley** — Largest US market share
4. **Siemens** — Largest global market share
5. **Mitsubishi** — Big in Asia, good for global reach
6. **Omron** — Common in packaging/food industries
7. **Delta** — Cost-effective, emerging markets
8. **ABB** — Process industries
9. **Beckhoff** — High-end automation
10. **Keyence** — Sensors + PLCs
