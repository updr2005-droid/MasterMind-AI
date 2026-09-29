"""
MarketMind AI – RAG Pipeline
Handles document ingestion, chunking, embedding, and retrieval using ChromaDB.
"""
from __future__ import annotations
import os
import uuid
import re
from typing import List, Dict, Any, Optional
from pathlib import Path
from loguru import logger

# Lazy imports for heavy deps
_chroma_client = None
_embedding_model = None
COLLECTION_NAME = "marketmind_knowledge_base"


def _get_chroma_collection():
    global _chroma_client
    if _chroma_client is None:
        import chromadb
        from backend.config import settings
        _chroma_client = chromadb.PersistentClient(path=settings.chroma_persist_dir)
    return _chroma_client.get_or_create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"},
    )


def _get_embedding_model():
    global _embedding_model
    if _embedding_model is None:
        from sentence_transformers import SentenceTransformer
        from backend.config import settings
        logger.info(f"Loading embedding model: {settings.embedding_model}")
        _embedding_model = SentenceTransformer(settings.embedding_model)
    return _embedding_model


def chunk_text(text: str, chunk_size: int = 512, overlap: int = 64) -> List[str]:
    """Split text into overlapping word-level chunks."""
    words = text.split()
    chunks = []
    start = 0
    while start < len(words):
        end = min(start + chunk_size, len(words))
        chunks.append(" ".join(words[start:end]))
        if end == len(words):
            break
        start += chunk_size - overlap
    return chunks


def embed_texts(texts: List[str]) -> List[List[float]]:
    model = _get_embedding_model()
    return model.encode(texts, show_progress_bar=False).tolist()


def ingest_document(
    content: str,
    metadata: Dict[str, Any],
    doc_id: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Chunk a document and add it to the ChromaDB collection.
    Returns summary of ingestion.
    """
    collection = _get_chroma_collection()
    doc_id = doc_id or str(uuid.uuid4())
    chunks = chunk_text(content)

    if not chunks:
        return {"doc_id": doc_id, "chunks_added": 0, "status": "empty"}

    embeddings = embed_texts(chunks)
    ids = [f"{doc_id}_chunk_{i}" for i in range(len(chunks))]
    metadatas = [{**metadata, "doc_id": doc_id, "chunk_index": i} for i in range(len(chunks))]

    collection.add(
        ids=ids,
        embeddings=embeddings,
        documents=chunks,
        metadatas=metadatas,
    )
    logger.info(f"Ingested doc '{doc_id}': {len(chunks)} chunks")
    return {"doc_id": doc_id, "chunks_added": len(chunks), "status": "success"}


def retrieve(
    query: str,
    n_results: int = 5,
    where: Optional[Dict] = None,
) -> List[Dict[str, Any]]:
    """
    Retrieve top-k relevant chunks from ChromaDB for a query.
    Returns list of {text, source, score, metadata}.
    """
    collection = _get_chroma_collection()
    count = collection.count()
    if count == 0:
        return []

    query_embedding = embed_texts([query])[0]
    kwargs = {"query_embeddings": [query_embedding], "n_results": min(n_results, count)}
    if where:
        kwargs["where"] = where

    results = collection.query(**kwargs)

    retrieved = []
    for i, doc in enumerate(results["documents"][0]):
        meta = results["metadatas"][0][i]
        distance = results["distances"][0][i] if "distances" in results else None
        score = round(1 - distance, 4) if distance is not None else None
        retrieved.append({
            "text": doc,
            "source": meta.get("source", meta.get("title", "Unknown")),
            "title": meta.get("title", ""),
            "doc_id": meta.get("doc_id", ""),
            "score": score,
            "metadata": meta,
        })
    return retrieved


def load_demo_knowledge_base() -> Dict[str, Any]:
    """
    Pre-load the demo Indian EV knowledge base docs into ChromaDB.
    Skips if already loaded.
    """
    from backend.data.sample_data import INDIAN_EV_MARKET
    collection = _get_chroma_collection()

    # Check if already loaded
    existing = collection.get(where={"doc_id": "doc_001"})
    if existing["ids"]:
        logger.info("Demo knowledge base already loaded — skipping.")
        return {"status": "already_loaded", "docs": len(INDIAN_EV_MARKET["rag_knowledge_base"])}

    loaded = 0
    for doc in INDIAN_EV_MARKET["rag_knowledge_base"]:
        result = ingest_document(
            content=doc["content"],
            metadata={
                "title": doc["title"],
                "source": doc["source"],
                "year": doc["year"],
                "market": "indian_ev",
            },
            doc_id=doc["doc_id"],
        )
        if result["status"] == "success":
            loaded += 1

    logger.info(f"Demo knowledge base loaded: {loaded} documents")
    return {"status": "loaded", "docs": loaded}


def parse_uploaded_file(file_path: str, filename: str) -> str:
    """Extract text content from uploaded PDF, DOCX, CSV, or TXT."""
    ext = Path(filename).suffix.lower()
    try:
        if ext == ".pdf":
            from pypdf import PdfReader
            reader = PdfReader(file_path)
            return "\n".join(page.extract_text() or "" for page in reader.pages)
        elif ext == ".docx":
            from docx import Document
            doc = Document(file_path)
            return "\n".join(para.text for para in doc.paragraphs)
        elif ext == ".csv":
            import pandas as pd
            df = pd.read_csv(file_path)
            return df.to_string(index=False)
        elif ext == ".txt":
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                return f.read()
        else:
            return ""
    except Exception as e:
        logger.error(f"File parse error for {filename}: {e}")
        return ""


def get_collection_stats() -> Dict[str, Any]:
    """Return stats about the current knowledge base."""
    try:
        collection = _get_chroma_collection()
        count = collection.count()
        return {"total_chunks": count, "collection": COLLECTION_NAME, "status": "ok"}
    except Exception as e:
        return {"total_chunks": 0, "collection": COLLECTION_NAME, "status": "error", "error": str(e)}
