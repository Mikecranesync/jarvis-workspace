#!/usr/bin/env python3
"""
Gist Publisher - Python library for automatic document publishing

Usage:
    from gist_publisher import publish_document, get_gist_url
    
    url = publish_document("path/to/doc.md", "Description")
    cached = get_gist_url("path/to/doc.md")  # Returns cached URL if exists
"""

import subprocess
import os
from pathlib import Path
from typing import Optional
import json

def publish_document(
    filepath: str,
    description: str = "Auto-published document",
    public: bool = True,
    update_if_exists: bool = True
) -> str:
    """
    Publish a document to GitHub Gist.
    
    Args:
        filepath: Path to the document
        description: Gist description
        public: Whether the Gist should be public
        update_if_exists: If True and Gist exists, update it
        
    Returns:
        Gist URL
    """
    filepath = Path(filepath)
    
    if not filepath.exists():
        raise FileNotFoundError(f"Document not found: {filepath}")
    
    # Check cache for existing Gist
    cached_url = get_gist_url(str(filepath))
    if cached_url and update_if_exists:
        gist_id = cached_url.split("/")[-1]
        return update_gist(gist_id, str(filepath), description)
    
    # Create new Gist
    visibility = "--public" if public else ""
    cmd = f'gh gist create "{filepath}" {visibility} --desc "{description}"'
    
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    
    if result.returncode != 0:
        raise RuntimeError(f"Failed to create Gist: {result.stderr}")
    
    # Extract URL from output
    for line in result.stdout.split("\n") + result.stderr.split("\n"):
        if "https://gist.github.com" in line:
            gist_url = line.strip()
            _cache_url(str(filepath), gist_url)
            return gist_url
    
    raise RuntimeError("Could not extract Gist URL from output")


def update_gist(gist_id: str, filepath: str, description: str = None) -> str:
    """Update an existing Gist with new content."""
    filepath = Path(filepath)
    filename = filepath.name
    
    cmd = f'gh gist edit {gist_id} -a "{filepath}"'
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    
    if result.returncode != 0:
        # If edit fails, create new
        return publish_document(str(filepath), description or "Updated document", update_if_exists=False)
    
    return f"https://gist.github.com/{gist_id}"


def get_gist_url(filepath: str) -> Optional[str]:
    """Get cached Gist URL for a file."""
    filepath = Path(filepath)
    cache_file = filepath.parent / ".gist_urls"
    
    if not cache_file.exists():
        return None
    
    filename = filepath.name
    with open(cache_file) as f:
        for line in f:
            if line.startswith(f"{filename}:"):
                return line.split(":", 1)[1].strip()
    
    return None


def _cache_url(filepath: str, gist_url: str):
    """Cache the Gist URL for a file."""
    filepath = Path(filepath)
    cache_file = filepath.parent / ".gist_urls"
    filename = filepath.name
    
    # Read existing entries
    entries = {}
    if cache_file.exists():
        with open(cache_file) as f:
            for line in f:
                if ":" in line:
                    name, url = line.split(":", 1)
                    entries[name] = url.strip()
    
    # Update entry
    entries[filename] = gist_url
    
    # Write back
    with open(cache_file, "w") as f:
        for name, url in entries.items():
            f.write(f"{name}:{url}\n")


def publish_job_documents(job_dir: str, pattern: str = "*.md") -> dict:
    """
    Publish all matching documents in a job directory.
    
    Returns dict mapping filename -> Gist URL
    """
    job_path = Path(job_dir)
    results = {}
    
    for doc in job_path.glob(pattern):
        if doc.name.startswith("."):
            continue
        try:
            url = publish_document(str(doc), f"{job_path.name}: {doc.stem}")
            results[doc.name] = url
        except Exception as e:
            results[doc.name] = f"ERROR: {e}"
    
    return results


# CLI interface
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python gist_publisher.py <filepath> [description]")
        sys.exit(1)
    
    filepath = sys.argv[1]
    description = sys.argv[2] if len(sys.argv) > 2 else "Auto-published document"
    
    try:
        url = publish_document(filepath, description)
        print(url)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
