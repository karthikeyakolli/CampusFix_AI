"""
CampusFix — Groq LLM Service Adapter (groq_service.py)
Provides ultra-fast sub-200ms LLaMA-3 inference via Groq API.
"""

import os
import json
import urllib.request
import urllib.parse
from typing import Dict, Any, List, Optional

class GroqService:
    """Ultra-fast Groq LLaMA-3 inference engine with safe fallback."""

    def __init__(self, api_key: Optional[str] = None):
        self._load_dotenv()
        self.api_key = api_key or os.environ.get("GROQ_API_KEY")
        self.model_name = "llama-3.3-70b-versatile"

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
        return bool(self.api_key and len(self.api_key.strip()) > 0)

    def fast_classify_and_structure(self, query: str) -> Dict[str, Any]:
        """
        Executes sub-200ms intent classification and dynamic question structuring via Groq LLaMA 3.3.
        """
        if not self.is_configured:
            return {"source": "Fallback-Classifier", "category": "general", "structured": False}

        prompt = f"""Classify the campus IT user query and return JSON with keys 'category' (wifi, login, printer, or general) and 'confidence' (0.0 to 1.0).
User Query: "{query}"
Return ONLY raw valid JSON."""

        try:
            url = "https://api.groq.com/openai/v1/chat/completions"
            payload = {
                "model": self.model_name,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.1,
                "max_tokens": 150,
                "response_format": {"type": "json_object"}
            }
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}"
            }
            req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers=headers)
            with urllib.request.urlopen(req, timeout=5) as resp:
                res_data = json.loads(resp.read().decode("utf-8"))
                content = res_data["choices"][0]["message"]["content"]
                parsed = json.loads(content)
                parsed["source"] = "Groq LLaMA 3.3 (Fast-Path)"
                return parsed
        except Exception as e:
            print(f"Groq API Call Note: {e}")
            return {"source": "Fallback-Classifier", "category": "general", "confidence": 0.5}

    def generate_fast_grounded_response(
        self, 
        query: str, 
        category: str, 
        location: Optional[str], 
        kb_evidence: List[str], 
        role: str = "Student"
    ) -> Dict[str, Any]:
        """
        Sub-200ms ultra-fast grounded response generation using Groq LLaMA-3.3-70B.
        """
        if not self.is_configured:
            return {"source": "Groq-Unavailable", "content": None}

        evidence_str = "\n".join(["- " + e for e in kb_evidence])
        prompt = f"""You are CollegeFix, an autonomous university IT support assistant.
User Role: {role}
Category: {category}
Location: {location or 'Unknown'}
User Query: "{query}"

Verified Evidence & Procedure Documents:
{evidence_str}

INSTRUCTIONS:
1. Provide a step-by-step structured resolution like ChatGPT.
2. Structure your response into clear Markdown sections using `### 🔍 Step 1: ...`, `### 🛠️ Step 2: ...`, and `### 📋 Step 3: ...`.
3. Use bold text, code blocks, and numbered lists for action points."""

        try:
            url = "https://api.groq.com/openai/v1/chat/completions"
            payload = {
                "model": self.model_name,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.1,
                "max_tokens": 400
            }
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}"
            }
            req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers=headers)
            with urllib.request.urlopen(req, timeout=4) as resp:
                res_data = json.loads(resp.read().decode("utf-8"))
                text = res_data["choices"][0]["message"]["content"]
                text = text.strip()
                return {
                    "source": "Groq LLaMA-3.3-70B (Fast-Path)",
                    "content": text
                }
        except Exception as e:
            print(f"Groq Synthesis Note: {e}")
            return {"source": "Groq-Fallback", "content": None}
