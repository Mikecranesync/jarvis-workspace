# 📊 OBSERVABILITY PLAN

## Two-Layer Observability Stack

### Layer 1: Infrastructure (Grafana + Prometheus)
- Server health, resources, containers
- Already running ✅

### Layer 2: AI/LLM (LangFuse)
- Traces, chains, token usage, learning
- Already running ✅

---

## 5 Dashboards to Build

### Dashboard 1: System Health
- CPU, RAM, Disk per service
- Container status (Running/Stopped/Failed)
- Network I/O
- Restart count (crash loops)
- Response time (API latency)
- Alerts (disk >90%, services down)

### Dashboard 2: AI Activity
- Interactions by stream (dev vs user)
- Teaching moments detected
- Lessons stored (growth rate)
- Token usage + cost
- Active synthetic users
- KB growth (total lessons, domains)

### Dashboard 3: Learning Insights
- Top teaching moments
- Lesson confidence distribution
- Impact of lessons (before/after)
- Proposed chains (automation opportunities)
- Synthetic user performance

### Dashboard 4: Two-Stream Comparison
- Volume: dev vs user
- Quality: teaching rate, confidence
- Cost: budget allocation
- Cross-pollination: shared learnings

### Dashboard 5: Production Readiness
- Component readiness scores
- Blockers to production
- Progress to 100M token corpus
- ETA to milestones

---

## Data Sources

| Dashboard | Source |
|-----------|--------|
| System Health | Prometheus + Docker metrics |
| AI Activity | LangFuse API |
| Learning Insights | LangFuse + ChromaDB |
| Two-Stream | LangFuse (tagged streams) |
| Production Readiness | Custom metrics endpoint |

---

*Created: 2026-02-02*
