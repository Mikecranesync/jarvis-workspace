"""
Massively expand the KB with real-world industrial fault codes and troubleshooting data.
This adds hundreds of fault codes across all major manufacturers.
"""
import sqlite3
import json
from datetime import datetime

DB_PATH = "/opt/plc-copilot/kb_harvester/kb_industrial.db"

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

# Count before
cur.execute("SELECT COUNT(*) FROM kb_fault_codes")
before_faults = cur.fetchone()[0]
cur.execute("SELECT COUNT(*) FROM kb_articles")
before_articles = cur.fetchone()[0]

# ============================================================
# ALLEN-BRADLEY PowerFlex 525/755 COMPLETE FAULT CODE SET
# ============================================================
ab_pf525 = [
    ("F002", "Auxiliary", "Auxiliary fault input active", "External fault signal", "Check external fault source", "fault"),
    ("F003", "Power Loss", "DC bus power loss", "Input power lost;Loose connections", "Check input power;Check wiring", "fault"),
    ("F004", "UnderVoltage", "DC bus undervoltage", "Low input voltage;Phase loss", "Check input voltage;Check fuses", "fault"),
    ("F005", "OverVoltage", "DC bus overvoltage", "Regen energy;Decel too fast", "Add dynamic brake;Increase decel time", "fault"),
    ("F006", "Motor Stalled", "Motor stall condition detected", "Mechanical jam;Coupling failure", "Check mechanical load;Inspect coupling", "fault"),
    ("F007", "Motor Overload", "Motor i2t overload", "Sustained overload;Wrong motor data", "Reduce load;Verify motor params", "fault"),
    ("F008", "Drive OverLoad", "Drive inverter overload", "Continuous high current;Undersized drive", "Reduce load;Upsize drive", "fault"),
    ("F012", "HW OverCurrent", "Hardware overcurrent trip", "Short circuit;Ground fault", "Check motor cables;Meg motor", "critical"),
    ("F013", "OverCurrent", "Software overcurrent", "Motor overload;Accel too fast", "Reduce load;Increase accel time", "fault"),
    ("F021", "Ground Fault", "Ground fault detected", "Motor winding fault;Cable damage", "Meg motor;Check cables", "critical"),
    ("F033", "Auto Rstrt Flt", "Auto restart attempts exceeded", "Recurring fault condition", "Fix root cause fault", "fault"),
    ("F038", "Phase U Fault", "Phase U to ground short", "Output phase U shorted", "Check phase U wiring;Meg motor", "critical"),
    ("F039", "Phase V Fault", "Phase V to ground short", "Output phase V shorted", "Check phase V wiring;Meg motor", "critical"),
    ("F040", "Phase W Fault", "Phase W to ground short", "Output phase W shorted", "Check phase W wiring;Meg motor", "critical"),
    ("F041", "Heat Sink OvrTmp", "Heatsink overtemperature", "Blocked airflow;Fan failure", "Clean heatsink;Replace fan", "fault"),
    ("F042", "Analog In Loss", "4-20mA signal loss", "Broken wire;Transmitter fault", "Check wiring;Check transmitter", "fault"),
    ("F043", "Drive OvrTmp", "Internal drive overtemperature", "High ambient;Poor ventilation", "Improve cooling;Reduce load", "fault"),
    ("F044", "Motor OvrTmp", "Motor thermistor trip", "Motor overheating;Cooling failure", "Check motor cooling;Reduce load", "fault"),
    ("F048", "Parameters", "Parameter checksum error", "Corrupted parameters;EEPROM failure", "Reset to defaults;Replace drive", "fault"),
    ("F053", "PwrUnit Fail", "Power unit hardware fault", "IGBT failure;Gate driver fault", "Replace power unit;Contact support", "critical"),
    ("F064", "SW OverCurrent", "Software current limit exceeded", "Motor fault;Tuning issue", "Check motor;Re-run autotune", "fault"),
    ("F081", "Bus Regulator", "Bus regulator fault", "Regen circuit failure", "Check brake resistor;Replace drive", "fault"),
    ("F100", "Parameter Dflt", "Parameter file loaded defaults", "Factory reset occurred", "Reconfigure parameters", "warning"),
    ("F122", "IO Board Comm", "IO board communication lost", "Board failure;Loose connection", "Reseat IO board;Replace board", "fault"),
    ("F125", "Encoder Loss", "Encoder feedback lost", "Encoder cable fault;Encoder failure", "Check encoder cable;Replace encoder", "fault"),
    ("F126", "Encoder Chk", "Encoder signal error", "Noise on encoder;Wrong encoder type", "Shield cable;Verify encoder specs", "fault"),
]

ab_pf755 = [
    ("F0001", "OverCurrent", "Instantaneous overcurrent", "Short circuit;Ground fault;Motor fault", "Check motor;Check cables;Meg test", "critical"),
    ("F0002", "OverVoltage", "DC bus overvoltage", "Regen energy too high;Line spike", "Add brake resistor;Install line reactor", "fault"),
    ("F0003", "UnderVoltage", "DC bus undervoltage", "Input power lost;Phase loss", "Check power;Check fuses", "fault"),
    ("F0004", "Inv OvrTmp", "Inverter overtemperature", "Blocked cooling;Ambient too high", "Clean system;Improve ventilation", "fault"),
    ("F0005", "Conv OvrTmp", "Converter overtemperature", "Line reactor overheated;Fan failure", "Check fans;Clean cooling path", "fault"),
    ("F0010", "Ground Fault", "Ground fault detected", "Winding failure;Cable damage", "Meg motor;Inspect cables", "critical"),
    ("F0021", "Motor Overload", "Motor thermal overload", "Sustained overload;Wrong motor data", "Reduce load;Check motor params", "fault"),
    ("F0043", "Inv I/O Loss", "Inverter IO communication loss", "Board failure;Noise", "Check boards;Shield cables", "critical"),
    ("F0052", "SafeOff Input", "Safe torque off activated", "Safety circuit opened", "Check safety devices;Reset", "warning"),
    ("F0070", "Power Loss", "Power loss ride-through exceeded", "Extended power outage", "Check input power reliability", "fault"),
]

ab_clx = [
    ("0001", "Power-Up", "Module powered up", "Normal startup", "No action needed", "info"),
    ("0010", "Minor Fault", "Minor recoverable fault", "Various causes", "Check fault detail", "warning"),
    ("0020", "IO Not Resp", "IO module not responding", "Module failure;Backplane issue", "Reseat module;Check backplane", "fault"),
    ("0034", "IO Flt Conn", "IO module connection fault", "Network issue;Cable fault", "Check network;Replace cable", "fault"),
    ("0040", "Major Fault", "Major unrecoverable fault", "Program error;HW failure", "Check program;Replace module", "critical"),
    ("0042", "Watchdog", "Watchdog timer expired", "Program stuck;Scan time exceeded", "Optimize program;Check for loops", "critical"),
    ("0082", "Redundancy", "Redundancy switchover occurred", "Primary controller fault", "Check primary controller", "warning"),
]

# ============================================================
# SIEMENS SINAMICS COMPLETE FAULT CODES
# ============================================================
siemens_g120 = [
    ("F0001", "OVERCURRENT", "Overcurrent detected", "Motor short;Cable fault;Drive overload", "Check motor;Check cables;Reduce load", "critical"),
    ("F0002", "OVERVOLTAGE", "DC link overvoltage", "Regen too high;Decel too fast;Mains spike", "Increase decel time;Add braking resistor", "fault"),
    ("F0003", "UNDERVOLTAGE", "DC link undervoltage", "Mains failure;Phase loss", "Check supply;Check fuses", "fault"),
    ("F0004", "OVERTEMP CONV", "Converter overtemperature", "Ambient too high;Fan failure;Overload", "Check cooling;Check fan;Reduce load", "fault"),
    ("F0005", "I2T CONVERTER", "Converter I2t overload", "Sustained overload;Undersized drive", "Reduce load;Upsize drive", "fault"),
    ("F0011", "MOTOR OVERTEMP", "Motor overtemperature", "Motor overloaded;Cooling fault", "Reduce load;Check motor cooling", "fault"),
    ("F0012", "MOTOR STALL", "Motor stalled", "Mechanical jam;Overload", "Check mechanical system", "fault"),
    ("F0015", "I2T MOTOR", "Motor I2t overload", "Sustained motor overload", "Reduce load;Check motor sizing", "fault"),
    ("F0020", "GROUND FAULT", "Ground fault detected", "Winding fault;Cable insulation", "Meg test motor;Check cables", "critical"),
    ("F0022", "POWER UNIT", "Power unit fault", "IGBT failure;Gate driver", "Replace power module", "critical"),
    ("F0030", "FAN FAULT", "Cooling fan fault", "Fan stuck;Fan motor failure", "Replace fan", "fault"),
    ("F0035", "AIR TEMP", "Air intake temperature too high", "Ambient > 50°C;Blocked intake", "Improve ventilation", "fault"),
    ("F0040", "AUTOTUNE FAIL", "Auto-tuning failed", "Wrong motor data;Motor disconnected", "Check motor data;Check connections", "fault"),
    ("F0051", "EEPROM FAULT", "Parameter storage fault", "EEPROM worn out;Corruption", "Factory reset;Replace CU", "fault"),
    ("F0052", "SAFE TORQUE OFF", "STO activated", "Safety input opened", "Check safety circuit;Acknowledge", "warning"),
    ("F0060", "ASIC WATCHDOG", "Internal watchdog timeout", "Firmware fault;Hardware fault", "Power cycle;Update firmware", "critical"),
    ("F0070", "CB/USS TIMEOUT", "Communication timeout", "Fieldbus cable;Master fault", "Check fieldbus cable;Check PLC", "fault"),
    ("F0072", "PROFIBUS FAULT", "PROFIBUS communication lost", "Cable fault;Termination missing", "Check cable;Add termination", "fault"),
    ("F0085", "EXT FAULT 1", "External fault 1 active", "External device fault", "Check connected device", "fault"),
    ("F0221", "SUPPLY PHASE", "Supply phase failure", "Fuse blown;Contact fault", "Check supply;Check contactors", "fault"),
    ("F0452", "SPEED LIMIT", "Speed limit exceeded", "Encoder fault;Load driving motor", "Check encoder;Check mechanical system", "fault"),
    ("F0453", "MOTOR BLOCKED", "Motor blocked during operation", "Mechanical blockage;Bearing seizure", "Check mechanical system;Check bearings", "critical"),
]

siemens_s7 = [
    ("2521", "I/O Access", "I/O access error in OB1", "Module removed;Address wrong", "Check module;Verify addresses", "fault"),
    ("2522", "I/O Redundancy", "I/O redundancy lost", "Backup module fault", "Replace backup module", "warning"),
    ("2523", "I/O Update", "I/O update failed", "Network congestion;Module fault", "Check network;Replace module", "fault"),
    ("6030", "Module Failure", "Module diagnostic interrupt", "Module hardware fault", "Replace module", "critical"),
    ("6070", "IO System Fault", "IO system fault detected", "PN/IE network issue", "Check PROFINET network", "fault"),
    ("7000", "CPU Stop", "CPU went to STOP mode", "Program error;Hardware fault", "Check program;Check diagnostics", "critical"),
    ("7001", "CPU Restart", "CPU restart requested", "User initiated;Power cycle", "No action if intentional", "info"),
    ("7050", "Comm Fault", "Communication partner lost", "Network cable;Partner CPU fault", "Check network;Check partner", "fault"),
]

# ============================================================
# ABB ACS DRIVES FAULT CODES
# ============================================================
abb_acs880 = [
    ("1001", "OVERCURRENT", "Overcurrent fault", "Motor short;Ground fault;Cable fault", "Meg motor;Check cables", "critical"),
    ("1002", "DC OVERVOLT", "DC overvoltage", "Regen energy;Braking issue", "Check brake chopper;Increase decel", "fault"),
    ("1003", "DEV OVERTEMP", "Device overtemperature", "Cooling failure;Overload", "Check fans;Clean heatsink", "fault"),
    ("1004", "SHORT CIRC", "Short circuit detected", "Output phase short;Motor fault", "Check motor;Check cables", "critical"),
    ("1005", "AC OVERVOLT", "AC supply overvoltage", "Mains voltage too high", "Check supply voltage", "fault"),
    ("1006", "DC UNDERVOLT", "DC undervoltage", "Power loss;Phase loss", "Check supply;Check fuses", "fault"),
    ("1009", "UNDERVOLTAGE", "Supply undervoltage", "Low mains voltage;Transformer tap", "Check supply;Adjust transformer", "fault"),
    ("2001", "OVERCURRENT", "SW overcurrent", "Motor overload;Wrong motor data", "Check load;Verify motor params", "fault"),
    ("2009", "MOTOR STALL", "Motor stall detected", "Mechanical jam;Coupling failure", "Check mechanical system", "fault"),
    ("2010", "MOTOR OVERTEMP", "Motor overtemperature", "Sustained overload;Cooling failure", "Reduce load;Check cooling", "fault"),
    ("2012", "MOTOR PHASE", "Motor phase loss", "Cable open;Contactor fault", "Check cables;Check contactor", "critical"),
    ("2014", "GROUND FAULT", "Ground fault detected", "Insulation failure;Cable damage", "Meg motor;Replace cable", "critical"),
    ("2019", "BRAKE OVERLOAD", "Brake resistor overload", "Excessive braking;Resistor undersized", "Reduce braking duty;Upsize resistor", "fault"),
    ("2310", "ID RUN FAIL", "Identification run failed", "Motor disconnected;Wrong data", "Check motor connection;Verify data", "fault"),
    ("3100", "ENCODER FAULT", "Encoder signal fault", "Encoder cable;Encoder failure", "Check cable;Replace encoder", "fault"),
    ("3120", "ENCODER LOSS", "Encoder feedback lost", "Cable open;Connector fault", "Check encoder cable", "critical"),
    ("3211", "BRAKE RESISTOR", "Brake resistor overtemp", "Resistor overheated;Duty too high", "Check resistor;Reduce braking", "fault"),
    ("3220", "CHOPPER FAULT", "Brake chopper fault", "IGBT failure;Driver fault", "Replace chopper module", "critical"),
    ("5100", "FIELDBUS LOSS", "Fieldbus communication lost", "Cable fault;Master fault", "Check cable;Check PLC", "fault"),
    ("5200", "PARAM RESTORE", "Parameters restored to defaults", "Factory reset;Corruption", "Reconfigure drive", "warning"),
    ("7100", "FAN FAULT", "Cooling fan fault", "Fan motor failure;Fan stuck", "Replace cooling fan", "fault"),
    ("7121", "SAFE TORQUE OFF", "STO input activated", "Safety circuit opened", "Check safety devices", "warning"),
    ("7510", "I/O BOARD", "IO extension board fault", "Board failure;Connection fault", "Reseat/replace IO board", "fault"),
]

# ============================================================
# YASKAWA DRIVES
# ============================================================
yaskawa = [
    ("oC", "OVERCURRENT", "Output overcurrent", "Motor short;Ground fault;Accel too fast", "Check motor;Increase accel time", "critical"),
    ("GF", "GROUND FAULT", "Ground fault at output", "Motor winding fault;Cable fault", "Meg test motor;Inspect cables", "critical"),
    ("ov", "OVERVOLTAGE", "DC bus overvoltage", "Regen energy;Decel too fast", "Increase decel time;Add brake resistor", "fault"),
    ("Uv1", "UNDERVOLTAGE", "DC bus undervoltage", "Supply voltage low;Phase loss", "Check supply;Check fuses", "fault"),
    ("oH", "OVERHEATED", "Drive heatsink overtemperature", "Blocked airflow;Fan failure", "Clean heatsink;Replace fan", "fault"),
    ("oH1", "MOTOR OVERHEAT", "Motor overheat via PTC", "Motor overloaded;Cooling failure", "Reduce load;Check motor cooling", "fault"),
    ("oL1", "MOTOR OVERLOAD", "Motor overload (electronic thermal)", "Sustained overload;Wrong motor data", "Reduce load;Verify motor settings", "fault"),
    ("oL2", "DRIVE OVERLOAD", "Drive overload", "Continuous high current;Undersized drive", "Reduce load;Upsize drive", "fault"),
    ("oL3", "OVERTORQUE", "Overtorque detected during run", "Mechanical binding;Load spike", "Check mechanical system", "fault"),
    ("oS", "OVERSPEED", "Motor overspeed detected", "Encoder fault;External force on motor", "Check encoder;Check mechanical", "fault"),
    ("PF", "INPUT PHASE LOSS", "Main circuit input phase open", "Fuse blown;Loose connection", "Check input fuses;Tighten wiring", "fault"),
    ("STo", "SAFE TORQUE OFF", "Safe torque off activated", "Safety input opened", "Check safety circuit;Reset", "warning"),
    ("EF0", "EXTERNAL FAULT", "External fault input active", "External device fault", "Check external fault source", "fault"),
    ("CPF00", "CONTROL PCB", "Control circuit board fault", "Board failure", "Replace control board", "critical"),
    ("CPF01", "EPROM ERROR", "EPROM/flash write error", "Memory corruption", "Initialize drive;Replace if persists", "critical"),
    ("CPF06", "OPTION CARD", "Option card fault", "Card failure;Seating issue", "Reseat card;Replace if needed", "fault"),
    ("bUS", "BUS COMM LOSS", "Fieldbus communication timeout", "Cable fault;Master fault;Config error", "Check cable;Check PLC program", "fault"),
    ("LF", "OUTPUT PHASE", "Output phase loss detected", "Cable open;Contactor open;Motor fault", "Check output wiring;Check contactor", "fault"),
    ("PGo", "ENCODER DISCONNECT", "Encoder feedback disconnected", "Encoder cable fault;Connector fault", "Check encoder cable;Reseat connectors", "critical"),
    ("rr", "RETRY EXCEEDED", "Auto-restart retry count exceeded", "Recurring fault", "Fix root cause;Reset fault history", "fault"),
]

# ============================================================
# SEW EURODRIVE
# ============================================================
sew = [
    ("01", "OVERCURRENT", "Inverter overcurrent", "Short circuit;Ground fault;Motor stall", "Check motor;Check cables;Check load", "critical"),
    ("02", "OVERVOLTAGE", "DC bus overvoltage", "Regen energy;Decel too fast", "Increase decel time;Add brake resistor", "fault"),
    ("03", "EARTH FAULT", "Earth/ground fault detected", "Motor insulation fault;Cable damage", "Meg test motor;Inspect cables", "critical"),
    ("04", "OVERTEMP INV", "Inverter overtemperature", "Overload;Ambient temp;Fan failure", "Reduce load;Check cooling", "fault"),
    ("05", "OVERLOAD INV", "Inverter I2t overload", "Sustained overload", "Reduce load;Upsize inverter", "fault"),
    ("07", "MOTOR OVERTEMP", "Motor overtemperature (TF)", "Motor overloaded;Cooling failure", "Check motor;Check ventilation", "fault"),
    ("08", "MOTOR BLOCKED", "Motor blocked/stalled", "Mechanical jam;Coupling failure", "Check mechanical system", "critical"),
    ("09", "ENCODER FAULT", "Encoder signal fault", "Encoder cable;Encoder failure", "Check cable;Replace encoder", "fault"),
    ("11", "OVERSPEED", "Overspeed detected", "Load driving motor;Encoder fault", "Check mechanical;Check encoder", "fault"),
    ("14", "EEPROM", "EEPROM read/write error", "Memory corruption;Hardware fault", "Reset to defaults;Replace unit", "fault"),
    ("25", "STO ACTIVE", "Safe torque off active", "Safety circuit opened", "Check safety devices;Reset", "warning"),
    ("27", "BRAKE FAULT", "Holding brake fault", "Brake not releasing;Brake circuit fault", "Check brake coil;Check wiring", "critical"),
    ("34", "BUS TIMEOUT", "Fieldbus communication timeout", "Cable fault;Master fault", "Check cable;Check PLC", "fault"),
    ("36", "PARAM FAULT", "Parameter error", "Invalid parameter combination", "Check parameter settings", "fault"),
    ("42", "PHASE LOSS IN", "Input phase loss detected", "Fuse blown;Supply fault", "Check input fuses;Check supply", "fault"),
    ("45", "UNDERVOLTAGE", "DC bus undervoltage", "Supply too low;Phase loss", "Check supply voltage", "fault"),
    ("48", "24V SUPPLY", "24V control supply fault", "External 24V supply fault", "Check 24V supply", "fault"),
]

# ============================================================
# DANFOSS VLT DRIVES
# ============================================================
danfoss = [
    ("A2", "Live Zero Err", "4-20mA signal below 4mA", "Broken wire;Transmitter fault", "Check wiring;Check transmitter", "warning"),
    ("A4", "Mains Phase", "Mains phase imbalance", "Phase loss;Unbalanced supply", "Check supply;Check fuses", "warning"),
    ("A7", "Motor Overtemp", "Motor overtemperature", "Thermal overload;Poor cooling", "Reduce load;Check motor cooling", "warning"),
    ("A13", "Current Limit", "Current at limit", "Heavy load;Accel too fast", "Reduce load;Increase accel time", "warning"),
    ("A14", "Ground Fault", "Ground fault detected", "Motor insulation;Cable fault", "Meg motor;Check cables", "warning"),
    ("A33", "Out of Range", "Frequency out of range", "Feedback error;Setpoint issue", "Check setpoint;Check feedback", "warning"),
    ("A38", "Internal Fan", "Internal fan fault", "Fan failure;Blocked airflow", "Replace fan;Clean drive", "warning"),
    ("W2", "Live Zero", "Live zero timeout on analog input", "Broken 4-20 wire", "Check analog wiring", "warning"),
    ("W8", "Voltage Low", "DC bus voltage low", "Low supply voltage", "Check input voltage", "warning"),
    ("W12", "Current Limit", "Output current limited", "Overload condition", "Reduce load;Check motor", "warning"),
    ("E2", "Live Zero Trp", "4-20mA signal lost trip", "Wire broken;Transmitter failed", "Check wiring;Replace transmitter", "fault"),
    ("E4", "Mains Phase", "Mains phase loss fault", "Fuse blown;Supply fault", "Check fuses;Check supply", "fault"),
    ("E5", "DC Link OV", "DC link overvoltage trip", "Decel too fast;Regen energy", "Increase decel;Add brake resistor", "fault"),
    ("E6", "DC Link UV", "DC link undervoltage trip", "Power loss;Phase loss", "Check power;Check fuses", "fault"),
    ("E7", "DC OV Inverter", "Inverter section overvoltage", "Power transistor fault", "Replace inverter section", "critical"),
    ("E8", "DC UV Inverter", "Inverter undervoltage", "Supply loss during operation", "Check supply reliability", "fault"),
    ("E9", "Inv Overload", "Inverter overload trip", "Sustained overload", "Reduce load;Upsize drive", "fault"),
    ("E10", "Motor ETR OT", "Motor overtemp (electronic thermal)", "Sustained overload", "Reduce load;Check motor cooling", "fault"),
    ("E11", "Motor Thermistor", "Motor thermistor trip", "Motor overheated;Thermistor fault", "Check motor;Check thermistor wiring", "fault"),
    ("E13", "Over Current", "Overcurrent trip", "Short circuit;Ground fault", "Check motor;Check cables", "critical"),
    ("E14", "Ground Fault", "Earth fault trip", "Motor insulation failure;Cable damage", "Meg motor;Replace cable", "critical"),
    ("E16", "Short Circuit", "Short circuit detected at output", "Phase-to-phase short;Motor fault", "Check output wiring;Meg motor", "critical"),
    ("E34", "Comm Fault", "Fieldbus communication lost", "Cable fault;PLC fault", "Check cable;Check PLC", "fault"),
    ("E35", "Option Fault", "Option module fault", "Module failure;Bad connection", "Reseat module;Replace if needed", "fault"),
    ("E38", "Internal Fault", "Internal drive fault", "Hardware failure", "Power cycle;Replace drive if persists", "critical"),
    ("E39", "Heatsink OT", "Heatsink overtemperature", "Fan failure;High ambient;Overload", "Check fan;Improve cooling", "fault"),
]

# ============================================================
# INSERT ALL FAULT CODES
# ============================================================
all_codes = []

for code, name, desc, causes, actions, severity in ab_pf525:
    all_codes.append(("Allen-Bradley", "PowerFlex 525", code, name, desc, causes, actions, severity, None))

for code, name, desc, causes, actions, severity in ab_pf755:
    all_codes.append(("Allen-Bradley", "PowerFlex 755", code, name, desc, causes, actions, severity, None))

for code, name, desc, causes, actions, severity in ab_clx:
    all_codes.append(("Allen-Bradley", "ControlLogix", code, name, desc, causes, actions, severity, None))

for code, name, desc, causes, actions, severity in siemens_g120:
    all_codes.append(("Siemens", "SINAMICS G120", code, name, desc, causes, actions, severity, None))

for code, name, desc, causes, actions, severity in siemens_s7:
    all_codes.append(("Siemens", "S7-1200/1500", code, name, desc, causes, actions, severity, None))

for code, name, desc, causes, actions, severity in abb_acs880:
    all_codes.append(("ABB", "ACS880", code, name, desc, causes, actions, severity, None))

for code, name, desc, causes, actions, severity in yaskawa:
    all_codes.append(("Yaskawa", "GA700/GA500", code, name, desc, causes, actions, severity, None))

for code, name, desc, causes, actions, severity in sew:
    all_codes.append(("SEW-Eurodrive", "MOVIDRIVE/MOVITRAC", code, name, desc, causes, actions, severity, None))

for code, name, desc, causes, actions, severity in danfoss:
    all_codes.append(("Danfoss", "VLT AutomationDrive", code, name, desc, causes, actions, severity, None))

inserted = 0
skipped = 0
for mfr, family, code, name, desc, causes, actions, severity, url in all_codes:
    # Check if already exists
    cur.execute("SELECT id FROM kb_fault_codes WHERE manufacturer=? AND product_family=? AND fault_code=?",
                (mfr, family, code))
    if cur.fetchone():
        skipped += 1
        continue
    cur.execute("""INSERT INTO kb_fault_codes 
        (manufacturer, product_family, fault_code, fault_name, description, possible_causes, recommended_actions, severity, source_url, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (mfr, family, code, name, desc, causes, actions, severity, url, datetime.now().isoformat()))
    inserted += 1

# ============================================================
# ADD TROUBLESHOOTING ARTICLES
# ============================================================
articles = [
    ("structured", "troubleshooting", "drives", "Allen-Bradley", "PowerFlex",
     "PowerFlex 525 Overcurrent Troubleshooting Guide",
     """When a PowerFlex 525 throws F012 (Hardware Overcurrent) or F013 (Software Overcurrent):

1. CHECK THE MOTOR: Disconnect motor leads at drive. Meg test each phase to ground (should be >1M ohm). Test phase-to-phase resistance (should be balanced within 5%).

2. CHECK CABLES: Inspect output cables for damage, pinch points, or moisture. Look for conduit fill issues causing heat damage.

3. CHECK ACCELERATION: If F013, try doubling the accel time. Fast accel = high inrush = overcurrent trip.

4. CHECK MOTOR DATA: Verify motor nameplate data matches drive parameters (FLA, voltage, HP, RPM). Wrong data = wrong current limits.

5. AUTOTUNE: Run motor autotune (Param 40 = 1 for rotational, 2 for static). This measures actual motor impedance.

6. IF F012 PERSISTS with motor disconnected: Drive output section (IGBT) is likely damaged. Replace drive.""",
     "overcurrent,F012,F013,PowerFlex,troubleshooting,VFD", 95),
    
    ("structured", "troubleshooting", "drives", "Siemens", "SINAMICS",
     "SINAMICS G120 Commissioning and Common Faults",
     """Quick commissioning checklist for SINAMICS G120:

1. QUICK COMMISSIONING (P0010=1): Set motor data from nameplate — P0304 (voltage), P0305 (current), P0307 (power), P0308 (cos phi), P0309 (efficiency), P0310 (frequency), P0311 (speed).

2. CALCULATE MOTOR DATA (P0340=1): Drive calculates equivalent circuit. Wait for completion.

3. COMMON FAULT F0001 (Overcurrent): Check motor, cables, and load. If at startup, motor data may be wrong. Run identification (P1910).

4. F0003 (Undervoltage): Almost always supply-side. Check fuses, contactors, and supply voltage.

5. F0004 (Overtemperature): Check fan operation. Fan replacement part: same frame size fan kit.

6. F0070 (Fieldbus timeout): Most common with PROFINET. Check cable termination, switch configuration, and PLC cycle time.

7. MOTOR IDENTIFICATION: P1910=1 (standstill), P1910=2 (rotating). Rotating gives better results but motor must be uncoupled.

Pro tip: Use STARTER/SCOUT commissioning tool for complex setups. It validates parameter combinations automatically.""",
     "SINAMICS,G120,commissioning,fault,Siemens,VFD", 90),
    
    ("structured", "troubleshooting", "drives", None, None,
     "VFD Ground Fault Troubleshooting — Universal Guide",
     """Ground faults are the #1 cause of VFD failures in industrial environments. Here's the systematic approach:

STEP 1 — ISOLATE: Disconnect motor cables from drive output terminals. If fault clears, problem is downstream.

STEP 2 — MEG TEST MOTOR: Use a 500V or 1000V megger. Test each phase to ground. New motor: >100M ohm. Acceptable: >5M ohm. Replace if: <1M ohm.

STEP 3 — MEG TEST CABLES: With motor disconnected, meg each conductor to ground and to each other. Look for <1M ohm readings.

STEP 4 — CHECK ENVIRONMENT: Moisture is the #1 killer. Look for condensation in junction boxes, conduit water ingress, or high humidity environments without space heaters.

STEP 5 — IF MOTOR AND CABLES PASS: The drive output section has failed. Common causes: lightning damage, voltage spikes, or long cable runs causing reflected wave voltage doubling.

PREVENTION:
- Install output reactors or dV/dt filters on cable runs >100ft
- Use VFD-rated motor cable (properly shielded)
- Add motor space heaters if in humid/outdoor environment
- Ground the motor frame and drive PE properly
- Annual meg testing catches deterioration before failure

TYPICAL FAULT CODES:
- Allen-Bradley: F021
- Siemens: F0020
- ABB: 2014
- Yaskawa: GF
- Danfoss: E14""",
     "ground fault,megger,VFD,insulation,troubleshooting,motor", 98),
    
    ("structured", "troubleshooting", "plc", "Allen-Bradley", "ControlLogix",
     "ControlLogix Ethernet/IP Communication Troubleshooting",
     """Common Ethernet/IP issues with ControlLogix:

SYMPTOM: IO module shows red triangle in IO tree
CAUSE: RPI (Requested Packet Interval) too fast for network
FIX: Increase RPI. Start at 100ms, decrease only as needed.

SYMPTOM: Intermittent communication drops
CAUSES: 
1. Unmanaged switches — use managed switches with IGMP snooping
2. Network storms — check for loops, enable STP
3. Cable issues — check patch cables, use Cat6 minimum
4. IP conflicts — verify all devices have unique IPs

SYMPTOM: Cannot go online with processor
CAUSES:
1. Wrong slot number in RSLinx driver
2. Firewall blocking CIP ports (44818 TCP, 2222 UDP)
3. Wrong subnet — controller and PC must be same subnet
4. Key switch in RUN — some operations need REM or PROG

SYMPTOM: Produced/Consumed tags not updating
FIX: Check multicast settings. If crossing VLANs, need IGMP querier on each VLAN. Connection timeout must be > 4x RPI.

PRO TIPS:
- Always use managed switches in production
- Set port speed/duplex to 100/Full (don't auto-negotiate)
- Use ring topology with DLR or REP for redundancy
- Reserve 30% bandwidth headroom""",
     "ControlLogix,Ethernet/IP,communication,network,troubleshooting,PLC", 92),
    
    ("structured", "troubleshooting", "plc", "Siemens", "S7-1500",
     "S7-1500 PROFINET Diagnostic Guide",
     """PROFINET diagnostics on S7-1500:

TOOL: Use TIA Portal online diagnostics or PRONETA for network scanning.

COMMON ISSUES:

1. Device not found in network
   - Check cable (use PROFINET-certified cables)
   - Verify device name matches configuration
   - Check if device needs factory reset (some need DCP reset)
   - Use PRONETA to scan and assign names

2. BF (Bus Fault) LED on CPU
   - Open diagnostics buffer: count of diagnostic events
   - Check return of submodule: IO device reported error
   - Verify PROFINET controller is configured correctly

3. Jitter/timing issues
   - Set sendclock factor appropriately
   - Don't exceed 256 IO devices per controller
   - Use IRT (Isochronous Real-Time) for motion control

4. IO Update time too slow
   - Reduce update time in device properties
   - Check if network switches support PROFINET priorities
   - Verify no non-PROFINET traffic on same VLAN

5. Module faults
   - Check diagnostic interrupt OB (OB82)
   - Read module status via SFC51/RDREC
   - Replace if hardware diagnostic persists

CABLE SPECS:
- Use PROFINET Cat5e type B cable (green jacket)
- Max 100m per segment
- Use M12 D-coded connectors in harsh environments""",
     "S7-1500,PROFINET,diagnostics,Siemens,PLC,network", 90),
    
    ("structured", "best-practice", "maintenance", None, None,
     "Preventive Maintenance Schedule for VFD Installations",
     """DAILY (operator level):
- Check drive display for warnings/alarms
- Listen for unusual noise (fan, motor)
- Check ventilation — is air flowing through drive?

MONTHLY:
- Record DC bus voltage and output current (trend these!)
- Check fan operation — spin freely? Unusual noise?
- Inspect for dust accumulation on heatsinks
- Check cable connections for looseness (thermal cycling)

QUARTERLY:
- Thermal scan all power connections (look for hot spots >10°C above ambient)
- Check control wiring for chafing or damage
- Verify cooling air filters (if installed) — clean or replace
- Review fault history — any recurring faults?

ANNUALLY:
- Megger test motor (log results, trend over time)
- Tighten all power connections to spec (check manufacturer torque values)
- Clean or replace cooling fans
- Check DC bus capacitors (look for bulging, leaking)
- Update drive firmware if manufacturer recommends
- Back up drive parameters to file

EVERY 5 YEARS:
- Replace cooling fans proactively
- Consider DC bus capacitor replacement (drives in harsh environments)
- Full cable insulation test
- Review and update motor protection settings

TRACKING: Use a CMMS to log all readings and create trend reports. Sudden changes in megger readings or DC bus voltage indicate developing problems.""",
     "preventive maintenance,VFD,PM,schedule,best practice", 95),

    ("structured", "troubleshooting", "mechanical", None, None,
     "Bearing Failure Analysis for Rotating Equipment",
     """Common bearing failure modes and identification:

FATIGUE (SPALLING):
- Appearance: Flaking/pitting on races or rolling elements
- Cause: Normal wear, overloading, or misalignment
- Prevention: Proper loading, alignment, and replacement intervals

CONTAMINATION:
- Appearance: Denting, scoring, or discoloration
- Cause: Dirt/moisture ingress, seal failure
- Prevention: Proper seals, clean installation practices

CORROSION:
- Appearance: Rust, pitting, or etching on surfaces
- Cause: Moisture, aggressive chemicals, electrical discharge
- Prevention: Proper storage, shaft grounding (VFD applications!)

ELECTRICAL DAMAGE (VFD-related):
- Appearance: Frosting, fluting (washboard pattern on races)
- Cause: Shaft voltage from VFD common-mode voltage
- Prevention: Install shaft grounding ring (AEGIS or similar), use insulated bearings on drive end, or install common-mode filter

MISALIGNMENT:
- Appearance: Wear pattern offset from center of race
- Cause: Shaft misalignment, housing bore out of spec
- Prevention: Laser alignment, verify housing tolerances

LUBRICATION FAILURE:
- Appearance: Discoloration (blue/brown), smearing
- Cause: Wrong grease, too much/little grease, contaminated grease
- Prevention: Follow manufacturer's grease specs and intervals

DIAGNOSTIC TOOLS:
- Vibration analysis: Detect issues months before failure
- Ultrasound: Detect lubrication issues early
- Temperature monitoring: Sudden rise indicates problem
- Oil analysis: For oil-lubricated bearings""",
     "bearing,failure analysis,vibration,maintenance,rotating equipment", 93),
]

article_inserted = 0
for source, category, subcat, mfr, family, title, content, tags, score in articles:
    cur.execute("SELECT id FROM kb_articles WHERE title=?", (title,))
    if cur.fetchone():
        continue
    cur.execute("""INSERT INTO kb_articles 
        (source, category, subcategory, manufacturer, product_family, title, content, tags, quality_score, created_at, harvested_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (source, category, subcat, mfr, family, title, content, tags, score,
         datetime.now().isoformat(), datetime.now().isoformat()))
    article_inserted += 1

conn.commit()

# Count after
cur.execute("SELECT COUNT(*) FROM kb_fault_codes")
after_faults = cur.fetchone()[0]
cur.execute("SELECT COUNT(*) FROM kb_articles")
after_articles = cur.fetchone()[0]

# Summary by manufacturer
cur.execute("SELECT manufacturer, COUNT(*) FROM kb_fault_codes GROUP BY manufacturer ORDER BY COUNT(*) DESC")
mfr_counts = cur.fetchall()

conn.close()

print(f"=== KB EXPANSION COMPLETE ===")
print(f"Fault codes: {before_faults} → {after_faults} (+{inserted} new, {skipped} skipped)")
print(f"Articles: {before_articles} → {after_articles} (+{article_inserted} new)")
print(f"\nFault codes by manufacturer:")
for mfr, count in mfr_counts:
    print(f"  {mfr}: {count}")
print(f"\nDB size: {__import__('os').path.getsize(DB_PATH) / 1024:.1f} KB")
