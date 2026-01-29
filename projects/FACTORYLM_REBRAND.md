# FactoryLM Rebrand & Migration

## Overview
Consolidating all industrial AI products under the **FactoryLM** brand using a Digital Twin architecture.

> **Digital Twin Philosophy:** What we build internally = What customers get

## Repository
- **GitHub:** https://github.com/Mikecranesync/factorylm
- **Created:** 2026-01-29

## Migration Phases

| Phase | Description | GitHub Issue | Status |
|-------|-------------|--------------|--------|
| 1 | Foundation Setup | [#1](https://github.com/Mikecranesync/factorylm/issues/1) | 🚧 In Progress |
| 2 | PLC Copilot Migration | [#2](https://github.com/Mikecranesync/factorylm/issues/2) | ⏳ Pending |
| 3 | CMMS (Atlas) Migration | [#3](https://github.com/Mikecranesync/factorylm/issues/3) | ⏳ Pending |
| 4 | AI Assistant Framework | [#4](https://github.com/Mikecranesync/factorylm/issues/4) | ⏳ Pending |
| 5 | Knowledge Base | [#5](https://github.com/Mikecranesync/factorylm/issues/5) | ⏳ Pending |
| 6 | Integration & Launch | [#6](https://github.com/Mikecranesync/factorylm/issues/6) | ⏳ Pending |

## Source Components

| Component | Current Location | Target Location |
|-----------|-----------------|-----------------|
| PLC Copilot | `/opt/plc-copilot/`, Rivet-PRO | `factorylm/services/plc-copilot/` |
| CMMS | `/root/jarvis-workspace/projects/cmms/` | `factorylm/apps/cmms/` |
| AI Assistant | Clawdbot/Jarvis config | `factorylm/services/assistant/` |
| Second Brain | `/root/jarvis-workspace/second-brain/` | `factorylm/apps/portal/` |
| Core Infra | Various | `factorylm/packages/` |

## Architecture

```
factorylm/
├── apps/                    # User-facing applications
│   ├── cmms/               # CMMS (Atlas → FactoryLM)
│   ├── portal/             # Second Brain / Knowledge Base
│   └── dashboard/          # Unified dashboard
├── services/               # Backend services
│   ├── plc-copilot/        # Photo analysis → work orders
│   ├── assistant/          # AI assistant engine
│   └── api/                # Shared API gateway
├── packages/               # Shared libraries
│   ├── auth/               # Authentication
│   ├── db/                 # Database schemas
│   └── ui/                 # Shared UI components
└── infra/                  # Infrastructure as code
    ├── docker/
    └── k8s/
```

## Timeline
- **Weeks 1-2:** Foundation + PLC Copilot
- **Weeks 3-4:** CMMS migration
- **Weeks 5-6:** AI Assistant framework
- **Week 7:** Knowledge Base
- **Week 8:** Integration & Launch

## Trello
- **Card:** To be created (need API token)
- **Label:** FactoryLM

## Notes
- This is a unification effort, not a rewrite
- Existing functionality must be preserved
- Customer-facing from day one (digital twin = our internal tools become the product)

---
*Created: 2026-01-29*
*Owner: @jarvis*
