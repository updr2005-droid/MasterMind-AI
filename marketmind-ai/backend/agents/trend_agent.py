"""
MarketMind AI – Market Trend Agent
"""
from typing import Dict, Any
from backend.data.sample_data import INDIAN_EV_MARKET
from backend.utils.granite_client import call_granite


class TrendAgent:
    SYSTEM_PROMPT = (
        "You are a market trends and industry analyst. "
        "Identify emerging trends, historical patterns, and demand dynamics "
        "with clear evidence and timeline projections."
    )

    def run(self, query: str, market_id: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        if market_id == "indian_ev" or "india" in query.lower() or "ev" in query.lower():
            trends = INDIAN_EV_MARKET["trends"]
            prompt = f"Summarize the key market trends for: {query}"
            ai_response = call_granite(
                prompt=prompt,
                system_prompt=self.SYSTEM_PROMPT,
                demo_response=(
                    "Key emerging trends: Battery-as-a-Service (BaaS) gaining traction for affordability; "
                    "V2G integration pilots underway in Maharashtra; two-wheeler EV sales grew 3x in 2022. "
                    "Historical pattern shows explosive adoption following fuel price spikes. "
                    "Segment-wise: 2-wheelers dominate volume (63%), 3-wheelers lead in logistics. "
                    "Geographic concentration in top 6 states (66% of sales) creating regional opportunity."
                ),
            )
            return {
                **trends,
                "ai_summary": ai_response["text"],
                "ai_model": ai_response["model"],
                "agent": "TrendAgent",
            }

        prompt = (
            f"Identify market trends for: {query}. "
            "Include: emerging trends, historical patterns, demand trends, technology shifts, regulatory changes."
        )
        ai_response = call_granite(prompt=prompt, system_prompt=self.SYSTEM_PROMPT)
        return {
            "emerging_trends": [],
            "historical_sales": [],
            "ai_summary": ai_response["text"],
            "ai_model": ai_response["model"],
            "agent": "TrendAgent",
        }
