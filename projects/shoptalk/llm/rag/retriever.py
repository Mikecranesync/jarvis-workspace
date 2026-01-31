#!/usr/bin/env python3
"""
ShopTalk RAG (Retrieval-Augmented Generation) Pipeline
Enhances LLM responses with equipment knowledge base.
"""

import json
import numpy as np
from pathlib import Path
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

# Simple embedding using TF-IDF (no external dependencies)
# For production, use sentence-transformers or similar

@dataclass
class Document:
    """A document in the knowledge base."""
    id: str
    content: str
    metadata: Dict
    embedding: Optional[np.ndarray] = None


class SimpleEmbedder:
    """Simple TF-IDF based embedder for edge deployment."""
    
    def __init__(self):
        self.vocabulary = {}
        self.idf = {}
        self.fitted = False
    
    def fit(self, documents: List[str]):
        """Build vocabulary and IDF from documents."""
        # Build vocabulary
        doc_freq = {}
        for doc in documents:
            words = set(self._tokenize(doc))
            for word in words:
                doc_freq[word] = doc_freq.get(word, 0) + 1
                if word not in self.vocabulary:
                    self.vocabulary[word] = len(self.vocabulary)
        
        # Calculate IDF
        n_docs = len(documents)
        for word, freq in doc_freq.items():
            self.idf[word] = np.log(n_docs / (freq + 1)) + 1
        
        self.fitted = True
    
    def _tokenize(self, text: str) -> List[str]:
        """Simple tokenization."""
        # Lowercase and split on non-alphanumeric
        import re
        return re.findall(r'\b\w+\b', text.lower())
    
    def embed(self, text: str) -> np.ndarray:
        """Embed a single text."""
        if not self.fitted:
            raise ValueError("Embedder not fitted. Call fit() first.")
        
        words = self._tokenize(text)
        word_counts = {}
        for word in words:
            word_counts[word] = word_counts.get(word, 0) + 1
        
        # TF-IDF vector
        vector = np.zeros(len(self.vocabulary))
        for word, count in word_counts.items():
            if word in self.vocabulary:
                tf = count / len(words) if words else 0
                idf = self.idf.get(word, 1)
                vector[self.vocabulary[word]] = tf * idf
        
        # Normalize
        norm = np.linalg.norm(vector)
        if norm > 0:
            vector = vector / norm
        
        return vector


class KnowledgeBase:
    """Knowledge base with retrieval capabilities."""
    
    def __init__(self, kb_path: str = None):
        self.documents: List[Document] = []
        self.embedder = SimpleEmbedder()
        
        if kb_path:
            self.load(kb_path)
    
    def load(self, kb_path: str):
        """Load knowledge base from JSON file."""
        with open(kb_path) as f:
            kb_data = json.load(f)
        
        # Convert to documents
        docs = []
        
        # Equipment knowledge
        for eq_type, config in kb_data.get("equipment", {}).items():
            # Add equipment overview
            doc = Document(
                id=f"equipment_{eq_type}",
                content=f"Equipment: {eq_type}. Sensors: {', '.join(config.get('sensors', []))}.",
                metadata={"type": "equipment", "equipment": eq_type}
            )
            docs.append(doc)
            
            # Add fault patterns
            for fault in config.get("faults", []):
                symptoms = ", ".join([f"{k}={v}" for k, v in fault.get("symptoms", {}).items()])
                actions = ". ".join(fault.get("actions", []))
                doc = Document(
                    id=f"fault_{eq_type}_{fault['name']}",
                    content=f"Fault: {fault['name']} on {eq_type}. Symptoms: {symptoms}. Diagnosis: {fault['diagnosis']}. Actions: {actions}",
                    metadata={"type": "fault", "equipment": eq_type, "fault": fault["name"]}
                )
                docs.append(doc)
        
        # Fault patterns
        for pattern in kb_data.get("fault_patterns", []):
            symptoms = ", ".join([f"{k}={v}" for k, v in pattern.get("symptoms", {}).items()])
            actions = ". ".join(pattern.get("actions", []))
            doc = Document(
                id=f"pattern_{pattern['equipment']}_{pattern['fault_name']}",
                content=f"Pattern: {pattern['fault_name']}. Equipment: {pattern['equipment']}. Symptoms: {symptoms}. Diagnosis: {pattern['diagnosis']}. Actions: {actions}",
                metadata={"type": "pattern", "equipment": pattern["equipment"]}
            )
            docs.append(doc)
        
        # Best practices
        for i, practice in enumerate(kb_data.get("best_practices", [])):
            doc = Document(
                id=f"practice_{i}",
                content=f"Best practice: {practice}",
                metadata={"type": "best_practice"}
            )
            docs.append(doc)
        
        # General knowledge
        for key, value in kb_data.get("general_knowledge", {}).items():
            doc = Document(
                id=f"general_{key}",
                content=f"{key}: {value}",
                metadata={"type": "general"}
            )
            docs.append(doc)
        
        self.documents = docs
        
        # Fit embedder and embed documents
        texts = [d.content for d in self.documents]
        self.embedder.fit(texts)
        
        for doc in self.documents:
            doc.embedding = self.embedder.embed(doc.content)
        
        print(f"Loaded {len(self.documents)} documents into knowledge base")
    
    def add_document(self, doc_id: str, content: str, metadata: Dict = None):
        """Add a document to the knowledge base."""
        doc = Document(
            id=doc_id,
            content=content,
            metadata=metadata or {},
            embedding=self.embedder.embed(content) if self.embedder.fitted else None
        )
        self.documents.append(doc)
    
    def search(self, query: str, top_k: int = 3, 
               filter_type: str = None) -> List[Tuple[Document, float]]:
        """Search for relevant documents."""
        query_embedding = self.embedder.embed(query)
        
        results = []
        for doc in self.documents:
            if filter_type and doc.metadata.get("type") != filter_type:
                continue
            
            if doc.embedding is not None:
                score = np.dot(query_embedding, doc.embedding)
                results.append((doc, score))
        
        # Sort by score descending
        results.sort(key=lambda x: x[1], reverse=True)
        
        return results[:top_k]
    
    def get_context(self, query: str, top_k: int = 3) -> str:
        """Get context string for RAG."""
        results = self.search(query, top_k)
        
        if not results:
            return ""
        
        context_parts = []
        for doc, score in results:
            if score > 0.1:  # Relevance threshold
                context_parts.append(f"[{doc.metadata.get('type', 'info')}] {doc.content}")
        
        return "\n\n".join(context_parts)


class RAGPipeline:
    """Complete RAG pipeline for ShopTalk."""
    
    def __init__(self, kb_path: str, llm_fn=None):
        """
        Initialize RAG pipeline.
        
        Args:
            kb_path: Path to knowledge base JSON
            llm_fn: Function that takes (prompt, context) and returns response
        """
        self.kb = KnowledgeBase(kb_path)
        self.llm_fn = llm_fn
    
    def query(self, question: str, top_k: int = 3) -> Dict:
        """
        Run RAG query.
        
        Args:
            question: User question
            top_k: Number of documents to retrieve
            
        Returns:
            Dict with context, response, and sources
        """
        # Retrieve context
        context = self.kb.get_context(question, top_k)
        sources = self.kb.search(question, top_k)
        
        # Build prompt
        if context:
            augmented_prompt = f"""Use the following context to help answer the question.

Context:
{context}

Question: {question}

Answer based on the context and your knowledge of industrial equipment maintenance."""
        else:
            augmented_prompt = question
        
        # Generate response
        if self.llm_fn:
            response = self.llm_fn(augmented_prompt)
        else:
            response = f"[No LLM configured. Context retrieved:]\n\n{context}"
        
        return {
            "question": question,
            "context": context,
            "response": response,
            "sources": [{"id": doc.id, "score": score} for doc, score in sources]
        }


if __name__ == "__main__":
    # Test the RAG pipeline
    kb_path = Path(__file__).parent.parent / "data" / "knowledge_base.json"
    
    if kb_path.exists():
        print("Testing RAG Pipeline")
        print("=" * 40)
        
        kb = KnowledgeBase(str(kb_path))
        
        # Test queries
        queries = [
            "What causes high motor current on a conveyor?",
            "How do I fix a belt jam?",
            "Pump cavitation symptoms",
            "Safety procedures for maintenance"
        ]
        
        for query in queries:
            print(f"\nQuery: {query}")
            results = kb.search(query, top_k=2)
            for doc, score in results:
                print(f"  [{score:.3f}] {doc.content[:100]}...")
    else:
        print(f"Knowledge base not found at {kb_path}")
        print("Run generate_training_data.py first to create it.")
