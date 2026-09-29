"""
MarketMind AI – Multi-Agent Orchestrator
Coordinates all specialized agents in sequence to produce complete market research.
"""
from __future__ import annotations
from typing import Dict, Any, Optional
from loguru import logger

from backend.agents.research_agent import ResearchAgent
from backend.agents.rag_agent import RAGAgent
from backend.agents.competitor_agent import CompetitorAgent
from backend.agents.sentiment_agent import SentimentAgent
from backend.agents.trend_agent import TrendAgent
from backend.agents.prediction_agent import PredictionAgent
from backend.agents.report_agent import ReportAgent


class AgentOrchestrator:
    """
    Runs the full MarketMind AI agent pipeline:
    Research → RAG → Competitor → Sentiment → Trend → Prediction → Report
    """

    def __init__(self):
        self.research_agent = ResearchAgent()
        self.rag_agent = RAGAgent()
        self.competitor_agent = CompetitorAgent()
        self.sentiment_agent = SentimentAgent()
        self.trend_agent = TrendAgent()
        self.prediction_agent = PredictionAgent()
        self.report_agent = ReportAgent()

    def run(self, query: str, market_id: str = "custom") -> Dict[str, Any]:
        """
        Execute the full research pipeline for a market query.
        Returns a combined result dict ready for the API response.
        """
        logger.info(f"Starting agent pipeline | query='{query}' | market={market_id}")
        results: Dict[str, Any] = {"query": query, "market_id": market_id, "pipeline_steps": []}

        # Step 1: Research Agent
        logger.info("[1/7] Research Agent")
        research = self.research_agent.run(query, market_id)
        results["research"] = research
        results["pipeline_steps"].append({"step": "research", "status": "complete", "agent": "ResearchAgent"})

        # Step 2: RAG Knowledge Agent
        logger.info("[2/7] RAG Agent")
        rag = self.rag_agent.run(query, context=research)
        results["rag"] = rag
        results["pipeline_steps"].append({"step": "rag", "status": "complete", "agent": "RAGAgent"})

        # Step 3: Competitor Analysis Agent
        logger.info("[3/7] Competitor Agent")
        competitors = self.competitor_agent.run(query, market_id, context=research)
        results["competitors"] = competitors
        results["pipeline_steps"].append({"step": "competitors", "status": "complete", "agent": "CompetitorAgent"})

        # Step 4: Sentiment Analysis Agent
        logger.info("[4/7] Sentiment Agent")
        sentiment = self.sentiment_agent.run(query, market_id, context=research)
        results["sentiment"] = sentiment
        results["pipeline_steps"].append({"step": "sentiment", "status": "complete", "agent": "SentimentAgent"})

        # Step 5: Market Trend Agent
        logger.info("[5/7] Trend Agent")
        trends = self.trend_agent.run(query, market_id, context=research)
        results["trends"] = trends
        results["pipeline_steps"].append({"step": "trends", "status": "complete", "agent": "TrendAgent"})

        # Step 6: Predictive Insights Agent
        logger.info("[6/7] Prediction Agent")
        predictions = self.prediction_agent.run(query, market_id, context={**research, **trends})
        results["predictions"] = predictions
        results["pipeline_steps"].append({"step": "predictions", "status": "complete", "agent": "PredictionAgent"})

        # Step 7: Report Agent
        logger.info("[7/7] Report Agent")
        report = self.report_agent.run(query, market_id, context=results)
        results["report"] = report
        results["pipeline_steps"].append({"step": "report", "status": "complete", "agent": "ReportAgent"})

        logger.info("Agent pipeline complete.")
        return results
