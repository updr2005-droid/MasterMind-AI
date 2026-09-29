"""
MarketMind AI – RAG Knowledge Agent
Retrieves relevant documents and synthesizes a grounded answer.
"""
from typing import Dict, Any, List
from backend.rag.pipeline import retrieve, get_collection_stats
from backend.utils.granite_client import call_granite


class RAGAgent:
    """
    Agent 2: Retrieve relevant knowledge base chunks and synthesize a RAG answer.
    Shows sources and avoids hallucination by grounding in retrieved docs.
    """

    SYSTEM_PROMPT = (
        "You are a knowledge synthesis expert. "
        "Answer questions using ONLY information from the provided document excerpts. "
        "If information is not in the documents, say so explicitly. "
        "Always cite sources."
    )

    def run(self, query: str, context: Dict[str, Any] = None, n_results: int = 5) -> Dict[str, Any]:
        # Retrieve from vector DB
        chunks = retrieve(query, n_results=n_results)

        if not chunks:
            return {
                "answer": "No documents found in the knowledge base. Load the demo data or upload documents via the Knowledge Base page.",
                "sources": [],
                "chunks_used": 0,
                "grounded": False,
                "agent": "RAGAgent",
            }

        # Build context for LLM
        context_text = "\n\n".join(
            f"[Source: {c['source']}]\n{c['text']}" for c in chunks
        )
        prompt = (
            f"Based on the following document excerpts, answer this question:\n"
            f"Question: {query}\n\n"
            f"Documents:\n{context_text[:3000]}\n\n"
            f"Answer (cite sources):"
        )

        demo_answer = (
            f"Based on {len(chunks)} retrieved document(s) from the knowledge base:\n\n"
            + "\n".join(f"• {c['title']}: {c['text'][:120]}..." for c in chunks[:3])
        )

        ai_response = call_granite(
            prompt=prompt,
            system_prompt=self.SYSTEM_PROMPT,
            demo_response=demo_answer,
        )

        sources = [
            {
                "title": c.get("title", ""),
                "source": c.get("source", ""),
                "excerpt": c["text"][:200] + "...",
                "relevance_score": c.get("score"),
                "doc_id": c.get("doc_id", ""),
            }
            for c in chunks
        ]

        return {
            "answer": ai_response["text"],
            "sources": sources,
            "chunks_used": len(chunks),
            "grounded": True,
            "ai_model": ai_response["model"],
            "agent": "RAGAgent",
        }

    def get_kb_stats(self) -> Dict[str, Any]:
        return get_collection_stats()
