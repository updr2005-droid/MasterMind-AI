"""
MarketMind AI – Quick Demo Server
Serves the dashboard at http://localhost:8000 using only stdlib (no dependencies needed).
Use this if you can't install the full requirements.

Run: python demo_server.py
"""

import json
import os
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path
import sys

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent / "backend"))

try:
    from data.sample_data import get_indian_ev_demo_data
    DEMO_DATA = get_indian_ev_demo_data()
except Exception as e:
    print(f"Warning: Could not load sample data ({e}). Using minimal fallback.")
    DEMO_DATA = {"meta": {"market": "Indian EV Market", "mode": "demo"}}

FRONTEND_PATH = Path(__file__).parent / "frontend" / "templates" / "index.html"


class MarketMindHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        print(f"  [{self.address_string()}] {format % args}")

    def do_GET(self):
        if self.path == "/" or self.path == "/index.html":
            self.serve_html()
        elif self.path == "/api/demo/indian-ev" or self.path == "/health":
            self.serve_json(DEMO_DATA if "demo" in self.path else {"status": "ok"})
        elif self.path.startswith("/api/research/") and self.path.endswith("/result"):
            self.serve_json(DEMO_DATA)
        elif self.path.startswith("/api/research/") and self.path.endswith("/status"):
            self.serve_json({"status": "complete", "progress": 100, "steps": []})
        elif self.path == "/api/rag/documents":
            self.serve_json({"documents": []})
        else:
            self.send_error(404)

    def do_POST(self):
        content_len = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_len) if content_len else b"{}"

        if self.path == "/api/research/start":
            self.serve_json({"session_id": "demo-session", "status": "complete"})
        elif self.path == "/api/rag/query":
            self.serve_json({
                "answer": "Demo mode: Start the full FastAPI backend (python backend/main.py) for live RAG queries.",
                "sources": [], "confidence": 0.0
            })
        elif self.path == "/api/chat":
            try:
                data = json.loads(body)
                msg = data.get("message", "")
                self.serve_json({"response": self._canned_response(msg), "session_id": "demo"})
            except Exception:
                self.serve_json({"response": "Demo mode active.", "session_id": "demo"})
        elif self.path == "/api/report/generate":
            self.serve_json({"format": "json", "content": DEMO_DATA, "generated_at": "2025"})
        else:
            self.serve_json({"status": "ok"})

    def _canned_response(self, msg):
        m = msg.lower()
        r = DEMO_DATA.get("research", {})
        if "size" in m or "market" in m:
            return f"The {r.get('market_name','EV market')} is valued at ${r.get('market_size','4.7')}B growing at {r.get('market_growth_rate','49')}% CAGR."
        if "competitor" in m:
            comps = DEMO_DATA.get("competitors", {}).get("competitors", [])
            names = [c["name"] for c in comps[:3]]
            return f"Top competitors: {', '.join(names)}. Tata Motors leads with 28.3% share."
        if "risk" in m:
            risks = DEMO_DATA.get("predictions", {}).get("key_risks", [])
            return f"Key risks: {', '.join(r['title'] for r in risks[:3])}."
        return f"[Demo Mode] Start the full backend (python backend/main.py) for IBM Granite AI responses. Demo data loaded for: {r.get('market_name','Indian EV Market')}"

    def serve_html(self):
        try:
            content = FRONTEND_PATH.read_bytes()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", len(content))
            self.end_headers()
            self.wfile.write(content)
        except FileNotFoundError:
            self.send_error(404, f"index.html not found at {FRONTEND_PATH}")

    def serve_json(self, data):
        content = json.dumps(data, indent=2).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Content-Length", len(content))
        self.end_headers()
        self.wfile.write(content)

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    server = HTTPServer(("0.0.0.0", port), MarketMindHandler)
    print(f"""
╔══════════════════════════════════════════════════════════╗
║          MarketMind AI – Quick Demo Server               ║
╠══════════════════════════════════════════════════════════╣
║  Dashboard:  http://localhost:{port}                      ║
║  Mode:       Demo (Indian EV Market)                     ║
║  Ctrl+C to stop                                          ║
╚══════════════════════════════════════════════════════════╝

For full AI features (IBM Granite + RAG), run:
  pip install -r requirements.txt
  cp .env.example .env   # add your watsonx credentials
  cd backend && python main.py
""")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
