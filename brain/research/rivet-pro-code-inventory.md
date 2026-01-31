# Rivet-PRO Code Inventory — Extraction to FactoryLM

*Deep dive completed: 2026-01-30*
*Following Constitution Amendment VI: One Brand (FactoryLM)*

---

## Executive Summary

Rivet-PRO contains **502 Python files** with extensive production-ready code. 
Key extractable components worth **months of development time**.

---

## 🔴 HIGH PRIORITY — Extract Immediately

### 1. WhatsApp Adapter (Complete)
**Location:** `rivet_pro/adapters/whatsapp/`
**Files:** 5 files, ~40KB total
**Value:** Production-ready WhatsApp integration

| File | Size | Purpose |
|------|------|---------|
| `twilio_client.py` | 8KB | Async Twilio wrapper, send/receive |
| `handlers.py` | 14KB | Text, photo, voice message handling |
| `twilio_webhook.py` | 9KB | FastAPI webhook with signature verification |
| `client.py` | 7KB | High-level client interface |
| `__init__.py` | 2KB | Exports |

**Key Features:**
- ✅ Async Twilio API wrapper
- ✅ Voice message transcription (Whisper/Groq)
- ✅ Photo download and processing
- ✅ Venezuela country code detection (+58)
- ✅ Spanish language detection
- ✅ Signature verification for security
- ✅ Rate limiting support

---

### 2. Internationalization (i18n)
**Location:** `rivet_pro/core/i18n/`
**Files:** 5 files
**Value:** Complete Spanish localization for Venezuela

| File | Size | Purpose |
|------|------|---------|
| `translator.py` | 5KB | Translation service with interpolation |
| `detector.py` | 7KB | Language detection from phone/text |
| `middleware.py` | 6KB | FastAPI middleware for language |
| `translations/es.json` | 4KB | Spanish strings (maintenance terms!) |
| `translations/en.json` | 4KB | English strings |

**Spanish translations include:**
- All bot messages
- Equipment types (motor, VFD, PLC, etc.)
- Troubleshooting steps
- Manufacturer names
- Error messages

---

### 3. Message Router (Multi-Channel)
**Location:** `rivet_pro/core/services/message_router.py`
**Size:** 18KB
**Value:** Platform-agnostic message handling

**Features:**
- Routes messages to correct handlers
- Works across WhatsApp, Telegram, any channel
- Returns structured `BotResponse` objects
- Handles photos, text, commands

---

### 4. OCR / Photo Processing Pipeline
**Location:** `rivet_pro/core/services/`
**Files:** 4 services, ~70KB total

| Service | Size | Purpose |
|---------|------|---------|
| `ocr_service.py` | 15KB | Multi-provider OCR with cost optimization |
| `photo_pipeline_service.py` | 28KB | 3-stage photo analysis pipeline |
| `photo_service.py` | 20KB | Photo handling and caching |
| `screening_service.py` | 11KB | Fast industrial detection (Groq) |

**Features:**
- Multi-provider chain (Groq → DeepSeek → Claude)
- Cost optimization (cheapest first)
- Equipment nameplate extraction
- Fault code detection
- Condition assessment
- Photo hash caching

---

### 5. Equipment Taxonomy
**Location:** `rivet_pro/core/services/equipment_taxonomy.py`
**Size:** 15KB
**Value:** 50+ manufacturers, equipment classification

**Includes:**
- VFD manufacturers (Allen-Bradley, Siemens, ABB, Yaskawa, etc.)
- PLC brands
- Motor manufacturers
- Pattern matching for model numbers
- Fault code extraction

---

### 6. Claude AI Analyzer
**Location:** `rivet_pro/core/services/claude_analyzer.py`
**Size:** 24KB
**Value:** AI-powered troubleshooting synthesis

**Features:**
- Combines specs + history + KB for analysis
- Structured output (solutions, citations, recommendations)
- Safety warning extraction
- Cost tracking

---

## 🟡 MEDIUM PRIORITY — Extract When Needed

### 7. Semantic Search Service
**Location:** `rivet_pro/core/services/semantic_search_service.py`
**Size:** 12KB
- OpenAI embeddings
- Sentence-transformers fallback
- PostgreSQL vector search

### 8. Knowledge Base Services
**Location:** `rivet_pro/core/services/kb_*.py`
**Files:** 8 services, ~140KB

| Service | Purpose |
|---------|---------|
| `kb_search_service.py` | Search knowledge base |
| `kb_parse_service.py` | Parse documents |
| `kb_enrichment_*.py` | Auto-enrich content |
| `kb_download_service.py` | Download manuals |
| `kb_analytics_service.py` | Usage analytics |

### 9. Manual Services
**Location:** `rivet_pro/core/services/manual_*.py`
**Files:** 7 services, ~150KB

| Service | Purpose |
|---------|---------|
| `manual_service.py` | Main manual handling (48KB!) |
| `manual_matcher_service.py` | Match equipment to manuals |
| `manual_rag_service.py` | RAG for manual Q&A |
| `manual_indexing_service.py` | Index manual content |
| `manual_download_manager.py` | Download and cache |
| `manual_qa_service.py` | Q&A interface |
| `manual_vision_service.py` | Visual manual analysis |

### 10. Work Order Service
**Location:** `rivet_pro/core/services/work_order_service.py`
**Size:** 16KB
- Create work orders from diagnostics
- Track equipment history

### 11. Feedback Service
**Location:** `rivet_pro/core/services/feedback_service.py`
**Size:** 21KB
- User feedback collection
- Approval workflow
- Analytics

### 12. LLM Manager
**Location:** `rivet_pro/core/services/llm_manager.py`
**Size:** 12KB
- Multi-provider LLM routing
- Cost tracking
- Fallback chains

---

## 🟢 LOW PRIORITY — Reference Only

### 13. Workers (Background Jobs)
**Location:** `rivet_pro/workers/`
**Files:** 14 workers

| Worker | Purpose |
|--------|---------|
| `atom_creator.py` | Create KB atoms |
| `batch_embeddings.py` | Batch embedding generation |
| `daily_kb_builder.py` | Daily KB maintenance |
| `pdf_downloader.py` | Download PDFs |
| `text_extractor.py` | Extract text from docs |
| `recursive_chunker.py` | Chunk large documents |

### 14. Adapters (LLM)
**Location:** `rivet_pro/adapters/llm/`
- LLM provider routing
- Ralph orchestrator (AI agent)

### 15. Telegram Adapter
**Location:** `rivet_pro/adapters/telegram/`
- Reference for adapter pattern
- Similar to WhatsApp

---

## Extraction Plan

### Phase 1 (This Week) — Venezuela MVP
1. **WhatsApp Adapter** → `factorylm/adapters/whatsapp/`
2. **i18n** → `factorylm/core/i18n/`
3. **Message Router** → `factorylm/core/services/`
4. **Equipment Taxonomy** → `factorylm/core/services/`

### Phase 2 (Next 2 Weeks) — Full Diagnostics
5. **OCR/Photo Pipeline** → `factorylm/core/services/`
6. **Claude Analyzer** → `factorylm/core/services/`
7. **Semantic Search** → `factorylm/core/services/`

### Phase 3 (Month 2) — Knowledge Base
8. **KB Services** → `factorylm/core/kb/`
9. **Manual Services** → `factorylm/core/manuals/`
10. **Work Orders** → `factorylm/core/services/`

---

## Dependencies to Install

```bash
# Core
pip install twilio httpx asyncpg openai anthropic

# OCR/Vision
pip install groq sentence-transformers

# Web
pip install fastapi pydantic pydantic-settings

# Utils
pip install python-dotenv
```

---

## Estimated Value

| Component | Dev Time Saved | Status |
|-----------|---------------|--------|
| WhatsApp Adapter | 2-3 weeks | Ready to extract |
| i18n + Spanish | 1 week | Ready to extract |
| Message Router | 1-2 weeks | Ready to extract |
| OCR Pipeline | 3-4 weeks | Ready to extract |
| Equipment Taxonomy | 2 weeks | Ready to extract |
| Claude Analyzer | 2 weeks | Ready to extract |
| KB Services | 4-6 weeks | Needs adaptation |
| Manual Services | 4-6 weeks | Needs adaptation |

**Total: ~4-5 months of development already done.**

---

## Next Steps

1. ✅ Inventory complete
2. ⏳ Mike approves extraction plan
3. ⏳ Create `factorylm/adapters/` structure
4. ⏳ Copy WhatsApp adapter (rebrand RIVET → FactoryLM)
5. ⏳ Copy i18n with translations
6. ⏳ Test with Twilio sandbox
7. ⏳ Create PR following Engineering Commandments

---

*Following Constitution Amendment VI: Everything is FactoryLM.*
