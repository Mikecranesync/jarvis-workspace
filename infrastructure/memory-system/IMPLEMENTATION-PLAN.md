# Jarvis Memory System Implementation Plan

## Executive Summary

Jarvis's current memory_search is broken due to Gemini embeddings API key being flagged. This plan implements a **local, self-hosted solution using ChromaDB with sentence-transformers** for immediate replacement, followed by a hybrid architecture evaluation.

## Current System Analysis

### Broken Components
- **Embedding Provider**: Gemini embeddings API (key flagged)
- **Memory Search Tool**: `/root/jarvis-workspace/clawdbot-search/src/agents/tools/memory-tool.ts`
- **Memory Manager**: Complex TypeScript implementation with vector search

### Current Architecture
- **Files**: Memory stored in `/root/jarvis-workspace/memory/*.md`
- **Search**: Vector similarity + FTS hybrid search
- **Storage**: SQLite with sqlite-vec extension
- **Chunking**: 400 tokens, 80 token overlap
- **Integration**: Direct tool integration with Clawdbot

## Priority 1: Quick Fix (30-minute implementation)

### Solution: ChromaDB + Sentence Transformers
- **Why ChromaDB**: MIT licensed, embedded database, no external dependencies
- **Why sentence-transformers**: All-MiniLM-L6-v2 is 22MB, runs on CPU, good for semantic search
- **Target**: Drop-in replacement for current memory_search functionality

### Technical Specifications
```python
# Core Stack
- ChromaDB 0.4.24+ (embedded mode)
- sentence-transformers[all] 
- Model: all-MiniLM-L6-v2 (384-dimensional embeddings)
- Python 3.12 compatible
- Memory footprint: ~200MB on 4GB VPS
```

### Implementation Components
1. **memory_service.py**: ChromaDB wrapper with search/index functionality
2. **install.sh**: Automated setup script
3. **Integration layer**: HTTP API for Clawdbot compatibility
4. **Auto-indexing**: Cron job for new memory files

## Architecture Review

### Option 1: ChromaDB (Chosen for Quick Fix)
**Pros:**
- Embedded, no server required
- MIT licensed
- Python-native
- ~100MB RAM footprint
- Persistent storage
- Filter support
- Simple API

**Cons:**
- Not optimized for edge computing
- Limited scalability
- Python dependency for Clawdbot integration

### Option 2: Mem0 (Future Consideration)
**Pros:**
- Apache 2.0 licensed
- Multi-level memory (User/Session/Agent)
- 26% accuracy improvement vs OpenAI Memory
- 91% faster responses
- Built for production AI agents

**Cons:**
- Still requires external LLM for memory extraction
- More complex setup
- Newer project (potential stability concerns)

### Option 3: LanceDB (Future Edge Deployment)
**Pros:**
- Apache 2.0 licensed
- Columnar format (efficient storage)
- Multimodal support
- Rust performance
- Perfect for edge/Pi deployment
- No vendor lock-in

**Cons:**
- Rust dependency for optimal performance
- More complex setup
- Overkill for current needs

### Option 4: Generative Agents Memory (Research Interest)
**Architecture Components:**
- **Observation**: Raw experience storage
- **Reflection**: Higher-level pattern synthesis  
- **Retrieval**: Dynamic memory access for planning

**Pros:**
- Human-like memory organization
- Temporal awareness
- Reflection capabilities

**Cons:**
- Research prototype
- Complex implementation
- Requires sophisticated LLM integration

## Recommended Hybrid Approach

### Phase 1: Immediate (Current Implementation)
- ChromaDB + sentence-transformers on VPS
- HTTP API for Clawdbot integration
- Auto-indexing of memory files

### Phase 2: Enhanced Memory (2-4 weeks)
- Integrate Mem0 memory extraction
- Multi-level memory architecture
- Reflection and synthesis capabilities

### Phase 3: Edge Deployment (4-8 weeks)  
- LanceDB on Raspberry Pi
- Local inference with Ollama
- Distributed memory architecture

## Implementation Details

### File Structure
```
/root/jarvis-workspace/infrastructure/memory-system/
├── IMPLEMENTATION-PLAN.md
├── install.sh
├── memory_service.py
├── config.py
├── requirements.txt
├── test_memory_search.py
├── cron/
│   └── auto_index.py
└── docs/
    ├── API.md
    └── INTEGRATION.md
```

### API Design
```python
# HTTP API Endpoints
POST /search
{
    "query": "string",
    "max_results": 6,
    "min_score": 0.35,
    "source": "memory|sessions"
}

Response:
{
    "results": [
        {
            "path": "memory/2026-02-06.md",
            "startLine": 15,
            "endLine": 20,
            "score": 0.87,
            "snippet": "...",
            "source": "memory"
        }
    ],
    "provider": "chromadb",
    "model": "all-MiniLM-L6-v2"
}
```

### Memory Indexing Strategy
```python
# Document Processing
1. Watch /root/jarvis-workspace/memory/*.md
2. Chunk into 400 token segments (80 token overlap)
3. Generate embeddings with sentence-transformers
4. Store in ChromaDB with metadata:
   - file_path
   - start_line / end_line
   - content_hash
   - timestamp
   - source_type
```

## Integration with Clawdbot

### Current Integration Points
- **Memory Tool**: `src/agents/tools/memory-tool.ts`
- **Search Function**: `memory_search(query, maxResults, minScore)`
- **Config**: `src/agents/memory-search.ts`

### Replacement Strategy
1. **HTTP Proxy**: Create HTTP wrapper around ChromaDB service
2. **Port Mapping**: Run on localhost:5432 (or configurable)
3. **API Compatibility**: Match existing response format
4. **Error Handling**: Graceful fallback behavior

### Configuration Changes Required
```typescript
// In clawdbot config, switch to local HTTP provider
{
  "memorySearch": {
    "enabled": true,
    "provider": "local",
    "remote": {
      "baseUrl": "http://localhost:5432",
      "apiKey": null
    },
    "sources": ["memory"],
    "fallback": "none"
  }
}
```

## Testing Strategy

### Unit Tests
- ChromaDB CRUD operations
- Embedding generation
- Search relevance scoring
- File watching and indexing

### Integration Tests  
- End-to-end search workflow
- Clawdbot tool integration
- Memory file updates
- Performance benchmarks

### Performance Requirements
- **Search Latency**: <500ms for typical queries
- **Memory Usage**: <200MB steady state
- **Index Time**: <5s for typical daily memory file
- **Availability**: 99.9% uptime on VPS

## Deployment Plan

### Phase 1: Development Setup (30 minutes)
1. Run install.sh on VPS
2. Index existing memory files
3. Start memory service
4. Test search functionality

### Phase 2: Clawdbot Integration (60 minutes)
1. Update Clawdbot memory configuration
2. Deploy HTTP proxy wrapper
3. Test memory_search tool
4. Validate search results

### Phase 3: Production Deployment (30 minutes)
1. Setup systemd service
2. Configure auto-indexing cron job
3. Add monitoring and logging
4. Document operational procedures

## Risk Mitigation

### Technical Risks
- **Performance**: ChromaDB may be slower than sqlite-vec
  - *Mitigation*: Benchmark and optimize, consider migration to LanceDB if needed
- **Memory Usage**: sentence-transformers model size
  - *Mitigation*: Use quantized model, monitor memory usage
- **Dependencies**: Python dependencies for Node.js codebase
  - *Mitigation*: Docker container or HTTP API isolation

### Operational Risks
- **Service Downtime**: HTTP service failure
  - *Mitigation*: Systemd auto-restart, health checks
- **Data Loss**: ChromaDB corruption
  - *Mitigation*: Regular backups, rebuild capability
- **Index Drift**: Memory files not auto-indexed
  - *Mitigation*: File watching + cron job redundancy

## Success Metrics

### Phase 1 Success Criteria
- [ ] memory_search returns relevant results
- [ ] Search latency <500ms for 95% of queries
- [ ] Memory usage <200MB
- [ ] All existing memory files indexed successfully
- [ ] Zero external API dependencies

### Integration Success Criteria
- [ ] Clawdbot memory_search tool works end-to-end
- [ ] Search quality comparable to previous system
- [ ] No breaking changes to existing memory workflow
- [ ] Auto-indexing works for new memory files

## Future Roadmap

### Q1 2026: Enhanced Memory
- Implement Mem0 for better memory extraction
- Add reflection and synthesis capabilities
- Multi-level memory architecture

### Q2 2026: Edge Deployment
- Port to LanceDB for Raspberry Pi
- Distributed memory across edge devices
- Local inference with Ollama

### Q3 2026: Advanced Features
- Multimodal memory (images, audio)
- Temporal memory patterns
- Proactive memory recommendations

## Conclusion

This implementation plan provides a **practical, immediate solution** to the broken memory system while setting up a foundation for advanced memory capabilities. The ChromaDB + sentence-transformers approach offers the right balance of simplicity, performance, and local control for the current requirements.

The modular architecture allows for future enhancement with Mem0's advanced features and LanceDB's edge capabilities without disrupting the core functionality.

**Estimated Total Implementation Time: 2 hours**
**Confidence Level: 95% zero-shot implementation success**