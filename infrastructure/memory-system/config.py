"""Configuration for Jarvis Memory System"""
import os

# Service configuration
SERVICE_HOST = "127.0.0.1"
SERVICE_PORT = 5433

# Memory configuration
MEMORY_DIR = "/root/jarvis-workspace/memory"
CHROMADB_DIR = "/root/jarvis-workspace/infrastructure/memory-system/chromadb_data"
COLLECTION_NAME = "jarvis_memory"

# Model configuration (lite version uses ChromaDB defaults)
EMBEDDING_MODEL = "default"
EMBEDDING_DIM = 384

# Search configuration
DEFAULT_MAX_RESULTS = 6
DEFAULT_MIN_SCORE = 0.1
CHUNK_SIZE = 400  # tokens
CHUNK_OVERLAP = 80  # tokens

# Approximate chars per token for chunking
CHARS_PER_TOKEN = 4

# File watching
WATCH_DEBOUNCE_SECONDS = 2

# Logging
LOG_LEVEL = "INFO"
