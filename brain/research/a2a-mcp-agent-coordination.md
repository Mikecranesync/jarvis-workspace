# A2A & MCP: Agent Coordination Frameworks Research

**Status:** COMPLETE
**Created:** 2026-01-30
**Agent:** Jarvis (for self-improvement)
**Trello Card:** 697b6d267ce303a2e6807f9e

---

## Executive Summary

Two major protocols are emerging for AI agent coordination in 2025-2026:

| Protocol | Creator | Purpose | Released |
|----------|---------|---------|----------|
| **A2A (Agent2Agent)** | Google | Agent-to-Agent communication | April 2025 |
| **MCP (Model Context Protocol)** | Anthropic | Agent-to-Tools/Data connection | November 2024 |

**Key insight:** These are **complementary, not competing**:
- **MCP is vertical** — connects agents to tools and data sources
- **A2A is horizontal** — connects agents to other agents

---

## A2A Protocol (Google)

### What It Is

A2A (Agent2Agent) is an open communication protocol that enables AI agents to:
- Communicate with each other regardless of framework
- Securely exchange information
- Coordinate actions across platforms
- Delegate sub-tasks to specialized agents

### Key Features

1. **Interoperability**
   - Agents built in Python can talk to agents in JavaScript
   - Works across Google, OpenAI, Anthropic, etc.
   - Vendor-agnostic design

2. **Security**
   - Uses HTTPS and OAuth/API keys
   - Designed for enterprise environments
   - Authentication between agents

3. **Task Delegation**
   - Master agent can assign sub-tasks
   - Results flow back through protocol
   - Supports complex multi-agent workflows

### Architecture

```
┌─────────────┐     A2A Protocol     ┌─────────────┐
│   Agent A   │◄──────────────────►│   Agent B   │
│  (Planner)  │                     │ (Executor)  │
└─────────────┘                     └─────────────┘
       │                                   │
       │ A2A                               │ A2A
       ▼                                   ▼
┌─────────────┐                     ┌─────────────┐
│   Agent C   │                     │   Agent D   │
│ (Researcher)│                     │  (Writer)   │
└─────────────┘                     └─────────────┘
```

### Implementation

Google provides:
- **A2A SDKs** for Python, JavaScript, etc.
- **Agent Development Kit (ADK)** with native A2A support (July 2025)
- Open-source specification at a2a-protocol.org

### Partners (50+ at launch)
- Salesforce
- SAP
- ServiceNow
- Workday
- MongoDB
- Box

---

## MCP Protocol (Anthropic)

### What It Is

MCP (Model Context Protocol) is an open standard for connecting AI models to:
- External data sources
- Business tools
- Development environments
- APIs and databases

### Key Features

1. **Tool Integration**
   - Standard interface for any tool
   - Model-agnostic design
   - Plug-and-play architecture

2. **Context Management**
   - Pass relevant context to models
   - Retrieve data from external sources
   - Maintain state across interactions

3. **Open Source**
   - Fully open specification
   - Community-driven development
   - Broad adoption

### Architecture

```
┌─────────────────────────────────────────┐
│               AI Agent                   │
│         (Claude, GPT, etc.)             │
└─────────────┬───────────────────────────┘
              │ MCP
              ▼
┌─────────────────────────────────────────┐
│           MCP Server                     │
└─────┬─────────┬─────────┬───────────────┘
      │         │         │
      ▼         ▼         ▼
┌─────────┐ ┌─────────┐ ┌─────────┐
│Database │ │  API    │ │  File   │
│(Postgres)│ │(Trello) │ │(System) │
└─────────┘ └─────────┘ └─────────┘
```

### Implementation

- MCP servers can be written in any language
- SDKs available for Python, TypeScript
- Specification at modelcontextprotocol.io

---

## A2A vs MCP Comparison

| Aspect | A2A | MCP |
|--------|-----|-----|
| **Purpose** | Agent ↔ Agent | Agent ↔ Tools/Data |
| **Communication** | Horizontal | Vertical |
| **Primary use** | Multi-agent orchestration | Tool integration |
| **Security model** | OAuth, API keys, HTTPS | Server authentication |
| **Best for** | Complex workflows with specialized agents | Single agent with many tools |

### When to Use Each

**Use A2A when:**
- Multiple agents need to collaborate
- Delegating tasks to specialized agents
- Cross-vendor agent communication
- Enterprise multi-agent systems

**Use MCP when:**
- Connecting an agent to databases
- Integrating with APIs (Trello, GitHub, etc.)
- Accessing file systems
- Building tool-augmented agents

**Use Both when:**
- Building production multi-agent systems
- Agents need both tool access AND coordination
- Enterprise-scale AI deployments

---

## Relevance to Jarvis/Clawdbot

### Current Architecture

```
┌─────────────────────────────────────────┐
│              Clawdbot                    │
│         (Main Jarvis Agent)             │
└─────────────┬───────────────────────────┘
              │ Internal
              ▼
┌─────────────────────────────────────────┐
│           Tools (Built-in)               │
│  exec, browser, message, trello, etc.   │
└─────────────────────────────────────────┘
```

### Potential A2A Integration

```
┌─────────────────────────────────────────┐
│         Jarvis (Orchestrator)            │
│              Clawdbot                    │
└──────┬────────────┬────────────┬────────┘
       │ A2A        │ A2A        │ A2A
       ▼            ▼            ▼
┌──────────┐  ┌──────────┐  ┌──────────┐
│ Content  │  │ Outreach │  │  Code    │
│  Agent   │  │  Agent   │  │  Agent   │
└──────────┘  └──────────┘  └──────────┘
```

### Benefits for Our System

1. **Specialized Agents**
   - Content Agent: Writes LinkedIn posts, blogs
   - Outreach Agent: Manages email campaigns
   - Code Agent: Handles development tasks
   - Research Agent: Web research and analysis

2. **Parallel Execution**
   - Multiple agents work simultaneously
   - Jarvis orchestrates and aggregates

3. **Scalability**
   - Add new specialized agents easily
   - Each agent can be optimized for its task

4. **Resilience**
   - If one agent fails, others continue
   - Better error isolation

---

## Implementation Recommendations

### Short-Term (Now)

Current Clawdbot cron-based agent system works well. Continue using:
- Trello for task tracking
- Cron jobs for agent triggers
- Single Claude instance with context switching

### Medium-Term (3-6 months)

1. **Add MCP servers** for:
   - Trello (replace direct API calls)
   - GitHub (standardize git operations)
   - Email (MailerLite, SMTP)

2. **Experiment with sub-agents** using Clawdbot's spawn feature:
   - Spawn specialized sessions for specific tasks
   - Return results to main session

### Long-Term (6-12 months)

1. **Full A2A implementation** when:
   - Running multiple persistent agents
   - Need cross-model communication (Claude + GPT)
   - Enterprise deployment requirements

2. **Consider frameworks**:
   - Google ADK for A2A-native development
   - LangGraph for complex agent workflows
   - AutoGen for multi-agent systems

---

## Resources

### A2A
- Spec: https://a2a-protocol.org/latest/
- Google Blog: https://developers.googleblog.com/en/a2a-a-new-era-of-agent-interoperability/
- ADK Docs: https://cloud.google.com/agent-development-kit

### MCP
- Spec: https://modelcontextprotocol.io/specification/
- Anthropic Announcement: https://www.anthropic.com/news/model-context-protocol
- GitHub: https://github.com/anthropics/mcp

---

## Conclusion

For Jarvis/FactoryLM's current stage:
- **MCP is more immediately relevant** — we need better tool integration
- **A2A is future-ready** — when we scale to true multi-agent systems

Recommendation: Start with MCP servers for Trello and GitHub, experiment with Clawdbot's spawn for parallel agents, then evaluate A2A as complexity grows.

---

**Ready for Implementation Planning**
