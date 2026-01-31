# Computer Use & Browser Automation — Open Source Research

*Research for: PLC Workbench AI Assistant*
*Date: 2026-01-30*
*Status: Research only — no building yet*

---

## Use Case

Run AI on Mike's laptop at PLC workbench that can:
- Control PLC software (TIA Portal, RSLogix 5000, etc.)
- Take screenshots, click buttons, fill forms
- Automate repetitive programming tasks
- Potentially interact with HMI development tools

---

## Top Open Source Options

### Tier 1: Full Computer Control (Best for PLC Software)

#### 1. Open Interpreter ⭐⭐⭐⭐⭐
| Attribute | Value |
|-----------|-------|
| **GitHub** | github.com/OpenInterpreter/open-interpreter |
| **Stars** | 62,000 |
| **Language** | Python |
| **What it does** | Natural language → computer control |
| **Runs locally** | ✅ Yes |
| **LLM Options** | Claude, GPT, Llama, any local LLM |

**Why it's great for PLC:**
- Can execute shell commands, Python, JavaScript
- Can control mouse/keyboard via PyAutoGUI
- Works with any desktop application
- Voice mode available

**Install:**
```bash
pip install open-interpreter
interpreter
```

---

#### 2. Self-Operating Computer ⭐⭐⭐⭐
| Attribute | Value |
|-----------|-------|
| **GitHub** | github.com/OthersideAI/self-operating-computer |
| **Stars** | 10,000 |
| **Language** | Python |
| **What it does** | Multimodal AI operates full desktop |
| **Runs locally** | ✅ Yes |
| **LLM Options** | GPT-4V, Claude Vision, local vision models |

**Why it's great for PLC:**
- Uses screenshots + vision models
- Can "see" and click on any UI element
- Perfect for proprietary PLC software that has no API
- Simulates human interaction

---

#### 3. Agent-S ⭐⭐⭐⭐
| Attribute | Value |
|-----------|-------|
| **GitHub** | github.com/simular-ai/Agent-S |
| **Stars** | 9,600 |
| **Language** | Python |
| **What it does** | Desktop agent like a human |
| **Runs locally** | ✅ Yes |

**Why it's great for PLC:**
- Designed for complex multi-step tasks
- Can handle proprietary Windows applications
- Good for automating PLC programming workflows

---

### Tier 2: Browser Automation (If PLC software is web-based)

#### 4. Browser Use ⭐⭐⭐⭐⭐
| Attribute | Value |
|-----------|-------|
| **GitHub** | github.com/browser-use/browser-use |
| **Stars** | 77,000 |
| **Language** | Python |
| **What it does** | AI-powered browser automation |
| **Runs locally** | ✅ Yes |

**Why it's interesting:**
- Incredibly popular (77k stars!)
- Makes any website AI-accessible
- Could work with web-based SCADA/HMI systems
- Built on Playwright

---

#### 5. Skyvern ⭐⭐⭐⭐
| Attribute | Value |
|-----------|-------|
| **GitHub** | github.com/Skyvern-AI/skyvern |
| **Stars** | 20,000 |
| **Language** | Python |
| **What it does** | Browser automation with AI |
| **Runs locally** | ✅ Yes |

---

#### 6. Puppeteer ⭐⭐⭐⭐
| Attribute | Value |
|-----------|-------|
| **GitHub** | github.com/puppeteer/puppeteer |
| **Stars** | 93,000 |
| **Language** | TypeScript/JavaScript |
| **What it does** | Control Chrome/Firefox programmatically |
| **Runs locally** | ✅ Yes |

**Classic choice for:**
- Web scraping
- Automated testing
- PDF generation
- Screenshot capture

**Limitation:** Browser only — can't control desktop apps

---

#### 7. Playwright ⭐⭐⭐⭐
| Attribute | Value |
|-----------|-------|
| **GitHub** | github.com/microsoft/playwright |
| **Stars** | 82,000 |
| **Language** | TypeScript/JavaScript/Python |
| **What it does** | Cross-browser automation |
| **Runs locally** | ✅ Yes |

**Better than Puppeteer because:**
- Multi-browser (Chrome, Firefox, Safari)
- Better API design
- Microsoft-backed
- Python bindings available

---

### Tier 3: Low-Level Control

#### 8. PyAutoGUI ⭐⭐⭐
| Attribute | Value |
|-----------|-------|
| **GitHub** | github.com/asweigart/pyautogui |
| **Stars** | 12,000 |
| **Language** | Python |
| **What it does** | Mouse & keyboard automation |

**Use when:**
- You need raw mouse/keyboard control
- Building custom automation scripts
- Other tools don't work with specific software

---

## Recommendation for PLC Workbench

### Primary: Open Interpreter
**Why:**
1. Most mature and well-documented
2. Works with any desktop application
3. Can use Claude API or local Llama models
4. Natural language interface
5. Already has computer control capabilities

### Secondary: Self-Operating Computer
**Why:**
1. Vision-based (sees what you see)
2. Perfect for clicking on TIA Portal buttons
3. Doesn't need API access to PLC software

### Combination Approach:
```
Open Interpreter (brain)
    ↓
PyAutoGUI (hands) + Screenshot (eyes)
    ↓
PLC Software (TIA Portal, RSLogix, etc.)
```

---

## Architecture Concept

```
┌─────────────────────────────────────────────────────┐
│                   Mike's Laptop                     │
│                                                     │
│  ┌──────────────┐      ┌──────────────────────┐    │
│  │   Claude /   │      │    PLC Software      │    │
│  │   Local LLM  │◄────►│  (TIA Portal, etc.)  │    │
│  └──────────────┘      └──────────────────────┘    │
│         │                        ▲                  │
│         ▼                        │                  │
│  ┌──────────────┐      ┌──────────────────────┐    │
│  │    Open      │─────►│     PyAutoGUI        │    │
│  │  Interpreter │      │  (mouse/keyboard)    │    │
│  └──────────────┘      └──────────────────────┘    │
│         │                                           │
│         ▼                                           │
│  ┌──────────────┐                                   │
│  │  Screenshot  │ ◄── Vision model sees screen     │
│  │   Capture    │                                   │
│  └──────────────┘                                   │
└─────────────────────────────────────────────────────┘
```

---

## Next Steps (When Ready to Build)

1. **Install Open Interpreter** on laptop
2. **Test with simple task** (open Notepad, type text)
3. **Test with PLC software** (open project, navigate menus)
4. **Create custom prompts** for common PLC tasks
5. **Integrate with FactoryLM** knowledge base

---

## Resources

| Resource | URL |
|----------|-----|
| Open Interpreter Docs | docs.openinterpreter.com |
| Puppeteer Docs | pptr.dev |
| Playwright Docs | playwright.dev |
| Browser Use Docs | browser-use.com |
| Claude Computer Use | anthropic.com/claude/computer-use |

---

*Research complete. Ready to build when Mike gives green light.*
