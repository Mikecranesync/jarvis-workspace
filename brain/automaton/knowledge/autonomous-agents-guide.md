# Autonomous Agents Knowledge Base

**Source:** Anthropic Official Documentation + Research
**Added:** 2026-01-31
**Purpose:** Make the Automaton more autonomous

---

## Core Principle: Give Claude a Computer

The key design principle is that Claude needs the same tools humans use:
- Find files in a codebase
- Write and edit files
- Run commands
- Debug and iterate
- Access to terminal/bash

By giving Claude access to a computer (via terminal), it can do all sorts of digital work.

---

## The Agentic Loop

Agents operate in a specific feedback loop:

```
GATHER CONTEXT → TAKE ACTION → VERIFY WORK → REPEAT
```

This is how we should think about every task.

---

## Types of Agentic Systems

### 1. Workflows (Predefined Paths)
- **Prompt Chaining:** Task → Subtask 1 → Subtask 2 → Result
- **Routing:** Classify input → Route to specialized handler
- **Parallelization:** Run subtasks simultaneously
- **Orchestrator-Workers:** Central LLM delegates to worker LLMs

### 2. Agents (Dynamic Paths)
- LLM dynamically directs its own processes
- Maintains control over how it accomplishes tasks
- Uses tools based on environmental feedback in a loop

---

## When to Use Agents

✅ **Use agents when:**
- Open-ended problems
- Can't predict required steps
- Can't hardcode a fixed path
- Need flexibility and model-driven decisions
- Tasks that scale in trusted environments

❌ **Don't use agents when:**
- Simple prompts are enough
- Task is well-defined with fixed steps
- Latency/cost tradeoffs aren't worth it

---

## Building Blocks for Autonomy

### 1. Gathering Context
- **Agentic Search:** Use bash (grep, tail, find) to search files
- **File System:** Folder structure = context engineering
- **Subagents:** Spin off parallel searches, return only relevant info
- **Compaction:** Auto-summarize when context limit approaches

### 2. Taking Action
- **Tools:** Primary actions Claude will consider
- **Bash & Scripts:** Flexible work using computer
- **Code Generation:** Precise, composable, reusable
- **MCPs:** Model Context Protocol for external integrations

### 3. Verifying Work
- **Rules:** Clearly defined success criteria, linting
- **Visual Feedback:** Screenshots for UI tasks
- **LLM as Judge:** Another model evaluates output

---

## Best Practices

### Tool Design (ACI - Agent-Computer Interface)
1. Put yourself in the model's shoes
2. Use clear parameter names and descriptions
3. Include example usage and edge cases
4. Test extensively with sample inputs
5. "Poka-yoke" - make it hard to make mistakes
6. Use absolute paths, not relative

### Agent Design Principles
1. **Maintain simplicity** in agent design
2. **Prioritize transparency** - show planning steps
3. **Craft ACI carefully** - tool docs and testing
4. Start simple, add complexity only when needed

### Prompt Engineering Tools
- Give model enough tokens to "think"
- Keep format close to natural text
- No formatting overhead (counting lines, escaping)
- Write great docstrings for each tool

---

## Workflow Patterns

### Prompt Chaining
```
Input → LLM 1 → Gate (check) → LLM 2 → Output
```
Use when: Task decomposes cleanly into fixed subtasks

### Routing
```
Input → Classifier → Route A → Handler A
                  → Route B → Handler B
```
Use when: Distinct categories need separate handling

### Parallelization
```
Input → [LLM 1, LLM 2, LLM 3] → Aggregate → Output
```
Use when: Subtasks can run in parallel

### Orchestrator-Workers
```
Input → Orchestrator → [Worker 1, Worker 2, ...] → Synthesize → Output
```
Use when: Can't predict subtasks needed

### Evaluator-Optimizer
```
Input → Generator → Evaluator → Feedback Loop → Output
```
Use when: Clear evaluation criteria, iterative refinement helps

---

## Applying to Our Automaton

### Current Implementation
- Heartbeat loop ✅
- Cron-based autonomous jobs ✅
- Task queue ✅
- Memory/context in files ✅
- Tool access (exec, browser, etc.) ✅

### Improvements to Make
1. **Better verification loops** - Check our own work more
2. **Subagent parallelization** - Spawn workers for research
3. **Clearer tool documentation** - ACI improvements
4. **Visual feedback** - Screenshot verification where applicable
5. **Compaction strategy** - Auto-summarize long contexts

---

## Key Quotes

> "Success in the LLM space isn't about building the most sophisticated system. It's about building the RIGHT system for your needs."

> "Start with simple prompts, optimize them with evaluation, and add multi-step agentic systems only when simpler solutions fall short."

> "Think about how much effort goes into HCI. Plan to invest just as much in ACI (Agent-Computer Interface)."

> "We spent MORE time optimizing our tools than the overall prompt."

---

*This knowledge should inform all autonomous behavior.*
