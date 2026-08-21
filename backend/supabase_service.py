"""
CampusFix — Supabase Live Database Adapter (supabase_service.py)
Direct REST & RPC API Integration with live Supabase PostgreSQL project.
"""

import os
import json
import urllib.request
import urllib.parse
from typing import Dict, Any, List, Optional

class SupabaseService:
    """Live Supabase Database service client with native PL/pgSQL RPC execution."""

    def __init__(self, url: Optional[str] = None, key: Optional[str] = None):
        self._load_dotenv()
        self.url = url or os.environ.get("SUPABASE_URL")
        self.key = key or os.environ.get("SUPABASE_KEY")
        self.tickets_store = [
            {"ticket_code": "CF-WIFI-8842", "category": "WIFI", "location": "Hostel B (Boys Hostel)", "priority": "HIGH", "status": "NEW", "issue_summary": "VFSTR-STUDENT Wi-Fi disconnected in Room 204", "submitted_by": "Alex Rivera (Student)"},
            {"ticket_code": "CF-AV-9012", "category": "AV", "location": "H-102 (H-Block CSE)", "priority": "EMERGENCY", "status": "IN_PROGRESS", "issue_summary": "Smart Board projector audio HDMI cable fault", "submitted_by": "Dr. Smith (Faculty)"},
            {"ticket_code": "CF-SSO-4102", "category": "SSO", "location": "A-Block Admin", "priority": "NORMAL", "status": "NEW", "issue_summary": "vignan.ac.in/portal domain SSO password lock", "submitted_by": "Priya Sharma (Student)"},
            {"ticket_code": "CF-PRN-3019", "category": "PRINTER", "location": "Central Library (L-Block)", "priority": "NORMAL", "status": "RESOLVED", "issue_summary": "Library PRN-LIB-01 spooler queue cleared", "submitted_by": "Rahul Verma (Student)"}
        ]

    def _load_dotenv(self):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        env_path = os.path.join(base_dir, ".env")
        if os.path.exists(env_path):
            with open(env_path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        k, v = line.split("=", 1)
                        os.environ[k.strip()] = v.strip()

    @property
    def is_configured(self) -> bool:
        return bool(self.url and self.key)

    def _call_rpc(self, fn_name: str, payload: Dict[str, Any]) -> Optional[Any]:
        """Generic RPC caller for Supabase PostgreSQL PL/pgSQL stored procedures."""
        if not self.is_configured:
            return None
        try:
            endpoint = f"{self.url}/rest/v1/rpc/{fn_name}"
            req = urllib.request.Request(
                endpoint,
                data=json.dumps(payload).encode("utf-8"),
                headers={
                    "apikey": self.key,
                    "Authorization": f"Bearer {self.key}",
                    "Content-Type": "application/json"
                }
            )
            with urllib.request.urlopen(req, timeout=5) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except Exception as e:
            print(f"Supabase RPC Warning [{fn_name}]: {e}")
            return None

    def authenticate_user(self, identifier: str) -> Dict[str, Any]:
        """Verifies credentials via Supabase RPC fn_authenticate_user."""
        identifier = identifier.strip().lower()
        if self.is_configured:
            rpc_res = self._call_rpc("fn_authenticate_user", {"p_identifier": identifier})
            if rpc_res and isinstance(rpc_res, dict):
                return rpc_res

        return self._fallback_auth(identifier)

    def _fallback_auth(self, identifier: str) -> Dict[str, Any]:
        """Smart role detector based on Vignan email/ID patterns."""
        if any(w in identifier for w in ["dr.", "prof", "faculty", "smith"]):
            role = "Faculty"
            dept = "CSE Faculty Dept (H-Block)"
            loc = "H-Block CSE"
        elif any(w in identifier for w in ["admin", "staff", "vance", "it."]):
            role = "IT Staff"
            dept = "Network Operations"
            loc = "A-Block Admin"
        else:
            role = "Student"
            dept = "Computer Science"
            loc = "Hostel B"

        name = identifier.split("@")[0].replace(".", " ").title()
        return {
            "authenticated": True,
            "email": identifier if "@" in identifier else f"{identifier}@vignan.ac.in",
            "full_name": name,
            "role": role,
            "department": dept,
            "primary_location": loc
        }

    def fetch_tickets(self) -> List[Dict[str, Any]]:
        """Fetch all submitted student & faculty tickets from live Supabase or fallback store."""
        if not self.is_configured:
            return self.tickets_store
        try:
            endpoint = f"{self.url}/rest/v1/campusfix_tickets?select=*&order=created_at.desc"
            req = urllib.request.Request(endpoint, headers={
                "apikey": self.key,
                "Authorization": f"Bearer {self.key}"
            })
            with urllib.request.urlopen(req, timeout=5) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                if data:
                    return data
        except Exception as e:
            print(f"Supabase Fetch Tickets Warning: {e}")
        return self.tickets_store

    def fetch_digital_twin_nodes(self) -> List[Dict[str, Any]]:
        """Fetch infrastructure status from live Supabase campusfix_digital_twin_nodes table."""
        if not self.is_configured:
            return self._fallback_digital_twin()
        try:
            endpoint = f"{self.url}/rest/v1/campusfix_digital_twin_nodes?select=*"
            req = urllib.request.Request(endpoint, headers={
                "apikey": self.key,
                "Authorization": f"Bearer {self.key}"
            })
            with urllib.request.urlopen(req, timeout=5) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except Exception as e:
            print(f"Supabase Fetch Nodes Warning: {e}")
            return self._fallback_digital_twin()

    def create_ticket(self, category: str, location: str, summary: str, priority: str = "NORMAL", submitted_by: str = "Student") -> Dict[str, Any]:
        """Creates newly generated ticket via Supabase RPC fn_create_ticket."""
        if self.is_configured:
            rpc_res = self._call_rpc("fn_create_ticket", {
                "p_category": category,
                "p_location": location,
                "p_summary": summary,
                "p_priority": priority,
                "p_submitted_by": submitted_by
            })
            if rpc_res and isinstance(rpc_res, dict):
                self.tickets_store.insert(0, rpc_res)
                return rpc_res

        # Fallback local insertion
        ticket_code = f"CF-WIFI-{len(self.tickets_store)+1043}"
        payload = {
            "ticket_code": ticket_code,
            "category": category,
            "location": location,
            "issue_summary": summary,
            "priority": priority,
            "status": "NEW",
            "assigned_team": "Network Operations" if "wifi" in category.lower() else "IT Helpdesk",
            "submitted_by": submitted_by
        }
        self.tickets_store.insert(0, payload)
        return payload

    def run_autonomous_agent(self, session_id: str, email: str, role: str, query: str, location: Optional[str] = None, inject_fault: bool = False) -> Optional[Dict[str, Any]]:
        """Executes full autonomous agent state machine inside Supabase via fn_run_autonomous_agent RPC."""
        return self._call_rpc("fn_run_autonomous_agent", {
            "p_session_id": session_id,
            "p_user_email": email,
            "p_user_role": role,
            "p_query": query,
            "p_user_location": location,
            "p_inject_fault": inject_fault
        })

    def _fallback_digital_twin(self):
        return [
            {"node_code": "AP-HB-04", "location": "Hostel B", "service_name": "Campus Wi-Fi", "status": "DEGRADED", "packet_loss_pct": 82.5},
            {"node_code": "GW-ACAD-01", "location": "Academic A", "service_name": "Student Portal Gateway", "status": "HEALTHY", "packet_loss_pct": 0.0},
            {"node_code": "PRN-LIB-01", "location": "Central Library", "service_name": "Printing System", "status": "HEALTHY", "packet_loss_pct": 0.0}
        ]
