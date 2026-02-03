# 📋 WORKFLOW DOCUMENTATION PROCESS

**This is a foundational process. All workflows MUST be documented.**

---

## 🎯 Purpose

Every AI workflow, automation, and voice→code execution must be:
1. Logged with proof of work
2. Documented in Flowise (visual representation)
3. Committed to GitHub
4. Reviewable by humans

---

## 📍 Documentation Locations

| Type | Location | Format |
|------|----------|--------|
| Proof of Work | `/evidence/workflows/` | JSONL + MD |
| Visual Flows | Flowise (port 3001) | Drag & Drop |
| Process Docs | `/processes/` | Markdown |
| Code | `/opt/master_of_puppets/` | Python |

---

## 🔄 Automatic Logging

Every command through Jarvis is automatically logged:

```python
from workers.workflow_logger import log_telegram_command

log_telegram_command(
    message="User's message",
    action="What was done",
    result="Output",
    success=True,
    duration_ms=150.5
)
```

---

## 🌊 Flowise Integration

### Access
- **URL:** http://165.245.138.91:3001
- **Login:** mike / CNI9EgSKBu6vm18t

### Create New Workflow
1. Open Flowise
2. Click "Add New" → "Chatflow"
3. Name it descriptively (e.g., "Voice to Code Executor")
4. Build the flow visually
5. Save and test

### Programmatic Access
```python
import requests

FLOWISE_URL = "http://localhost:3001"
API_KEY = "cd25ef26ae7e4ec9293ce8cdfbc80bcf8ed6ccd1c486922011c1fc9ad5f707ec"

# List all flows
response = requests.get(
    f"{FLOWISE_URL}/api/v1/chatflows",
    headers={"Authorization": f"Bearer {API_KEY}"}
)
flows = response.json()

# Execute a flow
response = requests.post(
    f"{FLOWISE_URL}/api/v1/prediction/{flow_id}",
    headers={"Authorization": f"Bearer {API_KEY}"},
    json={"question": "Your input here"}
)
```

---

## 📊 Daily Review

Every day, review:
1. `/evidence/workflows/YYYY-MM-DD.jsonl` - Raw logs
2. `/evidence/workflows/WORKFLOW_SUMMARY.md` - Quick summary
3. Flowise dashboard - Visual flows

---

## ✅ Checklist for New Workflows

- [ ] Define input/output
- [ ] Create in Flowise (visual)
- [ ] Add logging to code
- [ ] Test with proof of work
- [ ] Commit to GitHub
- [ ] Update this document if needed

---

## 🔗 Related Files

- `/opt/master_of_puppets/workers/workflow_logger.py` - Logging code
- `/opt/master_of_puppets/integrations/flowise.py` - Flowise client
- `/root/jarvis-workspace/KEYMASTER.md` - Credentials
- `/root/jarvis-workspace/NETWORK_MAP.md` - Network topology

---

*This process is foundational. All team members and AI agents must follow it.*
