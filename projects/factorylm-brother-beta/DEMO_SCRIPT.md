# FactoryLM Telegram Bot - Demo Script for Brother

**Target User**: Brother (Mike's brother, maintenance tech in Indiana)  
**Goal**: Validate core bot functionality with real-world scenarios  
**Duration**: 30 minutes hands-on testing  

---

## 🎬 Demo Overview

This script walks through the most common maintenance scenarios Brother will encounter. Each test validates core bot capabilities and demonstrates value for daily operations.

**What Brother Will Test**:
1. Equipment photo analysis (motor nameplates, drives, etc.)
2. Work order creation and tracking
3. Fault code lookup for common equipment  
4. Parts cross-reference functionality
5. Voice query processing (if implemented)

---

## 🚀 Demo Script

### **Test 1: Motor Nameplate Analysis** ⭐ (PRIMARY TEST)
**Scenario**: "I need to identify this motor and check if it needs replacement"

#### Step 1: Take Photo of Motor Nameplate
```
Action: Brother takes photo of any motor nameplate in the facility
Expected: Clear photo showing manufacturer, model, specs

📸 Photo Tips:
• Good lighting on nameplate
• Hold camera steady 
• Include full nameplate in frame
• Avoid glare/reflections
```

#### Step 2: Send Photo to Bot
```
1. Open Telegram
2. Find @FactoryLMBot (or configured bot name)
3. Send photo to bot
4. Wait for analysis response (should be < 15 seconds)
```

#### Expected Bot Response:
```
🏭 Equipment Analysis Complete
━━━━━━━━━━━━━━━━━━━━━━

Equipment: AC Motor  
Manufacturer: Baldor Electric
Model: EM3615T
Condition: 🟢 GOOD

Description:
3-phase induction motor, 5 HP, 1750 RPM, 
208-230/460V, TEFC enclosure

Visible Issues:
  ✅ None detected

━━━━━━━━━━━━━━━━━━━━━━
📋 CMMS Work Order

WO #: 1001
Priority: 🟡 MEDIUM  
Asset: New: Baldor Motor EM3615T
Title: Inspect 5HP Motor - Production Line

Action Required:
Routine inspection and lubrication check

🔗 View Work Order: [link]
🔗 View Asset: [link]

⚡ Powered by FactoryLM
```

#### Validation Checklist:
- [ ] Bot correctly identified motor manufacturer
- [ ] Specifications extracted accurately 
- [ ] Work order created in CMMS
- [ ] Asset added to equipment database
- [ ] Response time under 15 seconds

---

### **Test 2: VFD Fault Code Lookup** ⚠️ 
**Scenario**: "Drive is showing fault F072, what does it mean?"

#### Step 1: Text Query
```
Brother types: "What is fault code F072 on Allen-Bradley drive?"
```

#### Expected Bot Response:
```
⚠️ Fault Code Lookup

Equipment: Allen-Bradley PowerFlex Drive
Code: F072
Description: Ground Fault Protection Trip

🔧 Solution:
1. De-energize drive and motor
2. Check motor leads for damage
3. Test insulation resistance with megohmmeter
4. Verify proper grounding connections
5. Check for moisture in motor junction box

🛠️ Tools Required:
• Multimeter
• Megohmmeter  
• Basic hand tools

⚠️ Safety: LOTO required - High voltage present

Priority: 🔴 HIGH - Production affecting

Would you like me to create a work order for this repair?
```

#### Alternative: Photo of Drive Display
```
Brother can also take photo of drive showing fault code
Bot should recognize the display and provide same information
```

#### Validation Checklist:
- [ ] Fault code correctly identified
- [ ] Detailed solution provided
- [ ] Safety warnings included
- [ ] Tool requirements listed
- [ ] Option to create work order offered

---

### **Test 3: Equipment Database Lookup**
**Scenario**: "What's the maintenance history on Pump 7?"

#### Step 1: Equipment Query
```
Brother types: "Show me details for Pump 7" 
OR: "What pumps do we have in the system?"
```

#### Expected Bot Response:
```
🏭 Equipment Details: Pump 7

Asset ID: #45
Name: Main Hydraulic Pump 7
Location: Utility Room B
Status: OPERATIONAL

Specifications:
• Manufacturer: Rexroth
• Model: A10V071
• Pressure: 3000 PSI
• Flow Rate: 45 GPM

📋 Recent Maintenance:
• 2024-01-15: Hydraulic fluid change (WO #987)
• 2024-01-03: Pressure relief valve inspection (WO #934)
• 2023-12-20: Quarterly PM completed (WO #901)

⏰ Next Scheduled Maintenance:
• Quarterly PM due: March 15, 2024
• Annual rebuild due: December 2024

🔗 View Full History: [CMMS link]
```

#### Alternative: List All Equipment
```
If "Pump 7" doesn't exist, bot shows list of available equipment:

🏭 Facility Equipment

Injection Molding Machines:
• Machine 1 - Cincinnati Milacron VT-165 (#12)
• Machine 2 - Haitian MA1800III (#13)

Pumps & Hydraulics:
• Main Hydraulic Pump (#45)
• Cooling Water Pump (#46)

Other Equipment:
• Air Compressor Unit (#67)
• Chiller System (#78)

Type equipment name for details, or take a photo!
```

#### Validation Checklist:
- [ ] Equipment search working
- [ ] Maintenance history displayed
- [ ] Next PM dates shown
- [ ] Links to CMMS functional

---

### **Test 4: Parts Cross-Reference Lookup**
**Scenario**: "I need a replacement bearing, what are my options?"

#### Step 1: Parts Query
```
Brother types: "Cross reference for SKF bearing 6205"
OR takes photo of bearing with part number visible
```

#### Expected Bot Response:
```
🧩 Parts Cross-Reference

Original Part: SKF 6205
Description: Deep groove ball bearing
Size: 25mm ID x 52mm OD x 15mm W

✅ Available Cross-References:
• Timken: 205PP
• NSK: 6205DDU  
• FAG: 6205-2RSR
• Generic: 6205-RS

💰 Pricing (Est):
• OEM (SKF): $12.50
• Timken: $11.80
• Generic: $8.95

📦 Inventory Status:
• On hand: 2 units (SKF original)
• Reorder point: 5 units
• Lead time: 3-5 days

🛒 Recommended Action:
Order 10 units of Timken 205PP (best value)
Create purchase request?

🔗 View in Inventory System
```

#### Validation Checklist:
- [ ] Part correctly identified
- [ ] Cross-references provided
- [ ] Inventory status shown
- [ ] Pricing information included
- [ ] Purchase suggestion made

---

### **Test 5: Work Order Creation**
**Scenario**: "Create work order for bearing replacement"

#### Step 1: Direct Work Order Creation
```
Brother types: "Create work order for bearing replacement on Pump 7"
```

#### Expected Bot Response:
```
🔧 Creating Work Order...

Title: Bearing Replacement - Pump 7
Equipment: Main Hydraulic Pump (#45)  
Priority: 🟡 MEDIUM
Estimated Duration: 4 hours

Description:
Replace main shaft bearing (SKF 6205) on hydraulic pump 7.
Customer reported noise and vibration during operation.

Required Parts:
• SKF 6205 bearing (Qty: 1)
• Hydraulic fluid (Qty: 2 gal)
• O-ring kit (Qty: 1)

Required Tools:
• Bearing puller set
• Hydraulic jack
• Torque wrench
• Multimeter

Safety Requirements:
• LOTO procedure P-045
• PPE: Safety glasses, gloves
• Confined space permit if applicable

Work Order #1047 created successfully!

🔗 View Work Order: [CMMS link]
📱 Track progress in CMMS app

Next steps:
1. Schedule downtime
2. Gather tools and parts
3. Execute LOTO procedure
4. Begin repair
```

#### Validation Checklist:
- [ ] Work order created in CMMS
- [ ] Appropriate parts listed
- [ ] Tools and safety requirements included
- [ ] Work order number assigned
- [ ] Links to CMMS working

---

### **Test 6: Voice Query (If Implemented)**
**Scenario**: "Hands-free operation while working on equipment"

#### Step 1: Voice Message
```
Brother holds voice button and says:
"Hey FactoryLM, what's the status of Machine 2?"
```

#### Expected Bot Response:
```
🎤 Voice Query Processed

🏭 Machine 2 Status:

Equipment: Haitian MA1800III Injection Molder
Current Status: OPERATIONAL
Last Cycle: 45 seconds ago

Recent Alerts:
• Temperature zone 3 running 5°F high (minor)
• Cycle time trending up 3% this shift

Active Work Orders:
• None currently assigned

Next Scheduled Maintenance:
• Weekly PM due: Friday 3/15
• Hydraulic filter change due: 150 hours

Overall Health: 🟢 GOOD
Production Impact: NONE

Need more details? Ask specific questions or take a photo!

🔊 [Audio response also plays if TTS enabled]
```

#### Validation Checklist:
- [ ] Voice message recognized
- [ ] Appropriate equipment found
- [ ] Status information provided
- [ ] Audio response played (if TTS enabled)

---

## 🎯 Success Metrics

### Primary Success Indicators:
- [ ] **Equipment Recognition**: 90%+ accuracy on motor nameplates, drives, pumps
- [ ] **Response Time**: < 15 seconds for photo analysis
- [ ] **Work Order Creation**: Successfully integrates with CMMS
- [ ] **User Satisfaction**: Brother finds it useful for daily work

### Performance Benchmarks:
- **Photo Processing**: 10-15 seconds average
- **Text Queries**: 2-3 seconds response
- **Voice Processing**: 5-8 seconds (if enabled)
- **Database Lookups**: < 2 seconds

### Quality Checks:
- Equipment specifications correctly extracted
- Work orders contain relevant details
- Fault codes provide actionable solutions
- Parts cross-references are accurate

---

## 🐛 Common Issues & Solutions

### Photo Analysis Problems
**Issue**: "Bot says it can't identify the equipment"
**Solutions**:
- Retake photo with better lighting
- Get closer to nameplate/label
- Clean nameplate if dirty
- Try different angle

### CMMS Integration Issues  
**Issue**: "Work order not appearing in CMMS"
**Solutions**:
- Check CMMS login credentials
- Verify bot has proper permissions
- Try refreshing CMMS web interface
- Check server logs for errors

### Bot Not Responding
**Issue**: "Bot doesn't respond to messages"
**Solutions**:
- Check internet connection
- Restart bot service: `systemctl restart brother-bot`
- Verify bot token is correct
- Check if bot is in maintenance mode

---

## 📊 Demo Results Template

**Test Completion:**
- [ ] Motor nameplate analysis: PASS/FAIL
- [ ] Fault code lookup: PASS/FAIL  
- [ ] Equipment database lookup: PASS/FAIL
- [ ] Parts cross-reference: PASS/FAIL
- [ ] Work order creation: PASS/FAIL
- [ ] Voice queries: PASS/FAIL

**Brother's Feedback:**
```
Overall Experience: ⭐⭐⭐⭐⭐ (1-5 stars)

Most Useful Feature: ________________

Biggest Issue: ____________________

Suggestions for Improvement: 
_________________________________
_________________________________

Would you use this daily? YES/NO

Ready for plant-wide rollout? YES/NO
```

**Next Steps Based on Results:**
- **All Pass**: Ready for production deployment
- **Minor Issues**: Address specific bugs, re-test
- **Major Issues**: Revise architecture, additional development needed

---

## 🚀 Post-Demo Actions

### If Successful (80%+ tests pass):
1. **Production Deployment**: Enable bot for Brother's daily use
2. **Training Documentation**: Create user guide for Brother's team
3. **Monitoring Setup**: Track usage patterns and performance
4. **Feedback Loop**: Weekly check-ins with Brother for improvements

### If Issues Found:
1. **Bug Fixes**: Address critical issues first
2. **Re-testing**: Schedule follow-up demo session  
3. **Feature Adjustments**: Modify based on Brother's feedback
4. **Timeline Update**: Revise rollout schedule if needed

### Success Celebration 🎉
When Brother says "This is exactly what we needed!" - mission accomplished!

**Remember**: Brother is our first external user. His success validates the entire FactoryLM vision for industrial AI assistance.