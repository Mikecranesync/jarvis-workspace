# 🏗️ CODEBASE DIGITAL TWIN
## FactoryLM / Master of Puppets / Rivet-PRO

*Generated: 2026-02-02*

---

## The Problem

We have **2,767 Python files** scattered across multiple locations:
- Code copied, not imported
- Same files in 3+ places
- No single source of truth
- Unclear what's production vs experimental

---

## Current State: The Spaghetti Map

```
┌─────────────────────────────────────────────────────────────────────┐
│                        PRODUCTION (Running Now)                      │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  /opt/master_of_puppets/          /opt/plc-copilot/                 │
│  ├── celery_app.py                ├── photo_to_cmms_bot.py          │
│  ├── workers/ (22 agents)         ├── user_db.py                    │
│  │   ├── monkey_tasks.py          └── cmms_bot.py                   │
│  │   ├── evolution_tasks.py                                         │
│  │   ├── keymaster_tasks.py       DOCKER CONTAINERS                 │
│  │   ├── synthetic_user_tasks.py  ├── cmms-backend                  │
│  │   ├── content_capture_tasks.py ├── cmms-frontend                 │
│  │   └── ...18 more               ├── n8n                           │
│  └── .env                         ├── flowise                       │
│                                   ├── grafana                       │
│  systemd services:                ├── influxdb                      │
│  - master-of-puppets.service      ├── mautic                        │
│  - master-of-puppets-beat.service └── postgres/redis                │
│  - plc-copilot.service                                              │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│                    SOURCE REPOS (The Mess)                           │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  /root/jarvis-workspace/projects/Rivet-PRO/  (502 .py files)        │
│  ├── rivet_pro/core/           # Original app code                  │
│  ├── agents/                   # LangChain agents                   │
│  ├── integrations/             # CMMS, Twilio, etc                  │
│  ├── harvest_blocks/           # KB extraction                      │
│  ├── tests/                    # Unit tests                         │
│  ├── deploy/                   # Deployment configs                 │
│  └── ycb/                      # YouTube content                    │
│                                                                      │
│  /root/jarvis-workspace/factorylm-dev/  (34 .py files)              │
│  ├── services/plc-modbus/      # PLC communication                  │
│  ├── services/maintenance-llm/ # LLM service                        │
│  └── common/                   # Shared utilities                   │
│                                                                      │
│  /root/jarvis-workspace/rivet-pro/  (DUPLICATE of above)            │
│  /root/jarvis-workspace/rivet-pro-search/  (ANOTHER DUPLICATE)      │
│  /root/jarvis-workspace/sandbox/  (MORE DUPLICATES)                 │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Consolidation Target: The Monolith

```
/opt/factorylm/                    # SINGLE SOURCE OF TRUTH
├── factorylm/                     # Python package
│   ├── __init__.py
│   ├── core/                      # Core business logic
│   │   ├── llm/                   # LLM interfaces
│   │   ├── plc/                   # PLC communication
│   │   └── cmms/                  # CMMS integration
│   │
│   ├── agents/                    # Celery workers (from master_of_puppets)
│   │   ├── monkey.py
│   │   ├── evolution.py
│   │   ├── keymaster.py
│   │   └── ...
│   │
│   ├── bots/                      # Telegram/chat interfaces
│   │   ├── photo_bot.py
│   │   └── cmms_bot.py
│   │
│   ├── api/                       # REST/GraphQL endpoints
│   │   ├── fastapi_app.py
│   │   └── routes/
│   │
│   └── utils/                     # Shared utilities
│       ├── logging.py
│       ├── config.py
│       └── tokens.py
│
├── tests/                         # All tests
├── scripts/                       # CLI tools
├── deploy/                        # Docker, systemd, k8s
├── docs/                          # Documentation
│
├── pyproject.toml                 # Single dependency file
├── .env.example
└── README.md
```

---

## Migration Plan

### Phase 1: Inventory & Dedup (Week 1)
- [ ] Map all 2,767 files to their function
- [ ] Identify true duplicates vs forks
- [ ] Create dependency graph
- [ ] Decide what's production vs trash

### Phase 2: Create Monolith Skeleton (Week 2)
- [ ] Create `/opt/factorylm/` structure
- [ ] Set up pyproject.toml with all deps
- [ ] Create base classes and interfaces
- [ ] Set up proper logging/config

### Phase 3: Migrate Workers (Week 3)
- [ ] Move master_of_puppets workers
- [ ] Keep Celery, consolidate tasks
- [ ] Single .env file
- [ ] Update systemd services

### Phase 4: Migrate Bots & APIs (Week 4)
- [ ] Consolidate Telegram bots
- [ ] Merge API endpoints
- [ ] Single FastAPI app

### Phase 5: Clean Up (Week 5)
- [ ] Delete duplicate directories
- [ ] Archive old code
- [ ] Update all imports
- [ ] Full test suite

---

## Key Decisions Needed

1. **Package name:** `factorylm` or `rivet` or `master_of_puppets`?
2. **Keep Celery or switch to:** Celery, Dramatiq, or plain async?
3. **API framework:** FastAPI (current) or keep multiple?
4. **Database:** Postgres only, or keep InfluxDB for time-series?
5. **Deployment:** Docker Compose, K8s, or bare metal?

---

## Duplicates to Kill

| Location | Files | Action |
|----------|-------|--------|
| `/root/jarvis-workspace/rivet-pro/` | 502 | DELETE (copy of Rivet-PRO) |
| `/root/jarvis-workspace/rivet-pro-search/` | 502 | DELETE (another copy) |
| `/root/jarvis-workspace/sandbox/` | ~500 | ARCHIVE then delete |
| `/root/jarvis-workspace/clawdbot-search/` | misc | Keep (Clawdbot dev) |

**Potential disk recovery:** ~2GB

---

## The Goal

From this:
```
2,767 files across 10+ directories
├── No tests run
├── No CI/CD
├── Copy-paste inheritance
└── "It works on my machine"
```

To this:
```
factorylm/
├── 100% test coverage on core
├── GitHub Actions CI/CD
├── pip install factorylm
├── Single docker-compose up
└── "It works everywhere"
```

---

## Next Action

Run the Cartographer agent to build the full dependency graph:
```bash
celery -A celery_app call cartographer.map_codebase
```

Then we sculpt.
