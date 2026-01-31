# THE AUTOMATON HIERARCHY

*Master of Puppets → Code-Twin → Four Automata → The Monkey*

---

## MASTER OF PUPPETS (This Chat)

The original Claudebot. Understands:
- Business strategy
- Meta-level empire building  
- Constitution + Amendments + Commandments
- Decides WHAT the automata should do

**Two Knowledge Bases:**
1. **Product KB** - FactoryLM, maintenance LLM products
2. **Business KB** - Meta business strategy, e-commerce, wealth building

---

## TWO MULTIBOT INSTANCES (Code-Twins)

Two separate multibot instances on the VPS (formerly ClaudeBot/B-Bot):

### Lane A: MAINTENANCE MULTIBOT
- **Purpose**: FactoryLM, PLCs, industrial maintenance
- **Knowledge Base**: Factory KB, equipment manuals, PLC tags, maintenance procedures
- **Tools**: Manual Hunter, Alarm Triage, PLC simulators
- **Called by**: Automata for any Lane A (Product Cell) work

### Lane B: BUSINESS MULTIBOT  
- **Purpose**: Meta-business strategy, e-commerce, wealth building
- **Knowledge Base**: Business strategy KB, e-commerce tactics, rare strategies
- **Tools**: Market research, competitive analysis, financial modeling
- **Called by**: Automata for any Lane B (Empire Building) work

**Routing Rule**: Master of Puppets NEVER does low-level work directly. Routes via Monkey → Automata → correct Multibot based on lane.

---

## THE FOUR AUTOMATA

### Automaton 1: THE SPEC-MAKER
Takes natural language and produces:
- Formal specification
- Initial workflow (Flowise/n8n/MCP/code)
- Tests
- 5-second report for 11-year-old verification

**Port: 8090-8092** (Manual Hunter, Alarm Triage, Workflow Tracker)

### Automaton 2: THE WEAVER
Lives in GitHub. On each commit + hourly cron:
- Pulls repos
- Refactors and stitches workflows into coherent products
- Runs sandboxed end-to-end tests
- Only ships when answers are grounded in manuals/KB/PLC sim

**Port: 8093**

### Automaton 3: THE CODE CARTOGRAPHER
- Scans large existing repos
- Builds maps of files → functions → services
- Proposes workflow boundaries
- Drafts Flowise/n8n/MCP definitions
- Hands specs to Automaton 1 for formalization

**Port: 8095** (Planned)

### Automaton 4: THE WATCHMAN
Watches runtime behavior:
- Logs, token usage, errors, latency
- Detects drift, hallucination risks, brittle edges
- Opens maintenance tickets when:
  - Workflow fails tests
  - Answers look implausible
  - Token cost too high
  - User feedback is bad

**Port: 8094**

---

## THE MONKEY AT THE CRANK

Keeps everything running 24/7 within token budget.
- Hourly cron jobs (Big Ben tick)
- GitHub webhooks
- Budget monitoring
- Health checks

---

## FOUNDATIONAL LAW

**Constitution + Amendments + Commandments**

1. **MY WORDS = THE SPEC**
2. Every action follows the 4-step loop:
   - Spec → Build → Prove → 5-second Kid Check
3. Every workflow must be:
   - Versioned in GitHub
   - Observed (logging, token usage)
   - Tested end-to-end in sandbox
   - Grounded in real data, NOT hallucinations

---

## CURRENT SERVICES

| Automaton | Service | Port | Status |
|-----------|---------|------|--------|
| 1 | Manual Hunter | 8090 | ✅ LIVE |
| 1 | Alarm Triage | 8091 | ✅ LIVE |
| 1 | Workflow Tracker | 8092 | ✅ LIVE |
| 2 | The Weaver | 8093 | ✅ LIVE |
| 4 | The Watchman | 8094 | ✅ LIVE |
| 3 | Code Cartographer | 8095 | ✅ LIVE |
| - | Flowise | 3001 | ✅ LIVE |
| - | n8n | 5678 | ✅ LIVE |

---

## THE 5-SECOND VIEW

For every answer:
- **Question**: What the user asked
- **Answer**: What the system determined
- **Evidence**: Manual page, KB entry, PLC sim proof

If an 11-year-old can see all three and say "yeah, that makes sense" → PASSED.

---

*Master of Puppets pulls the strings. The Automata do the work. The Monkey keeps it running.*
