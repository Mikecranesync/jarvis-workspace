# FactoryLM Hardware Packs - Product Strategy

*Created: Feb 3, 2026*

## Strategy

Resell proven third-party industrial modules with:
- FactoryLM branding
- Pre-configured for our gateway
- 20-30% markup for config/testing/docs
- QR code → FactoryLM web UI

**Key insight:** Don't reinvent hardware. Bundle, configure, document.

---

## Product Line

### 📊 Analog Pack (AP Series)

| SKU | Description | Based On | Est. Cost | Sell Price |
|-----|-------------|----------|-----------|------------|
| AP-4 | 4-channel 4-20mA/0-10V | Datexel DAT10024 | $150 | $199 |
| AP-8 | 8-channel 4-20mA input | Lucid Control | $200 | $269 |

**Candidates:**
- Datexel DAT10024 - 4ch isolated 4-20mA/0-10V outputs, Modbus RTU
- Jewell DIN-125 - 4-20mA current input, isolated, Modbus
- LucidControl/Lucid485 - 4/8 analog inputs, RS-485 Modbus RTU
- Widgetlords - Low-cost 4-20mA RS485 Modbus (4/8 ch)

---

### 🌬️ Pneumatic Pack (PP Series)

| SKU | Description | Contents | Est. Cost | Sell Price |
|-----|-------------|----------|-----------|------------|
| PP-1 | I/P + P/I Starter | I/P transducer + P/I transmitter + tubing + fittings | $300 | $399 |

**Candidates:**
- ControlAir 500-AC - 4-20mA → 3-15 psi (I/P)
- Moore Industries PIT - 3-15 psi → 4-20mA (P/I)

---

### 🔌 Remote I/O Pack (IO Series)

| SKU | Description | Based On | Est. Cost | Sell Price |
|-----|-------------|----------|-----------|------------|
| IO-8 | 8-channel mixed I/O | Valtoris WiFi/Ethernet | $180 | $249 |

**Candidates:**
- Valtoris Remote I/O - 8 AI/DI, relays, Modbus TCP/RTU
- Use as "dumb Modbus I/O" behind our gateway

---

### 🔗 Serial Pack (SP Series)

| SKU | Description | Contents | Est. Cost | Sell Price |
|-----|-------------|----------|-----------|------------|
| SP-2 | Serial Converter Kit | USB-RS232 + USB-RS485 + terminal adapters | $50 | $79 |

---

## What Ships With Each Pack

1. ✅ Pre-written config template for FactoryLM gateway
2. ✅ Wiring diagram (laminated)
3. ✅ QR code → FactoryLM web UI for that pack
4. ✅ Quick start guide
5. ✅ Known-good tested with our software

---

## Implementation Roadmap

### Phase 1: Select & Test (1 week)
- [ ] Pick 1-2 brands per function
- [ ] Order samples
- [ ] Integrate via Modbus RTU in gateway
- [ ] Document quirks

### Phase 2: Productize (1 week)
- [ ] Create SKUs
- [ ] Write config templates
- [ ] Design wiring diagrams
- [ ] Create QR-linked web UI pages

### Phase 3: List & Sell
- [ ] Add to factorylm.com/hardware
- [ ] Pricing page
- [ ] Shopify/Stripe integration
- [ ] Inventory with supplier

---

## Supplier Links

- Datexel: https://www.datexel.com/isolated-modbus-rtu-4-20ma-output-dat10024.html
- Jewell: https://jewellinstruments.com/products/dgh/modbus-modules/din-125-modbus-4-20ma-current-input-module/
- LucidControl: https://www.lucid-control.com/product/rs-485-modbus-rtu-analog-input-module-4-8-daq-channels/
- Widgetlords: https://widgetlords.com/products/analog-input-module-8-channels-4-20ma-rs485-modbus-interface
- ControlAir: https://tecotechnology.com/products/control-air-l-transducer-i-p-4-20ma-3-15psi-1-17vdc-500-acw
- Valtoris: https://valtoris.com/shop/industrial-networking-connectivity/remote-io-controller-en/remote-io-module-rs485-wifi-ethernet-valtoris/

---

## Margin Analysis

| Pack | Cost | Price | Margin | Margin % |
|------|------|-------|--------|----------|
| AP-4 | $150 | $199 | $49 | 25% |
| AP-8 | $200 | $269 | $69 | 26% |
| PP-1 | $300 | $399 | $99 | 25% |
| IO-8 | $180 | $249 | $69 | 28% |
| SP-2 | $50 | $79 | $29 | 37% |

**Average margin: ~28%**

---

*The real money is in the software subscription. Hardware packs are customer acquisition.*
