#!/usr/bin/env python3
"""
Batch PDF Ingestion Script

Directly processes PDFs without Redis queue.
Usage: python scripts/ingest_pdfs.py
"""

import asyncio
import os
import sys
from pathlib import Path

# Force CPU for embeddings
os.environ['CUDA_VISIBLE_DEVICES'] = ''

# Add project root
sys.path.insert(0, str(Path(__file__).parent.parent))

# Load .env
env_file = Path(__file__).parent.parent / '.env'
if env_file.exists():
    for line in env_file.read_text().splitlines():
        if '=' in line and not line.startswith('#'):
            k, v = line.split('=', 1)
            os.environ.setdefault(k.strip().replace('\r', ''), v.strip().replace('\r', ''))


# Industrial equipment PDF URLs - Verified accessible 2024
PDF_URLS = [
    # Siemens SINAMICS V20 Operating Instructions (Complete)
    "https://cache.industry.siemens.com/dl/files/056/104426056/att_70877/v1/v20_operating_instructions_complete_en-US_en-US.pdf",

    # Siemens SINAMICS G120 Function Manual
    "https://support.industry.siemens.com/cs/attachments/52614597/Function_Manual_en-US.pdf",

    # Siemens SINAMICS G120 PM240-2 Hardware Installation
    "https://support.industry.siemens.com/cs/attachments/109750315/G120_PM2402_hw_inst_man_0817_en-US.pdf",

    # Siemens SINAMICS S120 AC Drive Manual
    "https://cache.industry.siemens.com/dl/files/000/99673000/att_51983/v1/GH6_0414_eng_en-US.pdf",

    # Rockwell PowerFlex 4M User Manual (Sept 2024)
    "https://literature.rockwellautomation.com/idc/groups/literature/documents/um/22f-um001_-en-e.pdf",

    # Rockwell PowerFlex 4 User Manual (Sept 2024)
    "https://literature.rockwellautomation.com/idc/groups/literature/documents/um/22a-um001_-en-e.pdf",

    # Rockwell PowerFlex 40P User Manual (Sept 2024)
    "https://literature.rockwellautomation.com/idc/groups/literature/documents/um/22d-um001_-en-e.pdf",

    # ABB ACS880-01 Hardware Manual
    "https://beta-power.co.uk/wp-content/uploads/2024/03/ACS880-01_Drives_hardware-manual.pdf",

    # ABB ACS880 Drive Manual
    "https://vfds.com/content/manuals/abb/abb-acs880-manual.pdf",

    # ABB ACS880 Application Programming Manual
    "https://cdn.logic-control.com/docs/abb-drives/acs880/ACS880-01/EN_ACS880_Drive_application_programming_manual_C_A4.pdf",
]


async def main():
    import asyncpg
    from rivet_pro.workers.kb_ingestion_worker import KBIngestionWorker

    print("=" * 60)
    print("  KB Batch Ingestion")
    print("=" * 60)

    worker = KBIngestionWorker()
    worker.db_pool = await asyncpg.create_pool(
        os.environ['DATABASE_URL'],
        min_size=1,
        max_size=3
    )

    # Count before
    before = await worker.db_pool.fetchval("SELECT COUNT(*) FROM knowledge_atoms")
    print(f"\nAtoms before: {before}")
    print(f"URLs to process: {len(PDF_URLS)}\n")

    total_atoms = 0
    success_count = 0

    for i, url in enumerate(PDF_URLS, 1):
        print(f"\n[{i}/{len(PDF_URLS)}] {url[:60]}...")

        try:
            success, atoms = await worker._process_url(url)
            if success:
                total_atoms += atoms
                success_count += 1
                print(f"    ✅ {atoms} atoms")
            else:
                print(f"    ❌ Failed")
        except Exception as e:
            print(f"    ❌ Error: {e}")

    # Count after
    after = await worker.db_pool.fetchval("SELECT COUNT(*) FROM knowledge_atoms")

    print("\n" + "=" * 60)
    print("  Summary")
    print("=" * 60)
    print(f"  URLs processed: {success_count}/{len(PDF_URLS)}")
    print(f"  Atoms created: {total_atoms}")
    print(f"  Total in DB: {before} -> {after} (+{after - before})")
    print(f"  Cost: $0.00 (FREE local embeddings)")
    print("=" * 60)

    await worker.db_pool.close()


if __name__ == '__main__':
    asyncio.run(main())
