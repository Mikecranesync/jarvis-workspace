# FactoryLM Monorepo Consolidation Report
**Generated:** February 5, 2026  
**Scope:** 8 GitHub repositories analyzed for consolidation  
**Focus:** Production-ready code identification for factorylm monorepo  

---

## Executive Summary

After analyzing 8 repositories (747 total Python files, 185,347 total lines), there is a clear opportunity to consolidate valuable production code into the factorylm monorepo. **Agent-Factory** contains the most substantial codebase with mature production systems, while **factorylm** represents the target architecture. Key findings:

- **Agent-Factory**: 636 Python files (172,951 lines) - MASSIVE production system
- **factorylm**: 83 Python files (12,393 lines) - Target monorepo architecture 
- **factorylm-core**: 24 Python files - Core utilities (production-ready)
- Other repos: Minimal Python code or specialized purposes

## Repository Analysis

### 1. Agent-Factory ⭐ **PRIMARY CONSOLIDATION TARGET**
**Size:** 636 Python files, 172,951 lines  
**Status:** Production system with extensive capabilities  
**Quality:** High - mature, tested, documented

#### Key Production-Ready Components:

**Core Infrastructure:**
- `agent_factory/core/` - Orchestrator (1,368 lines), database manager (831 lines)
- `agent_factory/llm/` - LLM routing and adapters (494 lines router)
- `agent_factory/memory/` - Storage and session management (952 lines)
- `agent_factory/observability/` - Monitoring, tracing, cost tracking

**Telegram Integration (HIGHLY VALUABLE):**
- `agent_factory/integrations/telegram/` - Complete bot framework
  - `rivet_pro_handlers.py` (1,391 lines) - Rivet Pro integration
  - `orchestrator_bot.py` (1,233 lines) - Main bot orchestration
  - `telegram_adapter.py` (1,167 lines) - Core adapter
  - `management_handlers.py` (1,022 lines) - Admin functionality
  - OCR pipeline with multiple providers (Claude, Gemini, GPT-4V)
  - Voice transcription and handling

**Services & APIs:**
- `agent_factory/api/` - FastAPI routers for Stripe, work orders, manuals
- `agent_factory/rivet_pro/` - Industrial knowledge platform
  - Database integration (632 lines)
  - Stripe payments (604 lines) 
  - Intent detection and context extraction (544 lines)
  - Research pipeline and forum scraping (381 lines)

**Industrial Tools:**
- `agent_factory/tools/factoryio/` - Factory.io integration
- `agent_factory/field_eye/` - Computer vision for industrial applications
- `agent_factory/intake/equipment_taxonomy.py` - Equipment classification

**Agent Frameworks:**
- `agents/` - 70+ specialized agents for content, research, media
- `agent_factory/workflows/` - Ingestion chains and collaboration patterns

#### Recommended for Import:
1. **Core orchestrator and LLM routing** → `factorylm/core/orchestration/`
2. **Telegram integration framework** → `factorylm/services/telegram/`
3. **Observability and monitoring** → `factorylm/core/observability/`
4. **Industrial tools (Factory.io, equipment)** → `factorylm/services/industrial/`
5. **Agent workflow system** → `factorylm/core/agents/`

#### Archive (Experimental):
- `phoenix_integration/` - Evaluation framework (can be reimplemented)
- `examples/` - Demo code (keep for reference)
- Many test files (migrate only core framework tests)

### 2. factorylm ⭐ **TARGET MONOREPO**
**Size:** 83 Python files, 12,393 lines  
**Status:** Well-structured monorepo foundation  
**Quality:** High - follows modern patterns

#### Current Structure (KEEP):
```
core/src/factorylm/
├── llm/           # LLM clients (Claude, Groq, DeepSeek)
├── utils/         # Validators, logger
└── config.py      # Configuration management

services/
├── plc-copilot/   # PLC photo → CMMS bot (940 lines)
└── plc-modbus/    # Modbus/Factory.io integration

plc-client/        # PLC communication library
scripts/           # Deployment and diagnostic tools
```

#### Integration Points:
- Existing LLM framework can absorb Agent-Factory's router
- PLC integrations align with industrial focus
- Service architecture ready for Telegram bot import

### 3. factorylm-core ✅ **MERGE IMMEDIATELY**
**Size:** 24 Python files  
**Status:** Production-ready core utilities  
**Quality:** High - clean, focused

#### Contents:
- Core abstractions and interfaces
- Utility functions
- Base classes for LLM integration

#### Recommendation: 
**IMPORT ALL** → `factorylm/core/` (non-conflicting merge)

### 4. pi-gateway ✅ **SPECIALIZED COMPONENT**
**Size:** 3 Python files  
**Status:** Edge device gateway  
**Quality:** Production-ready

#### Recommendation:
**IMPORT** → `factorylm/services/edge/pi-gateway/`

### 5. Other Repositories

#### mikes-brain (3 Python files)
- Documentation and knowledge management
- **ARCHIVE** - Templates and docs only, minimal code

#### factorylm-mini (0 Python files)
- Firmware for edge devices  
- **SEPARATE** - Keep as standalone firmware repo

#### ralph (0 Python files)  
- Shell tooling for development
- **SEPARATE** - Keep as development tool

#### IndustrialSkillsHub (1 Python file)
- Next.js frontend application
- **SEPARATE** - Frontend should remain independent

---

## Recommended Consolidation Plan

### Phase 1: Foundation (Week 1)
1. **Merge factorylm-core** → `factorylm/core/`
2. **Import pi-gateway** → `factorylm/services/edge/`
3. **Set up import directory structure**

### Phase 2: Core Systems (Week 2-3)
1. **Agent-Factory core infrastructure**:
   - LLM routing → `factorylm/core/llm/`
   - Orchestrator → `factorylm/core/orchestration/`
   - Memory/storage → `factorylm/core/memory/`

2. **Observability framework**:
   - Monitoring → `factorylm/core/observability/`
   - Cost tracking → `factorylm/core/analytics/`

### Phase 3: Services (Week 4-5)
1. **Telegram bot platform**:
   - Complete framework → `factorylm/services/telegram/`
   - OCR pipeline → `factorylm/services/ocr/`
   - Voice processing → `factorylm/services/voice/`

2. **Industrial integrations**:
   - Factory.io tools → `factorylm/services/industrial/factoryio/`
   - Equipment taxonomy → `factorylm/services/industrial/equipment/`

### Phase 4: Agent Framework (Week 6)
1. **Core agent system** → `factorylm/core/agents/`
2. **Workflow engine** → `factorylm/core/workflows/`
3. **Selected production agents** (quality screening required)

## Suggested Monorepo Structure

```
factorylm/
├── core/
│   ├── llm/              # From Agent-Factory + existing
│   ├── orchestration/    # From Agent-Factory orchestrator
│   ├── memory/           # From Agent-Factory memory
│   ├── observability/    # From Agent-Factory observability
│   ├── agents/           # From Agent-Factory agent framework  
│   ├── workflows/        # From Agent-Factory workflows
│   └── config/           # Unified configuration
│
├── services/
│   ├── telegram/         # Complete bot framework (Agent-Factory)
│   ├── plc-copilot/      # Existing (keep)
│   ├── plc-modbus/       # Existing (keep) 
│   ├── industrial/       # Factory.io, equipment (Agent-Factory)
│   ├── ocr/              # Vision pipeline (Agent-Factory)
│   ├── voice/            # Voice processing (Agent-Factory)
│   └── edge/             # Pi gateway and edge services
│
├── apps/                 # Keep existing
├── packages/             # Keep existing  
├── scripts/              # Merge deployment scripts
└── docs/                 # Consolidated documentation
```

## Quality Assessment

### Production Ready (Import Priority 1):
- **Agent-Factory**: Core orchestrator, LLM router, Telegram framework
- **factorylm**: All existing code (well-structured)
- **factorylm-core**: Complete utilities library
- **pi-gateway**: Edge device integration

### Production Ready (Import Priority 2):  
- **Agent-Factory**: Observability, industrial tools, agent framework
- **Agent-Factory**: API services, workflow engine

### Experimental (Archive/Reference):
- **Agent-Factory**: Specific agents (need individual quality review)
- **Agent-Factory**: Phoenix integration (evaluations)
- **mikes-brain**: Documentation templates

### Not Python (Separate):
- **factorylm-mini**: Firmware (C/C++)
- **ralph**: Shell tooling
- **IndustrialSkillsHub**: Next.js frontend

## Implementation Notes

### Critical Dependencies:
- Agent-Factory uses Poetry → Migrate to existing factorylm package.json/requirements
- Extensive environment variables → Audit and consolidate configuration
- Database dependencies → Ensure compatibility with existing services

### Testing Strategy:
- Import Agent-Factory's test framework patterns
- Maintain existing factorylm test structure  
- Create integration tests for merged components

### Migration Risks:
1. **Configuration conflicts** - Agent-Factory has complex env setup
2. **Database schema differences** - May need migration scripts
3. **Import size** - Agent-Factory is massive, careful selection needed

### Success Metrics:
- All critical services running in monorepo
- Telegram bot fully functional
- PLC integrations maintained
- Industrial tools operational
- Observability coverage >90%

---

## Conclusion

The consolidation opportunity is significant. Agent-Factory contains a mature, production-ready platform that aligns perfectly with factorylm's industrial AI vision. The existing factorylm structure provides an excellent foundation for receiving these components.

**Recommendation**: Proceed with phased consolidation, prioritizing core infrastructure and Telegram services first, followed by industrial tools and agent framework.

**Estimated effort**: 6 weeks for complete consolidation  
**Risk level**: Medium (complexity offset by code quality)  
**Business value**: High (immediate access to production capabilities)