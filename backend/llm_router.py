"""
CampusFix — Multi-LLM Routing Engine (llm_router.py)
Hybrid multi-LLM orchestrator combining Groq (fast routing), OpenRouter (DeepSeek R1/Qwen), and Gemini (RAG synthesis & vision).
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
        Sub-1.5 second high-speed grounded RAG synthesis via OpenRouter LLaMA 3.3-70B.
        """
        evidence_str = "\n".join(["- " + e for e in kb_evidence])
        prompt = f"""You are CollegeFix, an autonomous university IT support assistant.
User Role: {role}
Category: {category}
Location: {location or 'Unknown'}
User Query: "{query}"

Verified Evidence & Procedure Documents:
{evidence_str}

INSTRUCTIONS:
1. Provide a direct, helpful, concise resolution in clear standard English.
2. DO NOT use asterisks (* or **), bullet formatting symbols, or markdown tags.
3. Keep the answer under 3 sentences."""

        system_instruction = "You are CollegeFix AI. Write only in clean, natural English prose without markdown asterisks."

        content = None
        if self.openrouter.is_available():
            content = self.openrouter.chat_completion(prompt=prompt, system_instruction=system_instruction)
            source_info = "OpenRouter (LLaMA-3.3-70B)"

        if content:
            content = content.replace("*", "").strip()

        return {
            "content": content,
            "source": source_info if content else "Engine"
        }
