"""
CampusFix AI — Backend Data Models & Schemas (models.py)
Supports Pydantic schemas when available, with clean dataclass fallbacks.
"""

from typing import List, Optional, Dict, Any
from enum import Enum
from datetime import datetime

class UserRole(str, Enum):
    STUDENT = "Student"
    FACULTY = "Faculty"
    IT_STAFF = "IT Staff"
    ADMIN = "Admin"

class TicketPriority(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"

class TicketStatus(str, Enum):
    NEW = "NEW"
    ASSIGNED = "ASSIGNED"
    IN_PROGRESS = "IN_PROGRESS"
    RESOLVED = "RESOLVED"
    ESCALATED = "ESCALATED"
    CLOSED = "CLOSED"

class HealthStatus(str, Enum):
    HEALTHY = "HEALTHY"
    DEGRADED = "DEGRADED"
    OUTAGE = "OUTAGE"
    MAINTENANCE = "MAINTENANCE"

try:
    from pydantic import BaseModel, Field

    class StructuredQuestion(BaseModel):
        question_text: str
        target_entity: str
        options: List[str]

    class ChatRequest(BaseModel):
        message: str
        role: UserRole = UserRole.STUDENT
        session_id: Optional[str] = "session-demo-001"
        location: Optional[str] = None
        image_base64: Optional[str] = None

    class DiagnoseRequest(BaseModel):
        message: str
        location: Optional[str] = None
        category: Optional[str] = None
        role: UserRole = UserRole.STUDENT

    class TicketCreateRequest(BaseModel):
        issue_summary: str
        category: str
        location: str
        priority: TicketPriority = TicketPriority.MEDIUM
        role: UserRole = UserRole.STUDENT
        evidence_data: Optional[Dict[str, Any]] = None

    class SimulationScenarioRequest(BaseModel):
        scenario_name: str

    class AgentEvent(BaseModel):
        step_name: str
        title: str
        detail: Optional[str] = None
        timestamp: str = Field(default_factory=lambda: datetime.now().strftime("%H:%M:%S"))

    class ChatResponse(BaseModel):
        message: str
        category: str
        confidence: float
        location: Optional[str] = None
        next_question: Optional[str] = None
        structured_question: Optional[Dict[str, Any]] = None
        evidence_list: List[str] = []
        timeline_events: List[AgentEvent] = []
        ticket_id: Optional[str] = None
        assigned_ticket: Optional[Dict[str, Any]] = None
        incident_correlated: bool = False
        simulated: bool = True

except ImportError:
    # Dataclass Fallback if pydantic is not installed
    from dataclasses import dataclass, field, asdict

    @dataclass
    class StructuredQuestion:
        question_text: str
        target_entity: str
        options: List[str]
        def dict(self): return asdict(self)

    @dataclass
    class AgentEvent:
        step_name: str
        title: str
        detail: Optional[str] = None
        timestamp: str = field(default_factory=lambda: datetime.now().strftime("%H:%M:%S"))
        def dict(self): return asdict(self)

    @dataclass
    class ChatRequest:
        message: str
        role: UserRole = UserRole.STUDENT
        session_id: Optional[str] = "session-demo-001"
        location: Optional[str] = None
        image_base64: Optional[str] = None

    @dataclass
    class DiagnoseRequest:
        message: str
        location: Optional[str] = None
        category: Optional[str] = None
        role: UserRole = UserRole.STUDENT

    @dataclass
    class TicketCreateRequest:
        issue_summary: str
        category: str
        location: str
        priority: TicketPriority = TicketPriority.MEDIUM
        role: UserRole = UserRole.STUDENT
        evidence_data: Optional[Dict[str, Any]] = None

    @dataclass
    class SimulationScenarioRequest:
        scenario_name: str

    @dataclass
    class ChatResponse:
        message: str
        category: str
        confidence: float
        location: Optional[str] = None
        next_question: Optional[str] = None
        structured_question: Optional[Dict[str, Any]] = None
        evidence_list: List[str] = field(default_factory=list)
        timeline_events: List[AgentEvent] = field(default_factory=list)
        ticket_id: Optional[str] = None
        assigned_ticket: Optional[Dict[str, Any]] = None
        incident_correlated: bool = False
        simulated: bool = True
        def dict(self):
            d = asdict(self)
            d["timeline_events"] = [e.dict() if hasattr(e, "dict") else e for e in self.timeline_events]
            return d
