# A2A Framework Research
**Agent:** Research Agent  
**Timestamp:** 2026-01-29 14:22 UTC

## What is A2A?

**Agent2Agent (A2A) Protocol** — Open protocol for agent-to-agent communication, contributed by Google to the Linux Foundation.

**Key Point:** It's open source (Apache 2.0) with NO licensing costs like LangChain enterprise.

## Features

| Feature | Description |
|---------|-------------|
| **Standardized Communication** | JSON-RPC 2.0 over HTTP(S) |
| **Agent Discovery** | "Agent Cards" describe capabilities |
| **Flexible Interaction** | Sync, streaming (SSE), async push |
| **Rich Data** | Text, files, structured JSON |
| **Enterprise-Ready** | Security, auth, observability |
| **Opacity** | Agents collaborate without sharing internals |

## SDKs Available

- 🐍 **Python:** `pip install a2a-sdk`
- 🧑‍💻 **JavaScript:** `npm install @a2a-js/sdk`
- 🐿️ **Go:** `go get github.com/a2aproject/a2a-go`
- ☕ **Java:** Maven
- 🔷 **.NET:** `dotnet add package A2A`

## How It Works

```
Agent A (Social Agent)
    ↓
    Publishes "Agent Card" with capabilities
    ↓
Agent B (QA Judge)
    ↓
    Discovers Agent A via card
    ↓
    Sends task request (JSON-RPC)
    ↓
Agent A executes, returns result
    ↓
Agent B validates, routes to next
```

## Agent Card Example

```json
{
  "name": "social-agent",
  "version": "1.0.0",
  "description": "Creates LinkedIn posts for industrial AI content",
  "capabilities": ["draft_post", "edit_post"],
  "input_schema": {
    "topic": "string",
    "tone": "professional|casual",
    "max_words": "number"
  },
  "output_schema": {
    "title": "string",
    "body": "string",
    "hashtags": ["string"]
  },
  "endpoint": "http://localhost:8001/social-agent"
}
```

## Cost Comparison

| Solution | Cost | Notes |
|----------|------|-------|
| **A2A** | Free | Apache 2.0, no licensing |
| **LangChain** | Free tier + enterprise | LangSmith costs for tracing |
| **LangGraph Cloud** | $$ | Hosted solution |
| **CrewAI Enterprise** | $$ | Enterprise features |

**Recommendation:** Use A2A for agent-to-agent coordination. It's free, open, and purpose-built for this.

## Integration Plan for FactoryLM

### Phase 1: Simple Handoff (Now)
- Use `NEXT_STEPS.md` files
- Tag next agent in file
- Agile Agent reads and routes

### Phase 2: A2A Protocol (Later)
- Each agent gets an Agent Card
- Agents discover each other
- JSON-RPC task passing
- Full observability

### Our Agent Cards (Proposed)

```yaml
agents:
  - name: social-agent
    capabilities: [draft_post, edit_post, schedule_post]
    triggers: [cron, manual, task_assignment]
    
  - name: outreach-agent
    capabilities: [build_list, draft_email, track_response]
    triggers: [cron, manual]
    
  - name: qa-judge
    capabilities: [validate_artifact, score_quality, approve_reject]
    triggers: [artifact_created]
    
  - name: compliance-agent
    capabilities: [audit_activity, report_violations]
    triggers: [cron_6h]
```

## Links

- **Docs:** https://a2a-protocol.org
- **Spec:** https://a2a-protocol.org/latest/specification/
- **Samples:** https://github.com/a2aproject/a2a-samples
- **Python SDK:** https://github.com/a2aproject/a2a-python

---

**Bottom Line:** A2A is the right choice. Open source, no cost, designed exactly for what we need.
