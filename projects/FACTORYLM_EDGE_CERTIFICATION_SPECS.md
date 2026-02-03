# FactoryLM Edge Device - Certification & Compliance Specifications

## Product: FactoryLM Edge Gateway
**Target Market:** Industrial facilities, manufacturing plants, maintenance teams
**Device Type:** Industrial IoT Gateway (Raspberry Pi 4 based)

---

## 🎯 Certification Goals

### Required Certifications (Priority Order)

| Certification | Region | Purpose | Priority |
|---------------|--------|---------|----------|
| FCC Part 15 | USA | Radio frequency emissions | P0 |
| CE Mark | EU | European conformity | P0 |
| UL/cUL Listing | USA/Canada | Safety certification | P1 |
| IEC 62443 | Global | Industrial cybersecurity | P1 |
| ATEX/IECEx | EU/Global | Hazardous areas (if applicable) | P2 |
| RoHS | EU | Hazardous substances | P0 |
| REACH | EU | Chemical compliance | P1 |

---

## 📋 Test Specifications

### 1. Electromagnetic Compatibility (EMC)

**Standard:** EN 55032 / FCC Part 15 Class A (Industrial)

| Test | Specification | Pass Criteria |
|------|---------------|---------------|
| Radiated Emissions | 30 MHz - 1 GHz | Below Class A limits |
| Conducted Emissions | 150 kHz - 30 MHz | Below Class A limits |
| ESD Immunity | IEC 61000-4-2 | ±8kV contact, ±15kV air |
| RF Immunity | IEC 61000-4-3 | 80-1000 MHz, 10 V/m |
| Surge Immunity | IEC 61000-4-5 | ±2kV line-to-line |

### 2. Environmental Testing

**Standard:** IEC 60068 series

| Test | Specification | Pass Criteria |
|------|---------------|---------------|
| Operating Temp | IEC 60068-2-1/2 | 0°C to +50°C |
| Storage Temp | IEC 60068-2-1/2 | -20°C to +70°C |
| Humidity | IEC 60068-2-30 | 10-90% RH non-condensing |
| Vibration | IEC 60068-2-6 | 10-500 Hz, 2g |
| Shock | IEC 60068-2-27 | 30g, 11ms |

### 3. Electrical Safety

**Standard:** IEC 62368-1 / UL 62368-1

| Test | Specification | Pass Criteria |
|------|---------------|---------------|
| Dielectric Strength | IEC 62368-1 | 1500V AC, 1 minute |
| Insulation Resistance | IEC 62368-1 | >10 MΩ |
| Ground Continuity | IEC 62368-1 | <0.1Ω |
| Leakage Current | IEC 62368-1 | <3.5mA |

### 4. Industrial Protocol Conformance

| Protocol | Standard | Test |
|----------|----------|------|
| Modbus TCP | Modbus-IDA Conformance | Modbus Conformance Test Tool |
| OPC UA | OPC Foundation CTT | Compliance Test Tool |
| MQTT | MQTT 3.1.1/5.0 | Eclipse Paho test suite |
| EtherNet/IP | ODVA Conformance | ODVA test procedures |

### 5. Cybersecurity

**Standard:** IEC 62443-4-2 (Component Security)

| Requirement | Level | Implementation |
|-------------|-------|----------------|
| Authentication | SL2 | User accounts, API keys |
| Authorization | SL2 | Role-based access |
| Data Integrity | SL2 | TLS 1.3, message signing |
| Data Confidentiality | SL2 | Encryption at rest/transit |
| Audit Logging | SL2 | All access logged |
| DoS Protection | SL1 | Rate limiting |

---

## 🧪 Observability & Tracing Requirements

### System Traces (Required for Certification)

```yaml
traces:
  - name: boot_sequence
    events:
      - hardware_init
      - os_boot
      - network_connect
      - tailscale_auth
      - service_start
      - health_check_pass
    retention: 90_days

  - name: plc_communication
    events:
      - connection_attempt
      - connection_success/failure
      - read_request
      - read_response
      - write_request (if applicable)
      - connection_close
    retention: 30_days

  - name: security_events
    events:
      - login_attempt
      - login_success/failure
      - api_access
      - config_change
      - firmware_update
    retention: 1_year

  - name: error_events
    events:
      - hardware_fault
      - network_timeout
      - protocol_error
      - service_crash
      - recovery_action
    retention: 1_year
```

### Metrics (Required for Quality)

```yaml
metrics:
  system:
    - cpu_usage_percent
    - memory_usage_percent
    - disk_usage_percent
    - temperature_celsius
    - uptime_seconds

  network:
    - bytes_sent
    - bytes_received
    - connection_count
    - latency_ms
    - packet_loss_percent

  plc:
    - read_count
    - read_errors
    - response_time_ms
    - connection_uptime

  business:
    - alerts_sent
    - diagnoses_requested
    - api_calls
```

### Health Check Specification

```json
{
  "endpoint": "/health",
  "interval_seconds": 30,
  "checks": [
    {"name": "system", "type": "cpu_memory_disk"},
    {"name": "network", "type": "connectivity"},
    {"name": "plc", "type": "connection_status"},
    {"name": "services", "type": "process_running"},
    {"name": "storage", "type": "log_rotation"}
  ],
  "alert_on": ["critical", "warning_3x"]
}
```

---

## 📁 Documentation Requirements (For Certification)

### Technical Documentation

| Document | Purpose | Status |
|----------|---------|--------|
| Hardware Schematic | Shows electrical design | ⬜ Needed |
| Bill of Materials | Component list | ⬜ Needed |
| PCB Layout | Board design (if custom) | N/A (COTS Pi) |
| Software Architecture | System design | ✅ Created |
| API Documentation | Interface specs | ⬜ Needed |
| Installation Guide | Setup procedures | ✅ Created |
| User Manual | Operation instructions | ⬜ Needed |

### Test Reports

| Report | Standard | Status |
|--------|----------|--------|
| EMC Test Report | EN 55032 | ⬜ Needed |
| Safety Test Report | IEC 62368-1 | ⬜ Needed |
| Environmental Test Report | IEC 60068 | ⬜ Needed |
| Protocol Conformance | Various | ⬜ Needed |
| Cybersecurity Assessment | IEC 62443 | ⬜ Needed |

---

## 🔧 Implementation Checklist

### Phase 1: Software Observability (This Week)
- [ ] Implement structured logging
- [ ] Add trace IDs to all requests
- [ ] Create health check endpoint
- [ ] Set up metrics collection
- [ ] Configure log rotation

### Phase 2: Testing Infrastructure (Next Week)
- [ ] Create automated test suite
- [ ] Set up CI/CD with tests
- [ ] Document test procedures
- [ ] Create test data generators

### Phase 3: Pre-Certification (Before Demo)
- [ ] Self-test EMC with SDR
- [ ] Verify power consumption
- [ ] Stress test for 72 hours
- [ ] Security penetration test

### Phase 4: Certification (Post-Demo)
- [ ] Select test lab (TUV, UL, Intertek)
- [ ] Submit for FCC/CE testing
- [ ] Address any failures
- [ ] Obtain certificates

---

## 💰 Estimated Certification Costs

| Certification | Estimated Cost | Timeline |
|---------------|----------------|----------|
| FCC Part 15 | $3,000 - $8,000 | 4-6 weeks |
| CE Mark (self-declare) | $2,000 - $5,000 | 4-8 weeks |
| UL Listing | $10,000 - $25,000 | 8-12 weeks |
| IEC 62443 | $15,000 - $30,000 | 12-16 weeks |

**Total (Basic FCC + CE):** ~$5,000 - $13,000
**Total (Full Industrial):** ~$30,000 - $70,000

---

## 🔗 Resources

- FCC Equipment Authorization: https://www.fcc.gov/engineering-technology/laboratory-division/general/equipment-authorization
- CE Marking Guide: https://ec.europa.eu/growth/single-market/ce-marking_en
- IEC 62443 Overview: https://www.isa.org/isa62443
- UL Product iQ: https://iq.ulprospector.com/

---

*Document created: 2026-02-03*
*Next review: Before Feb 10 demo*
