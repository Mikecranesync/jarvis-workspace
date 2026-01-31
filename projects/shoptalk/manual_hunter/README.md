# Manual Hunter

Equipment manual search, retrieval, and RAG system for ShopTalk.

**Origin:** Extracted from Rivet-PRO (Issue #20)

## Features

- **Local Manual Storage** - Check local files first (instant)
- **External Search** - Tavily API for web search
- **LLM Validation** - Groq/Claude validates manual matches
- **Confidence Scoring** - Store all manuals with ≥70% confidence
- **PDF Chunking** - Section-aware with overlap for RAG
- **Citations** - Return page numbers and section titles
- **Pre-loaded Manuals** - Siemens, Rockwell, ABB VFDs

## Architecture

```
User asks about equipment
        │
        ▼
┌───────────────────────────┐
│   ManualService           │
│   - Check local files     │
│   - Check database cache  │
│   - Search externally     │
└───────────┬───────────────┘
            │
            ▼
┌───────────────────────────┐
│   ManualMatcherService    │
│   - LLM validates match   │
│   - Confidence scoring    │
│   - Store in database     │
└───────────┬───────────────┘
            │
            ▼
┌───────────────────────────┐
│   ManualRAGService        │
│   - Vector similarity     │
│   - Retrieve chunks       │
│   - Format citations      │
└───────────┬───────────────┘
            │
            ▼
      Return link + page
```

## Files

```
manual_hunter/
├── services/
│   ├── manual_service.py         # Main search/cache service
│   ├── manual_matcher_service.py # LLM-validated matching
│   ├── manual_rag_service.py     # Vector RAG retrieval
│   └── pdf_chunker_service.py    # PDF parsing & chunking
├── handlers/
│   └── manual_qa_handler.py      # Telegram handler
├── scripts/
│   ├── ingest_pdfs.py            # Pre-load industrial manuals
│   └── create_manual_hunter_tables_v2.py # Database schema
└── data/
    └── manuals/                   # Local PDF storage
```

## Pre-loaded Manuals

The `ingest_pdfs.py` script loads these verified industrial equipment manuals:

### Siemens
- SINAMICS V20 Operating Instructions
- SINAMICS G120 Function Manual
- SINAMICS G120 PM240-2 Hardware Installation
- SINAMICS S120 AC Drive Manual

### Rockwell Automation
- PowerFlex 4M User Manual
- PowerFlex 4 User Manual
- PowerFlex 40P User Manual

### ABB
- ACS880-01 Hardware Manual
- ACS880 Drive Manual
- ACS880 Application Programming Manual

## Usage

### Search for a Manual

```python
from manual_hunter.services.manual_service import ManualService

service = ManualService(db)
result, report = await service.search_manual(
    manufacturer="Siemens",
    model="SINAMICS V20",
    prefer_local=True
)

if result:
    print(f"Manual URL: {result['url']}")
    print(f"Confidence: {result['confidence']}")
```

### RAG Retrieval from Manual

```python
from manual_hunter.services.manual_rag_service import ManualRAGService

rag = ManualRAGService(db_pool)
result = await rag.retrieve(
    query="How to reset fault code F0001?",
    manufacturer="Siemens",
    top_k=5
)

for chunk in result.chunks:
    print(f"Page {chunk.page_number}: {chunk.content[:100]}...")
```

## Database Schema

Requires PostgreSQL with pgvector extension:

```sql
-- Run create_manual_hunter_tables_v2.py to create:
-- - manuals (manual metadata)
-- - manual_chunks (vectorized content)
-- - manual_cache (search result cache)
```

## Configuration

Environment variables:
- `TAVILY_API_KEY` - For external manual search
- `ANTHROPIC_API_KEY` - For LLM validation (Claude)
- `GROQ_API_KEY` - For LLM validation (Groq, primary)
- `DATABASE_URL` - PostgreSQL connection string

## Integration

### WhatsApp
When user sends equipment model, search for manual and return link:
```
User: "I have a Siemens V20 VFD with fault F0001"
Bot: "Here's the Siemens SINAMICS V20 manual: [link]
      See page 127 for fault code F0001 troubleshooting."
```

### ShopTalk Diagnostics
Link diagnostic responses to relevant manual sections with citations.

---

*Extracted from Rivet-PRO per Constitution Amendment VI (FactoryLM consolidation)*
