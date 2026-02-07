# Multi-Agent Fleet Sync Research

**Date:** 2026-02-07  
**Purpose:** Find experts and repos for distributed AI agent state synchronization  
**Relevance:** FactoryLM edge architecture + Clawdbot mesh network

---

## 🎯 The 5 Key Players

### 1. João Moura - CrewAI
- **Role:** Founder & CEO of CrewAI
- **GitHub:** https://github.com/joaomdmoura
- **Repo:** https://github.com/crewAIInc/crewAI (40k+ stars)
- **Stats:** 1.4 Billion agentic automations, 60% of Fortune 500, 100k+ certified devs
- **Key Features:**
  - CrewAI Flows: Event-driven control with state management
  - Production-grade enterprise architecture
  - Crew Control Plane: Centralized monitoring & management
  - On-premise AND cloud deployment options ⭐

**Why This Matters for FactoryLM:**
- Already has enterprise fleet management concepts
- Centralized control plane = Factory Operations Center
- On-premise option = air-gapped friendly

---

### 2. Harrison Chase - LangGraph
- **Role:** CEO of LangChain
- **GitHub:** https://github.com/langchain-ai
- **Repo:** https://github.com/langchain-ai/langgraph
- **Key Features:**
  - **Durable execution** - survives failures, resumes exactly where left off
  - **Persistence layer** - built-in state management
  - **Checkpoints** - save/restore agent state
  - Used by: Klarna, Replit, Elastic

**Quote from Harrison (Sequoia interview):**
> "We've paid a ton of attention to the persistence layer that backs it."

**Why This Matters for FactoryLM:**
- Persistence = state sync foundation
- Checkpoints = snapshots that can be synced across nodes
- Battle-tested at scale

---

### 3. Chi Wang - AutoGen / AG2
- **Role:** Microsoft Research → AG2 (spin-off)
- **GitHub:** https://github.com/microsoft/autogen
- **Repo:** https://github.com/ag2ai/ag2 (community fork)
- **Paper:** "AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation"
- **Key Features:**
  - State-driven workflow approach
  - GrpcWorkerAgentRuntime for **distributed agents** ⭐
  - DockerCommandLineCodeExecutor for sandboxed execution

**Why This Matters for FactoryLM:**
- Microsoft-backed research = enterprise credibility
- gRPC distributed runtime = native distributed architecture
- Docker executor = safe edge execution

---

### 4. Kye Gomez - Swarms
- **Role:** Founder, Swarms Corp
- **GitHub:** https://github.com/kyegomez
- **Repo:** https://github.com/kyegomez/swarms
- **Website:** https://swarms.ai
- **Key Features:**
  - **Enterprise-Grade Production-Ready**
  - Agent Orchestration Protocol (AOP) for distributed deployment
  - Agent Registry Management
  - Backwards compatible with LangChain, AutoGen, CrewAI
  - Marketplace for sharing agents/prompts

**AOP (Agent Orchestration Protocol):**
> "Framework for deploying and managing agents as distributed services. Enables agent discovery, management, and execution through standardized protocols."

**Why This Matters for FactoryLM:**
- AOP = exactly what we need for fleet sync
- Agent Registry = centralized catalog of all edge nodes
- Already enterprise-ready, not experimental

---

### 5. OpenAI - Swarm (Educational)
- **Repo:** https://github.com/openai/swarm
- **Status:** Educational/experimental, not production
- **Key Insight:** Lightweight handoffs between agents

**Why This Matters:**
- Good for understanding concepts
- NOT for production use

---

## 📊 Comparison Matrix

| Feature | CrewAI | LangGraph | AutoGen | Swarms |
|---------|--------|-----------|---------|--------|
| **Stars** | 40k+ | 15k+ | 40k+ | 25k+ |
| **Production Ready** | ✅ | ✅ | ✅ | ✅ |
| **State Persistence** | ✅ Flows | ✅ Native | ✅ | ✅ |
| **Distributed Agents** | ⚠️ Via Control Plane | ⚠️ Via LangSmith | ✅ gRPC | ✅ AOP |
| **Edge Deployment** | ✅ On-prem | ❌ Cloud-focused | ⚠️ Docker | ✅ Native |
| **Air-Gap Friendly** | ✅ | ❌ | ⚠️ | ✅ |
| **Fleet Management** | ✅ Control Plane | ❌ | ❌ | ✅ Registry |
| **Backwards Compat** | ❌ | ❌ | ❌ | ✅ All frameworks |

---

## 🏆 Recommendation for FactoryLM

### Primary: Swarms (kyegomez/swarms)
**Why:**
1. Already has Agent Orchestration Protocol (AOP) for distributed deployment
2. Agent Registry = fleet management built-in
3. Enterprise-grade from day one
4. Backwards compatible with everything else
5. Edge-deployment friendly

### Secondary: LangGraph for Persistence
**Why:**
1. Best-in-class state persistence
2. Checkpoint/restore = snapshot sync between nodes
3. Durable execution = survives failures

### Hybrid Approach:
```
FactoryLM Edge Node
├── Swarms (agent orchestration)
│   └── AOP (inter-node communication)
├── LangGraph (state persistence)
│   └── Checkpoints (syncable state)
└── Syncthing/Git (file-level sync)
    └── Rules, knowledge, procedures
```

---

## 🔧 Implementation Plan

### Phase 1: Proof of Concept (This Week)
1. Fork `kyegomez/swarms`
2. Set up 3-node test (VPS + 2 laptops)
3. Test AOP for inter-agent messaging
4. Verify state sync works

### Phase 2: State Sync Layer
1. Implement checkpoint sync via git
2. Add Syncthing for real-time file sync
3. Test conflict resolution

### Phase 3: FactoryLM Integration
1. Wrap in FactoryLM Layer architecture
2. Layer 0 rules sync automatically
3. Layer 1 knowledge syncs on demand
4. Layer 3 (cloud) answers harden to all nodes

### Phase 4: Fire Drills
1. Kill VPS - verify laptops continue
2. Kill network - verify air-gap operation
3. Restore from checkpoint
4. Full fleet recovery

---

## 🔥 Fire Department Setup

### Recovery Hierarchy:
1. **Primary:** VPS Jarvis
2. **Backup 1:** Travel Laptop Jarvis
3. **Backup 2:** PLC Laptop Jarvis

### Automatic Failover:
- Each node monitors others via Tailscale
- If primary dies, backups alert Mike
- State checkpoints sync every 5 minutes
- Any node can restore from last checkpoint

### Manual Recovery:
- SSH to any node
- `git pull` to get latest state
- Restart agent

---

## 📚 Repos to Fork

1. **Primary:** `https://github.com/kyegomez/swarms`
   - For: Agent orchestration, AOP, fleet management

2. **Persistence:** `https://github.com/langchain-ai/langgraph`
   - For: State checkpoints, durable execution

3. **Reference:** `https://github.com/crewAIInc/crewAI`
   - For: Crew Control Plane concepts

4. **Reference:** `https://github.com/ag2ai/ag2`
   - For: gRPC distributed runtime patterns

---

## 🎬 Next Steps

1. [ ] Fork kyegomez/swarms
2. [ ] Read AOP documentation in depth
3. [ ] Create FactoryLM-specific agent definitions
4. [ ] Set up sync layer between 3 Clawdbot instances
5. [ ] Test failover scenarios
6. [ ] Document recovery procedures

---

*This is exactly what Mike described: a mesh of independent agents that can sync state and survive failures.*
