# Neon Vector DB Audit — Rivet-PRO

*Audit completed: 2026-01-30 02:45 UTC*

---

## Summary

**The infrastructure exists and is sophisticated!**

Rivet-PRO already has a complete vector database setup with:
- Neon PostgreSQL + pgvector
- Knowledge atoms table with embeddings
- Self-healing knowledge gap tracking
- Industrial maintenance taxonomy
- VPS KB Client for queries

---

## Connection Details

```
Host: ep-purple-hall-ahimeyn0-pooler.c-3.us-east-1.aws.neon.tech
Database: neondb
User: neondb_owner
Port: 5432
SSL: required
```

**Also VPS KB (backup):**
```
Host: 72.60.175.144
Database: rivet
User: rivet
```

---

## Schema: knowledge_atoms

```sql
CREATE TABLE knowledge_atoms (
    atom_id UUID PRIMARY KEY,
    
    -- Categorization
    type VARCHAR(50),           -- fault, procedure, spec, part, tip, safety
    manufacturer VARCHAR(255),
    model VARCHAR(255),
    equipment_type VARCHAR(100),
    
    -- Content
    title VARCHAR(500) NOT NULL,
    content TEXT NOT NULL,
    source_url VARCHAR(1000),
    
    -- Quality metrics
    confidence FLOAT DEFAULT 0.5,    -- 0.0-1.0
    human_verified BOOLEAN,
    usage_count INTEGER DEFAULT 0,
    
    -- Vector search (1536 dim for OpenAI)
    embedding vector(1536),
    
    -- Timestamps
    created_at TIMESTAMPTZ,
    last_verified TIMESTAMPTZ
);
```

---

## Schema: knowledge_gaps (Self-Healing)

```sql
CREATE TABLE knowledge_gaps (
    gap_id UUID PRIMARY KEY,
    
    -- Query context
    query TEXT NOT NULL,
    manufacturer VARCHAR(255),
    model VARCHAR(255),
    confidence_score FLOAT,
    
    -- Gap tracking
    occurrence_count INTEGER DEFAULT 1,
    priority FLOAT,  -- Auto: count × (1-confidence) × vendor_boost
    
    -- Research status
    research_status VARCHAR(50),  -- pending, in_progress, completed, failed
    resolved_atom_id UUID REFERENCES knowledge_atoms
);
```

**Self-Healing Flow:**
1. Query comes in with low confidence
2. Gap recorded with priority score
3. Research triggered (Siemens/Rockwell get 1.5x boost)
4. New atom created to fill gap
5. Gap marked resolved

---

## Industrial Taxonomy

```
├── electrical        (fuses, breakers, contactors, wiring)
├── drives            (VFDs, soft starters, servo drives)
├── motors            (AC, DC, servo, bearings, windings)
├── plc               (I/O, comms, programming, Rockwell/Siemens)
├── instrumentation   (sensors, transmitters, analyzers)
├── pneumatic         (valves, cylinders, compressors)
├── hydraulic         (pumps, valves, filters)
├── mechanical        (bearings, gears, belts, alignment)
├── lubrication       (oil analysis, grease, filtration)
├── welding           (MIG, TIG, spot, plasma)
├── conveyor          (belt, roller, screw, bucket)
├── pumps             (centrifugal, PD, seals)
├── hvac              (chillers, compressors, refrigerant)
├── safety            (LOTO, e-stops, safety PLCs)
├── power_distribution(switchgear, MCCs, grounding)
├── controls          (HMI, SCADA, networking)
├── predictive        (vibration, thermography, ultrasound)
└── general           (tools, best practices, standards)
```

---

## Embedding Model

Currently configured for:
- **OpenAI text-embedding-3-small** (1536 dimensions)
- Fallback: **Gemini text-embedding-004** (768 dimensions)

Vectorize module in `kb_harvester/vectorize.py` handles:
1. Chunking with hierarchical metadata
2. Embedding via Gemini or OpenAI
3. Storing in pgvector
4. Hybrid search (vector + metadata filtering)

---

## Existing Data

Sample seed data includes Siemens G120C fault codes:
- F0001 - Overcurrent
- F0002 - Overvoltage
- Basic parameter setup procedure

---

## What's Missing for Meta-Vision

To fully enable the Maintenance Intelligence Layer:

1. **Data Ingestion Pipeline**
   - [ ] Connect YCB output → knowledge_atoms
   - [ ] Connect CMMS work orders → knowledge_atoms
   - [ ] Connect Edge Adapter data → knowledge_atoms
   - [ ] Connect Jarvis conversations → knowledge_atoms

2. **Embedding Service**
   - [ ] Verify embedding service is running
   - [ ] Consider switching to local embeddings (nomic-embed-text via Ollama)

3. **Query Integration**
   - [ ] Connect Jarvis → VPS KB Client for RAG
   - [ ] Enable semantic search in conversations

---

## Files Reviewed

- `test_neon_connection.py` — Connection test script
- `rivet/integrations/vps_kb_client.py` — Query client
- `kb_harvester/vectorize.py` — Embedding + taxonomy
- `rivet_pro/migrations/009_knowledge_atoms.sql` — Schema

---

## Next Steps

1. Test Neon connection from VPS
2. Set up data ingestion for new sources
3. Configure Jarvis to use RAG

---

*Audit complete. Infrastructure is ready.*
