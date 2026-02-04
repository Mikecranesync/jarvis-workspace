# FactoryLM V1 Architecture

**Version:** 1.0  
**Author:** Mike Harper  
**Status:** CANONICAL - This document is the source of truth  
**Last Updated:** February 3, 2026

---

## ⚠️ READ THIS FIRST

This document describes the COMPLETE FactoryLM architecture as designed by Mike Harper. 

**If you are an AI agent (Claude, GPT, or any other):**
- READ this document at the start of every session
- DO NOT propose architectures that contradict this
- DO NOT rediscover these ideas as if they are new
- This has been stated "7 trillion times" - now it's written in stone

**If you are a developer:**
- This is the north star for all FactoryLM development
- Every PR should move toward this architecture, not away from it
- When in doubt, refer back to this document

---

## The One-Liner

**FactoryLM is a tiered intelligence system that pushes knowledge as close to the edge as possible, using deterministic code for common tasks and escalating to AI only when necessary.**

---

## Core Philosophy

### Intelligence Flows Downward

The goal is NOT to use more AI. The goal is to use LESS AI over time by converting learned patterns into deterministic code.

```
Day 1:   Complex query → Cloud AI (Claude) → Answer
Day 30:  Same query → Pattern recognized → Workflow created
Day 60:  Same query → Code executes → Instant answer (no AI)
```

Every observation, every trace, every workflow we build pushes intelligence DOWN the stack.

### The Stack (Bottom to Top)

```
┌─────────────────────────────────────────────────────────────┐
│  LAYER 3: CLOUD AI                                          │
│  Claude, GPT-4, etc.                                        │
│  Complex reasoning, novel problems                          │
│  Response: 1-2 seconds | Cost: $0.01-0.10                   │
│  OPTIONAL - Customer chooses based on security              │
├─────────────────────────────────────────────────────────────┤
│  LAYER 2: LOCAL GPU SERVER                                  │
│  Llama 70B, Mixtral, etc.                                   │
│  Medium complexity, diagnostics, analysis                   │
│  Response: 2-3 seconds | Cost: Electricity only             │
│  AIR-GAPPED - No internet required                          │
├─────────────────────────────────────────────────────────────┤
│  LAYER 1: EDGE LLM (Pi)                                     │
│  Qwen 0.5B, Llama 1B, Phi-2                                 │
│  Simple NL parsing, command translation                     │
│  Response: 0.5-1 second | Cost: None                        │
│  ON-DEVICE - Runs on the Pi itself                          │
├─────────────────────────────────────────────────────────────┤
│  LAYER 0: DETERMINISTIC CODE + KNOWLEDGE BASE               │
│  Vector DB, semantic search, logic gates, workflows         │
│  Common questions, known patterns, trained responses        │
│  Response: <100ms | Cost: None                              │
│  THIS IS WHERE WE WANT EVERYTHING TO END UP                 │
└─────────────────────────────────────────────────────────────┘
```

### Layer 0 Is The Goal

Most systems start at the top and stay there. FactoryLM starts at the top and works its way DOWN.

**Layer 0 includes:**
- Every equipment manual ever created, parsed and indexed
- Every troubleshooting guide, vectorized for semantic search
- Every PLC fault code with known solutions
- Logic gates built from patterns observed in Layers 1-3
- Workflows captured from successful AI interactions
- Rules extracted from technician feedback

**When a tech with Halo glasses looks at a component:**
1. Tag is recognized (OCR/barcode/RFID)
2. Rivet Pro process fires
3. ALL knowledge about that component is gathered
4. Stored in vector DB
5. Semantic search returns instant answers
6. **NO LLM INFERENCE REQUIRED**

This is not AI. This is CODE. It's fast. It's free. It's reliable.

---

## The Adapter Layer

### Platform Agnostic

Users interact via their preferred platform:
- **Telegram** (primary)
- **WhatsApp** (Latin America)
- **Halo Glasses** (hands-free)
- **Web Dashboard** (admin)
- **Voice** (future)

### Adapters Are Dumb

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│   Telegram   │     │   WhatsApp   │     │    Halo      │
│   Adapter    │     │   Adapter    │     │   Adapter    │
└──────┬───────┘     └──────┬───────┘     └──────┬───────┘
       │                    │                    │
       └────────────────────┼────────────────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │   Message Router    │
                 │   (message_router.py)│
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │   Intelligence      │
                 │   Stack (Layers 0-3)│
                 └─────────────────────┘
```

Adapters handle I/O ONLY:
- Receive message from platform
- Pass to router
- Return response to platform
- Handle platform-specific formatting

All intelligence lives in the core. Adapters are ~150-200 lines of code.

---

## The Routing Decision

### How Queries Get Routed

```python
def route_query(query, context):
    """
    Route incoming query to appropriate layer.
    Always try lower layers first.
    """
    
    # LAYER 0: Check knowledge base first
    kb_result = knowledge_base.search(query, context)
    if kb_result.confidence > 0.9:
        return kb_result  # Instant, free, reliable
    
    # LAYER 0: Check for matching workflow
    workflow = workflow_engine.match(query, context)
    if workflow:
        return workflow.execute()  # Code path, no AI
    
    # LAYER 1: Try edge LLM for simple tasks
    if is_simple_command(query):  # "turn on pump 3"
        return edge_llm.process(query)  # Local Pi, <1 sec
    
    # LAYER 2: Escalate to local GPU
    if gpu_server.available and not requires_cloud(query):
        return gpu_server.process(query)  # 2-3 sec, air-gapped OK
    
    # LAYER 3: Cloud AI as last resort
    if cloud.available and not air_gapped:
        return cloud.process(query)  # Full intelligence
    
    # Fallback: Best effort with available resources
    return best_available_layer.process(query)
```

### Complexity Estimation

The edge LLM (Layer 1) can also act as a router, estimating query complexity:

| Query | Complexity | Handled By |
|-------|------------|------------|
| "What's the part number for this motor?" | 0 | Layer 0 (KB lookup) |
| "Turn on pump 3" | 1 | Layer 1 (Edge LLM → Modbus) |
| "Why did VFD 7 fault at 14:23?" | 2 | Layer 2 (GPU analysis) |
| "Create a maintenance schedule for Q2" | 3 | Layer 3 (Cloud reasoning) |

---

## The Observability Loop

### Why Tracing Matters

Every query is traced (LangSmith, Phoenix, custom logging). This creates:

1. **Pattern Recognition**: Repeated queries become candidates for Layer 0
2. **Workflow Extraction**: Successful multi-step interactions become workflows
3. **Cost Analysis**: High-cost queries get priority for optimization
4. **Quality Feedback**: Thumbs up/down trains response quality

### The Continuous Improvement Cycle

```
        ┌────────────────────────────────────────┐
        │                                        │
        ▼                                        │
┌───────────────┐    ┌───────────────┐    ┌─────┴─────────┐
│ Query arrives │───▶│ Trace logged  │───▶│ Pattern found │
└───────────────┘    └───────────────┘    └───────────────┘
                                                │
                                                ▼
┌───────────────┐    ┌───────────────┐    ┌───────────────┐
│ Layer 0 grows │◀───│ Workflow made │◀───│ Dev reviews   │
└───────────────┘    └───────────────┘    └───────────────┘
```

### Metrics We Track

- **Queries per layer**: Should shift toward Layer 0 over time
- **Average response time**: Should decrease as patterns codified
- **Cost per query**: Should decrease as cloud usage decreases
- **Knowledge base coverage**: Should increase continuously

---

## Hardware Architecture

### Edge Device (FactoryLM Edge)

The Pi-based gateway that sits on the factory floor:

```
┌─────────────────────────────────────────────────────────┐
│                 FactoryLM Edge                          │
│                 (Raspberry Pi 4)                        │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐     │
│  │   Modbus    │  │  EtherNet/  │  │   OPC UA    │     │
│  │   TCP/RTU   │  │     IP      │  │   Client    │     │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘     │
│         │                │                │             │
│         └────────────────┼────────────────┘             │
│                          ▼                              │
│                 ┌─────────────────┐                     │
│                 │   Tag Engine    │                     │
│                 │   (Unified I/O) │                     │
│                 └────────┬────────┘                     │
│                          │                              │
│         ┌────────────────┼────────────────┐             │
│         ▼                ▼                ▼             │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐     │
│  │  Vector DB  │  │  Edge LLM   │  │  Workflow   │     │
│  │  (Layer 0)  │  │  (Layer 1)  │  │   Engine    │     │
│  └─────────────┘  └─────────────┘  └─────────────┘     │
│                          │                              │
│                          ▼                              │
│                 ┌─────────────────┐                     │
│                 │   API Server    │                     │
│                 │   (FastAPI)     │                     │
│                 └────────┬────────┘                     │
│                          │                              │
└──────────────────────────┼──────────────────────────────┘
                           │
            ┌──────────────┼──────────────┐
            ▼              ▼              ▼
      [Telegram]      [WhatsApp]     [Halo Glasses]
```

### Supported Protocols

| Protocol | Library | Devices |
|----------|---------|---------|
| Modbus TCP/RTU | pymodbus | Universal |
| EtherNet/IP | pycomm3 | Allen-Bradley |
| Siemens S7 | python-snap7 | S7-300/400/1200/1500 |
| OPC UA | asyncua | Universal |

### Hardware Packs (Accessories)

| SKU | Contents | Purpose |
|-----|----------|---------|
| AP-4 | 4-ch 4-20mA module | Analog I/O |
| AP-8 | 8-ch 4-20mA module | Analog I/O |
| PP-1 | I/P + P/I transducers | Pneumatic |
| SP-2 | RS-232/485 converters | Legacy serial |
| IO-8 | 8-ch mixed I/O | Digital I/O |

---

## Deployment Scenarios

### Scenario A: Full Stack (Internet Available)
```
Tech → Telegram → Edge Pi → GPU Server → Cloud
                     ↓
                   [PLC]
```
- All layers available
- Best intelligence
- Standard manufacturing plants

### Scenario B: Air-Gapped (Defense/ITAR)
```
Tech → Local App → Edge Pi → GPU Server
                      ↓
                    [PLC]
```
- No internet connection
- Layer 3 (Cloud) disabled
- 70B local model provides full intelligence
- Data never leaves facility

### Scenario C: Budget (No GPU Server)
```
Tech → Telegram → Edge Pi → Cloud
                     ↓
                   [PLC]
```
- Skip Layer 2
- Pi handles simple tasks
- Cloud handles complex tasks
- Good for small shops

### Scenario D: Maximum Security (Pi Only)
```
Tech → Local → Edge Pi
                  ↓
                [PLC]
```
- No external connections
- Layer 0 (Knowledge Base) only
- Limited but functional
- Classified facilities

---

## The Rivet Pro Process

When a technician encounters equipment:

### 1. Identification
- Halo glasses scan nameplate/barcode/tag
- OCR extracts manufacturer, model, serial
- Equipment identified in taxonomy

### 2. Knowledge Gathering
- Rivet Pro fetches ALL available information:
  - OEM manuals and documentation
  - Troubleshooting guides
  - Fault code databases
  - Historical maintenance records
  - Similar equipment comparisons

### 3. Storage
- Information vectorized and stored
- Indexed for semantic search
- Tagged with equipment metadata
- Available for instant retrieval

### 4. Delivery
- Technician asks question (voice or text)
- Layer 0 searches knowledge base
- Relevant sections returned instantly
- No LLM required for known information

### 5. Learning
- New information captured from interactions
- Gaps in knowledge base identified
- Research orchestrator fills gaps
- System gets smarter automatically

---

## Read-Only Constraint

### The Stethoscope Philosophy

FactoryLM is a **diagnostic tool**, not a control system.

```
┌────────────────────────────────────────────────────────┐
│                                                        │
│     FactoryLM CAN:           FactoryLM CANNOT:        │
│     ✓ Read tag values        ✗ Write to PLCs          │
│     ✓ Monitor I/O states     ✗ Change setpoints       │
│     ✓ Record fault codes     ✗ Start/stop equipment   │
│     ✓ Analyze trends         ✗ Modify programs        │
│     ✓ Suggest actions        ✗ Execute actions        │
│                                                        │
└────────────────────────────────────────────────────────┘
```

### Why Read-Only Matters

1. **Eliminates fear**: "What if it shuts down my line?" → Not possible
2. **IT approval**: No cybersecurity attack surface for control
3. **Insurance/liability**: Worst case is bad advice that human ignores
4. **Trust building**: Prove value before asking for control access

### Future Exception: Explicit Opt-In

If a customer EXPLICITLY wants write capability:
- Separate product tier
- Additional security layers
- Human-in-the-loop approval for all writes
- Full audit logging
- NOT the default, NOT the goal

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-02-03 | Initial canonical document |

---

## Appendix: Key Quotes from Mike

> "The first layer of intelligence is just regular computer logic. We build logic gates based on all the manuals that have ever been created."

> "Once we build the workflows, that's your first line of intelligence. It's code, it's fast. There's no thinking for common stuff."

> "Push intelligence out to the edge and back it up with larger models as you go out."

> "Depending on if the customer is committed to their air gap or not, we still deliver excellent results."

> "This has been stated 7 trillion times throughout my GitHub repo."

---

## Files That Must Reference This Document

When this document is approved, it will be added to:

- [ ] `/FACTORYLM_V1_ARCHITECTURE.md` (root of every repo)
- [ ] Every `CLAUDE.md` file (AI agent instructions)
- [ ] Every `AGENTS.md` file (agent guidelines)
- [ ] Every `.github/copilot-instructions.md`
- [ ] GitHub release tag: `architecture-v1.0`

---

**This is the source of truth. There is no other.**
