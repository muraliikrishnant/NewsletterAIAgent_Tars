from __future__ import annotations

import json
import os
import time
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

import requests

from .config import settings


@dataclass
class ChatMessage:
    role: str
    content: str


class OllamaClient:
    def __init__(self, base_url: str | None = None, model: str | None = None):
        self.base_url = (base_url or settings.ollama_host).rstrip("/")
        if self.base_url.endswith("/api"):
            self.base_url = self.base_url[:-4]
        self.model = model or settings.ollama_model

    def chat(self, messages: List[ChatMessage], temperature: float = 0.3, tools: Optional[List[Dict[str, Any]]] = None, stream: bool = False) -> str:
        url = f"{self.base_url}/api/chat"
        payload: Dict[str, Any] = {
            "model": self.model,
            "messages": [m.__dict__ for m in messages],
            "options": {"temperature": temperature},
            "stream": False,
            # Note: Ollama supports tool calling in newer versions; keep simple for portability
        }
        if tools:
            payload["tools"] = tools
        headers = {"Content-Type": "application/json"}
        if settings.ollama_api_key:
            headers["Authorization"] = f"Bearer {settings.ollama_api_key}"
        resp = requests.post(url, data=json.dumps(payload), headers=headers, timeout=120)
        resp.raise_for_status()
        data = resp.json()
        # When stream=false, Ollama returns the final message under 'message'
        if isinstance(data, dict) and "message" in data and isinstance(data["message"], dict):
            return data["message"].get("content", "").strip()
        # Fallback for different shapes
        if isinstance(data, dict) and "content" in data:
            return str(data["content"]).strip()
        return str(data).strip()


def simple_chat(system: str, user: str) -> str:
    client = OllamaClient()
    return client.chat([
        ChatMessage(role="system", content=system),
        ChatMessage(role="user", content=user),
    ])


def _load_style_assets(style_name: str = "bartlett_hormozi") -> tuple[str, list]:
    base = os.path.join(os.path.dirname(__file__), '..', '..', 'style_guides')
    md_path = os.path.abspath(os.path.join(base, f"{style_name}.md"))
    json_path = os.path.abspath(os.path.join(os.path.dirname(md_path), '..', 'style_examples', f"{style_name}.json"))
    guide = ''
    examples = []
    try:
        if os.path.exists(md_path):
            with open(md_path, 'r', encoding='utf-8') as f:
                guide = f.read()
    except Exception as e:
        print(f"Failed to load style markdown from {md_path}: {e}")
        guide = ''
    try:
        if os.path.exists(json_path):
            with open(json_path, 'r', encoding='utf-8') as f:
                payload = json.load(f)
                examples = payload.get('examples', []) if isinstance(payload, dict) else []
    except Exception:
        examples = []
    return guide, examples




def generate_with_style(task_prompt: str, style_name: str = "bartlett_hormozi") -> str:
    """Compose a prompt using the selected style guide and few-shot examples and call Ollama."""
    guide, examples = _load_style_assets(style_name)
    system_parts = [guide] if guide else []
    # include example prompts in system message to bias the model
    for ex in examples[:3]:
        p = ex.get('prompt') if isinstance(ex, dict) else None
        out = ex.get('output') if isinstance(ex, dict) else None
        if p and out:
            system_parts.append(f"Example prompt:\n{p}\nExample output:\n{out}")
    system = "\n\n".join([s for s in system_parts if s]) or "You are an expert newsletter writer."
    return simple_chat(system, task_prompt)
