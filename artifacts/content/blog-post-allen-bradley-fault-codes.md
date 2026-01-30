# Allen-Bradley Fault Codes: A Maintenance Tech's Complete Guide

*Target Keyword: "Allen-Bradley fault codes"*
*Word Count: ~1,600 words*
*Author: Mike Harper | FactoryLM*

---

## Introduction

Allen-Bradley PLCs power millions of machines worldwide. From CompactLogix to ControlLogix, these Rockwell Automation controllers are the backbone of American manufacturing.

But when a fault occurs, those blinking lights and error codes can bring production to a halt.

This guide covers the most common Allen-Bradley fault codes, what they mean, and how to fix them fast. Whether you're running a MicroLogix 1100 or a ControlLogix L8, these troubleshooting techniques apply.

Let's get your line back up.

---

## Understanding Allen-Bradley Fault Architecture

### Major vs Minor Faults

Allen-Bradley distinguishes between two fault severities:

**Major Faults (Type 1-13)**
- Stop program execution
- Require intervention to clear
- Usually indicate serious problems

**Minor Faults (Type 14+)**
- Don't stop execution (usually)
- Logged for diagnostics
- Can be configured to auto-clear

### Where to Find Fault Information

1. **Controller LEDs** — Quick status overview
2. **RSLogix 5000 / Studio 5000** — Detailed diagnostics when online
3. **Controller Properties > Faults** — Fault history
4. **GSV (Get System Value)** — Programmatic fault access
5. **HMI Fault Pages** — If configured

---

## The 7 Most Common Allen-Bradley Faults

### 1. Major Fault Type 1: Power-Up Fault

**What it looks like:** Controller faulted immediately after power cycle.

**What it means:** The controller detected a problem during power-up sequence.

**Common Code Variations:**
| Code | Description |
|------|-------------|
| 01 | Non-recoverable internal fault |
| 60 | Non-recoverable NVS fault |
| 61 | Energy storage fault |

**Troubleshooting:**
1. Check power supply voltage (should be 24VDC ±10%)
2. Inspect for loose connections at power terminals
3. Check the energy storage module (ESM) if equipped
4. Verify the battery is good (for retentive memory)

**Fix:**
- If voltage is good, try a full power cycle (30 seconds off)
- Replace the battery if low
- If Code 01 persists, the controller may need replacement

---

### 2. Major Fault Type 3: I/O Fault

**What it looks like:** "I/O tree" shows red X, modules faulted.

**What it means:** Communication problem with an I/O module.

**Common Code Variations:**
| Code | Description |
|------|-------------|
| 16 | I/O not responding |
| 20 | Module rack/slot fault |
| 23 | Connection request error |

**Troubleshooting:**
1. Check physical connections at the faulted module
2. Verify the module is seated properly in the backplane
3. Check for damaged pins on the backplane
4. Look for loose or damaged cables

**Fix:**
- Reseat the module (power off first)
- Check the configuration matches the physical hardware
- Replace the communication cable if damaged
- If module is bad, replace it

**Pro tip:** The fault usually tells you which rack/slot. Go straight to that location.

---

### 3. Major Fault Type 4: Program Fault

**What it looks like:** Controller goes to fault mode during execution.

**What it means:** Your program tried to do something illegal.

**Common Code Variations:**
| Code | Description |
|------|-------------|
| 20 | Array subscript out of range |
| 31 | JSR parameter count mismatch |
| 34 | Timer value exceeded |
| 82 | Arithmetic overflow |
| 83 | Stack underflow |

**Troubleshooting:**
1. Note the program, routine, and rung from the fault message
2. Go to that location in your code
3. Look for the illegal operation

**Common Causes:**
- Indirect addressing with bad pointer
- Math that produces infinity or NaN
- Jumping to routines with wrong parameter count
- Timer values out of range

**Fix:**
- Add bounds checking before array access
- Validate math inputs (check for division by zero)
- Verify JSR/RET parameter counts match

**Pro tip:** Add a fault routine that captures fault data before clearing — makes debugging much easier.

---

### 4. Major Fault Type 6: Watchdog Fault

**What it looks like:** Code 01 — "Watchdog task not executing fast enough."

**What it means:** Your program scan time exceeded the watchdog limit.

**Common Causes:**
- Too much code in a single scan
- Infinite or very long loops
- Waiting on communications that never complete
- Too many tasks competing for CPU

**Troubleshooting:**
1. Check the task's actual scan time vs configured watchdog
2. Look for loops that might run too long
3. Check if any single routine takes disproportionate time

**Fix:**
- Increase the watchdog timer (temporary band-aid)
- Optimize the slow code
- Split long loops across multiple scans
- Use event tasks for non-continuous operations

**Pro tip:** A 10ms continuous task should stay under 5ms average. Leave headroom.

---

### 5. Major Fault Type 11: Connection Lost

**What it looks like:** "Connection lost to [device]" in fault history.

**What it means:** Network communication to a remote device failed.

**Common Causes:**
- Network cable disconnected or damaged
- Remote device powered off or faulted
- IP address conflict or routing issue
- Switch or network infrastructure problem
- Excessive network traffic

**Troubleshooting:**
1. Ping the remote device
2. Check the physical connection at both ends
3. Verify IP addresses and subnet masks
4. Look at switch port LEDs
5. Check for duplicate IP addresses

**Fix:**
- Fix the physical connection
- Verify network configuration
- Add connection status monitoring to your code
- Implement graceful handling of lost connections

**Pro tip:** Always configure your RPI (Requested Packet Interval) appropriately. Too fast = network congestion. Too slow = slow response.

---

### 6. Minor Fault Type 14: Battery Low

**What it looks like:** Battery LED lit, minor fault logged.

**What it means:** The backup battery is low and needs replacement.

**Why it matters:** Without the battery, you'll lose:
- Retentive data during power loss
- Real-time clock accuracy
- Possibly your program (depending on controller)

**Fix:**
1. Order the correct battery (usually 1756-BA1 or 1756-BA2)
2. Replace while controller is powered ON
3. Allow 24 hours for new battery to charge
4. Clear the fault after replacement

**Pro tip:** Set a calendar reminder to replace batteries every 2-3 years, before they fault.

---

### 7. Fault Code 16: Module Not Present

**What it looks like:** Red X on module in I/O tree, Code 16.

**What it means:** Controller expects a module that isn't there.

**Common Causes:**
- Module physically removed
- Module failed completely
- Configuration mismatch (wrong module type)
- Backplane communication issue

**Troubleshooting:**
1. Is the module physically installed?
2. Is it the right module type?
3. Is it seated properly?
4. Are the backplane connector pins damaged?

**Fix:**
- Install the correct module
- Reseat if already installed
- Update configuration if module type changed
- Check backplane if module tests good elsewhere

---

## How to Clear Allen-Bradley Faults

### From RSLogix/Studio 5000
1. Connect online to the controller
2. Go to Controller Properties > Faults
3. Review the fault information
4. Fix the underlying issue
5. Click "Clear Major Fault" or "Clear Minor Faults"
6. Switch controller to Run mode

### From the Controller
1. Use the keyswitch or buttons (if equipped)
2. Some controllers auto-clear minors when issue resolves

### Programmatically
Use AFI (Always False Instruction) in your code to clear faults:
```
SSV(Controller, [controller_name], MajorFaultRecord, 0)
```

---

## Faster Diagnostics with AI

Digging through fault logs and manuals takes time — time you don't have when production is down.

### What if you could just snap a photo?

**FactoryLM** is an AI diagnostic tool that reads Allen-Bradley fault screens and tells you:
- What the fault means
- What probably caused it
- How to fix it
- What parts you might need

**How it works:**
1. Photo the fault screen with your phone
2. Send to FactoryLM via Telegram
3. Get your diagnosis in under 60 seconds

No laptop required. No manual lookups. Just answers.

[Try FactoryLM free →]

---

## Conclusion

Allen-Bradley faults follow patterns. Once you understand the architecture — major vs minor, fault types, common codes — troubleshooting becomes systematic rather than stressful.

**Key takeaways:**
- Check fault details in RSLogix/Studio 5000, not just the LED
- Type 3 and 11 faults are usually physical/network issues
- Type 4 faults mean your code did something illegal
- Type 6 watchdog faults mean your scan is too slow
- Always fix the root cause, then clear the fault

The faster you can diagnose, the faster you're back in production.

---

*Mike Harper has 20 years of experience in industrial maintenance and has probably seen every Allen-Bradley fault code at least twice. He built FactoryLM to help maintenance teams diagnose faster.*

---

## Related Articles
- Siemens S7-1200 Error Codes: Complete Guide
- EtherNet/IP Troubleshooting: Connection Lost Errors
- How to Read RSLogix 5000 Fault Logs Like a Pro

---

*Keywords: Allen-Bradley fault codes, ControlLogix troubleshooting, CompactLogix faults, RSLogix 5000 diagnostics, major fault type, Rockwell PLC errors*
