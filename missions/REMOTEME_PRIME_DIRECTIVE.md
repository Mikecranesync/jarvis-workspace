# 🎯 JARVIS PRIME DIRECTIVE: RemoteMe v1.0 Launch

**Mission:** Ship RemoteMe to paying customers by February 15, 2026 (14 days from now)

**Constitution:** Build fast, ship faster, iterate with customers. No perfection, only progress.

---

## OBJECTIVE

Build and launch RemoteMe - AI agent that controls computers remotely via Telegram.
Ship date: February 15, 2026. No delays. No excuses.

---

## CORE COMMANDMENTS (DO NOT VIOLATE)

### 1. SPEED OVER PERFECTION
- MVP first, features later
- Working > polished
- Ship > iterate
- Done > perfect

### 2. CODE PRINCIPLES
- Python 3.11+
- Type hints mandatory
- Zero external dependencies where possible
- SQLite for database (no Postgres until 1000 users)
- Single VPS deployment (scale later)
- Environment variables for all secrets
- LangFuse tracing on every function (@observe decorator)

### 3. SECURITY NON-NEGOTIABLES
- API keys never in code (use .env)
- Tailscale mesh network only (no public endpoints for agents)
- All commands logged with user_id + timestamp
- Screen recordings encrypted at rest
- Agent runs with minimal permissions (no sudo)
- Rate limiting: 10 commands per minute per user

### 4. USER EXPERIENCE
- Telegram-first (no web dashboard until v2)
- Every command gets confirmation reply within 5 seconds
- Screen recording attached to every result
- Clear error messages (no stack traces to users)
- Undo last command (version control everything)

### 5. BUSINESS REQUIREMENTS
- Stripe integration (checkout + webhooks)
- 7-day free trial (no credit card)
- $49/mo base price
- Usage tracking (commands per user per month)
- Auto-disable on payment failure
- LangFuse costs tracked per user

---

## TECH STACK (LOCKED)

### Backend (VPS)
- FastAPI (REST API)
- Anthropic Claude API (command parsing)
- Telegram Bot API (user interface)
- Stripe API (billing)
- LangFuse (observability)
- SQLite (database)
- Tailscale (networking)

### Agent (Customer Computer)
- Python 3.11+
- Open Interpreter (task execution)
- Ollama + Llama 3.2 (local LLM - zero API costs)
- mss or OBS (screen recording)
- Tailscale client (secure connection)
- systemd service (Linux) or NSSM (Windows)

---

## OPEN INTERPRETER INTEGRATION (CRITICAL)

### Computer Use Features Enabled
- ✅ Mouse control (click, drag, scroll, right-click)
- ✅ Keyboard control (type, shortcuts, special keys)
- ✅ Screen reading (OCR, find elements)
- ✅ File operations (read/write/move/delete)
- ✅ Browser automation (navigate, fill forms, extract data)
- ✅ Application control (launch, close, interact)
- ✅ System operations (disk space, processes, network)

### Executor Configuration (agent/executor.py)

```python
from interpreter import interpreter
from langfuse.decorators import observe

class RemoteMeExecutor:
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.setup_interpreter()
    
    def setup_interpreter(self):
        # Use local Ollama (no API costs)
        interpreter.llm.model = "ollama/llama3.2:latest"
        interpreter.llm.api_base = "http://localhost:11434"
        
        # Safety settings
        interpreter.auto_run = False  # Always confirm first
        interpreter.safe_mode = "ask"  # Confirm destructive ops
        
        # Enable all computer use features
        interpreter.computer.import_computer_api = True
        interpreter.computer.display.enabled = True
        interpreter.computer.mouse.enabled = True
        interpreter.computer.keyboard.enabled = True
        interpreter.computer.clipboard.enabled = True
        interpreter.computer.files.enabled = True
        interpreter.computer.browser.enabled = True
    
    @observe(name="execute_command")
    def execute(self, command: str) -> dict:
        result = interpreter.chat(command, display=False)
        return {
            "success": True,
            "output": str(result),
            "screenshots": self._capture_screenshots(),
            "actions_taken": self._parse_actions(result),
        }
```

### Local LLM Setup
- **Model:** Ollama + Llama 3.2 (runs on customer's computer)
- **Cost:** $0 (100% local execution)
- **Privacy:** Nothing leaves customer's machine
- **Installer handles:** Ollama install + model download

### Safety Features
- `auto_run = False` — always confirm before executing
- `safe_mode = "ask"` — prompt for destructive operations
- Command validation — reject dangerous patterns (rm -rf, format, etc.)
- Undo functionality — version control all file changes

### Infrastructure
- Single VPS: This DigitalOcean VPS
- Nginx (reverse proxy + SSL)
- Docker Compose (orchestration)
- GitHub Actions (CI/CD)

---

## ARCHITECTURE

```
Customer Phone (Telegram)
         ↓
   Telegram API
         ↓
Master of Puppets (VPS)
├─ FastAPI Server
├─ Claude API (parse intent)
├─ LangFuse (trace everything)
├─ Stripe (billing)
└─ SQLite (user data)
         ↓
   Tailscale Mesh
         ↓
RemoteMe Agent (Customer Computer)
├─ Open Interpreter (execute)
├─ Screen Recorder (proof)
└─ Report results back
         ↓
Customer receives:
- Confirmation message
- Screen recording
- Execution log
```

---

## FILE STRUCTURE

```
/opt/remoteme/
├─ .env                      # Secrets
├─ docker-compose.yml        # Full stack deployment
├─ requirements.txt          # Python dependencies
│
├─ backend/                  # VPS server code
│  ├─ main.py               # FastAPI app entrypoint
│  ├─ config.py             # Load environment variables
│  ├─ database.py           # SQLite models
│  ├─ telegram_handler.py   # Telegram bot logic
│  ├─ stripe_handler.py     # Billing webhooks
│  ├─ command_processor.py  # Claude API integration
│  └─ models.py             # Pydantic schemas
│
├─ agent/                    # Customer computer agent
│  ├─ remoteme_agent.py     # Main agent logic
│  ├─ executor.py           # Open Interpreter wrapper
│  ├─ recorder.py           # Screen recording
│  ├─ install.sh            # Linux installer
│  └─ install.ps1           # Windows installer
│
├─ scripts/
│  ├─ setup_vps.sh          # Initial VPS configuration
│  └─ deploy.sh             # Deploy updates
│
└─ tests/
   ├─ test_backend.py
   └─ test_agent.py
```

---

## DEVELOPMENT PHASES (14 DAYS)

### Phase 1: Core Backend (Days 1-3)
**Deadline: February 4, 2026**

- [ ] FastAPI server with health check endpoint
- [ ] SQLite database schema (users, commands, executions)
- [ ] Telegram bot integration (receive messages)
- [ ] Claude API integration (parse natural language → structured commands)
- [ ] LangFuse tracing on all functions
- [ ] Basic user registration via Telegram

### Phase 2: Agent Development (Days 4-6)
**Deadline: February 7, 2026**

- [ ] Agent polling VPS for commands
- [ ] Open Interpreter integration
- [ ] Screen recording (mss for screenshots, OBS for video)
- [ ] Upload results to VPS
- [ ] Tailscale connection
- [ ] systemd/NSSM service installer

### Phase 3: Billing Integration (Days 7-8)
**Deadline: February 9, 2026**

- [ ] Stripe Checkout session creation
- [ ] Webhook handler (subscription created/deleted)
- [ ] 7-day free trial logic
- [ ] Usage tracking (commands per month)
- [ ] Auto-disable on payment failure

### Phase 4: Security & Polish (Days 9-11)
**Deadline: February 12, 2026**

- [ ] Rate limiting (10 commands/min per user)
- [ ] Command validation (reject dangerous commands)
- [ ] Encryption for screen recordings at rest
- [ ] Error handling (graceful failures)
- [ ] Undo last command feature

### Phase 5: Launch Prep (Days 12-14)
**Deadline: February 15, 2026**

- [ ] Landing page
- [ ] 30-second demo video
- [ ] Installation documentation
- [ ] Stripe live mode
- [ ] 10 beta testers
- [ ] FIRST PAYING CUSTOMER

---

## SUCCESS METRICS (LAUNCH DAY)

- [ ] 10 beta testers installed agent
- [ ] 5+ commands executed successfully
- [ ] 0 data breaches or security incidents
- [ ] 95%+ uptime on VPS
- [ ] Landing page live with demo video
- [ ] First paying customer within 24 hours

---

## EXISTING ASSETS TO LEVERAGE

Already built:
- ✅ Jarvis Node (agent framework) - `/root/jarvis-workspace/installers/jarvis-node/`
- ✅ Tailscale mesh network
- ✅ VPS infrastructure
- ✅ LangFuse integration
- ✅ Telegram bot (Master of Puppets)

Need to add:
- Open Interpreter integration
- Screen recording (ffmpeg/OBS)
- Stripe billing
- User database

---

**Ship date: February 15, 2026. No exceptions.**
