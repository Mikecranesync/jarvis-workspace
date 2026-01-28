# LinkedIn Post Draft — January 27, 2026
## Status: DRAFT (needs Mike's approval)
## Topic: Introducing AI-powered torque stripe inspection

---

🔩 What if your phone could tell you if a bolt is loose?

In industrial maintenance, we paint torque stripes (witness marks) across bolt heads to detect rotation. If the stripe breaks — the bolt moved. Simple, right?

Except technicians inspect thousands of bolts per shift. Fatigue, lighting, and subjectivity make it easy to miss a broken stripe on a safety-critical joint.

Today I built an AI inspector that:
📸 Takes a photo of the bolt
🤖 Uses vision AI to detect if the stripe is intact or broken
✅❌ Returns PASS/FAIL with confidence % and a maintenance recommendation
🎬 Can analyze video — frame by frame — for walkdown inspections

The kicker? Pure color detection (HSV) failed completely — it couldn't tell a Coca-Cola can from a torque stripe. Adding a Vision Language Model (Gemini 2.0 Flash) gave it semantic understanding. It now *knows* what a bolt is.

This is where industrial AI is heading — not replacing the technician, but giving them superhuman consistency.

Building this in public. More updates coming.

#IndustrialAI #Maintenance #ReliabilityEngineering #MachineLearning #IndustrialIoT #PLC #TorqueInspection

---

**Image suggestion:** Side-by-side of the FAIL result with red glow overlay + the PASS result with green glow
