# PROPOSAL: PLC Laptop → Maintenance LLM Server

**Requested by:** Mike Harp  
**Date:** 2026-02-01  
**Source:** Perplexity research + Mike's vision  
**Status:** AWAITING APPROVAL

---

## EXECUTIVE SUMMARY

Transform the **PLC Laptop** into a dedicated **Maintenance LLM Server** with:
1. Local inference (Ollama + llama3:8b)
2. Full traceability to existing observability stack
3. Integration with Master of Puppets routing
4. Foundation for white paper extraction from our journey

---

## THREE PARALLEL TRACKS

### 🎯 Track 1: MAX TRACEABILITY (First Priority)

**Goal:** Record EVERYTHING during setup for knowledge base + white papers

| What | How | Output |
|------|-----|--------|
| Screen recording | OBS/Windows Game Bar | Video evidence |
| Command logging | `tee` to timestamped log files | Text audit trail |
| Action tracing | `@observe` decorators (already built) | LangFuse traces |
| Telegram export | Desktop export → JSON | Chat history for extraction |

**Integration with existing stack:**
- All logs → `/opt/factorylm-sync/traces/` → Syncthing → all devices
- All traces → LangFuse + InfluxDB → Grafana
- Fits our Trust Verification System (every claim has evidence)

---

### 💻 Track 2: PLC LAPTOP AS MAINTENANCE LLM

**New Identity in Network Map:**

```yaml
node: plc-laptop
role: Maintenance LLM Server
tailscale_ip: 100.72.2.99
purpose: Industrial AI inference for PLC troubleshooting
stack:
  - Ollama (port 11434)
  - llama3:8b model (4.7GB)
  - LangFuse instrumentation
  - InfluxDB metrics
```

**Phase A: Install Ollama (30 min)**
```bash
curl -fsSL https://ollama.com/install.sh | sh
ollama pull llama3:8b
# Test: ollama run llama3:8b "Explain PLC scan cycle"
```

**Phase B: Connect to Observability (1 hour)**
- Wrap all calls with `@observe(name="maintenance_llm_inference")`
- Send metrics to InfluxDB bucket: `llm_metrics`
- Route: Mike → Telegram → Master of Puppets → Maintenance Multibot → plc-laptop

**Phase C: Register in Master of Puppets (30 min)**
- Add to `NETWORK_TOPOLOGY` config
- Update routing rules: maintenance queries → plc-laptop
- The Watchman monitors health
- The Monkey schedules periodic checks

**Phase D: Grafana Dashboard (30 min)**
- Panel: Inference Latency
- Panel: Success Rate
- Panel: Requests per Minute
- Panel: Error Types
- Alerts: Latency > 5s, Error rate > 10%

---

### 📚 Track 3: TELEGRAM → WHITE PAPERS (Future)

**The Vision:**
```
Telegram Chat History (JSON export)
    ↓
Parse: Decisions, specs, rationale
    ↓
Cluster by topic (Vault, Automata, Observability...)
    ↓
LLM generates white paper sections
    ↓
Human review + approval
    ↓
Published documentation
```

**Out of scope for this weekend, but setup captures the raw material.**

---

## HOW THIS FITS THE AUTOMATA HIERARCHY

```
MIKE
  ↓ "Why is my Micro 820 showing Modbus error?"
MASTER OF PUPPETS
  ↓ Routes to Lane A (Maintenance)
MAINTENANCE MULTIBOT
  ↓ Calls plc-laptop for local inference
PLC-LAPTOP (Ollama)
  ↓ Returns answer
  ↓ Trace → LangFuse
  ↓ Metrics → InfluxDB → Grafana
RESPONSE TO MIKE
  ↓ With full audit trail
```

---

## INTEGRATION WITH EXISTING SYSTEMS

| Existing System | How It Connects |
|-----------------|-----------------|
| **Observability module** | Add `trace_maintenance_llm()` function |
| **LangFuse** | `@observe` decorator on all Ollama calls |
| **InfluxDB** | New bucket: `llm_metrics` |
| **Grafana** | New dashboard: "Maintenance LLM Health" |
| **Master of Puppets** | Route maintenance queries to plc-laptop |
| **The Watchman** | Monitor plc-laptop health |
| **Syncthing** | Logs sync to all devices |
| **Master Network Map (Vault)** | Register plc-laptop credentials |

---

## IMPLEMENTATION TIMELINE

| Day | Track | Tasks |
|-----|-------|-------|
| Today | 1 | Set up screen recording, logging |
| Today | 2A | Install Ollama on plc-laptop |
| Today | 2A | Download llama3:8b, test inference |
| Tomorrow | 2B | Connect to LangFuse + InfluxDB |
| Tomorrow | 2C | Register in Master of Puppets |
| Tomorrow | 2D | Create Grafana dashboard |
| Later | 3 | Export Telegram, build white paper generator |

---

## SUCCESS CRITERIA

By end of weekend:
- [ ] Ollama running on plc-laptop (port 11434)
- [ ] llama3:8b answering PLC questions
- [ ] Traces appearing in LangFuse
- [ ] Metrics appearing in Grafana
- [ ] Master of Puppets routing maintenance queries to plc-laptop
- [ ] All setup steps logged for white paper extraction
- [ ] Telegram history exported (JSON)

---

## COMMANDS READY TO EXECUTE

**When approved, the Spec-Maker will formalize these into executable tasks:**

```bash
# Phase A - On plc-laptop
curl -fsSL https://ollama.com/install.sh | sh
ollama pull llama3:8b
ollama run llama3:8b "You are the Maintenance LLM. Introduce yourself."

# Phase B - VPS creates client
# (Spec-Maker generates maintenance_llm_client.py)

# Phase C - Update Master of Puppets config
# (Spec-Maker generates config patch)

# Phase D - Grafana dashboard
# (Spec-Maker generates JSON for import)
```

---

## DECISION REQUIRED

**Mike, approve to send through Automata:**

1. ✅ **APPROVE** → Spec-Maker formalizes → Execution begins
2. ❌ **REJECT** → Provide feedback
3. 🔄 **MODIFY** → What changes?

---

*Spec Source: Perplexity research + Mike's voice → This proposal*  
*Next step: Automata process per Constitution*
