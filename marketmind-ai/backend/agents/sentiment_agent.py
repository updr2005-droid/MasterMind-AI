"""
MarketMind AI – Sentiment Analysis Agent
"""
from typing import Dict, Any
from backend.data.sample_data import INDIAN_EV_MARKET
from backend.utils.granite_client import call_granite


class SentimentAgent:
    SYSTEM_PROMPT = (
        "You are a customer sentiment analysis expert. "
        "Analyze customer feedback, reviews, and social data to extract sentiment patterns, "
        "key themes, and actionable insights."
    )

    def run(self, query: str, market_id: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        if market_id == "indian_ev" or "india" in query.lower() or "ev" in query.lower():
            sentiment = INDIAN_EV_MARKET["sentiment"]
            prompt = f"Summarize customer sentiment insights for: {query}"
            ai_response = call_granite(
                prompt=prompt,
                system_prompt=self.SYSTEM_PROMPT,
                demo_response=(
                    f"Analysis of {sentiment['total_reviews_analyzed']:,} reviews shows {sentiment['positive_percent']}% positive sentiment. "
                    "Primary drivers of positive sentiment: low running costs and smooth ride experience. "
                    "Primary concerns: range anxiety (67% of non-adopters), charging infrastructure gaps. "
                    "Ather Energy leads brand satisfaction; Ola Electric shows highest sentiment volatility. "
                    "Overall sentiment trend is improving as infrastructure expands."
                ),
            )
            return {
                **sentiment,
                "ai_summary": ai_response["text"],
                "ai_model": ai_response["model"],
                "agent": "SentimentAgent",
            }

        prompt = (
            f"Analyze customer sentiment for: {query}. "
            "Provide: overall sentiment score, positive/neutral/negative percentages, "
            "top positive themes, top negative themes, and key insights."
        )
        ai_response = call_granite(prompt=prompt, system_prompt=self.SYSTEM_PROMPT)
        return {
            "overall_score": 65,
            "positive_percent": 55,
            "neutral_percent": 25,
            "negative_percent": 20,
            "ai_summary": ai_response["text"],
            "ai_model": ai_response["model"],
            "agent": "SentimentAgent",
        }
