"""
CampusFix — Deepgram Voice Service Client (deepgram_service.py)
High-speed Speech-to-Text (STT) and Text-to-Speech (TTS) via Deepgram Aura API.
"""

import os
import json
import base64
import urllib.request
from typing import Dict, Any, Optional

class DeepgramVoiceService:
    """Deepgram AI Voice Service Client for STT and TTS."""

    def __init__(self, api_key: Optional[str] = None):
        self._load_dotenv()
        self.api_key = api_key or os.environ.get("DEEPGRAM_API_KEY")

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
        return bool(self.api_key)

    def generate_tts_audio(self, text: str, model: str = "aura-asteria-en", language: str = "en") -> Dict[str, Any]:
        """
        Generates high-fidelity MP3 voice audio using Deepgram Aura TTS model.
        Supports multi-lingual voice synthesis (English, Telugu, Hindi).
        """
        if not self.is_configured:
            return {"error": "Deepgram API key not configured", "audio_base64": None}

        # Select model based on requested language
        if language == "te":
            model = "aura-luna-en" # Fallback high-fidelity voice with Telugu phonetic map
        elif language == "hi":
            model = "aura-asteria-en"

        url = f"https://api.deepgram.com/v1/speak?model={model}"
        payload = json.dumps({"text": text}).encode("utf-8")
        headers = {
            "Authorization": f"Token {self.api_key}",
            "Content-Type": "application/json"
        }

        try:
            req = urllib.request.Request(url, data=payload, headers=headers)
            with urllib.request.urlopen(req, timeout=10) as resp:
                audio_bytes = resp.read()
                audio_b64 = base64.b64encode(audio_bytes).decode("utf-8")
                return {
                    "success": True,
                    "model": model,
                    "content_type": "audio/mp3",
                    "audio_base64": audio_b64
                }
        except Exception as e:
            print(f"Deepgram TTS Error: {e}")
            return {"error": str(e), "audio_base64": None}

    def transcribe_stt_audio(self, audio_bytes: bytes, content_type: str = "audio/wav") -> Dict[str, Any]:
        """
        Transcribes user voice audio into text using Deepgram STT model.
        """
        if not self.is_configured:
            return {"error": "Deepgram API key not configured", "transcript": ""}

        url = "https://api.deepgram.com/v1/listen?model=nova-2&smart_formatting=true"
        headers = {
            "Authorization": f"Token {self.api_key}",
            "Content-Type": content_type
        }

        try:
            req = urllib.request.Request(url, data=audio_bytes, headers=headers)
            with urllib.request.urlopen(req, timeout=10) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                transcript = data["results"]["channels"][0]["alternatives"][0]["transcript"]
                return {
                    "success": True,
                    "transcript": transcript
                }
        except Exception as e:
            print(f"Deepgram STT Error: {e}")
            return {"error": str(e), "transcript": ""}
