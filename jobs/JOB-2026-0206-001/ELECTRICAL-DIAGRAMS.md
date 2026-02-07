# ELECTRICAL DIAGRAMS - Conveyor Demo System
## JOB-2026-0206-001

**Document Version:** 1.0  
**Date:** 2026-02-06  
**System:** Variable Speed Conveyor with PLC Control  
**Components:** Micro820 PLC, VFD, 3-Phase Motor, FactoryLM Edge Device

---

## 1. SYSTEM OVERVIEW

```
┌─────────────────┐    ┌──────────────┐    ┌─────────────┐    ┌──────────────┐
│   120V/240V     │    │     VFD      │    │ 3-Phase     │    │  FactoryLM   │
│   Single Phase  │───▶│  PowerFlex   │───▶│   Motor     │    │  Edge Device │
│   Power Supply  │    │    525       │    │  (1/2 HP)   │    │ (Raspberry   │
└─────────────────┘    └──────────────┘    └─────────────┘    │     Pi)      │
         │                      │                             └──────────────┘
         │              ┌───────▼───────┐                             │
         │              │   Micro820    │                             │
         │              │     PLC       │◄────────────────────────────┘
         │              │   (Modbus)    │            Ethernet
         │              └───────────────┘
         │
    ┌────▼────┐
    │ E-STOP  │
    │ Circuit │
    └─────────┘
```

---

## 2. VFD WIRING DIAGRAM (PowerFlex 525)

### 2.1 Single Phase Input to 3-Phase Output

```
SINGLE PHASE INPUT (120V/240V)          VFD INTERNAL                3-PHASE OUTPUT
                                       
L1 (HOT) ──────────┐                  ┌─────────────────┐           T1 ─────▶ Motor U
                   │                  │                 │           
                   │    ┌─────────────┤   DC BUS &      ├─────────  T2 ─────▶ Motor V
N (NEUTRAL)────────┼────┤             │   INVERTER      │           
                   │    │             │   SECTION       │           T3 ─────▶ Motor W
L2/GND ────────────┘    │             │                 │           
                        │             └─────────────────┘           
                        │                                           
                    ┌───▼───┐         ┌─────────────────┐           
                    │ EMI   │         │    CONTROL      │           
                    │FILTER │         │   SECTION       │           
                    └───────┘         └─────────────────┘           
                                              │                     
                                      ┌───────▼───────┐             
                                      │   MODBUS      │             
                                      │   RTU PORT    │             
                                      │   (Terminal)  │             
                                      └───────────────┘             
```

### 2.2 VFD Terminal Connections (PowerFlex 525)

```
POWER TERMINALS:
┌─────┬─────┬─────┬─────┬─────┬─────┬─────┐
│ L1  │ L2  │ GND │ T1  │ T2  │ T3  │ BR+ │
└─────┴─────┴─────┴─────┴─────┴─────┴─────┘
  │     │     │     │     │     │     │
  │     │     │     │     │     │     └─── Brake Resistor +
  │     │     │     │     │     └───────── Motor Phase W
  │     │     │     │     └─────────────── Motor Phase V  
  │     │     │     └───────────────────── Motor Phase U
  │     │     └─────────────────────────── Ground
  │     └───────────────────────────────── Line 2 (or Neutral)
  └─────────────────────────────────────── Line 1 (Hot)

CONTROL TERMINALS:
┌───┬───┬───┬───┬───┬───┬───┬───┬───┬───┐
│ 1 │ 2 │ 3 │ 4 │ 5 │ 6 │ 7 │ 8 │ 9 │10 │
└───┴───┴───┴───┴───┴───┴───┴───┴───┴───┘
  │   │   │   │   │   │   │   │   │   │
  │   │   │   │   │   │   │   │   │   └─── +24V Out
  │   │   │   │   │   │   │   │   └─────── Digital Out Common
  │   │   │   │   │   │   │   └─────────── Digital Out 1
  │   │   │   │   │   │   └─────────────── Speed Reference 2
  │   │   │   │   │   └───────────────── Speed Reference 1  
  │   │   │   │   └───────────────────── Digital In Common
  │   │   │   └───────────────────────── Digital In 3 (Reset)
  │   │   └───────────────────────────── Digital In 2 (Stop)
  │   └───────────────────────────────── Digital In 1 (Start)
  └───────────────────────────────────── +24V Supply

COMM TERMINALS:
┌────┬────┬────┐
│ A+ │ B- │ GND│
└────┴────┴────┘
  │    │    │
  │    │    └────── Modbus GND
  │    └─────────── Modbus B- (Data-)
  └──────────────── Modbus A+ (Data+)
```

---

## 3. MOTOR CONNECTIONS

### 3.1 3-Phase Induction Motor Wiring

```
VFD OUTPUT                    MOTOR TERMINAL BOX
                             
T1 ────────────────────────── U1 (Phase 1)
                             │
T2 ────────────────────────── V1 (Phase 2) 
                             │
T3 ────────────────────────── W1 (Phase 3)
                             │
                         ┌───┴───┐
                         │WINDINGS│
PE (Ground) ─────────────┤       │
                         │  ┌─┐  │
                         │  │M│  │  Motor: 1/2 HP, 3-Phase
                         │  │ │  │  Voltage: 208-240V
                         │  │3│  │  Current: 2.4-2.1A  
                         │  │~│  │  RPM: 1725
                         │  │φ│  │  Enclosure: TEFC
                         │  └─┘  │
                         └───────┘

MOTOR NAMEPLATE WIRING:
┌──────────────────────────────┐
│  CONNECTION   │  VOLTAGE     │
├──────────────────────────────┤
│  WYE (Y)      │  208V-240V   │ ← Use this for VFD
│  DELTA (Δ)    │  460V        │
└──────────────────────────────┘

WYE CONNECTION (for 240V VFD):
   U1 ────┐
          │  ╲
          │   ╲ STAR
   V1 ─────────●─────── N (Neutral Point)
          │   ╱
          │  ╱
   W1 ────┘
```

### 3.2 Motor Protection & Monitoring

```
THERMAL PROTECTION:
┌─────────────────┐     ┌──────────────┐
│ Motor Thermal   │────▶│ VFD Terminal │
│ Switch (T1/T2)  │     │    3 & 4     │ (Digital In 3)
└─────────────────┘     └──────────────┘

ENCODER (Optional for precise control):
┌─────────────────┐     ┌──────────────┐
│ Incremental     │────▶│ PLC High     │
│ Encoder         │     │ Speed Input  │
│ (A,B,Z phases)  │     │ (if needed)  │
└─────────────────┘     └──────────────┘
```

---

## 4. MICRO820 PLC CONNECTIONS

### 4.1 PLC I/O Configuration

```
MICRO820 PLC (2080-LC20-20QWB)

INPUT TERMINALS (DC):          OUTPUT TERMINALS (Relay):
┌───┬───┬───┬───┬───┬───┐      ┌───┬───┬───┬───┬───┬───┐
│I0 │I1 │I2 │I3 │I4 │I5 │      │Q0 │Q1 │Q2 │Q3 │Q4 │Q5 │
└───┴───┴───┴───┴───┴───┘      └───┴───┴───┴───┴───┴───┘
 │   │   │   │   │   │          │   │   │   │   │   │
 │   │   │   │   │   └─E-Stop   │   │   │   │   │   └─VFD Reset
 │   │   │   │   └─Motor OL     │   │   │   │   └─Stack Light Grn
 │   │   │   └─VFD Fault        │   │   │   └─Stack Light Yel  
 │   │   └─Prox Sensor 2        │   │   └─Stack Light Red
 │   └─Prox Sensor 1            │   └─VFD Stop Command
 └─Start Button                 └─VFD Start Command

DC SUPPLY:
┌────┬────┐      ┌─────┬─────┐
│+24V│ 0V │      │+24V │ COM │
└────┴────┘      └─────┴─────┘
  │    │           │     │
  │    └───────────┼─────┘    (Input Common)
  │                │
  └────────────────┘          (24V Supply to inputs)
```

### 4.2 Modbus RTU Connection (PLC to VFD)

```
MICRO820 BUILT-IN MODBUS:      VFD MODBUS TERMINALS:
┌─────────────────┐           ┌─────────────────┐
│   Terminal 5    │──────────▶│      A+         │ (Data+)
│   (Data+)       │           │   (Terminal     │
├─────────────────┤    ┌──────┤    A+/5)        │
│   Terminal 6    │────┼─────▶│      B-         │ (Data-)
│   (Data-)       │    │      │   (Terminal     │
├─────────────────┤    │ ┌────┤    B-/6)        │  
│   Terminal 7    │────┼─┼───▶│     GND         │ (Shield)
│   (Common/GND)  │    │ │    │   (Terminal     │
└─────────────────┘    │ │    │    GND/7)       │
                       │ │    └─────────────────┘
120Ω TERMINATION:      │ │    
     ┌─────────────────┘ │    CABLE: Belden 3105A
     │                   │    (18 AWG, 3-conductor,
     │ 120Ω              │     shielded, twisted pair)
     │ ┌─────────────────┘    Length: < 1000 feet
     └─┤
       │
    ───┴───  GND

MODBUS PARAMETERS:
- Baud Rate: 9600 bps
- Data Bits: 8
- Parity: None  
- Stop Bits: 1
- VFD Node Address: 1
- PLC as Master (Node 0)
```

### 4.3 PLC Program Structure

```
MAIN PROGRAM LOGIC:

START_BUTTON (I0) ──┐
                    │    ┌───┐     VFD_START ──┐
E_STOP_OK (I5) ─────┤───▶│AND│───▶   (Q0)     │
                    │    └───┘                │
VFD_READY ──────────┘         ┌──────────────┘
(from Modbus)                 │
                              ▼
STOP_BUTTON ──┐          ┌────────┐
              │         ▶│ TIMER  │─── VFD_STOP (Q1)
E_STOP (¬I5) ─┴─ OR ────▶│  0.5s  │
                         └────────┘
VFD_FAULT ───────────────────┘
(from Modbus)

MODBUS READ/WRITE:
┌─────────────────────────────────────────┐
│ Read from VFD (Node 1):                 │
│ - Status Word (40001)                   │ 
│ - Actual Speed (40002)                  │
│ - Output Current (40003)                │
│ - Fault Code (40004)                    │
├─────────────────────────────────────────┤
│ Write to VFD (Node 1):                  │
│ - Control Word (40001)                  │
│ - Speed Reference (40002)               │
│ - Acceleration Time (40003)             │
│ - Deceleration Time (40004)             │
└─────────────────────────────────────────┘
```

---

## 5. EMERGENCY STOP CIRCUIT

### 5.1 E-Stop Safety Circuit (Category 3)

```
MAIN POWER CONTACTOR CONTROL:

120V L1 ──┐                                    ┌─── MAIN CONTACTOR
          │                                    │    COIL (MC1)
          │    ┌─────────┐    ┌──────────┐     │    ┌─────────┐
          └───▶│ E-STOP  │───▶│  SAFETY  │─────┼───▶│   MC1   │
               │ Button  │    │ RELAY    │     │    │  Coil   │
               │ (NC)    │    │ (Dual    │     │    └─────────┘
               │         │    │Channel)  │     │           
               └─────────┘    └──────────┘     │    ┌─────────┐
                    │              │           └───▶│   MC2   │
                    │              │                │  Coil   │ 
                    │              └─ Feedback ─────┤ (Backup)│
                    │                               └─────────┘
                    └─ Reset Button ──┐
                                      │
STATUS INDICATION:                    │
┌─────────────┐                       │
│ Stack Light │ ◄─────────────────────┘
│ Red: E-Stop │
│ Yel: Fault  │ ◄─ VFD Fault
│ Grn: Run    │ ◄─ VFD Running
└─────────────┘

POWER FLOW WITH E-STOP:
120V L1 ──┬─ E-STOP ─┬─ MC1 ─┬── VFD L1
          │          │       │
          │          │       └── PLC Power
          │          │
120V L2 ──┼──────────┼── MC1 ── VFD L2/N
          │          │
GND ──────┼──────────┴── MC1 ── VFD GND
          │
          └─── Control Circuit Common
```

### 5.2 Safety Relay Configuration

```
PILZ PNOZ s3 Safety Relay (Example):

INPUT TERMINALS:           OUTPUT TERMINALS:
┌───┬───┬───┬───┐         ┌───┬───┬───┬───┐
│S11│S12│S21│S22│         │13 │14 │23 │24 │
└───┴───┴───┴───┘         └───┴───┴───┴───┘
 │   │   │   │             │   │   │   │
 │   │   │   └─E-Stop 2    │   │   │   └─ MC2 Coil
 │   │   └─E-Stop 1        │   │   └─ MC2 Coil  
 │   └─Feedback from MC1   │   └─ MC1 Coil
 └─+24V Supply             └─ MC1 Coil

RESET CIRCUIT:
┌───┬───┐
│S33│S34│  ← Reset Button (NO)
└───┴───┘
 │   │
 │   └─ 0V
 └─ +24V

POWER SUPPLY:
┌───┬───┐
│A1 │A2 │  ← 24V DC Supply
└───┴───┘
```

---

## 6. FACTORYLM EDGE DEVICE INTEGRATION

### 6.1 Raspberry Pi Edge Device Connections

```
RASPBERRY PI 4B CONNECTIONS:

ETHERNET ──────────────────────┐
(To Factory Network)           │
                               │    ┌─────────────────┐
USB-C POWER ───────────────────┼───▶│  RASPBERRY PI   │
(5V, 3A Official Supply)       │    │     MODEL 4B    │
                               │    │   (factorylm-   │
                               │    │    edge-pi)     │
GPIO HEADER:                   │    └─────────────────┘
┌─────────────────────────────┐ │              │
│  2  4  6  8 10 12 14 16 ... │ │              │
│  1  3  5  7  9 11 13 15 ... │ │              ▼
└─────────────────────────────┘ │    ┌─────────────────┐
    │  │  │  │                  │    │   MICRO SD      │
    │  │  │  └─ GPIO14 (UART TX)│    │   (BalenaOS)    │
    │  │  └─ GPIO15 (UART RX) ──┼────│   64GB Class 10 │
    │  └─ Ground                 │    └─────────────────┘
    └─ 5V Power ────────────────┘
```

### 6.2 Data Collection Architecture

```
EDGE DEVICE DATA FLOW:

PLC (Micro820) ──┐                 ┌─── FactoryLM Cloud
                 │   ┌───────────┐ │    (Optional)
VFD (Modbus) ────┼──▶│   EDGE    │─┼──▶ https://api.factorylm.com
                 │   │  DEVICE   │ │    
Sensors ─────────┘   │(Rasp Pi)  │ └─── Local Dashboard
                     └───────────┘      http://100.97.210.121:3000
                           │
                           ▼
                    ┌─────────────┐
                    │   LOCAL     │
                    │  STORAGE    │ 
                    │ (SQLite +   │
                    │  InfluxDB)  │
                    └─────────────┘

DATA COLLECTION SERVICES:
┌─────────────────────────────────────────┐
│ Service          │ Purpose              │
├─────────────────────────────────────────┤
│ modbus-collector │ PLC & VFD data       │
│ mqtt-bridge      │ Local pub/sub        │ 
│ edge-api         │ REST API server      │
│ influxdb         │ Time-series DB       │
│ grafana          │ Dashboard/alerts     │
└─────────────────────────────────────────┘
```

### 6.3 Edge Device Software Stack

```
DOCKER CONTAINERS ON RASPBERRY PI:

┌─────────────────────────────────────────────────┐
│                   BalenaOS                      │
├─────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌──────────┐ │
│  │   MODBUS    │  │    MQTT     │  │   API    │ │
│  │ COLLECTOR   │  │   BROKER    │  │ SERVER   │ │  
│  │ (Python)    │  │(Mosquitto)  │  │(FastAPI) │ │
│  └─────────────┘  └─────────────┘  └──────────┘ │
├─────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌──────────┐ │
│  │  INFLUXDB   │  │   GRAFANA   │  │   NGINX  │ │
│  │(Time Series)│  │(Dashboard)  │  │(Reverse  │ │
│  │             │  │             │  │ Proxy)   │ │
│  └─────────────┘  └─────────────┘  └──────────┘ │
└─────────────────────────────────────────────────┘

NETWORK ACCESS:
- SSH: ssh root@100.97.210.121  
- Dashboard: http://100.97.210.121:3000
- API: http://100.97.210.121:8080
- MQTT: 100.97.210.121:1883
```

---

## 7. WIRING SCHEDULES & CABLE SPECIFICATIONS

### 7.1 Power Wiring Schedule

| Circuit | From | To | Cable Type | Size | Length | Notes |
|---------|------|----|-----------|----- |--------|-------|
| Main Power | Panel L1 | VFD L1 | THWN | 12 AWG | 10 ft | 20A Breaker |
| Main Power | Panel L2 | VFD L2 | THWN | 12 AWG | 10 ft | Neutral |  
| Ground | Panel GND | VFD GND | THWN | 12 AWG | 10 ft | Safety Ground |
| Motor | VFD T1 | Motor U1 | VFD Cable | 12 AWG | 15 ft | Shielded |
| Motor | VFD T2 | Motor V1 | VFD Cable | 12 AWG | 15 ft | Shielded |
| Motor | VFD T3 | Motor W1 | VFD Cable | 12 AWG | 15 ft | Shielded |
| PLC Power | 24V Supply | PLC +24V | THWN | 16 AWG | 3 ft | Control Power |

### 7.2 Control Wiring Schedule  

| Circuit | From | To | Cable Type | Size | Length | Notes |
|---------|------|----|-----------|----- |--------|-------|
| Modbus | PLC Term 5 | VFD A+ | Belden 3105A | 18 AWG | 6 ft | Data+ |
| Modbus | PLC Term 6 | VFD B- | Belden 3105A | 18 AWG | 6 ft | Data- |
| Modbus | PLC Term 7 | VFD GND | Belden 3105A | 18 AWG | 6 ft | Shield |
| Start Cmd | PLC Q0 | VFD Term 1 | Control Cable | 18 AWG | 6 ft | Digital In |
| Stop Cmd | PLC Q1 | VFD Term 2 | Control Cable | 18 AWG | 6 ft | Digital In |
| E-Stop | E-Stop NC | PLC I5 | Control Cable | 16 AWG | 8 ft | Safety |
| Prox 1 | Sensor 1 | PLC I1 | 4-Wire Cable | 18 AWG | 20 ft | +24V, 0V, Sig, Shd |
| Prox 2 | Sensor 2 | PLC I2 | 4-Wire Cable | 18 AWG | 25 ft | +24V, 0V, Sig, Shd |

### 7.3 Network/Communication Schedule

| Connection | Device A | Device B | Cable Type | Notes |
|------------|----------|----------|------------|-------|
| Ethernet | Raspberry Pi | Network Switch | Cat6 | Gigabit |
| Ethernet | PLC (if web) | Network Switch | Cat6 | Programming |
| USB | Raspberry Pi | USB Hub | USB 3.0 | Expansion |
| Power | Pi Supply | Wall Outlet | 5V/3A | Official Supply |

---

## 8. INSTALLATION NOTES

### 8.1 Safety Requirements
- All electrical work must be performed by qualified electricians
- Lock out/tag out (LOTO) procedures must be followed
- Verify zero energy state before working on equipment
- Use appropriate PPE (safety glasses, insulated tools, arc flash protection)
- Install arc fault circuit interrupters (AFCI) where required by code

### 8.2 Code Compliance  
- Installation must comply with NEC (National Electrical Code)
- Local electrical codes may have additional requirements
- UL listed components required for commercial installations
- Proper grounding and bonding per NEC Article 250

### 8.3 Testing & Commissioning
1. **Megger Test** - Insulation resistance test on all motor circuits
2. **Continuity Test** - Verify all connections per wiring diagrams
3. **Phase Rotation** - Confirm correct motor rotation direction  
4. **Modbus Communication** - Test PLC to VFD communication
5. **Safety Circuit** - Test emergency stop functionality
6. **Load Test** - Run system under normal operating conditions

### 8.4 Documentation Requirements
- As-built drawings showing actual installation
- Test certificates for all safety circuits  
- Modbus configuration backup
- PLC program backup with version control
- Startup/shutdown procedures
- Maintenance schedule and procedures

---

**END OF ELECTRICAL DIAGRAMS**  
**Document Control: JOB-2026-0206-001-ELECTRICAL-v1.0**