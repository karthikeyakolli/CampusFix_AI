import os
import json
import urllib.request
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

def _load_env_key(key_name: str) -> Optional[str]:
    val = os.getenv(key_name)
    if val:
        return val
    env_file = os.path.join(os.path.dirname(__file__), "..", ".env")
    if os.path.exists(env_file):
        with open(env_file, "r", encoding="utf-8") as f:
            for line in f:
                if line.startswith(f"{key_name}="):
                    return line.split("=", 1)[1].strip()
    return None

class OpenRouterService:
    """
    OpenRouter REST API Adapter for CampusFix Autonomous IT Engine.
    Supports routing queries to DeepSeek-R1, Qwen 2.5, or Meta LLaMA via OpenRouter.
    """
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or _load_env_key("OPENROUTER_API_KEY")
        self.endpoint = "https://openrouter.ai/api/v1/chat/completions"
        self.default_model = "deepseek/deepseek-chat"  # Extremely fast, intelligent model

    def is_available(self) -> bool:
        return bool(self.api_key)

    def chat_completion(
        self, 
        prompt: str, 
        system_instruction: Optional[str] = None, 
        temperature: float = 0.2, 
        max_tokens: int = 150,
        model: Optional[str] = "meta-llama/llama-3.3-70b-instruct"
    ) -> Optional[str]:
        if not self.is_available():
            logger.warning("OpenRouter API key missing.")
            return None

        target_model = model or self.default_model
        messages = []
        if system_instruction:
            messages.append({"role": "system", "content": system_instruction})
        messages.append({"role": "user", "content": prompt})

        payload = {
            "model": target_model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens
        }

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://vignan.ac.in",
            "X-Title": "Vignan CampusFix Autonomous IT Engine"
        }

        try:
            req = urllib.request.Request(
                self.endpoint, 
                data=json.dumps(payload).encode("utf-8"), 
                headers=headers,
                method="POST"
            )
            with urllib.request.urlopen(req, timeout=12) as response:
                if response.status == 200:
                    resp_data = json.loads(response.read().decode("utf-8"))
                    choices = resp_data.get("choices", [])
                    if choices:
                        return choices[0].get("message", {}).get("content", "").strip()
        except Exception as e:
            logger.error(f"OpenRouter API execution error: {e}")
            return None

        return None
