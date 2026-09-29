"""
MarketMind AI – Competitor Analysis Agent
"""
from typing import Dict, Any
from backend.data.sample_data import INDIAN_EV_MARKET
from backend.utils.granite_client import call_granite


class CompetitorAgent:
    SYSTEM_PROMPT = (
        "You are a competitive intelligence analyst. "
        "Provide structured competitor analysis with strengths, weaknesses, market positioning, "
        "and comparative insights backed by data."
    )

    def run(self, query: str, market_id: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        if market_id == "indian_ev" or "india" in query.lower() or "ev" in query.lower():
            competitors = INDIAN_EV_MARKET["competitors"]
            prompt = f"Summarize the competitive dynamics for: {query}"
            ai_response = call_granite(
                prompt=prompt,
                system_prompt=self.SYSTEM_PROMPT,
                demo_response=(
                    "The Indian EV market features intense competition across segments. "
                    "Ola Electric leads two-wheelers (34%), Tata Motors dominates passenger EVs (71%). "
                    "Key differentiators: pricing strategy, charging network, after-sales quality, and technology. "
                    "New entrants (BYD, Hyundai) are targeting premium segments while domestic players defend volume market."
                ),
            )
            return {
                "competitors": competitors,
                "total_players": len(competitors),
                "ai_summary": ai_response["text"],
                "ai_model": ai_response["model"],
                "agent": "CompetitorAgent",
            }

        prompt = f"Identify and analyze the top competitors for: {query}. Include market share, strengths, weaknesses, and positioning."
        ai_response = call_granite(prompt=prompt, system_prompt=self.SYSTEM_PROMPT)
        return {
            "competitors": [],
            "ai_summary": ai_response["text"],
            "ai_model": ai_response["model"],
            "agent": "CompetitorAgent",
        }
