# Work Order: WO-2026-001

## Header
| Field | Value |
|-------|-------|
| **WO Number** | WO-2026-001 |
| **Type** | Integration Setup |
| **Priority** | HIGH |
| **Status** | IN PROGRESS |
| **Created** | 2026-02-01 12:16 UTC |
| **Assigned To** | Mike Harp (USR-001) |
| **Asset** | FactoryLM VPS (factorylm-prod) |

## Description
**Set up LangFuse LLM Tracing for FactoryLM Platform**

Enable full observability of all LLM interactions across the FactoryLM system. Every prompt, response, and action must be traced and logged for:
- Knowledge base growth
- Trust verification
- System improvement
- Audit compliance

## Steps

### Step 1: Create LangFuse Cloud Account ✅
- [x] Go to https://cloud.langfuse.com
- [x] Sign up with FactoryLM email
- [x] Create project: "FactoryLM-Production"
- [x] Note API keys (public + secret)

### Step 2: Configure Environment Variables ✅
```bash
# Add to /opt/master_of_puppets/.env
LANGFUSE_SECRET_KEY=sk-lf-...
LANGFUSE_PUBLIC_KEY=pk-lf-...
LANGFUSE_HOST=https://cloud.langfuse.com
```

### Step 3: Integrate with Clawdbot ⬜
- [ ] Add LangFuse Python SDK
- [ ] Wrap OpenAI/Anthropic calls
- [ ] Test trace appears in dashboard

### Step 4: Integrate with Flowise ⬜
- [ ] Add LangFuse credentials to Flowise env
- [ ] Verify agent traces appear

### Step 5: Integrate with Master of Puppets ⬜
- [ ] Add LangFuse to Celery tasks
- [ ] Trace all automaton actions
- [ ] Verify in dashboard

### Step 6: Verify End-to-End ⬜
- [ ] Send test message via Telegram
- [ ] Verify trace appears in LangFuse
- [ ] Check knowledge atoms generated
- [ ] Calculate trust score

## Parts/Materials Required
- LangFuse Cloud account (free tier)
- API keys
- Python SDK: `pip install langfuse`

## Safety Notes
- API keys are secrets - store in .env only
- Do not log to public repos

## Completion Criteria
1. All LLM calls traced in LangFuse dashboard
2. Trust score calculable from traces
3. Knowledge atoms automatically extracted
4. Mike can verify any claim independently

---

## Work Log

### 2026-02-01 12:16 UTC - Started
- Created work order
- Researched LangFuse documentation
- User: Jarvis (AI Assistant)

### 2026-02-01 12:XX UTC - Awaiting User Action
- Need Mike to create LangFuse Cloud account
- Need API keys to proceed

---

*FactoryLM CMMS - Work Order Template v1.0*
