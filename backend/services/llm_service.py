"""
services/llm_service.py
OpenRouter LLM Service — all AI calls go through here.
Supports: Qwen Coder, Llama, Gemma, DeepSeek, Mistral
"""
import httpx
import json
import re
from typing import Optional
from ..config import get_settings

settings = get_settings()


class LLMService:
    """Handles all communication with OpenRouter API."""

    def __init__(self):
        self.api_key  = settings.openrouter_api_key
        self.model    = settings.openrouter_model
        self.base_url = settings.openrouter_base_url
        self.headers  = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type":  "application/json",
            "HTTP-Referer":  "https://coderefine.ai",
            "X-Title":       "CodeRefine AI",
        }

    async def _call(
        self,
        messages:    list[dict],
        temperature: float = 0.2,
        max_tokens:  int   = 4096,
    ) -> str:
        """
        Make a chat completion request to OpenRouter.
        Returns the raw text content from the model response.
        """
        payload = {
            "model":       self.model,
            "messages":    messages,
            "temperature": temperature,
            "max_tokens":  max_tokens,
        }

        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                self.base_url,
                headers=self.headers,
                json=payload,
            )
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"].strip()

    async def call_json(
        self,
        messages:    list[dict],
        temperature: float = 0.1,
        max_tokens:  int   = 4096,
    ) -> dict:
        """
        Make a call and parse the response as JSON.
        Strips markdown code fences if present.

        FIX: Replaced fragile split-based fence stripping with regex
        to correctly handle fences even when JSON content contains
        code blocks internally.
        """
        raw = await self._call(messages, temperature, max_tokens)

        # Strip leading ```json or ``` fence and trailing ``` fence
        raw = re.sub(r"^```(?:json)?\s*", "", raw.strip())
        raw = re.sub(r"\s*```$", "", raw.strip())

        try:
            return json.loads(raw.strip())
        except json.JSONDecodeError:
            # Attempt to extract JSON object from surrounding text
            start = raw.find("{")
            end   = raw.rfind("}") + 1
            if start != -1 and end > start:
                return json.loads(raw[start:end])
            raise ValueError(f"Model did not return valid JSON. Raw:\n{raw[:500]}")

    async def call_text(
        self,
        messages:    list[dict],
        temperature: float = 0.3,
        max_tokens:  int   = 2048,
    ) -> str:
        """Make a call and return plain text."""
        return await self._call(messages, temperature, max_tokens)

    async def check_connection(self) -> bool:
        """Ping OpenRouter to verify credentials are working."""
        try:
            result = await self._call(
                [{"role": "user", "content": "Reply with the single word: OK"}],
                max_tokens=5,
            )
            return "OK" in result or len(result) < 20
        except Exception:
            return False


# Singleton instance
llm = LLMService()
