"""
MarketMind AI – Research Agent
Generates structured market overview from query + demo/live data.
"""
from typing import Dict, Any
from backend.data.sample_data import INDIAN_EV_MARKET
from backend.utils.granite_client import call_granite


class ResearchAgent:
    """
    Agent 1: Conduct market research.
    Returns market overview, KPIs, key drivers/challenges, and executive summary.
    """

    SYSTEM_PROMPT = (
        "You are an expert market research analyst. "
        "Analyze markets and provide structured, data-backed insights. "
        "Be concise, factual, and cite specific numbers where available."
    )

    def run(self, query: str, market_id: str = "custom") -> Dict[str, Any]:
        if market_id == "indian_ev" or "india" in query.lower() or "electric vehicle" in query.lower() or "ev" in query.lower():
            data = INDIAN_EV_MARKET
            prompt = f"Provide a brief executive summary for this market research query: {query}"
            ai_response = call_granite(
                prompt=prompt,
                system_prompt=self.SYSTEM_PROMPT,
                demo_response=data["executive_summary"],
            )
            return {
                "market_name": data["market_name"],
                "description": data["description"],
                "overview": data["overview"],
                "kpis": data["kpis"],
                "opportunities": data["opportunities"],
                "key_findings": data["key_findings"],
                "executive_summary": ai_response["text"],
                "ai_model": ai_response["model"],
                "source": ai_response["source"],
                "agent": "ResearchAgent",
            }

        # Generic market (live mode)
        prompt = (
            f"Analyze this market research query: {query}\n\n"
            "Return a structured market overview with: market name, size, growth rate, "
            "key players, market segments, key drivers, key challenges, and executive summary."
        )
        ai_response = call_granite(prompt=prompt, system_prompt=self.SYSTEM_PROMPT)
        return {
            "market_name": query,
            "executive_summary": ai_response["text"],
            "ai_model": ai_response["model"],
            "source": ai_response["source"],
            "agent": "ResearchAgent",
        }
