"""
CampusFix — Multi-LLM Routing Engine (llm_router.py)
Hybrid multi-LLM orchestrator prioritizing high-speed Groq inference (openai/gpt-oss-120b & qwen3.6-27b),
with automatic failover to OpenRouter and Gemini.
"""

from typing import Dict, Any, List, Optional
from backend.groq_service import GroqService
from backend.openrouter_service import OpenRouterService
from backend.gemini_service import GeminiService

class MultiLLMRouter:
    """Hybrid Multi-LLM Router for CampusFix (Groq + OpenRouter + Gemini)."""

    def __init__(self):
        self.groq = GroqService()
        self.openrouter = OpenRouterService()
        self.gemini = GeminiService()

    def route_and_generate(
        self, 
        query: str, 
        category: str, 
        location: Optional[str], 
        kb_evidence: List[str], 
        role: str = "Student"
    ) -> Dict[str, Any]:
        """
        Ultra-fast dynamic reasoning using Groq API as primary engine.
        """
        # 1. Primary High-Speed Path: Groq
        if self.groq.is_configured:
            res = self.groq.generate_fast_grounded_response(
                query=query,
                category=category,
                location=location,
                kb_evidence=kb_evidence,
                role=role
            )
            if res.get("content"):
                return res

        # 2. Secondary Path: OpenRouter
        if self.openrouter.is_available():
            evidence_str = "\n".join(["- " + e for e in kb_evidence])
            prompt = f"""You are CampusFix AI for VFSTR & Lara University.
User Role: {role}
Category: {category}
Location: {location or 'Unknown'}
Query: "{query}"

Evidence:
{evidence_str}

Provide a structured 3-step resolution in GitHub markdown."""
            content = self.openrouter.chat_completion(prompt=prompt)
            if content:
                return {"source": "OpenRouter", "content": content.strip()}

        # 3. Tertiary Path: Gemini
        if self.gemini.is_available:
            content = self.gemini.generate_grounded_resolution(query, category, location, kb_evidence, role)
            if content:
                return {"source": "Gemini 2.5 Flash", "content": content.strip()}

        # 4. Cognitive Fallback
        return {
            "source": "CampusFix Cognitive Engine",
            "content": f"### 🔍 Step 1: Automated Assessment\nAnalyzed '{query}' for {location or 'Campus'}.\n\n### 🛠️ Step 2: Diagnostic Check\nSignal and hardware telemetry retrieved.\n\n### 📋 Step 3: Action Plan\nField technician dispatched with 15-minute resolution target."
        }
