#!/usr/bin/env python3
"""
Jarvis Memory System - ChromaDB Lite Implementation
Uses ChromaDB's default embeddings for fast installation without PyTorch
"""
import asyncio
import hashlib
import logging
import os
import re
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import chromadb
import uvicorn
from chromadb.config import Settings
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

# Import configuration
from config import *

# Override model name for default embeddings
EMBEDDING_MODEL = "default"
EMBEDDING_DIM = 384  # ChromaDB default

# Configure logging
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class SearchRequest(BaseModel):
    query: str
    max_results: Optional[int] = DEFAULT_MAX_RESULTS
    min_score: Optional[float] = DEFAULT_MIN_SCORE
    source: Optional[str] = "memory"

class SearchResult(BaseModel):
    path: str
    startLine: int
    endLine: int
    score: float
    snippet: str
    source: str

class SearchResponse(BaseModel):
    results: List[SearchResult]
    provider: str = "chromadb"
    model: str = EMBEDDING_MODEL
    fallback: Optional[str] = None

class MemoryFileHandler(FileSystemEventHandler):
    """File system event handler for watching memory file changes"""
    
    def __init__(self, memory_service: 'MemoryService'):
        self.memory_service = memory_service
        self.debounce_timer = None
    
    def on_modified(self, event):
        if not event.is_directory and event.src_path.endswith('.md'):
            self._schedule_reindex()
    
    def on_created(self, event):
        if not event.is_directory and event.src_path.endswith('.md'):
            self._schedule_reindex()
    
    def _schedule_reindex(self):
        """Debounce file changes to avoid excessive reindexing"""
        if self.debounce_timer:
            self.debounce_timer.cancel()
        
        def schedule_task():
            loop = asyncio.get_event_loop()
            if loop.is_running():
                asyncio.create_task(self.memory_service.index_memory_files())
            else:
                loop.run_until_complete(self.memory_service.index_memory_files())
        
        self.debounce_timer = asyncio.get_event_loop().call_later(
            WATCH_DEBOUNCE_SECONDS, schedule_task
        )

class MemoryService:
    """ChromaDB-based memory service for Jarvis (lightweight version)"""
    
    def __init__(self):
        self.client = None
        self.collection = None
        self.observer = None
        self.file_hashes: Dict[str, str] = {}
        
    async def initialize(self):
        """Initialize ChromaDB client"""
        try:
            logger.info("Initializing ChromaDB client (lite mode)...")
            
            # Create ChromaDB client with persistent storage
            self.client = chromadb.PersistentClient(
                path=CHROMADB_DIR,
                settings=Settings(
                    anonymized_telemetry=False,
                    allow_reset=False
                )
            )
            
            # Get or create collection with default embeddings
            try:
                self.collection = self.client.get_collection(name=COLLECTION_NAME)
                logger.info(f"Using existing collection: {COLLECTION_NAME}")
            except Exception:
                self.collection = self.client.create_collection(name=COLLECTION_NAME)
                logger.info(f"Created new collection: {COLLECTION_NAME}")
            
            logger.info("Memory service initialized successfully!")
            logger.info("Using ChromaDB default embeddings (no external model required)")
            
            # Start file watching if memory directory exists
            if os.path.exists(MEMORY_DIR):
                self._start_file_watcher()
            
        except Exception as e:
            logger.error(f"Failed to initialize memory service: {e}")
            raise
    
    def _start_file_watcher(self):
        """Start watching memory directory for file changes"""
        try:
            event_handler = MemoryFileHandler(self)
            self.observer = Observer()
            self.observer.schedule(event_handler, MEMORY_DIR, recursive=False)
            self.observer.start()
            logger.info(f"Started watching memory directory: {MEMORY_DIR}")
        except Exception as e:
            logger.error(f"Failed to start file watcher: {e}")
    
    def _chunk_text(self, text: str, chunk_size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> List[str]:
        """
        Chunk text into overlapping segments based on approximate token count
        """
        # Approximate token count using character count
        chars_per_chunk = chunk_size * CHARS_PER_TOKEN
        chars_overlap = overlap * CHARS_PER_TOKEN
        
        if len(text) <= chars_per_chunk:
            return [text]
        
        chunks = []
        start = 0
        
        while start < len(text):
            end = min(start + chars_per_chunk, len(text))
            
            # Try to break at sentence or paragraph boundaries
            if end < len(text):
                # Look for sentence endings within the last 20% of the chunk
                search_start = max(start + int(chars_per_chunk * 0.8), start + chars_overlap)
                sentence_end = text.rfind('.', search_start, end)
                if sentence_end > start:
                    end = sentence_end + 1
                else:
                    # Fall back to word boundaries
                    word_end = text.rfind(' ', search_start, end)
                    if word_end > start:
                        end = word_end
            
            chunk = text[start:end].strip()
            if chunk:
                chunks.append(chunk)
            
            # Move start position with overlap
            start = max(start + chars_per_chunk - chars_overlap, end)
            
            # Prevent infinite loops
            if start >= len(text):
                break
        
        return chunks
    
    def _get_file_hash(self, file_path: str) -> str:
        """Get MD5 hash of file for change detection"""
        try:
            with open(file_path, 'rb') as f:
                return hashlib.md5(f.read()).hexdigest()
        except Exception:
            return ""
    
    def _extract_line_numbers(self, full_text: str, chunk_text: str) -> Tuple[int, int]:
        """
        Extract start and end line numbers for a chunk within the full text
        """
        lines = full_text.split('\n')
        chunk_lines = chunk_text.split('\n')
        
        # Find the starting line
        start_line = 1
        for i, line in enumerate(lines):
            if chunk_lines[0].strip() in line:
                start_line = i + 1
                break
        
        end_line = start_line + len(chunk_lines) - 1
        
        return start_line, min(end_line, len(lines))
    
    async def index_memory_files(self):
        """Index all memory files, only processing changed files"""
        try:
            if not os.path.exists(MEMORY_DIR):
                logger.warning(f"Memory directory does not exist: {MEMORY_DIR}")
                return
            
            memory_files = list(Path(MEMORY_DIR).glob("*.md"))
            logger.info(f"Found {len(memory_files)} memory files to process")
            
            if not memory_files:
                logger.info("No memory files found to index")
                return
            
            indexed_count = 0
            
            for file_path in memory_files:
                try:
                    # Check if file has changed
                    current_hash = self._get_file_hash(str(file_path))
                    stored_hash = self.file_hashes.get(str(file_path))
                    
                    if current_hash == stored_hash and current_hash:
                        continue  # File hasn't changed
                    
                    await self._index_single_file(file_path)
                    self.file_hashes[str(file_path)] = current_hash
                    indexed_count += 1
                    
                except Exception as e:
                    logger.error(f"Failed to index {file_path}: {e}")
                    continue
            
            logger.info(f"Successfully indexed {indexed_count} memory files")
            
        except Exception as e:
            logger.error(f"Failed to index memory files: {e}")
            raise
    
    async def _index_single_file(self, file_path: Path):
        """Index a single memory file"""
        try:
            # Read file content
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if not content.strip():
                logger.warning(f"Skipping empty file: {file_path}")
                return
            
            # Remove existing chunks for this file
            rel_path = file_path.relative_to(Path(MEMORY_DIR))
            existing_ids = self.collection.get(
                where={"file_path": str(rel_path)}
            )["ids"]
            
            if existing_ids:
                self.collection.delete(ids=existing_ids)
                logger.debug(f"Removed {len(existing_ids)} existing chunks for {rel_path}")
            
            # Chunk the content
            chunks = self._chunk_text(content)
            
            if not chunks:
                logger.warning(f"No chunks generated for file: {file_path}")
                return
            
            # Prepare data for ChromaDB
            documents = []
            metadatas = []
            ids = []
            
            for i, chunk in enumerate(chunks):
                start_line, end_line = self._extract_line_numbers(content, chunk)
                
                chunk_id = f"{rel_path}_{i}_{int(time.time())}"
                
                documents.append(chunk)
                metadatas.append({
                    "file_path": str(rel_path),
                    "start_line": start_line,
                    "end_line": end_line,
                    "chunk_index": i,
                    "source": "memory",
                    "timestamp": datetime.now().isoformat()
                })
                ids.append(chunk_id)
            
            # Add to ChromaDB collection
            self.collection.add(
                documents=documents,
                metadatas=metadatas,
                ids=ids
            )
            
            logger.info(f"Indexed {file_path} with {len(chunks)} chunks")
            
        except Exception as e:
            logger.error(f"Failed to index file {file_path}: {e}")
            raise
    
    async def search(self, query: str, max_results: int = DEFAULT_MAX_RESULTS, 
                    min_score: float = DEFAULT_MIN_SCORE) -> List[SearchResult]:
        """
        Search memory using semantic similarity
        """
        try:
            if not self.collection:
                raise HTTPException(status_code=503, detail="Memory service not initialized")
            
            # Query ChromaDB
            results = self.collection.query(
                query_texts=[query],
                n_results=max(max_results * 2, 20),  # Get more results for filtering
                include=["documents", "metadatas", "distances"]
            )
            
            search_results = []
            
            if results["documents"] and results["documents"][0]:
                for i, (doc, metadata, distance) in enumerate(zip(
                    results["documents"][0],
                    results["metadatas"][0], 
                    results["distances"][0]
                )):
                    # Convert L2 distance to similarity score
                    # ChromaDB default uses L2/Euclidean distance (unbounded)
                    # Use exponential decay: score = exp(-distance/scale)
                    import math
                    score = math.exp(-distance / 2.0)  # Scale factor of 2 works well
                    
                    if score < min_score:
                        continue
                    
                    # Create snippet (limit length)
                    snippet = doc.strip()
                    if len(snippet) > 700:
                        snippet = snippet[:697] + "..."
                    
                    search_results.append(SearchResult(
                        path=f"memory/{metadata['file_path']}",
                        startLine=metadata["start_line"],
                        endLine=metadata["end_line"],
                        score=score,
                        snippet=snippet,
                        source=metadata["source"]
                    ))
            
            # Sort by score and limit results
            search_results.sort(key=lambda x: x.score, reverse=True)
            search_results = search_results[:max_results]
            
            logger.debug(f"Search query '{query}' returned {len(search_results)} results")
            return search_results
            
        except Exception as e:
            logger.error(f"Search failed: {e}")
            raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")
    
    async def get_stats(self) -> Dict:
        """Get memory system statistics"""
        try:
            if not self.collection:
                return {"error": "Service not initialized"}
            
            count = self.collection.count()
            memory_files = len(list(Path(MEMORY_DIR).glob("*.md"))) if os.path.exists(MEMORY_DIR) else 0
            
            return {
                "total_chunks": count,
                "memory_files": memory_files,
                "model": EMBEDDING_MODEL,
                "collection_name": COLLECTION_NAME,
                "memory_dir": MEMORY_DIR,
                "indexed_files": len(self.file_hashes)
            }
        except Exception as e:
            logger.error(f"Failed to get stats: {e}")
            return {"error": str(e)}
    
    def shutdown(self):
        """Cleanup resources"""
        if self.observer:
            self.observer.stop()
            self.observer.join()
        logger.info("Memory service shut down")

# Initialize global memory service
memory_service = MemoryService()

# FastAPI app
app = FastAPI(
    title="Jarvis Memory System (Lite)",
    description="ChromaDB-based semantic memory search for Jarvis (lightweight version)",
    version="1.0.0"
)

@app.on_event("startup")
async def startup_event():
    """Initialize memory service on startup"""
    await memory_service.initialize()
    await memory_service.index_memory_files()

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    memory_service.shutdown()

@app.post("/search", response_model=SearchResponse)
async def search_memory(request: SearchRequest):
    """Search memory files using semantic similarity"""
    results = await memory_service.search(
        query=request.query,
        max_results=request.max_results or DEFAULT_MAX_RESULTS,
        min_score=request.min_score or DEFAULT_MIN_SCORE
    )
    
    return SearchResponse(results=results)

@app.get("/stats")
async def get_stats():
    """Get memory system statistics"""
    return await memory_service.get_stats()

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        stats = await memory_service.get_stats()
        return {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "stats": stats
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }

@app.post("/reindex")
async def reindex_memory():
    """Force reindexing of all memory files"""
    try:
        # Clear existing hashes to force reindexing
        memory_service.file_hashes.clear()
        await memory_service.index_memory_files()
        return {"status": "success", "message": "Memory files reindexed successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Reindexing failed: {str(e)}")

if __name__ == "__main__":
    # Run the service
    logger.info(f"Starting Jarvis Memory System (lite) on {SERVICE_HOST}:{SERVICE_PORT}")
    uvicorn.run(
        app, 
        host=SERVICE_HOST, 
        port=SERVICE_PORT,
        log_level=LOG_LEVEL.lower()
    )