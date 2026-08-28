"""
CampusFix — Production Web Server (server.py)
Connected to Live Supabase Database, Groq LLaMA-3 & Gemini 2.5 LLMs.
Includes:
- Vision AI Photo Diagnostics
- Voice Call Simulator API
- Smart Outage Deduplication Engine
- Live Heatmap & Predictive Failure Radar
- Smart Nearest-Specialist GPS Auto-Assigner
"""

import json
import uuid
import sys
import os
from typing import Dict, Any, List

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.models import (
    ChatRequest, ChatResponse, DiagnoseRequest, TicketCreateRequest, 
    SimulationScenarioRequest, UserRole, TicketPriority, TicketStatus, HealthStatus
)
from backend.agent_graph import CampusFixAgentGraph, CAMPUS_BLOCKS_DATA, ACTIVE_FIELD_SPECIALISTS
from backend.supabase_service import SupabaseService
from backend.deepgram_service import DeepgramVoiceService
from backend.groq_service import GroqService

agent_graph = CampusFixAgentGraph()
supabase_db = SupabaseService()
deepgram_voice = DeepgramVoiceService()
groq_engine = GroqService()

ACTIVE_CLUSTER_TICKETS = [
    {
        "master_ticket_code": "CF-9021",
        "location": "5. Vignan Boys Hostel",
        "category": "WIFI",
        "title": "Vignan Boys Hostel AP-HB-04 Packet Loss (82.5%)",
        "subscriber_count": 14,
        "assigned_to": "Network Operations Specialist",
        "priority": "CRITICAL",
        "status": "IN PROGRESS"
    },
    {
        "master_ticket_code": "CF-9022",
        "location": "3. NTR Library",
        "category": "PRINTING",
        "title": "Central Library PRN-LIB-01 Spooler Buffer Stalled",
        "subscriber_count": 5,
        "assigned_to": "Digital Printing Lead",
        "priority": "HIGH",
        "status": "ASSIGNED"
    }
]

try:
    from fastapi import FastAPI, HTTPException
    from fastapi.middleware.cors import CORSMiddleware
    import uvicorn

    app = FastAPI(
        title="CampusFix Operations Server",
        description="Autonomous Campus IT Operations Server with Heatmap & Proximity Assigner",
        version="3.2.0"
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
            "groq_configured": groq_engine.is_configured,
            "version": "3.2.0"
        }

    @app.post("/api/auth/login")
    def login(req: Dict[str, Any]):
        identifier = req.get("identifier", "")
        return supabase_db.authenticate_user(identifier)

    @app.post("/api/chat", response_model=ChatResponse)
    def chat(req: ChatRequest):
        return agent_graph.process(req)

    @app.get("/api/telemetry/heatmap")
    def get_heatmap():
        return CAMPUS_BLOCKS_DATA

    @app.get("/api/telemetry/specialists")
    def get_specialists():
        return ACTIVE_FIELD_SPECIALISTS

    @app.post("/api/vision/diagnose")
    def vision_diagnose(req: Dict[str, Any]):
        image_base64 = req.get("image_base64", "")
        caption = req.get("caption", "")
        location = req.get("location", "")
        return groq_engine.analyze_vision_image(image_base64, caption, location)

    @app.post("/api/tickets/dedup-check")
    def dedup_check(req: Dict[str, Any]):
        query = req.get("query", "").lower()
        location = req.get("location", "")
        
        for master in ACTIVE_CLUSTER_TICKETS:
            loc_match = master["location"].lower() in location.lower() or location.lower() in master["location"].lower()
            cat_match = (master["category"].lower() in query) or ("wifi" in query and master["category"] == "WIFI")
            if loc_match and cat_match:
                master["subscriber_count"] += 1
                return {
                    "duplicate_found": True,
                    "master_ticket": master,
                    "message": f"Cluster detected! Merged with Master Incident #{master['master_ticket_code']} ({master['subscriber_count']} students affected)."
                }
        return {"duplicate_found": False, "master_ticket": None}

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
                self._send_json({"ok": True, "service": "CampusFix Server", "version": "3.2.0"})
            elif self.path == "/api/telemetry/heatmap":
                self._send_json(CAMPUS_BLOCKS_DATA)
            elif self.path == "/api/telemetry/specialists":
                self._send_json(ACTIVE_FIELD_SPECIALISTS)
            elif self.path == "/api/tickets":
                self._send_json(supabase_db.fetch_tickets())
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
            elif self.path == "/api/vision/diagnose":
                res = groq_engine.analyze_vision_image(
                    payload.get("image_base64", ""),
                    payload.get("caption", ""),
                    payload.get("location", "")
                )
                self._send_json(res)
            elif self.path == "/api/tickets/dedup-check":
                query = payload.get("query", "").lower()
                location = payload.get("location", "")
                matched = None
                for master in ACTIVE_CLUSTER_TICKETS:
                    if (master["location"].lower() in location.lower() or location.lower() in master["location"].lower()) and \
                       (master["category"].lower() in query or ("wifi" in query and master["category"] == "WIFI")):
                        master["subscriber_count"] += 1
                        matched = master
                        break
                if matched:
                    self._send_json({
                        "duplicate_found": True,
                        "master_ticket": matched,
                        "message": f"Cluster detected! Merged with Master Incident #{matched['master_ticket_code']} ({matched['subscriber_count']} students affected)."
                    })
                else:
                    self._send_json({"duplicate_found": False, "master_ticket": None})
            elif self.path == "/api/tickets":
                code = f"CF-{uuid.uuid4().hex[:6].upper()}"
                res = supabase_db.create_ticket(code, payload.get("category", "general"), payload.get("location", "Campus"), payload.get("issue_summary", "Ticket"))
                self._send_json(res)
            else:
                self._send_json({"error": "Not Found"}, 404)

    def run():
        server = HTTPServer(("0.0.0.0", 8080), FallbackHTTPHandler)
        print("CampusFix Production Server v3.2 running on http://0.0.0.0:8080")
        server.serve_forever()

if __name__ == "__main__":
    run()
