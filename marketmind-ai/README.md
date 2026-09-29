# 📊 MarketMind AI
## Intelligent Agentic Market Research & Business Intelligence Assistant

> **College Mini-Project** | LangFlow + IBM watsonx.ai + IBM Granite + RAG + Agentic AI

---

## 🎯 Project Overview

MarketMind AI is a **fully functional, agentic AI-powered market research platform** that analyzes any market, product, or company and generates actionable business intelligence. It uses **7 specialized AI agents** powered by **IBM Granite** (via IBM watsonx.ai), a **RAG knowledge pipeline**, and renders results in a **professional interactive dashboard**.

### ✨ Key Features

| Feature | Description |
|---------|-------------|
| 🤖 **7 AI Agents** | Research, RAG, Competitor, Sentiment, Trend, Prediction, Report |
| 🧠 **IBM Granite** | IBM's enterprise foundation model via watsonx.ai |
| 📚 **RAG Pipeline** | Upload PDFs/CSVs → chunk → embed → FAISS search → cite sources |
| 📊 **Live Dashboard** | Market overview, KPIs, charts, sentiment, trends, forecasts |
| 🔮 **Predictions** | AI-generated market forecasts with confidence intervals + disclaimer |
| 🏎️ **Demo Mode** | Full Indian EV Market dataset — works without API keys |
| 🌙 **Dark/Light Mode** | Professional SaaS-quality UI |
| 📄 **Report Export** | Generate printable executive reports |

---

## 🏗️ Architecture

```
User Query
    │
    ▼
┌─────────────────────────────────────────────────────────────┐
│                    MarketMind AI Pipeline                    │
│                                                             │
│  ┌──────────┐   ┌──────────┐   ┌────────────────────────┐  │
│  │ Research │──▶│   RAG    │──▶│  Competitor Analysis   │  │
│  │  Agent   │   │  Agent   │   │       Agent            │  │
│  └──────────┘   └──────────┘   └────────────────────────┘  │
│       │              │                    │                  │
│       ▼              ▼                    ▼                  │
│  ┌──────────┐   ┌──────────┐   ┌────────────────────────┐  │
│  │Sentiment │   │  Trend   │   │   Predictive Insights  │  │
│  │  Agent   │   │  Agent   │   │       Agent            │  │
│  └──────────┘   └──────────┘   └────────────────────────┘  │
│       │              │                    │                  │
│       └──────────────┴────────────────────┘                 │
│                            │                                │
│                      ┌─────▼──────┐                        │
│                      │   Report   │                        │
│                      │   Agent    │                        │
│                      └─────┬──────┘                        │
└────────────────────────────┼────────────────────────────────┘
                             │
                    ┌────────▼────────┐
                    │   Interactive   │
                    │   Dashboard     │
                    └─────────────────┘
```

### Technology Stack

```
Frontend:    HTML5 + CSS3 + JavaScript + Chart.js
Backend:     Python 3.10+ · FastAPI · uvicorn
Agents:      LangFlow workflow · IBM watsonx.ai SDK
LLM:         IBM Granite (ibm/granite-13b-instruct-v2)
RAG:         sentence-transformers · FAISS vector DB
Parsing:     pdfplumber · python-docx · pandas
```

---

## 📂 Project Structure

```
marketmind-ai/
├── backend/
│   ├── main.py                    # FastAPI app · all API endpoints
│   ├── agents/
│   │   └── orchestrator.py        # Multi-agent orchestrator + IBM Granite prompts
│   ├── rag/
│   │   └── pipeline.py            # RAG pipeline (extract·chunk·embed·index·retrieve)
│   ├── data/
│   │   └── sample_data.py         # Complete Indian EV Market demo dataset
│   └── utils/
│       └── report_generator.py    # HTML/JSON report formatter
├── frontend/
│   └── templates/
│       └── index.html             # Full SPA dashboard (8 sections · dark mode · charts)
├── langflow/
│   └── marketmind_flow.json       # LangFlow workflow definition (7 agents)
├── docs/                          # Architecture diagrams (add your own)
├── .env.example                   # Environment variable template
├── requirements.txt               # Python dependencies
└── README.md                      # This file
```

---

## 🚀 Quick Start

### Option A — Demo Mode (No API Keys Needed)

```bash
# 1. Clone / download the project
cd marketmind-ai

# 2. Install dependencies
pip install fastapi uvicorn python-dotenv

# 3. Start the backend
cd backend
python main.py

# 4. Open the dashboard
# Visit: http://localhost:8000
# Click "▶ Run Demo" to see the Indian EV Market analysis
```

### Option B — Full AI Mode (IBM watsonx.ai)

```bash
# 1. Create your environment file
cp .env.example .env

# 2. Fill in your IBM credentials in .env:
#    WATSONX_API_KEY=your_key
#    WATSONX_PROJECT_ID=your_project_id

# 3. Install all dependencies
pip install -r requirements.txt

# 4. Start the backend
cd backend
python main.py

# 5. Visit http://localhost:8000
#    Select "Full AI Analysis" mode in Market Research
```

---

## 🔑 Getting IBM watsonx.ai Credentials

1. **IBM Cloud Account** → https://cloud.ibm.com (free tier available)
2. **Create API Key** → IAM → API Keys → Create → Copy key to `.env`
3. **Create watsonx Project** → https://dataplatform.cloud.ibm.com
4. **Copy Project ID** → Project → Manage → General → Project ID
5. **Granite Model** → No additional setup needed; `ibm/granite-13b-instruct-v2` is available in all regions

---

## 📊 Dashboard Sections

| Section | What it shows |
|---------|---------------|
| 🏠 **Dashboard** | KPI cards · Forecast chart · Market share · Sentiment trend · AI summary |
| 🔍 **Market Research** | Agent pipeline · Market overview · Drivers · Challenges · Summary |
| ⚔️ **Competitors** | Market share donut · YoY growth bar · Competitor cards · Feature matrix |
| 💬 **Sentiment** | Positive/Neutral/Negative % · Brand sentiment · Theme analysis · Insights |
| 📈 **Trends** | Demand index · Emerging trends · Historical patterns · Tech/Regulatory |
| 🔮 **Predictions** | 2024–2030 forecast · Scenario analysis · Opportunities · Risks |
| 📚 **Knowledge Base** | Upload PDFs/CSVs · FAISS indexing · RAG query with source attribution |
| 📄 **Reports** | Executive summary · Key findings · Recommendations · Print/PDF export |
| 🤖 **AI Chat** | Context-aware chat using research data · IBM Granite responses |

---

## 🤖 Agent Details

### 1. Research Agent
**Prompt strategy:** Structured JSON output with market size, CAGR, key players, drivers, challenges, regulatory context, and executive summary. Uses IBM Granite's instruction-following capabilities.

### 2. RAG Knowledge Agent
**Pipeline:** Document upload → text extraction (PDF/DOCX/CSV) → 512-token overlapping chunks → sentence-transformer embeddings → FAISS cosine similarity → top-5 chunk retrieval → source-cited answers.

### 3. Competitor Analysis Agent
**Output:** Competitor profiles with market share, products, strengths/weaknesses, positioning, revenue estimates. Generates feature comparison matrix.

### 4. Sentiment Analysis Agent
**Output:** Positive/Neutral/Negative percentages, NPS score, top themes by volume, example quotes, trend direction.

### 5. Market Trend Agent
**Output:** 5 emerging trends with impact levels, historical patterns, technology/regulatory shifts, demand index data.

### 6. Predictive Insights Agent
**Output:** 5-year market size forecast with confidence intervals, quarterly demand forecast, scenario analysis (best/base/worst case), opportunity and risk matrices. **Always includes AI disclaimer.**

### 7. Report Generation Agent
**Output:** Professional executive report with 300-word summary, 7 key findings, 5 prioritized strategic recommendations, sources, confidence rating.

---

## 🏎️ Demo: Indian EV Market (3–5 Minute Presentation)

The demo dataset includes:
- **Market Size:** $4.7B (2024) → projected $52.5B (2030) at 49.2% CAGR
- **5 Competitors:** Tata Motors, Ola Electric, Ather Energy, Bajaj Auto, Hero Electric
- **Sentiment:** 15,420 reviews analyzed · 58% positive · NPS 34
- **Trends:** BaaS, V2G, Solid-State Batteries, Fleet Electrification
- **Predictions:** 2024–2030 forecast with best/base/worst scenarios
- **Report:** Full executive report with recommendations

### Demo Flow (5 minutes)
1. `(0:00)` Open dashboard → show KPI cards and overview
2. `(0:45)` Market Research → show agent pipeline running
3. `(1:30)` Competitors → show market share chart and comparison matrix
4. `(2:15)` Sentiment → show donut chart, brand sentiment, theme analysis
5. `(3:00)` Predictions → show forecast chart + scenario analysis
6. `(3:45)` Knowledge Base → upload a PDF → query it → show sources
7. `(4:30)` Reports → generate and show executive report
8. `(5:00)` AI Chat → ask "What are the key risks?" → show Granite response

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Dashboard frontend |
| `GET` | `/health` | Health check |
| `POST` | `/api/research/start` | Start research pipeline |
| `GET` | `/api/research/{id}/status` | Poll pipeline progress |
| `GET` | `/api/research/{id}/result` | Get full results |
| `POST` | `/api/rag/upload` | Upload document for RAG |
| `POST` | `/api/rag/query` | Query knowledge base |
| `GET` | `/api/rag/documents` | List indexed documents |
| `POST` | `/api/chat` | Context-aware AI chat |
| `POST` | `/api/report/generate` | Generate report |
| `GET` | `/api/demo/indian-ev` | Get demo dataset |
| `GET` | `/docs` | Interactive API documentation |

---

## 🔄 LangFlow Integration

To use the included LangFlow workflow:

```bash
# Install LangFlow
pip install langflow

# Start LangFlow
langflow run

# Import the workflow
# LangFlow UI → Import → Select: langflow/marketmind_flow.json
# Configure: Set your watsonx.ai credentials in each node
# Run: Trigger the flow from the API or LangFlow UI
```

The LangFlow workflow (`langflow/marketmind_flow.json`) defines the complete 7-agent pipeline with IBM Granite nodes, RAG retriever, and all agent connections.

---

## ⚠️ Important Notes

- **AI Predictions:** All forecasts are clearly labeled as AI-generated estimates. Not for investment decisions.
- **Demo Mode:** Works fully without API keys using pre-built Indian EV data.
- **RAG Fallback:** If FAISS is unavailable, the system automatically falls back to keyword-based search.
- **Model Fallback:** If watsonx credentials are not set, all agents use realistic sample data.
- **No Hard-coded Keys:** All credentials are loaded from `.env` via `python-dotenv`. Never commit `.env` to Git.

---

## 📋 Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `WATSONX_API_KEY` | For live AI | IBM Cloud API key |
| `WATSONX_PROJECT_ID` | For live AI | watsonx.ai project ID |
| `WATSONX_URL` | Optional | Default: us-south endpoint |
| `GRANITE_MODEL_ID` | Optional | Default: granite-13b-instruct-v2 |
| `EMBED_MODEL` | Optional | Default: all-MiniLM-L6-v2 |
| `CHUNK_SIZE` | Optional | Default: 512 tokens |

---

## 🏆 Technical Highlights

- **Agentic AI:** 7 specialized agents with distinct roles, sequential execution, and result aggregation
- **RAG:** Real document ingestion pipeline with FAISS vector search and source attribution
- **Explainability:** Every prediction includes methodology, confidence levels, and AI disclaimer
- **Fallback Architecture:** Deterministic sample data ensures 100% demo reliability
- **Modern Frontend:** Single-page application with 8 sections, 10+ charts, dark mode, responsive design
- **Clean Code:** No hard-coded secrets, proper error handling, modular architecture

---

## 👥 Team & Attribution

- **Project:** MarketMind AI – College Mini Project
- **AI Engine:** IBM Granite via IBM watsonx.ai
- **Workflow:** LangFlow
- **RAG:** FAISS + sentence-transformers
- **Charts:** Chart.js

---

*MarketMind AI is an educational project demonstrating Agentic AI + RAG capabilities using IBM's enterprise AI stack.*
