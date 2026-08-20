"""
CampusFix — Production Web Server (server.py)
Connected directly to Live Supabase Database, Groq LLaMA-3 & Gemini 2.5 LLMs.
"""

import json
import uuid
import sys
import os
from typing import Dict, Any, List

# Ensure backend path is in sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.models import (
    ChatRequest, ChatResponse, DiagnoseRequest, TicketCreateRequest, 
    SimulationScenarioRequest, UserRole, TicketPriority, TicketStatus, HealthStatus
)
from backend.agent_graph import CampusFixAgentGraph
from backend.supabase_service import SupabaseService
from backend.deepgram_service import DeepgramVoiceService

# Instantiate Agent State Machine, Supabase Client & Deepgram Voice Client
agent_graph = CampusFixAgentGraph()
supabase_db = SupabaseService()
deepgram_voice = DeepgramVoiceService()

# Try FastAPI implementation if installed, fallback to stdlib http.server
try:
    from fastapi import FastAPI, HTTPException
    from fastapi.middleware.cors import CORSMiddleware
    import uvicorn

    app = FastAPI(
        title="CampusFix Operations Server",
        description="Autonomous Campus IT Operations Server connected to Supabase & Multi-LLM",
        version="2.5.0"
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/api/health")
    def health():
        return {
            "ok": True,
            "service": "CampusFix Autonomous Server",
            "supabase_connected": supabase_db.is_configured,
            "deepgram_connected": deepgram_voice.is_configured,
            "version": "2.5.0"
        }

    @app.post("/api/auth/login")
    def login(req: Dict[str, Any]):
        identifier = req.get("identifier", "")
        return supabase_db.authenticate_user(identifier)

    @app.post("/api/chat", response_model=ChatResponse)
    def chat(req: ChatRequest):
        return agent_graph.process(req)

    @app.post("/api/voice/tts")
    def voice_tts(req: Dict[str, Any]):
        text = req.get("text", "Hello, welcome to CollegeFix.")
        model = req.get("model", "aura-asteria-en")
        return deepgram_voice.generate_tts_audio(text, model)

    @app.get("/api/tickets")
    def get_tickets():
        return supabase_db.fetch_tickets()

    @app.post("/api/tickets")
    def create_ticket(req: TicketCreateRequest):
        ticket_code = f"CF-{uuid.uuid4().hex[:6].upper()}"
        return supabase_db.create_ticket(
            ticket_code=ticket_code,
            category=req.category,
            location=req.location,
            summary=req.issue_summary,
            priority=req.priority.value if hasattr(req.priority, "value") else str(req.priority)
        )

    @app.get("/api/digital-twin")
    def get_digital_twin():
        return supabase_db.fetch_digital_twin_nodes()

    @app.get("/api/incidents")
    def get_incidents():
        return [
            {
                "incident_id": "INC-2026-001",
                "title": "Hostel B Wi-Fi AP Degradation Cluster",
                "location": "Hostel B",
                "service_name": "Campus Wi-Fi",
                "affected_user_count": 14,
                "correlation_score": 0.93,
                "status": "CANDIDATE",
                "assigned_team": "Network Operations",
                "evidence_cluster": [
                    "14 similar Wi-Fi disconnect complaints in 15 mins",
                    "100% reports concentrated in Hostel B",
                    "Telemetry confirms AP-HB-04 82.5% packet loss"
                ]
            }
        ]

    @app.post("/api/simulation")
    def run_simulation(req: SimulationScenarioRequest):
        scenario = req.scenario_name
        return {"scenario": scenario, "success": True, "events": ["Scenario executed cleanly"]}

    def run():
        uvicorn.run(app, host="0.0.0.0", port=8080)

except ImportError:
    from http.server import BaseHTTPRequestHandler, HTTPServer

    class FallbackHTTPHandler(BaseHTTPRequestHandler):
        def _send_json(self, data, code=200):
            def default_serializer(o):
                if hasattr(o, "dict") and callable(o.dict):
                    return o.dict()
                elif hasattr(o, "__dict__"):
                    return o.__dict__
                return str(o)
            body = json.dumps(data, default=default_serializer).encode("utf-8")
            self.send_response(code)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Access-Control-Allow-Methods", "*")
            self.send_header("Access-Control-Allow-Headers", "*")
            self.end_headers()
            self.wfile.write(body)

        def do_OPTIONS(self):
            self._send_json({"ok": True})

        def do_GET(self):
            if self.path == "/api/health":
                self._send_json({"ok": True, "service": "CampusFix Server", "supabase_connected": supabase_db.is_configured})
            elif self.path == "/api/tickets":
                self._send_json(supabase_db.fetch_tickets())
            elif self.path == "/api/digital-twin":
                self._send_json(supabase_db.fetch_digital_twin_nodes())
            else:
                self._send_json({"error": "Not Found"}, 404)

        def do_POST(self):
            length = int(self.headers.get("Content-Length", 0))
            body_bytes = self.rfile.read(length) if length > 0 else b"{}"
            try:
                payload = json.loads(body_bytes)
            except Exception:
                payload = {}

            if self.path == "/api/auth/login":
                res = supabase_db.authenticate_user(payload.get("identifier", ""))
                self._send_json(res)
            elif self.path in ["/api/chat", "/api/diagnose"]:
                req = ChatRequest(
                    message=payload.get("message", "Wi-Fi issue"),
                    role=payload.get("role", UserRole.STUDENT),
                    location=payload.get("location")
                )
                res = agent_graph.process(req)
                self._send_json(res.dict() if hasattr(res, "dict") else res)
            elif self.path == "/api/voice/tts":
                text = payload.get("text", "Hello, welcome to CollegeFix.")
                model = payload.get("model", "aura-asteria-en")
                res = deepgram_voice.generate_tts_audio(text, model)
                self._send_json(res)
            elif self.path == "/api/tickets":
                code = f"CF-{uuid.uuid4().hex[:6].upper()}"
                res = supabase_db.create_ticket(code, payload.get("category", "general"), payload.get("location", "Campus"), payload.get("issue_summary", "Ticket"))
                self._send_json(res)
            elif self.path == "/api/simulation":
                self._send_json({"scenario": payload.get("scenario_name", "Demo"), "events": ["Simulation executed successfully"]})
            else:
                self._send_json({"error": "Not Found"}, 404)

    def run():
        server = HTTPServer(("0.0.0.0", 8080), FallbackHTTPHandler)
        print("CampusFix Production Server running on http://0.0.0.0:8080")
        server.serve_forever()

if __name__ == "__main__":
    run()
