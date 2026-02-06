#!/usr/bin/env python3
"""
Auto-indexing cron job for Jarvis Memory System (Lite)
Runs every 5 minutes to index new/modified memory files
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import asyncio
from memory_service_lite import MemoryService
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def main():
    """Index any new or modified memory files"""
    try:
        service = MemoryService()
        await service.initialize()
        
        # Force re-index of all files (checks timestamps internally)
        await service.index_memory_files()
        
        logger.info("Auto-indexing completed successfully")
    except Exception as e:
        logger.error(f"Auto-indexing failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
