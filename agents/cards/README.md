# Agent Cards

*A2A-style capability declarations for the Jarvis agent fleet.*

---

## What Are Agent Cards?

Agent Cards are JSON documents that describe what each agent can do, how to interact with it, and what triggers it. They follow patterns from Google's A2A Protocol for agent interoperability.

## Available Agents

| Agent | File | Trigger | Autonomy |
|-------|------|---------|----------|
| **Orchestrator** | `orchestrator.json` | Direct message, heartbeat | High |
| **Monitor Agent** | `monitor.json` | 15-min cron | High |
| **Code Agent** | `code-agent.json` | 30-min cron, signals | Medium |
| **Agile Agent** | `agile-agent.json` | 5-min cron | High |
| **Research Agent** | `research-agent.json` | 4-hour cron, on-demand | High |

## Card Structure

```json
{
  "name": "Agent Name",
  "description": "What the agent does",
  "url": "jarvis://agents/name",
  "version": "1.0.0",
  "capabilities": {
    "modalities": ["text", "voice", "code"],
    "autonomy_level": "high|medium|low"
  },
  "skills": [
    {
      "id": "skill_id",
      "name": "Skill Name",
      "description": "What the skill does"
    }
  ],
  "triggers": {
    "cron": "When triggered by cron",
    "on_demand": "When delegated by orchestrator"
  },
  "outputs": {
    "artifacts": ["file types produced"],
    "notifications": ["channels notified"]
  }
}
```

## Usage

### Discovering Agents
```python
import json
from pathlib import Path

cards_dir = Path("agents/cards")
for card_file in cards_dir.glob("*.json"):
    card = json.loads(card_file.read_text())
    print(f"{card['name']}: {card['description']}")
```

### Checking Capabilities
```python
card = json.loads(Path("agents/cards/code-agent.json").read_text())
skills = [s['id'] for s in card['skills']]
# ['issue_processing', 'pr_creation', 'code_review', ...]
```

## Constitutional Alignment

All agents operate under the Jarvis Constitution:
- **Article III**: Proactive Agency
- **Article IV**: One-Team Principle
- **Article V**: Boundaries and Guardrails
- **Amendment II**: No Drift (24/7 Factory)
- **Amendment III**: Proof of Work

## Future: A2A Integration

When we implement full A2A Protocol:
1. Agent Cards become discoverable at `/.well-known/agent.json`
2. Agents can communicate via standard A2A messages
3. External agents can collaborate with our fleet

---

*Created: 2026-01-30 | GitHub Issue: #15*
