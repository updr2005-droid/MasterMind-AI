"""
MarketMind AI – IBM Granite / watsonx.ai LLM wrapper
Handles both live watsonx.ai calls and demo mode simulation.
"""
from __future__ import annotations
import os
import json
import time
from typing import Any, Dict, Optional
from loguru import logger

# Lazy import — only needed when not in demo mode
_watsonx_client = None


def _get_watsonx_client():
    global _watsonx_client
    if _watsonx_client is None:
        try:
            from ibm_watsonx_ai import APIClient, Credentials
            from backend.config import settings
            credentials = Credentials(
                url=settings.watsonx_url,
                api_key=settings.watsonx_api_key,
            )
            _watsonx_client = APIClient(credentials)
        except Exception as e:
            logger.warning(f"watsonx.ai client init failed: {e}")
            raise
    return _watsonx_client


def call_granite(
    prompt: str,
    system_prompt: str = "",
    max_tokens: int = 1024,
    temperature: float = 0.3,
    demo_response: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Call IBM Granite via watsonx.ai.
    Falls back to demo_response when DEMO_MODE=true.
    Returns dict with 'text', 'model', 'tokens_used', 'source'.
    """
    from backend.config import settings

    if settings.demo_mode:
        # Simulate slight latency for realism in demos
        time.sleep(0.4)
        response_text = demo_response or _simulate_granite_response(prompt)
        return {
            "text": response_text,
            "model": f"{settings.granite_model_id} (demo)",
            "tokens_used": len(prompt.split()) + len(response_text.split()),
            "source": "demo_simulation",
        }

    # --- Live watsonx.ai call ---
    try:
        from ibm_watsonx_ai.foundation_models import ModelInference
        from ibm_watsonx_ai.metanames import GenTextParamsMetaNames as GenParams

        client = _get_watsonx_client()
        model = ModelInference(
            model_id=settings.granite_model_id,
            api_client=client,
            project_id=settings.watsonx_project_id,
            params={
                GenParams.MAX_NEW_TOKENS: max_tokens,
                GenParams.TEMPERATURE: temperature,
                GenParams.STOP_SEQUENCES: ["<|endoftext|>"],
            },
        )

        full_prompt = f"<|system|>\n{system_prompt}\n<|user|>\n{prompt}\n<|assistant|>\n" if system_prompt else prompt
        response = model.generate_text(prompt=full_prompt)

        return {
            "text": response,
            "model": settings.granite_model_id,
            "tokens_used": len(full_prompt.split()) + len(response.split()),
            "source": "watsonx_live",
        }
    except Exception as e:
        logger.error(f"watsonx.ai call failed: {e}")
        return {
            "text": f"[Error calling IBM Granite: {str(e)}]",
            "model": settings.granite_model_id,
            "tokens_used": 0,
            "source": "error",
            "error": str(e),
        }


def _simulate_granite_response(prompt: str) -> str:
    """
    Returns a realistic demo response based on prompt keywords.
    Used in demo mode to avoid requiring live credentials.
    """
    prompt_lower = prompt.lower()
    if "executive summary" in prompt_lower or "summarize" in prompt_lower:
        return (
            "Based on comprehensive market analysis, the Indian Electric Vehicle market represents "
            "one of the most dynamic growth opportunities in the Asia-Pacific region. The market is "
            "driven by a powerful convergence of supportive government policy, rising conventional fuel "
            "costs, and rapidly falling battery technology costs. With a projected CAGR of 49.5% through "
            "2030, the market offers significant opportunities for investors, manufacturers, and technology "
            "providers who can navigate the infrastructure and supply chain challenges ahead."
        )
    elif "competitor" in prompt_lower or "competition" in prompt_lower:
        return (
            "The competitive landscape is dominated by Ola Electric in the two-wheeler segment with 34% "
            "market share, while Tata Motors commands 71% of the passenger EV segment. Ather Energy "
            "maintains a premium positioning with superior technology ratings. New entrants including BYD "
            "and Hyundai are intensifying competition in the ₹15L+ segment. The market is expected to "
            "consolidate around 3-4 major players in each segment over the next 3 years."
        )
    elif "sentiment" in prompt_lower or "review" in prompt_lower:
        return (
            "Customer sentiment analysis across 45,280 reviews reveals broadly positive market reception "
            "(61% positive). The primary positive driver is operational cost savings — customers report "
            "saving ₹3,000-5,000 per month compared to petrol vehicles. Key concerns include range anxiety "
            "(cited by 67% of non-adopters) and inadequate charging infrastructure in Tier-2 cities. "
            "After-sales service quality is the leading brand loyalty risk factor."
        )
    elif "trend" in prompt_lower or "forecast" in prompt_lower or "predict" in prompt_lower:
        return (
            "Emerging trends indicate Battery-as-a-Service (BaaS) models and V2G integration as the "
            "next major disruption vectors. The market is projected to grow from $4.89B in 2024 to "
            "$113.99B by 2030. Key demand catalysts include FAME III policy launch, battery cost "
            "reduction below $70/kWh, and expansion of fast-charging networks. Commercial fleet "
            "electrification is expected to contribute 35% of volume by 2026."
        )
    else:
        return (
            "Analysis complete. The Indian EV market shows strong fundamentals with accelerating "
            "adoption driven by government incentives, improving technology, and shifting consumer "
            "preferences toward sustainable and cost-effective mobility solutions."
        )
