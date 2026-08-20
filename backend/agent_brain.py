"""
CampusFix — Cognitive Agent Brain (agent_brain.py)
Perception & Dynamic Question Builder for VFSTR Vadlamudi Blocks (A, N, H, P, U & Hostels).
"""

import json
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, asdict
from backend.models import StructuredQuestion

@dataclass
class CognitivePercept:
    intent: str
    urgency: str
    location: Optional[str]
    service: str
    missing_entities: List[str]
    raw_query: str

class PerceptEngine:
    """Perceives user intent and extracts VFSTR Vadlamudi blocks (A, N, H, P, U & Hostels)."""

    VFSTR_BLOCKS = {
        "a-block": "A-Block (NTR Vignan Bhavan Admin)",
        "admin": "A-Block (NTR Vignan Bhavan Admin)",
        "h-block": "H-Block (A.P.J. Abdul Kalam CSE/IT)",
        "cse": "H-Block (A.P.J. Abdul Kalam CSE/IT)",
        "n-block": "N-Block (Pharmacy & Bio-Tech)",
        "pharmacy": "N-Block (Pharmacy & Bio-Tech)",
        "p-block": "P-Block (Civil Engineering)",
        "civil": "P-Block (Civil Engineering)",
        "u-block": "U-Block (Mechanical & Robotics)",
        "mech": "U-Block (Mechanical & Robotics)",
        "library": "Central Library (L-Block)",
        "l-block": "Central Library (L-Block)",
        "hostel b": "Hostel B (Vignan Boys Hostel)",
        "boys hostel": "Hostel B (Vignan Boys Hostel)",
        "priyadarshini": "Priyadarshini Girls Hostel (P-Hostel)",
        "girls hostel": "Priyadarshini Girls Hostel (P-Hostel)",
        "oat": "Open Air Theatre (OAT) & SAC",
        "sports": "Vignan Sports Complex & Gymnasium",
        "canteen": "Vignan Main Food Court & Canteen"
    }

    def perceive(self, query: str, user_location: Optional[str] = None) -> CognitivePercept:
        t = query.lower()
        
        # 1. Intent Detection
        if any(w in t for w in ["wifi", "wi-fi", "internet", "signal", "ap-hb", "vfstr-student", "vfstr-faculty"]):
            intent = "wifi_outage"
            service = "VFSTR Campus Wi-Fi"
        elif any(w in t for w in ["login", "portal", "password", "sso", "roll number", "auth", "vignan.ac.in"]):
            intent = "login_issue"
            service = "Vignan Student/Faculty SSO Portal"
        elif any(w in t for w in ["printer", "print", "jam", "xerox", "prn-lib-01", "library print"]):
            intent = "printer_fault"
            service = "Central Library Printing System"
        elif any(w in t for w in ["av", "projector", "smart classroom", "smart board", "hpc", "h-102", "u-201", "n-104"]):
            intent = "faculty_av_dispatch"
            service = "Smart Classroom & Lab AV System"
        elif any(w in t for w in ["fee", "payment", "hall ticket", "exam fee", "gateway"]):
            intent = "fee_portal_issue"
            service = "Vignan Examination & Fee Gateway"
        elif any(w in t for w in ["attendance", "app", "grade sheet", "marks"]):
            intent = "attendance_discrepancy"
            service = "Vignan Student Attendance Portal"
        elif any(w in t for w in ["rfid", "ieee", "ezproxy", "book checkout", "journal"]):
            intent = "rfid_library_issue"
            service = "Digital Library & EZProxy System"
        elif any(w in t for w in ["power", "ro water", "ac", "biometric gate", "curfew", "socket"]):
            intent = "hostel_power_amenity"
            service = "Hostel Infrastructure & Amenities"
        else:
            intent = "general_inquiry"
            service = "VFSTR Campus IT Infrastructure"

        # 2. Urgency Perception
        if any(w in t for w in ["urgent", "immediately", "exam", "class now", "blocked", "outage", "down"]):
            urgency = "URGENT"
        else:
            urgency = "NORMAL"

        # 3. Location Extraction
        location = user_location
        if not location:
            for key, val in self.VFSTR_BLOCKS.items():
                if key in t:
                    location = val
                    break

        # 4. Identify Missing Entities
        missing_entities = []
        if not location and intent in ["wifi_outage", "printer_fault", "faculty_av_dispatch"]:
            missing_entities.append("location")

        return CognitivePercept(
            intent=intent,
            urgency=urgency,
            location=location,
            service=service,
            missing_entities=missing_entities,
            raw_query=query
        )

class DynamicQuestionBuilder:
    """Constructs dynamic diagnostic questions with option pills for Blocks A, N, H, P, U."""

    def build_question(self, percept: CognitivePercept) -> Optional[StructuredQuestion]:
        if "location" in percept.missing_entities:
            if percept.intent == "wifi_outage":
                return StructuredQuestion(
                    question_text="📍 Which VFSTR Vadlamudi campus block or hostel are you experiencing this issue at?",
                    target_entity="location",
                    options=[
                        "Hostel B (Vignan Boys Hostel)",
                        "Priyadarshini Girls Hostel (P-Hostel)",
                        "H-Block (A.P.J. Abdul Kalam CSE/IT)",
                        "N-Block (Pharmacy & Bio-Tech)",
                        "U-Block (Mechanical & Robotics)",
                        "P-Block (Civil Engineering)",
                        "A-Block (NTR Vignan Bhavan)"
                    ]
                )
            elif percept.intent == "faculty_av_dispatch":
                return StructuredQuestion(
                    question_text="🎥 Which classroom or lab block requires AV dispatch?",
                    target_entity="location",
                    options=[
                        "H-Block Smart Classroom H-102",
                        "U-Block Seminar Hall U-201",
                        "N-Block Bio-Tech Smart Lab",
                        "P-Block Civil CAD Lab"
                    ]
                )

        return None

class CognitiveBrain:
    """Master Cognitive Engine for VFSTR Blocks A, N, H, P, U."""

    def __init__(self):
        self.percept_engine = PerceptEngine()
        self.question_builder = DynamicQuestionBuilder()

    def think(self, query: str, user_location: Optional[str] = None) -> Dict[str, Any]:
        percept = self.percept_engine.perceive(query, user_location)
        structured_q = self.question_builder.build_question(percept)
        
        return {
            "percept": asdict(percept),
            "structured_question": asdict(structured_q) if structured_q else None
        }
