# FactoryLM — YouTube Video Scripts

*Task: [V-PLC-12] Launch YouTube Channel*
*Ready to record or render with Manim*

---

## Video 1: Introduction to FactoryLM

**Title:** "AI-Powered PLC Diagnostics in 60 Seconds | FactoryLM Demo"
**Length:** 3-5 minutes
**Goal:** Explain what FactoryLM does and show a live demo

### Script

**[0:00-0:30] Hook**
```
You're standing in front of a machine that's down. 
The PLC is throwing an error code you've never seen before.
Your options: dig through a 500-page manual, call the vendor and wait on hold, or Google and hope for the best.

What if you could just snap a photo and get the answer in 60 seconds?

That's FactoryLM. Let me show you.
```

**[0:30-1:30] The Problem**
```
Every maintenance tech knows this pain. Unfamiliar fault codes. 
Equipment you don't work on every day. 
The senior guy who knew everything just retired.

Industry data says the average diagnostic delay costs $500-$1000 per hour in downtime.
And it happens more often than anyone wants to admit.
```

**[1:30-3:00] The Demo**
```
Here's how FactoryLM works.

[Show Telegram on phone]

Step 1: Open Telegram. It's free, works on any phone.

Step 2: Take a photo of your error screen.

[Take photo of PLC error]

Step 3: Send it to FactoryLM.

[Send photo]

Now watch...

[Wait for response]

In under 60 seconds, you get:
- The probable cause
- Step-by-step troubleshooting
- Parts you might need

No manuals. No phone calls. No waiting.
```

**[3:00-4:00] Why It Works**
```
FactoryLM is trained on 20 years of industrial troubleshooting data.
It knows Siemens, Allen-Bradley, ABB, Schneider, Mitsubishi — all the major brands.

And it gets smarter with every diagnosis.

This isn't replacing technicians. It's giving you superhuman memory.
```

**[4:00-4:30] CTA**
```
Want to try it? 

We're offering free trials for maintenance managers who want to test it with their teams.

Link in the description to book a 15-minute demo.

I'm Mike Harper — 20 years in cranes and industrial maintenance. 
This is the tool I wish I had when I started.

See you in the next video.
```

---

## Video 2: How to Diagnose Siemens S7 Error Codes

**Title:** "Siemens S7 Error Codes Explained | Common Faults & Fixes"
**Length:** 8-10 minutes
**Goal:** SEO content + demonstrate expertise

### Script

**[0:00-0:30] Hook**
```
Siemens S7 PLCs are everywhere — and so are their cryptic error codes.

Today I'm breaking down the 5 most common S7 faults, what they actually mean, and how to fix them fast.

Let's dive in.
```

**[0:30-2:00] Error 1: SF (System Fault)**
```
First up: the SF light. System Fault.

This is Siemens telling you something's wrong, but not what.

Common causes:
1. Hardware failure — check your modules
2. Configuration mismatch — wrong hardware config loaded
3. Power supply issues — voltage fluctuations

How to diagnose:
- Go online with TIA Portal or STEP 7
- Check the diagnostic buffer
- Look for the specific fault code

Quick fix: Power cycle first. Seriously. It works more often than you'd think.
```

**[2:00-3:30] Error 2: BUSF (Bus Fault)**
```
BUSF means your PROFIBUS or PROFINET network has a problem.

Common causes:
1. Loose cable connection
2. Terminated incorrectly
3. Duplicate addresses
4. EMI interference

How to diagnose:
- Check physical connections first
- Use the network diagnostics in TIA Portal
- Look for the specific station that's offline

Pro tip: Bus faults are almost always physical. Check your cables before you check your code.
```

**[3:30-5:00] Error 3: OB Error (Organization Block)**
```
OB errors happen when the PLC doesn't know what to do.

Most common: OB121 — Programming error
This means your code is trying to do something illegal.

Causes:
1. Division by zero
2. Array index out of bounds
3. Pointer to non-existent memory

How to fix:
- Check the diagnostic buffer for the exact address
- Look at that line of code
- Add error handling

The diagnostic buffer is your friend. It tells you exactly where the problem is.
```

**[5:00-6:30] Error 4: STOP Mode**
```
Your PLC is in STOP. Production is down. Everyone's panicking.

Common causes:
1. Someone put it in STOP manually
2. Watchdog timeout
3. Memory error
4. Program download failed

How to diagnose:
- Check the mode switch (is it set to RUN?)
- Look at the diagnostic buffer
- Check if someone was programming

Before you panic: Check the obvious. Is the switch in the right position?
```

**[6:30-8:00] Error 5: Connection Errors**
```
Can't connect to your PLC? 

Common causes:
1. Wrong IP address
2. Firewall blocking
3. Network configuration mismatch
4. PG/PC interface not set correctly

How to fix:
- Ping the PLC first
- Check your network settings in TIA Portal
- Make sure you're on the same subnet

Pro tip: If you're on PROFINET, make sure your laptop is set to the right network adapter.
```

**[8:00-8:30] CTA**
```
Those are the 5 most common Siemens S7 errors.

If you want instant diagnosis without all this manual work, check out FactoryLM. 
Photo the error, get the answer in 60 seconds.

Link in the description.

What error codes give you the most trouble? Drop a comment below.

Subscribe for more PLC troubleshooting content.
```

---

## Video 3: FactoryLM vs. Manual Diagnosis (Side-by-Side)

**Title:** "I Diagnosed 5 PLC Errors: AI vs. Manual | Which is Faster?"
**Length:** 6-8 minutes
**Goal:** Show value through direct comparison

### Script

**[0:00-0:30] Hook**
```
I'm going to diagnose 5 real PLC errors two ways:
- The old way: manuals, Google, and experience
- The new way: FactoryLM AI

Let's see which is faster.
```

**[0:30-6:00] The Race**
```
[Show 5 different error codes]
[Time both methods]
[Show results side by side]

Manual method: Average X minutes
FactoryLM: Average Y seconds

Winner: [dramatic reveal]
```

**[6:00-7:00] Analysis**
```
The manual method works. It's how we've all done it for years.

But time is money. Every minute you're diagnosing is a minute of downtime.

FactoryLM isn't about replacing your skills — it's about getting you to the answer faster so you can actually fix the problem.
```

**[7:00-7:30] CTA**
```
Want to try FactoryLM on your own errors?

Free trial in the description.

Thanks for watching. See you next time.
```

---

## YouTube SEO Notes

### Keywords to Target
- "PLC error codes"
- "Siemens S7 troubleshooting"
- "Allen Bradley fault codes"
- "PLC diagnostics"
- "maintenance troubleshooting"

### Thumbnail Best Practices
- Bold text overlay
- Error code visible
- Before/after or vs. format
- High contrast colors

### Tags
```
PLC, PLC troubleshooting, Siemens S7, Allen Bradley, maintenance, industrial automation, fault codes, error codes, diagnostics, AI maintenance, FactoryLM
```

---

*Scripts ready. Record or render with Manim.*
