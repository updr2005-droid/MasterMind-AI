"""
MarketMind AI – FastAPI Backend
Exposes REST endpoints consumed by the frontend dashboard.
"""
from __future__ import annotations
import os
import uuid
import shutil
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, HTTPException, UploadFile, File, Form, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel
from loguru import logger

from backend.config import settings
from backend.agents.orchestrator import AgentOrchestrator
from backend.agents.rag_agent import RAGAgent
from backend.rag.pipeline import (
    ingest_document,
    load_demo_knowledge_base,
    retrieve,
    parse_uploaded_file,
    get_collection_stats,
)

# ── App Setup ──────────────────────────────────────────────────────────────────
app = FastAPI(
    title="MarketMind AI",
    description="Intelligent Agentic Market Research & Business Intelligence Assistant",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve frontend static files
FRONTEND_DIR = Path(__file__).parent.parent / "frontend"
if FRONTEND_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(FRONTEND_DIR / "assets")), name="static")

UPLOAD_DIR = Path(__file__).parent.parent / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)

# Singletons
orchestrator = AgentOrchestrator()
rag_agent = RAGAgent()


# ── Pydantic Models ────────────────────────────────────────────────────────────
class ResearchRequest(BaseModel):
    query: str
    market_id: Optional[str] = "indian_ev"

class ChatRequest(BaseModel):
    message: str
    context: Optional[str] = ""

class RAGQueryRequest(BaseModel):
    query: str
    n_results: Optional[int] = 5


# ── Startup ────────────────────────────────────────────────────────────────────
@app.on_event("startup")
async def startup_event():
    logger.info("MarketMind AI starting up…")
    if settings.demo_mode:
        try:
            result = load_demo_knowledge_base()
            logger.info(f"Demo KB: {result}")
        except Exception as e:
            logger.warning(f"Demo KB load failed (non-fatal): {e}")


# ── Root ───────────────────────────────────────────────────────────────────────
@app.get("/")
async def root():
    index = FRONTEND_DIR / "index.html"
    if index.exists():
        return FileResponse(str(index))
    return {"message": "MarketMind AI API", "docs": "/docs", "status": "running"}


@app.get("/health")
async def health():
    kb_stats = get_collection_stats()
    return {
        "status": "healthy",
        "demo_mode": settings.demo_mode,
        "model": settings.granite_model_id,
        "knowledge_base": kb_stats,
    }


# ── Core Research Pipeline ─────────────────────────────────────────────────────
@app.post("/api/research")
async def run_research(request: ResearchRequest):
    """
    Run the full 7-agent pipeline: Research → RAG → Competitor → Sentiment →
    Trend → Prediction → Report.
    """
    if not request.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty")
    try:
        results = orchestrator.run(query=request.query, market_id=request.market_id)
        return {"success": True, "data": results}
    except Exception as e:
        logger.error(f"Research pipeline error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/demo")
async def get_demo_data():
    """Return the full Indian EV demo dataset directly (fast, no LLM call)."""
    from backend.data.sample_data import INDIAN_EV_MARKET
    return {"success": True, "data": INDIAN_EV_MARKET}


# ── RAG Endpoints ──────────────────────────────────────────────────────────────
@app.post("/api/rag/query")
async def rag_query(request: RAGQueryRequest):
    """Query the knowledge base using RAG."""
    result = rag_agent.run(query=request.query, n_results=request.n_results)
    return {"success": True, "data": result}


@app.post("/api/rag/upload")
async def upload_document(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    title: str = Form(default=""),
    source: str = Form(default="User Upload"),
):
    """Upload and ingest a PDF, CSV, TXT, or DOCX into the RAG knowledge base."""
    ext = Path(file.filename).suffix.lower().lstrip(".")
    if ext not in settings.allowed_extensions_list:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type '.{ext}'. Allowed: {settings.allowed_extensions_list}",
        )

    # Save to disk
    file_id = str(uuid.uuid4())
    dest = UPLOAD_DIR / f"{file_id}_{file.filename}"
    with open(dest, "wb") as f:
        shutil.copyfileobj(file.file, f)

    # Ingest in background
    def _ingest():
        text = parse_uploaded_file(str(dest), file.filename)
        if text.strip():
            result = ingest_document(
                content=text,
                metadata={
                    "title": title or file.filename,
                    "source": source,
                    "filename": file.filename,
                },
                doc_id=file_id,
            )
            logger.info(f"Ingested upload: {result}")

    background_tasks.add_task(_ingest)

    return {
        "success": True,
        "message": f"File '{file.filename}' accepted for ingestion.",
        "file_id": file_id,
    }


@app.get("/api/rag/stats")
async def kb_stats():
    return {"success": True, "data": get_collection_stats()}


@app.post("/api/rag/load-demo")
async def load_demo_kb():
    """Manually trigger loading the demo knowledge base."""
    result = load_demo_knowledge_base()
    return {"success": True, "data": result}


# ── Chat Endpoint ──────────────────────────────────────────────────────────────
@app.post("/api/chat")
async def chat(request: ChatRequest):
    """
    Conversational Q&A: answer a question using RAG retrieval + Granite.
    """
    result = rag_agent.run(query=request.message)
    return {"success": True, "data": result}


# ── Individual Agent Endpoints ─────────────────────────────────────────────────
@app.post("/api/agents/research")
async def run_research_agent(request: ResearchRequest):
    from backend.agents.research_agent import ResearchAgent
    return {"success": True, "data": ResearchAgent().run(request.query, request.market_id)}

@app.post("/api/agents/competitors")
async def run_competitor_agent(request: ResearchRequest):
    from backend.agents.competitor_agent import CompetitorAgent
    return {"success": True, "data": CompetitorAgent().run(request.query, request.market_id)}

@app.post("/api/agents/sentiment")
async def run_sentiment_agent(request: ResearchRequest):
    from backend.agents.sentiment_agent import SentimentAgent
    return {"success": True, "data": SentimentAgent().run(request.query, request.market_id)}

@app.post("/api/agents/trends")
async def run_trend_agent(request: ResearchRequest):
    from backend.agents.trend_agent import TrendAgent
    return {"success": True, "data": TrendAgent().run(request.query, request.market_id)}

@app.post("/api/agents/predictions")
async def run_prediction_agent(request: ResearchRequest):
    from backend.agents.prediction_agent import PredictionAgent
    return {"success": True, "data": PredictionAgent().run(request.query, request.market_id)}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "backend.main:app",
        host=settings.backend_host,
        port=settings.backend_port,
        reload=settings.debug,
    )
