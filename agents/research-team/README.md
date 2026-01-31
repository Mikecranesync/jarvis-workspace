# Research Agent Team

**Created:** 2026-01-31
**Purpose:** Monitor GitHub repos, YouTube, and tech news for updates

---

## Agents

### 1. GitHub Watcher Agent
**Schedule:** Daily at 3 PM UTC (peak dev activity)
**Monitors:**
- Key repos for updates, releases, issues
- Forks and new interesting projects
- AI/ML framework releases

### 2. YouTube Tech Agent
**Schedule:** Daily at 5 PM UTC (after content releases)
**Monitors:**
- AI Engineer Conference channel
- Industrial automation channels
- Trending tech videos

### 3. Tech News Agent
**Schedule:** Daily at 2 PM UTC
**Monitors:**
- Hacker News top stories
- AI-related news
- Industrial IoT news

---

## Watched Repositories

### Priority 1: Core Infrastructure
| Repo | Why We Watch |
|------|--------------|
| `clawdbot/clawdbot` | Our core platform |
| `Mikecranesync/clawdbot` | Our fork |
| `cloudflare/moltworker` | Workers deployment |
| `VoltAgent/awesome-openclaw-skills` | Skills collection |

### Priority 2: AI/LLM Tools
| Repo | Why We Watch |
|------|--------------|
| `anthropics/anthropic-cookbook` | Claude best practices |
| `openai/openai-cookbook` | GPT patterns |
| `langchain-ai/langchain` | LLM orchestration |
| `run-llama/llama_index` | RAG patterns |

### Priority 3: Industrial/IoT
| Repo | Why We Watch |
|------|--------------|
| `home-assistant/core` | IoT patterns |
| `eclipse/mosquitto` | MQTT broker |
| `FreeOpcUa/python-opcua` | OPC UA library |
| `riptideio/pymodbus` | Modbus library |

---

## YouTube Channels

### AI/Tech
- AI Engineer Conference
- Two Minute Papers
- Yannic Kilcher
- Andrej Karpathy

### Industrial
- RealPars
- Automation Direct
- PLC Professor

---

## Output

Daily digest sent to Mike via Telegram at 6 PM UTC:
- New releases from watched repos
- Interesting new repos
- Trending AI videos
- Tech news highlights

Files saved to: `brain/research/daily-digest/`

---

## Implementation

Cron jobs in Clawdbot trigger these agents. Each agent:
1. Runs its search/check
2. Saves findings to markdown
3. Sends summary to Telegram (if noteworthy)
