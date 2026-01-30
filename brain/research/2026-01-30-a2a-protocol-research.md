# A2A Protocol Research

*Date: 2026-01-30*
*GitHub Issue: #13*
*Trello: https://trello.com/c/RQmmLKkf*

---

## Executive Summary

**A2A (Agent-to-Agent Protocol)** is Google's open standard for enabling AI agents to communicate and collaborate across different platforms and frameworks. It's the emerging standard for inter-agent communication, designed to complement MCP (Model Context Protocol) which handles tool access.

**Key Insight:** MCP is for tools, A2A is for agents.

---

## What A2A Solves

The problem: Multiple agents built by different teams, using different tech, with opaque inner workings—how do they collaborate?

Current state: "They don't" or "with custom, brittle integration code."

A2A provides: A common language for agents to interact without revealing internal secrets.

---

## Core Principles

| Tenet | Description |
|-------|-------------|
| **Simple** | Built on HTTP, SSE, JSON-RPC — existing standards |
| **Enterprise Ready** | Authentication, security, privacy, tracing, monitoring |
| **Async First** | Long-running tasks, human-in-the-loop workflows |
| **Modality Agnostic** | Text, audio/video, forms, iframes |
| **Opaque Execution** | Agents don't reveal internals — black-box collaboration |

---

## How It Works

### 1. Agent Card
Every agent publishes a JSON "business card":
```json
{
  "name": "StockInfoAgent",
  "description": "Provides current stock price information.",
  "url": "http://stock-info.example.com/a2a",
  "provider": { "organization": "ABCorp" },
  "version": "1.0.0",
  "skills": [
    {
      "id": "get_stock_price_skill",
      "name": "Get Stock Price",
      "description": "Retrieves current stock price for a company"
    }
  ]
}
```

### 2. Discovery
Client fetches Agent Card from well-known URL (`/.well-known/agent.json`)

### 3. Task Lifecycle
- **Initiation** — Client sends message with unique Task ID
- **Processing** — Agent works on task (may take minutes/hours/days)
- **Updates** — Real-time feedback via SSE
- **Completion** — Terminal state (completed/failed/canceled)

### 4. Message Exchange
Agents communicate via structured messages with "parts" that can be:
- Text
- Structured data
- Files/artifacts
- UI components

---

## A2A vs MCP

| | MCP | A2A |
|---|-----|-----|
| **Purpose** | Connect LLMs to tools | Connect agents to agents |
| **Scope** | Structured inputs/outputs | Autonomous collaboration |
| **Analogy** | Mechanic's tools | Mechanics talking to each other |
| **Use Case** | Agent → Database/API | Agent → Agent delegation |

**Both are needed.** MCP for tools, A2A for coordination.

---

## Relevance to Jarvis Architecture

### Current State
Our MULTI_AGENT_ARCHITECTURE.md defines:
- Orchestrator (main Jarvis)
- Specialized agents (Monitor, Code, Agile, etc.)
- Communication via workspace files and Telegram

### A2A Opportunity
1. **Formalize agent interfaces** — Agent Cards for each Jarvis agent
2. **Enable external collaboration** — Connect to other A2A-compatible agents
3. **Standardize handoffs** — Task lifecycle instead of ad-hoc NEXT_STEPS.md

### Implementation Path
```
Phase 1: Document agents as Agent Cards (local)
Phase 2: Implement A2A endpoint on main Jarvis
Phase 3: Enable external A2A connections (future)
```

---

## Key Partners Using A2A

- Atlassian, Box, Cohere
- Intuit, Langchain, MongoDB
- PayPal, Salesforce, SAP
- ServiceNow, UKG, Workday

**50+ technology partners** — this is becoming a standard.

---

## Recommended Actions

1. **Create Agent Cards** for our existing agents
2. **Implement handoff protocol** using A2A task lifecycle pattern
3. **Keep watching** — A2A is young but growing fast

---

## Sources

- https://a2aprotocol.ai/
- https://google.github.io/A2A/
- https://www.oreilly.com/radar/designing-collaborative-multi-agent-systems-with-the-a2a-protocol/
- https://github.com/a2aproject/A2A

---

*Research completed per Amendment I (Open Source First) and Article III (Proactive Agency)*
