"""
MarketMind AI – Report Generation Agent
Synthesizes all agent outputs into a structured executive report.
"""
from typing import Dict, Any
import datetime
from backend.data.sample_data import INDIAN_EV_MARKET
from backend.utils.granite_client import call_granite


class ReportAgent:
    SYSTEM_PROMPT = (
        "You are a senior business intelligence consultant. "
        "Synthesize market research findings into clear, actionable executive reports. "
        "Be precise, use data points, and structure your output professionally."
    )

    def run(self, query: str, market_id: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        prompt = (
            f"Generate an executive report summary for: {query}. "
            "Include: executive summary, key findings, strategic recommendations, and conclusion."
        )

        if market_id == "indian_ev" or "india" in query.lower() or "ev" in query.lower():
            demo_summary = INDIAN_EV_MARKET["executive_summary"]
            ai_response = call_granite(
                prompt=prompt,
                system_prompt=self.SYSTEM_PROMPT,
                demo_response=demo_summary,
            )
            return {
                "title": f"Market Intelligence Report: {INDIAN_EV_MARKET['market_name']}",
                "generated_at": datetime.datetime.now().isoformat(),
                "executive_summary": ai_response["text"],
                "key_findings": INDIAN_EV_MARKET["key_findings"],
                "opportunities": INDIAN_EV_MARKET["opportunities"],
                "risks": INDIAN_EV_MARKET["forecast"]["risks"],
                "sources": [
                    "IBM Granite AI (ibm/granite-13b-instruct-v2)",
                    "SMEV Q4 2024 Market Report",
                    "FAME II Policy Documents – Ministry of Heavy Industries",
                    "BloombergNEF Battery Price Survey 2024",
                    "JMK Research Consumer EV Adoption Survey 2024",
                    "Bureau of Energy Efficiency (BEE) EV Charging Report 2024",
                    "RAG Knowledge Base (uploaded documents)",
                ],
                "ai_model": ai_response["model"],
                "agent": "ReportAgent",
                "pipeline_summary": _build_pipeline_summary(context),
            }

        ai_response = call_granite(prompt=prompt, system_prompt=self.SYSTEM_PROMPT)
        return {
            "title": f"Market Intelligence Report: {query}",
            "generated_at": datetime.datetime.now().isoformat(),
            "executive_summary": ai_response["text"],
            "key_findings": [],
            "sources": ["IBM Granite AI", "RAG Knowledge Base"],
            "ai_model": ai_response["model"],
            "agent": "ReportAgent",
        }


def _build_pipeline_summary(context: Dict[str, Any]) -> Dict[str, Any]:
    """Extract high-level summary of all pipeline steps for the report."""
    if not context:
        return {}
    steps = context.get("pipeline_steps", [])
    return {
        "total_steps": len(steps),
        "agents_used": [s["agent"] for s in steps],
        "all_complete": all(s["status"] == "complete" for s in steps),
    }
