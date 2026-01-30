"""
Neon Vector DB Ingestion Pipeline

Feeds data from various sources into the knowledge_atoms table.
Supports:
- Jarvis memory/research files
- YCB scripts and storyboards
- Manual entries

Usage:
    python -m tools.neon_ingest --source memory
    python -m tools.neon_ingest --source research
    python -m tools.neon_ingest --file path/to/file.md
    python -m tools.neon_ingest --stats
"""

import os
import sys
import json
import uuid
import hashlib
import psycopg2
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional, Dict, Any, List
import argparse

# Neon connection details
NEON_HOST = "ep-purple-hall-ahimeyn0-pooler.c-3.us-east-1.aws.neon.tech"
NEON_DATABASE = "neondb"
NEON_USER = "neondb_owner"
NEON_PASSWORD = "npg_c3UNa4KOlCeL"
NEON_PORT = 5432

# Workspace paths
WORKSPACE = Path("/root/jarvis-workspace")
MEMORY_DIR = WORKSPACE / "memory"
BRAIN_DIR = WORKSPACE / "brain"
YCB_DIR = WORKSPACE / "projects/Rivet-PRO/ycb"


def get_connection():
    """Get database connection."""
    return psycopg2.connect(
        host=NEON_HOST,
        database=NEON_DATABASE,
        user=NEON_USER,
        password=NEON_PASSWORD,
        port=NEON_PORT,
        sslmode='require'
    )


def hash_content(content: str) -> str:
    """Generate content hash for deduplication."""
    return hashlib.sha256(content.encode()).hexdigest()[:32]


def extract_summary(content: str, max_length: int = 500) -> str:
    """Extract a summary from content (first paragraph or truncated)."""
    lines = content.strip().split('\n')
    
    # Skip title lines
    summary_lines = []
    for line in lines:
        if line.startswith('#'):
            continue
        if line.strip():
            summary_lines.append(line.strip())
            if len(' '.join(summary_lines)) > max_length:
                break
    
    summary = ' '.join(summary_lines)[:max_length]
    if len(summary) < max_length and not summary:
        summary = content[:max_length]
    
    return summary or "No summary available"


def ingest_atom(
    title: str,
    content: str,
    atom_type: str = "concept",  # Valid: concept, procedure, specification, pattern, fault, reference
    source_url: Optional[str] = None,
    manufacturer: str = "general",
    difficulty: str = "beginner",
    source_document: str = "jarvis-workspace",
) -> Optional[str]:
    """
    Ingest a single knowledge atom into Neon.
    Returns atom_id if successful, None if duplicate or error.
    """
    conn = get_connection()
    cur = conn.cursor()
    
    try:
        atom_id = str(uuid.uuid4())
        
        # Check for duplicate title
        cur.execute(
            "SELECT atom_id FROM knowledge_atoms WHERE title = %s LIMIT 1",
            (title,)
        )
        if cur.fetchone():
            print(f"  ⏭️  Duplicate: {title[:50]}...")
            return None
        
        # Extract summary
        summary = extract_summary(content)
        
        # Insert new atom matching the actual schema
        cur.execute("""
            INSERT INTO knowledge_atoms 
            (atom_id, atom_type, title, summary, content, manufacturer, 
             difficulty, source_document, source_pages, source_url,
             created_by)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id
        """, (
            atom_id,
            atom_type,  # atom_type (required)
            title,
            summary,
            content,
            manufacturer,
            difficulty,
            source_document,
            [],  # source_pages (empty array)
            source_url,
            'jarvis'
        ))
        
        conn.commit()
        print(f"  ✅ Ingested: {title[:50]}...")
        return atom_id
        
    except Exception as e:
        conn.rollback()
        print(f"  ❌ Error: {e}")
        return None
    finally:
        cur.close()
        conn.close()


def parse_markdown_file(filepath: Path) -> List[Dict[str, Any]]:
    """Parse a markdown file into ingestable chunks."""
    atoms = []
    
    content = filepath.read_text()
    filename = filepath.name
    
    # Extract title from first H1
    lines = content.split('\n')
    title = filename.replace('.md', '').replace('-', ' ').title()
    for line in lines:
        if line.startswith('# '):
            title = line[2:].strip()
            break
    
    # Determine atom type and source URL
    # Valid atom_types: concept, procedure, specification, pattern, fault, reference
    if 'research' in str(filepath):
        atom_type = 'reference'  # Research docs are references
    elif 'memory' in str(filepath):
        atom_type = 'reference'  # Session notes are references
    else:
        atom_type = 'concept'  # General documents are concepts
    
    source_url = f"jarvis://workspace/{filepath.relative_to(WORKSPACE)}"
    
    atoms.append({
        'title': title,
        'content': content,
        'atom_type': atom_type,
        'source_url': source_url
    })
    
    return atoms


def ingest_memory():
    """Ingest all memory files."""
    print("\n=== Ingesting Memory Files ===\n")
    
    ingested = 0
    skipped = 0
    
    for filepath in MEMORY_DIR.glob("*.md"):
        print(f"Processing: {filepath.name}")
        atoms = parse_markdown_file(filepath)
        
        for atom in atoms:
            result = ingest_atom(
                title=atom['title'],
                content=atom['content'],
                atom_type=atom['atom_type'],
                source_url=atom['source_url'],
                source_document=filepath.name
            )
            if result:
                ingested += 1
            else:
                skipped += 1
    
    print(f"\n✅ Ingested: {ingested}, ⏭️  Skipped: {skipped}")
    return ingested


def ingest_research():
    """Ingest all research files."""
    print("\n=== Ingesting Research Files ===\n")
    
    ingested = 0
    skipped = 0
    
    research_dir = BRAIN_DIR / "research"
    if not research_dir.exists():
        print("No research directory found")
        return 0
    
    for filepath in research_dir.glob("*.md"):
        print(f"Processing: {filepath.name}")
        atoms = parse_markdown_file(filepath)
        
        for atom in atoms:
            result = ingest_atom(
                title=atom['title'],
                content=atom['content'],
                atom_type='reference',  # Research files are reference material
                source_url=atom['source_url'],
                source_document=filepath.name
            )
            if result:
                ingested += 1
            else:
                skipped += 1
    
    print(f"\n✅ Ingested: {ingested}, ⏭️  Skipped: {skipped}")
    return ingested


def ingest_ycb():
    """Ingest YCB scripts and templates."""
    print("\n=== Ingesting YCB Content ===\n")
    
    ingested = 0
    skipped = 0
    
    # Ingest template documentation
    for template_dir in (YCB_DIR / "rendering").glob("*"):
        if template_dir.is_dir():
            for filepath in template_dir.glob("*.py"):
                content = filepath.read_text()
                title = f"YCB Template: {filepath.stem}"
                
                result = ingest_atom(
                    title=title,
                    content=content,
                    atom_type='template',
                    source_url=f"ycb://templates/{filepath.name}",
                    source_document=filepath.name
                )
                if result:
                    ingested += 1
                else:
                    skipped += 1
    
    print(f"\n✅ Ingested: {ingested}, ⏭️  Skipped: {skipped}")
    return ingested


def ingest_file(filepath: str):
    """Ingest a single file."""
    path = Path(filepath)
    if not path.exists():
        print(f"File not found: {filepath}")
        return 0
    
    print(f"\n=== Ingesting: {path.name} ===\n")
    
    atoms = parse_markdown_file(path)
    ingested = 0
    
    for atom in atoms:
        result = ingest_atom(
            title=atom['title'],
            content=atom['content'],
            atom_type=atom['atom_type'],
            source_url=atom['source_url'],
            source_document=path.name
        )
        if result:
            ingested += 1
    
    return ingested


def show_stats():
    """Show current knowledge base stats."""
    conn = get_connection()
    cur = conn.cursor()
    
    print("\n=== Knowledge Base Stats ===\n")
    
    cur.execute("SELECT COUNT(*) FROM knowledge_atoms")
    total = cur.fetchone()[0]
    print(f"Total atoms: {total}")
    
    cur.execute("""
        SELECT atom_type, COUNT(*) 
        FROM knowledge_atoms 
        GROUP BY atom_type 
        ORDER BY COUNT(*) DESC
    """)
    print("\nBy atom_type:")
    for row in cur.fetchall():
        print(f"  {row[0] or 'unknown'}: {row[1]}")
    
    cur.execute("""
        SELECT created_by, COUNT(*) 
        FROM knowledge_atoms 
        GROUP BY created_by 
        ORDER BY COUNT(*) DESC
    """)
    print("\nBy source:")
    for row in cur.fetchall():
        print(f"  {row[0] or 'unknown'}: {row[1]}")
    
    cur.execute("""
        SELECT created_at::date, COUNT(*) 
        FROM knowledge_atoms 
        GROUP BY created_at::date 
        ORDER BY created_at::date DESC
        LIMIT 7
    """)
    print("\nRecent activity:")
    for row in cur.fetchall():
        print(f"  {row[0]}: {row[1]} atoms")
    
    cur.close()
    conn.close()


def main():
    parser = argparse.ArgumentParser(description='Neon Vector DB Ingestion')
    parser.add_argument('--source', choices=['memory', 'research', 'ycb', 'all'],
                        help='Source to ingest')
    parser.add_argument('--file', help='Single file to ingest')
    parser.add_argument('--stats', action='store_true', help='Show stats')
    
    args = parser.parse_args()
    
    if args.stats:
        show_stats()
        return
    
    if args.file:
        ingest_file(args.file)
        return
    
    if args.source == 'memory':
        ingest_memory()
    elif args.source == 'research':
        ingest_research()
    elif args.source == 'ycb':
        ingest_ycb()
    elif args.source == 'all':
        ingest_memory()
        ingest_research()
        ingest_ycb()
    else:
        show_stats()


if __name__ == '__main__':
    main()
