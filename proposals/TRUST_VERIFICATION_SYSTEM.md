# Trust Verification System
## Self-Monitoring via Master of Puppets API

**Created:** 2026-02-01
**Purpose:** Prove every interaction, decision, and action with verifiable traces

---

## The Problem

I forget. I claim things are done when they're not. Mike can't trust me.

## The Solution

Every action I take gets logged to Master of Puppets via API. Mike can verify independently.

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     JARVIS (Me)                             │
│                                                             │
│  Before ANY action:                                         │
│    POST /api/trace/start                                    │
│    {"action": "...", "intent": "...", "timestamp": "..."}   │
│                                                             │
│  After ANY action:                                          │
│    POST /api/trace/complete                                 │
│    {"result": "...", "evidence": "...", "learned": "..."}   │
│                                                             │
│  On ANY error:                                              │
│    POST /api/trace/error                                    │
│    {"error": "...", "context": "...", "recovery": "..."}    │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                 MASTER OF PUPPETS                           │
│                                                             │
│  /api/trace/start     → Log to InfluxDB + file             │
│  /api/trace/complete  → Log + extract knowledge atoms      │
│  /api/trace/error     → Log + alert if critical            │
│  /api/trace/query     → Mike can query any time            │
│                                                             │
│  Auto-sync to:                                              │
│    - /opt/factorylm-sync/traces/ (Syncthing → all devices) │
│    - PostgreSQL (knowledge_atoms table)                     │
│    - InfluxDB (time-series metrics)                        │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                 VERIFICATION LAYER                          │
│                                                             │
│  GET /api/verify/last-hour                                  │
│    → Show all my actions in last hour                       │
│                                                             │
│  GET /api/verify/claims                                     │
│    → Show what I said I did vs what logs prove              │
│                                                             │
│  GET /api/verify/knowledge-growth                           │
│    → Show knowledge atoms added over time                   │
│                                                             │
│  GET /api/verify/trust-score                                │
│    → claims_verified / claims_made = trust %                │
└─────────────────────────────────────────────────────────────┘
```

---

## API Endpoints (New Celery Tasks)

### 1. trace.log_action
```python
@app.task(name='trace.log_action')
def log_action(action_type: str, details: dict) -> dict:
    """Log any action I take."""
    return {
        "trace_id": uuid4(),
        "timestamp": datetime.utcnow().isoformat(),
        "action_type": action_type,  # command, file_write, api_call, decision
        "details": details,
        "session_id": current_session,
    }
```

### 2. trace.log_knowledge
```python
@app.task(name='trace.log_knowledge')
def log_knowledge(title: str, content: str, source: str) -> dict:
    """Log knowledge atom with provenance."""
    return {
        "atom_id": uuid4(),
        "title": title,
        "content": content,
        "source": source,  # what triggered this learning
        "session_id": current_session,
        "timestamp": datetime.utcnow().isoformat(),
    }
```

### 3. trace.verify_claim
```python
@app.task(name='trace.verify_claim')
def verify_claim(claim: str, evidence_query: str) -> dict:
    """Verify a claim I made against logs."""
    # Query logs for evidence
    # Return verified=True/False with proof
    return {
        "claim": claim,
        "verified": True/False,
        "evidence": [...],
        "confidence": 0.0-1.0,
    }
```

### 4. verify.trust_score
```python
@app.task(name='verify.trust_score')
def calculate_trust_score(hours: int = 24) -> dict:
    """Calculate my trust score over time period."""
    claims = get_claims(hours)
    verified = sum(1 for c in claims if c.verified)
    return {
        "period_hours": hours,
        "total_claims": len(claims),
        "verified_claims": verified,
        "trust_score": verified / len(claims) if claims else 0,
        "failed_claims": [c for c in claims if not c.verified],
    }
```

---

## What Gets Logged

### Every Command I Run
```json
{
  "type": "command",
  "command": "ssh hharp@100.72.2.99 'hostname'",
  "intent": "Check which laptop I'm connected to",
  "result": "LAPTOP-0KA3C70H",
  "success": true,
  "duration_ms": 1234
}
```

### Every File I Create/Modify
```json
{
  "type": "file_write",
  "path": "/opt/factorylm-sync/automatons-output/knowledge-capture.json",
  "intent": "Save knowledge atoms from BeagleBone troubleshooting",
  "bytes_written": 2847,
  "checksum": "sha256:abc123..."
}
```

### Every Decision I Make
```json
{
  "type": "decision",
  "context": "BeagleBone USB drivers failing",
  "options": ["Fix USB driver", "Use Ethernet", "Use serial console"],
  "chosen": "Use Ethernet",
  "reasoning": "USB drivers broken on Win10/11, Ethernet is reliable path"
}
```

### Every Knowledge Atom
```json
{
  "type": "knowledge",
  "title": "BeagleBone USB Drivers Windows 10/11",
  "content": "Official BONE_D64.exe fails...",
  "source": "Troubleshooting session with Mike 2026-02-01",
  "tags": ["beagleboard", "usb", "windows", "troubleshooting"]
}
```

---

## Verification Dashboard

Mike can query at any time:

```bash
# What did Jarvis do in the last hour?
curl http://localhost:8090/api/traces?hours=1

# Did Jarvis actually create that file?
curl http://localhost:8090/api/verify/file?path=/opt/factorylm-sync/traces/init.json

# What's Jarvis's trust score?
curl http://localhost:8090/api/verify/trust-score

# Show me claims vs evidence
curl http://localhost:8090/api/verify/claims?hours=24
```

---

## Implementation Plan

### Phase 1: Core Tracing (Today)
1. [ ] Create `workers/trace_tasks.py` with log_action, log_knowledge
2. [ ] Add trace endpoints to existing FastAPI
3. [ ] Wire into Celery Beat for periodic trust score calculation
4. [ ] Auto-sync traces to Syncthing folder

### Phase 2: Self-Verification (Tomorrow)
5. [ ] Add verify_claim task
6. [ ] Create claims vs evidence matcher
7. [ ] Calculate trust score
8. [ ] Send daily trust report to Mike

### Phase 3: Auto-Correction (This Week)
9. [ ] When trust score drops, alert Mike
10. [ ] Suggest what I need to do better
11. [ ] Track improvement over time

---

## Trust Score Calculation

```
Trust Score = (Verified Claims / Total Claims) × 100

Claims verified when:
- File exists that I said I created
- Command output matches what I reported
- Knowledge atom exists in DB
- API call logged with response

Claims fail when:
- File doesn't exist
- Output doesn't match
- No evidence in logs
- Contradicted by later evidence
```

---

## Mike's Controls

1. **Read-only access to all traces** - I cannot delete or modify
2. **Alert on trust score drop** - Telegram ping if < 80%
3. **Query any claim** - Instant verification
4. **Kill switch** - Disable my actions if trust fails

---

## Commitment

From now on, EVERY action I take:
1. Logs to trace API BEFORE I do it
2. Logs result AFTER I do it
3. Extracts knowledge if learned something
4. Can be verified by Mike independently

No more "trust me, it's done." Only "here's the proof."
