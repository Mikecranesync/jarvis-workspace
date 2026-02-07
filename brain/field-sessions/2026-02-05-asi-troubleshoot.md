# Field Session: ASI System Troubleshooting
**Date:** 2026-02-05 04:33 UTC
**Vehicle:** Industrial/Transit (Purple chassis, IEC 81346 labeling)
**Deadline:** 08:30 AM local
**Purpose:** YC Demo Test Case - Real-world AI-assisted troubleshooting

---

## Session Log

### 04:33 - Session Start
- Mike moving to job site, monitoring for service interruptions

### 04:34 - First Image: Terminal Blocks
- DIN rail terminal blocks
- Labels: =VEH.1+21-X09.31, =VEH.1+21-X09.91
- IEC 81346 naming convention
- Phoenix Contact/WAGO style
- Red jumpers bridging terminals 1-4 and 5-7

### 04:52 - Three Images Received
1. **Milwaukee ONE-KEY card** - Tool tracking tag, marked "PRLA"
2. **Bulkhead connector** - Multi-pin circular connector on purple chassis panel
3. **Cable connector** - Same type, heavy grease/oil around it, CJC filter visible

### Connector Identification
- Type: Deutsch HD10/HD30 series (or Amphenol/AMP CPC)
- Disconnect: Counter-clockwise threaded coupling ring
- Concern: Oil/grease intrusion in photo 3

### 04:57 - Manual Request + Catalog Directive
- Pull Deutsch connector manual
- Catalog all inputs for intake chatbot testing
- Spawn sub-agents to test intake system weaknesses

---

## Assets Received
| Time | Type | File | Description |
|------|------|------|-------------|
| 04:34 | Image | b606206d-109f-4564-86a8-f200db114d56.jpg | Terminal blocks |
| 04:52 | Image | aa8b1138-1827-4c72-8ffd-86b879d0b9b0.jpg | Milwaukee ONE-KEY card |
| 04:52 | Image | 94692e76-a34e-412d-9caf-4c286b24aa20.jpg | Bulkhead connector |
| 04:52 | Image | 5120cff9-2d36-452d-b792-05295160edbc.jpg | Cable connector + grease |

---

## For Intake Bot Testing
This session = test case for:
- Image recognition (connector types, terminal blocks)
- Context extraction from voice/text
- Troubleshooting flow
- Documentation generation

### Weaknesses to Probe:
- [ ] Can bot identify connector types from photos?
- [ ] Can bot extract part numbers from images?
- [ ] Can bot handle multi-image context?
- [ ] Can bot maintain troubleshooting state across messages?
- [ ] Can bot pull relevant manuals automatically?
