# ShopTalk Tuesday Demo Script
## Factory I/O + Edge AI Live Presentation

### Duration: 5-10 minutes

---

## Setup (Before Demo)

### Hardware
- [ ] BeagleBone/RPi connected via USB
- [ ] WireGuard tunnel active
- [ ] Factory I/O running on Mike's PC
- [ ] Modbus server enabled in Factory I/O

### Software
- [ ] ShopTalk trained on normal operation
- [ ] Voice set to Spanish
- [ ] Camera ready for recording

---

## Demo Flow

### 1. Opening (30 sec)
**[Show the device]**

"This is a $50 device. It's running AI that can diagnose factory equipment problems - in real-time, offline, in any language."

**[Hold up BeagleBone/RPi]**

### 2. The Setup (1 min)
**[Show Factory I/O on screen]**

"This is Factory I/O - an industrial simulation that talks to real PLCs. Right now, it's connected to our edge device over Modbus."

**[Point to the simulated conveyor]**

"We've got a conveyor system here. Motors, sensors, the works."

### 3. Normal Operation (1 min)
**[Run ShopTalk monitoring]**

"The AI has already learned what 'normal' looks like. It's been watching this system run."

**[Show terminal with green checkmarks]**

"Everything's healthy. Motor speed, current draw, temperature - all within expected ranges."

### 4. Inject the Fault (2 min)
**[Trigger conveyor jam in Factory I/O]**

"Now watch what happens when something goes wrong..."

**[Wait for alarm]**

"🚨 The AI caught it immediately. Listen to what it says."

**[ShopTalk speaks in Spanish]**

"Corriente alta del motor detectada. Posible sobrecarga mecánica."

"That's Spanish. It just told the operator: High motor current detected. Possible mechanical overload."

### 5. The Key Points (1 min)

"Three things to notice here:

1. **Speed** - It caught the problem in under a second
2. **Offline** - No cloud. Everything runs locally on this device
3. **Multilingual** - Spanish, English, Portuguese - whatever the operator speaks

This is ShopTalk. Industrial AI that actually works on the factory floor."

### 6. Close (30 sec)

"We're launching this Tuesday. DM me if you want one for your factory."

**[Hold up device again]**

"$50. Works anywhere. Speaks any language."

---

## Technical Backup

### If Something Fails

**Connection Issues:**
```bash
# Check WireGuard
wg show wg0

# Restart connection
systemctl restart wg-quick@wg0
```

**ShopTalk Not Starting:**
```bash
# Check service
systemctl status shoptalk

# Run manually
cd /opt/factorylm/shoptalk
python3 demo.py --test
```

**No Audio:**
- Use text output instead
- Say the diagnosis yourself

### Demo Commands

```bash
# Run demo (English)
python3 demo.py --scenario jam

# Run demo (Spanish with voice)
python3 demo.py --scenario jam --language es --voice

# Quick test
python3 demo.py --test
```

---

## Recording Notes

1. **Lighting** - Face the window or use ring light
2. **Audio** - Use lapel mic if possible
3. **Framing** - Device in hand, screen visible behind
4. **Energy** - This is exciting! Show it.

### B-Roll Ideas
- Close-up of BeagleBone/RPi
- Factory I/O conveyor running
- Terminal showing real-time monitoring
- Spanish text on screen

---

## Post-Demo

- [ ] Upload to LinkedIn
- [ ] Tweet thread with key moments
- [ ] DM interested parties
- [ ] Collect email addresses
