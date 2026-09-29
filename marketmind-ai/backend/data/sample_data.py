"""
MarketMind AI – Indian Electric Vehicle Market Demo Dataset
All numbers are representative/illustrative for demo purposes.
"""

INDIAN_EV_MARKET = {
    "market_id": "indian_ev",
    "market_name": "Indian Electric Vehicle (EV) Market",
    "description": (
        "India's electric vehicle market is one of the fastest-growing in Asia, "
        "driven by government FAME II subsidies, rising fuel prices, and increasing "
        "environmental awareness. The market covers two-wheelers, three-wheelers, "
        "passenger cars, and commercial vehicles."
    ),
    "overview": {
        "market_size_2023_usd_billion": 3.21,
        "market_size_2024_usd_billion": 4.89,
        "projected_2030_usd_billion": 113.99,
        "cagr_percent": 49.5,
        "total_ev_sales_2023": 1_525_696,
        "total_ev_sales_2024": 1_960_000,
        "ev_penetration_percent_2024": 6.8,
        "top_segment": "Two-Wheelers (63%)",
        "key_policy": "FAME II Scheme, PLI for Advanced Chemistry Cell",
        "charging_stations_2024": 12_146,
    },
    "kpis": [
        {"label": "Market Size (2024)", "value": "$4.89B", "change": "+52%", "trend": "up"},
        {"label": "EV Sales (2024)", "value": "1.96M", "change": "+28%", "trend": "up"},
        {"label": "Market CAGR", "value": "49.5%", "change": "2024–2030", "trend": "up"},
        {"label": "EV Penetration", "value": "6.8%", "change": "+1.9pp", "trend": "up"},
        {"label": "Charging Stations", "value": "12,146", "change": "+44%", "trend": "up"},
        {"label": "Gov. Subsidy (FAME II)", "value": "₹10,000Cr", "change": "Active", "trend": "neutral"},
    ],
    "competitors": [
        {
            "name": "Ola Electric",
            "segment": "Two-Wheeler",
            "market_share_percent": 34.2,
            "flagship_product": "S1 Pro, S1 Air",
            "price_range_inr": "79,999 – 1,49,999",
            "strengths": ["Largest market share", "Hypercharger network", "Software-first approach", "Aggressive pricing"],
            "weaknesses": ["Service quality issues", "Software bugs reported", "Limited model range"],
            "positioning": "Mass-market leader",
            "revenue_fy24_cr": 5010,
            "yoy_growth_percent": 90,
        },
        {
            "name": "TVS Motor (iQube)",
            "segment": "Two-Wheeler",
            "market_share_percent": 18.5,
            "flagship_product": "iQube S, iQube Electric",
            "price_range_inr": "94,490 – 1,27,490",
            "strengths": ["Strong dealer network", "Brand trust", "Good range", "Service reliability"],
            "weaknesses": ["Higher price point", "Limited charging ecosystem"],
            "positioning": "Premium reliable EV",
            "revenue_fy24_cr": 2800,
            "yoy_growth_percent": 42,
        },
        {
            "name": "Bajaj Chetak",
            "segment": "Two-Wheeler",
            "market_share_percent": 11.3,
            "flagship_product": "Chetak Premium, Chetak 2901",
            "price_range_inr": "95,000 – 1,30,000",
            "strengths": ["Heritage brand", "Build quality", "Strong distribution"],
            "weaknesses": ["Conservative design", "Slower iteration cycle"],
            "positioning": "Heritage-premium segment",
            "revenue_fy24_cr": 1650,
            "yoy_growth_percent": 28,
        },
        {
            "name": "Tata Motors (EV Cars)",
            "segment": "Passenger Car",
            "market_share_percent": 71.0,  # within EV car segment
            "flagship_product": "Nexon EV, Tiago EV, Punch EV",
            "price_range_inr": "8,49,000 – 19,00,000",
            "strengths": ["Dominant in PV-EV segment", "Widest model range", "Trust factor", "Safety ratings"],
            "weaknesses": ["Long delivery wait times", "Charging infrastructure gaps"],
            "positioning": "EV car market leader",
            "revenue_fy24_cr": 44000,
            "yoy_growth_percent": 55,
        },
        {
            "name": "MG Motor India",
            "segment": "Passenger Car",
            "market_share_percent": 9.2,
            "flagship_product": "ZS EV, Comet EV",
            "price_range_inr": "6,99,000 – 24,98,000",
            "strengths": ["Diverse price range", "Advanced features", "Competitive range"],
            "weaknesses": ["SAIC ownership concerns", "Limited service centres"],
            "positioning": "Feature-rich challenger",
            "revenue_fy24_cr": 8700,
            "yoy_growth_percent": 22,
        },
        {
            "name": "Ather Energy",
            "segment": "Two-Wheeler",
            "market_share_percent": 10.8,
            "flagship_product": "Ather 450X, Ather 450 Apex",
            "price_range_inr": "1,34,999 – 1,54,999",
            "strengths": ["Tech-forward brand", "AtherGrid fast-charging", "Premium build", "OTA updates"],
            "weaknesses": ["Premium pricing limits mass market", "Grid availability"],
            "positioning": "Tech-premium EV",
            "revenue_fy24_cr": 1800,
            "yoy_growth_percent": 38,
        },
    ],
    "sentiment": {
        "overall_score": 68,
        "positive_percent": 61,
        "neutral_percent": 22,
        "negative_percent": 17,
        "total_reviews_analyzed": 45280,
        "sources": ["Amazon Reviews", "MouthShut", "Google Reviews", "Reddit r/India", "News Comments"],
        "positive_themes": [
            "Low running cost (₹0.5/km vs ₹4/km petrol)",
            "Smooth and silent ride",
            "Government subsidies making EVs affordable",
            "Tech features and smartphone integration",
            "Eco-friendly / lower emissions",
        ],
        "negative_themes": [
            "Range anxiety on long trips",
            "Insufficient charging infrastructure in Tier-2/3 cities",
            "High upfront purchase price",
            "After-sales service quality",
            "Battery degradation concerns",
        ],
        "neutral_themes": [
            "Waiting for more model options",
            "Comparing with ICE vehicles",
            "Policy/subsidy uncertainty",
        ],
        "brand_sentiment": {
            "Ola Electric": {"positive": 55, "neutral": 20, "negative": 25},
            "TVS iQube": {"positive": 72, "neutral": 18, "negative": 10},
            "Bajaj Chetak": {"positive": 68, "neutral": 22, "negative": 10},
            "Tata EV": {"positive": 74, "neutral": 16, "negative": 10},
            "Ather Energy": {"positive": 80, "neutral": 12, "negative": 8},
            "MG Motor": {"positive": 63, "neutral": 25, "negative": 12},
        },
    },
    "trends": {
        "emerging_trends": [
            "Battery-as-a-Service (BaaS) / swappable batteries",
            "V2G (Vehicle-to-Grid) integration pilots",
            "Electric 3-wheelers disrupting last-mile logistics",
            "OEM-owned fast-charging networks",
            "AI-based range optimization and predictive maintenance",
            "Localisation of battery cell manufacturing (PLI push)",
            "Electric buses for public transport (BEST, DTC adoption)",
        ],
        "historical_sales": [
            {"year": 2019, "sales": 152000, "market_size_bn": 0.28},
            {"year": 2020, "sales": 236802, "market_size_bn": 0.44},
            {"year": 2021, "sales": 327000, "market_size_bn": 0.68},
            {"year": 2022, "sales": 1013000, "market_size_bn": 1.45},
            {"year": 2023, "sales": 1525696, "market_size_bn": 3.21},
            {"year": 2024, "sales": 1960000, "market_size_bn": 4.89},
        ],
        "segment_split_2024": {
            "Two-Wheeler": 63,
            "Three-Wheeler": 28,
            "Passenger Car": 7,
            "Bus & Commercial": 2,
        },
        "top_states_by_sales_2024": [
            {"state": "Uttar Pradesh", "share_percent": 15.2},
            {"state": "Maharashtra", "share_percent": 14.8},
            {"state": "Karnataka", "share_percent": 12.1},
            {"state": "Tamil Nadu", "share_percent": 9.3},
            {"state": "Rajasthan", "share_percent": 7.6},
            {"state": "Gujarat", "share_percent": 7.1},
            {"state": "Others", "share_percent": 33.9},
        ],
    },
    "forecast": {
        "methodology": "CAGR-based projection with policy adjustment factor",
        "confidence": "Medium (AI-generated estimate, not investment advice)",
        "projections": [
            {"year": 2025, "sales_estimate": 2500000, "market_size_bn": 6.8, "ev_penetration": 9.2},
            {"year": 2026, "sales_estimate": 3400000, "market_size_bn": 10.1, "ev_penetration": 13.1},
            {"year": 2027, "sales_estimate": 4800000, "market_size_bn": 16.2, "ev_penetration": 19.4},
            {"year": 2028, "sales_estimate": 6500000, "market_size_bn": 26.8, "ev_penetration": 27.2},
            {"year": 2029, "sales_estimate": 8800000, "market_size_bn": 44.9, "ev_penetration": 36.1},
            {"year": 2030, "sales_estimate": 11500000, "market_size_bn": 113.99, "ev_penetration": 45.0},
        ],
        "key_drivers": [
            "FAME III policy expected with enhanced subsidies",
            "Battery cost reduction (LFP cells falling to $60/kWh by 2027)",
            "Expansion of public charging to 4,50,000 stations by 2030",
            "Increasing awareness post COP28 commitments",
            "New model launches across all OEMs (₹5L – ₹50L range)",
        ],
        "risks": [
            "Raw material supply chain (Lithium, Cobalt) volatility",
            "Policy reversal or subsidy withdrawal",
            "Infrastructure lag in rural and Tier-3 markets",
            "Consumer financing challenges",
            "ICE OEM lobbying",
        ],
    },
    "opportunities": [
        "Fleet electrification (delivery/logistics) – 3M+ commercial vehicles",
        "EV financing and insurance products",
        "Battery recycling & second-life battery market",
        "Rural EV penetration through affordable models (sub-₹60,000)",
        "Software/telematics layer – data monetization",
        "Export opportunity to SE Asia from Indian EV manufacturers",
    ],
    "key_findings": [
        "India's EV market grew 28% YoY in units sold in 2024.",
        "Two-wheelers dominate at 63% of all EV sales.",
        "Tata Motors holds ~71% share of the passenger EV segment.",
        "Ola Electric leads two-wheeler EVs with 34% market share.",
        "Customer sentiment is broadly positive but service quality remains a pain point.",
        "Charging infrastructure is the #1 barrier cited by non-adopters.",
        "The market is projected to reach $113.99B by 2030 at 49.5% CAGR.",
        "Government policy (FAME II/III) is the single largest demand driver.",
    ],
    "rag_knowledge_base": [
        {
            "doc_id": "doc_001",
            "title": "FAME II Scheme Overview",
            "content": (
                "The Faster Adoption and Manufacturing of Electric Vehicles (FAME) India Phase II scheme "
                "was approved in March 2019 with a budget outlay of ₹10,000 crore for a period of 3 years. "
                "The scheme focuses on supporting the electrification of public and shared transportation. "
                "Key beneficiaries include electric 2-wheelers, 3-wheelers, 4-wheelers, buses, and charging infrastructure. "
                "Under FAME II, approximately 10 lakh electric 2-wheelers, 5 lakh electric 3-wheelers, "
                "55,000 electric 4-wheelers, and 7,090 electric buses are being supported. "
                "The scheme provides demand incentives to buyers and capital grants for charging infrastructure."
            ),
            "source": "Ministry of Heavy Industries, Government of India",
            "year": 2023,
        },
        {
            "doc_id": "doc_002",
            "title": "Indian EV Market Competitive Landscape 2024",
            "content": (
                "The Indian EV market is highly competitive with both domestic and international players. "
                "Ola Electric has emerged as the dominant player in the two-wheeler segment with over 34% market share "
                "following its aggressive pricing strategy and Hypercharger network expansion. "
                "Tata Motors remains unchallenged in the passenger EV segment with products like Nexon EV Max, "
                "Tiago EV, and Punch EV spanning multiple price points. "
                "International players like BYD and Volvo are also entering the premium segment. "
                "The commercial vehicle EV space is seeing rapid growth with players like Euler Motors, "
                "Mahindra Electric, and Tata Motors competing for fleet orders."
            ),
            "source": "SMEV (Society of Manufacturers of Electric Vehicles) Annual Report 2024",
            "year": 2024,
        },
        {
            "doc_id": "doc_003",
            "title": "Battery Technology Trends in Indian EV Market",
            "content": (
                "Indian EV manufacturers are primarily using Lithium Iron Phosphate (LFP) and NMC battery chemistries. "
                "LFP batteries are preferred for their thermal stability, longer cycle life (>3000 cycles), "
                "and lower cost. The average battery cost in India stood at approximately $120/kWh in 2024, "
                "projected to fall to $60/kWh by 2027 due to localisation under the PLI scheme. "
                "Ola Electric and Ather Energy are investing in in-house cell manufacturing capabilities. "
                "Battery swapping technology, championed by companies like Gogoro (via partnership) and "
                "Sun Mobility, is gaining traction in the commercial 3-wheeler segment for last-mile delivery."
            ),
            "source": "BloombergNEF India EV Outlook 2024",
            "year": 2024,
        },
        {
            "doc_id": "doc_004",
            "title": "Charging Infrastructure Report India",
            "content": (
                "As of December 2024, India had approximately 12,146 public EV charging stations, "
                "with Maharashtra (2,135), Delhi (1,886), and Karnataka (1,462) leading the count. "
                "The government targets 4,50,000 public charging points by 2030 under the National Electric "
                "Mobility Mission Plan. Major contributors include EESL (government PSU), Tata Power EV, "
                "Ola Electric's Hypercharger network (4,000+ stations), AtherGrid (1,400+ stations), "
                "and ChargeZone. The charger-to-EV ratio currently stands at 1:160, far below the "
                "recommended 1:10 ratio, highlighting the critical infrastructure gap."
            ),
            "source": "Bureau of Energy Efficiency (BEE) EV Charging Report 2024",
            "year": 2024,
        },
        {
            "doc_id": "doc_005",
            "title": "Consumer Adoption Study – Indian EV Buyers",
            "content": (
                "A survey of 8,500 EV buyers and intenders across 12 Indian cities (2024) revealed: "
                "71% cited lower running costs as the primary purchase driver; "
                "58% were influenced by government subsidies; "
                "45% were motivated by environmental concerns; "
                "Key barriers included: range anxiety (67%), charging infrastructure (62%), "
                "high upfront cost (54%), and lack of model variety (31%). "
                "Brand trust was the #1 factor for 2-wheeler buyers, while range was the #1 factor "
                "for 4-wheeler buyers. 78% of respondents in Tier-1 cities expressed intent to buy EV "
                "as their next vehicle, vs 34% in Tier-2 cities and only 18% in Tier-3 cities."
            ),
            "source": "JMK Research Consumer EV Adoption Survey 2024",
            "year": 2024,
        },
    ],
    "executive_summary": (
        "The Indian Electric Vehicle market is experiencing explosive growth, driven by favorable government policies, "
        "increasing fuel costs, and improving technology. The market grew 28% in unit sales in FY2024 and is projected "
        "to reach $113.99 billion by 2030 at a CAGR of 49.5%. Two-wheelers dominate with 63% share, while passenger "
        "EVs are gaining traction led by Tata Motors. Key challenges remain: charging infrastructure gaps, high upfront "
        "costs, and service quality. Opportunities lie in fleet electrification, battery technology, and rural market "
        "penetration. Investors and manufacturers should focus on charging ecosystem development and affordable "
        "financing to unlock the next growth phase."
    ),
}
