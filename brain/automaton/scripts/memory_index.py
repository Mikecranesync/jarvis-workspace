#!/usr/bin/env python3
"""
Memory Index — Semantic Search for Automaton Knowledge

Indexes all brain/ and memory/ files for fast semantic search.
Uses simple TF-IDF for now, can be upgraded to embeddings later.
"""

import json
import re
import math
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from collections import defaultdict
from datetime import datetime

WORKSPACE = Path("/root/jarvis-workspace")
BRAIN_DIR = WORKSPACE / "brain"
MEMORY_DIR = WORKSPACE / "memory"
INDEX_FILE = BRAIN_DIR / "automaton" / "memory_index.json"


class MemoryIndex:
    """Simple TF-IDF based memory search."""
    
    def __init__(self):
        self.documents: Dict[str, str] = {}  # path -> content
        self.word_doc_freq: Dict[str, int] = defaultdict(int)  # word -> num docs containing it
        self.doc_word_freq: Dict[str, Dict[str, int]] = {}  # doc -> word -> count
        self.total_docs = 0
        
    def _tokenize(self, text: str) -> List[str]:
        """Simple tokenization."""
        text = text.lower()
        # Remove markdown formatting
        text = re.sub(r'[#*`\[\]\(\)]', ' ', text)
        # Split on non-alphanumeric
        tokens = re.findall(r'[a-z0-9]+', text)
        # Filter short tokens
        return [t for t in tokens if len(t) > 2]
    
    def index_file(self, path: Path) -> bool:
        """Index a single file."""
        try:
            content = path.read_text()
            rel_path = str(path.relative_to(WORKSPACE))
            
            self.documents[rel_path] = content
            tokens = self._tokenize(content)
            
            # Count word frequencies in this document
            word_freq = defaultdict(int)
            for token in tokens:
                word_freq[token] += 1
            
            self.doc_word_freq[rel_path] = dict(word_freq)
            
            # Update document frequencies
            for word in set(tokens):
                self.word_doc_freq[word] += 1
            
            return True
        except Exception as e:
            print(f"Error indexing {path}: {e}")
            return False
    
    def build_index(self) -> Dict:
        """Build index from all brain/ and memory/ files."""
        self.documents = {}
        self.word_doc_freq = defaultdict(int)
        self.doc_word_freq = {}
        
        indexed = 0
        
        # Index brain/ files
        for path in BRAIN_DIR.rglob("*.md"):
            if self.index_file(path):
                indexed += 1
        
        # Index memory/ files
        for path in MEMORY_DIR.rglob("*.md"):
            if self.index_file(path):
                indexed += 1
        
        self.total_docs = len(self.documents)
        
        # Save index
        self._save_index()
        
        return {
            "indexed": indexed,
            "total_docs": self.total_docs,
            "unique_words": len(self.word_doc_freq)
        }
    
    def _save_index(self):
        """Save index to disk."""
        index_data = {
            "updated": datetime.utcnow().isoformat(),
            "total_docs": self.total_docs,
            "documents": list(self.documents.keys()),
            "word_doc_freq": dict(self.word_doc_freq),
            "doc_word_freq": self.doc_word_freq
        }
        
        INDEX_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(INDEX_FILE, "w") as f:
            json.dump(index_data, f, indent=2)
    
    def _load_index(self) -> bool:
        """Load index from disk."""
        if not INDEX_FILE.exists():
            return False
        
        try:
            with open(INDEX_FILE) as f:
                data = json.load(f)
            
            self.total_docs = data["total_docs"]
            self.word_doc_freq = defaultdict(int, data["word_doc_freq"])
            self.doc_word_freq = data["doc_word_freq"]
            
            # Reload document content
            for doc_path in data["documents"]:
                full_path = WORKSPACE / doc_path
                if full_path.exists():
                    self.documents[doc_path] = full_path.read_text()
            
            return True
        except Exception as e:
            print(f"Error loading index: {e}")
            return False
    
    def _tfidf_score(self, query_tokens: List[str], doc_path: str) -> float:
        """Calculate TF-IDF score for a document given query."""
        if doc_path not in self.doc_word_freq:
            return 0.0
        
        doc_words = self.doc_word_freq[doc_path]
        total_words = sum(doc_words.values())
        
        score = 0.0
        for token in query_tokens:
            tf = doc_words.get(token, 0) / total_words if total_words > 0 else 0
            
            # IDF with smoothing
            doc_freq = self.word_doc_freq.get(token, 0)
            idf = math.log((self.total_docs + 1) / (doc_freq + 1)) + 1
            
            score += tf * idf
        
        return score
    
    def search(self, query: str, limit: int = 10) -> List[Tuple[str, float, str]]:
        """Search for documents matching query."""
        # Ensure index is loaded
        if not self.documents:
            if not self._load_index():
                self.build_index()
        
        query_tokens = self._tokenize(query)
        
        if not query_tokens:
            return []
        
        # Score all documents
        scores = []
        for doc_path in self.documents:
            score = self._tfidf_score(query_tokens, doc_path)
            if score > 0:
                # Get snippet
                content = self.documents[doc_path]
                snippet = self._get_snippet(content, query_tokens)
                scores.append((doc_path, score, snippet))
        
        # Sort by score
        scores.sort(key=lambda x: -x[1])
        
        return scores[:limit]
    
    def _get_snippet(self, content: str, query_tokens: List[str], 
                     max_length: int = 200) -> str:
        """Extract a relevant snippet from content."""
        content_lower = content.lower()
        
        # Find first occurrence of any query token
        best_pos = len(content)
        for token in query_tokens:
            pos = content_lower.find(token)
            if pos != -1 and pos < best_pos:
                best_pos = pos
        
        if best_pos == len(content):
            best_pos = 0
        
        # Get context around match
        start = max(0, best_pos - 50)
        end = min(len(content), best_pos + max_length)
        
        snippet = content[start:end].strip()
        if start > 0:
            snippet = "..." + snippet
        if end < len(content):
            snippet = snippet + "..."
        
        return snippet.replace("\n", " ")


def main():
    import sys
    
    index = MemoryIndex()
    
    if len(sys.argv) < 2:
        print("Usage: memory_index.py [build|search <query>|stats]")
        sys.exit(1)
    
    cmd = sys.argv[1]
    
    if cmd == "build":
        result = index.build_index()
        print(f"Indexed {result['indexed']} files")
        print(f"Total documents: {result['total_docs']}")
        print(f"Unique words: {result['unique_words']}")
    
    elif cmd == "search":
        if len(sys.argv) < 3:
            print("Usage: memory_index.py search <query>")
            sys.exit(1)
        
        query = " ".join(sys.argv[2:])
        results = index.search(query)
        
        print(f"Results for: {query}\n")
        for path, score, snippet in results:
            print(f"[{score:.3f}] {path}")
            print(f"  {snippet}\n")
    
    elif cmd == "stats":
        if not index._load_index():
            print("No index found. Run 'build' first.")
            sys.exit(1)
        
        print(f"Total documents: {index.total_docs}")
        print(f"Unique words: {len(index.word_doc_freq)}")
        print(f"Documents indexed:")
        for doc in sorted(index.documents.keys()):
            print(f"  - {doc}")


if __name__ == "__main__":
    main()
