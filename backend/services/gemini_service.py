import os
import json
import requests
from dotenv import load_dotenv

load_dotenv(override=True)

_raw_key = os.getenv("OPENROUTER_API_KEY", "")
OPENROUTER_API_KEY = _raw_key.strip().strip("'\"").strip()

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"


MODEL = "arcee-ai/trinity-large-preview:free"


def _chat(messages: list) -> str:
    """Call OpenRouter API with a messages array."""
    if not OPENROUTER_API_KEY:
        raise ValueError("OPENROUTER_API_KEY is not set in your .env file")

    response = requests.post(
        OPENROUTER_URL,
        headers={
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": "http://localhost:8000",
            "X-Title": "BrandCraft"
        },
        json={
            "model": MODEL,
            "messages": messages
        },
        timeout=60
    )
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"].strip()


def _parse_json(text: str) -> dict:
    """Strip markdown fences and parse JSON."""
    text = text.strip()
    if text.startswith("```"):
        text = text.split("```")[1]
        if text.startswith("json"):
            text = text[4:]
    return json.loads(text.strip())


def generate_brand_names(niche: str, tone: str, audience: str) -> dict:
    prompt = f"""You are an expert brand naming consultant.
Generate 6 unique, memorable brand names for a {niche} business.
Target audience: {audience}
Brand tone: {tone}

For each name return:
- name: the brand name
- tagline: a catchy one-liner tagline
- meaning: brief explanation of why this name works (1-2 sentences)
- style: personality descriptor (e.g., Bold, Playful, Sophisticated)

Respond ONLY in this exact JSON format (no markdown fences):
{{
  "names": [
    {{"name": "...", "tagline": "...", "meaning": "...", "style": "..."}}
  ]
}}"""

    text = _chat([
        {"role": "system", "content": "You are an expert brand naming consultant. Always respond with valid JSON only, no markdown."},
        {"role": "user", "content": prompt}
    ])
    return _parse_json(text)


def generate_brand_content(brand_name: str, niche: str, content_type: str, tone: str) -> dict:
    prompts = {
        "tagline": f"""Create 5 powerful taglines for '{brand_name}', a {niche} brand with a {tone} tone.
Return JSON only: {{"taglines": [{{"text": "...", "use_case": "..."}}]}}""",

        "bio": f"""Write 3 versions of a brand bio for '{brand_name}' ({niche}, {tone} tone):
- short: 50 words for Twitter/X
- medium: 100 words for Instagram/LinkedIn
- long: 200 words for website About page
Return JSON only: {{"bios": {{"short": "...", "medium": "...", "long": "..."}}}}""",

        "ad_copy": f"""Write 3 ad copies for '{brand_name}' ({niche}, {tone} tone).
Each with: headline, body (2-3 sentences), cta, platform.
Return JSON only: {{"ads": [{{"platform": "Facebook", "headline": "...", "body": "...", "cta": "..."}}]}}""",

        "email": f"""Write a welcome email for '{brand_name}' ({niche}, {tone} tone).
Return JSON only: {{"subject": "...", "preview": "...", "body": "...", "sign_off": "..."}}""",

        "social": f"""Write 4 social media posts for '{brand_name}' ({niche}, {tone} tone) for different platforms.
Return JSON only: {{"posts": [{{"platform": "...", "content": "...", "hashtags": ["..."]}}]}}"""
    }

    text = _chat([
        {"role": "system", "content": "You are a brand content writer. Always respond with valid JSON only, no markdown fences."},
        {"role": "user", "content": prompts[content_type]}
    ])
    return _parse_json(text)


def branding_assistant_chat(messages: list, user_message: str) -> str:
    system = """You are BrandCraft AI, an expert branding consultant with 20 years of experience.
You help entrepreneurs and creators build powerful brand identities from scratch.
You are warm, encouraging, and give actionable, specific advice.
Ask clarifying questions to understand their vision. Guide them step by step through:
1. Brand purpose & mission
2. Target audience definition
3. Brand personality & tone
4. Naming strategy
5. Visual identity direction
6. Content voice & messaging

Keep responses concise (under 200 words) but impactful. Use bullet points sparingly."""

    conversation = [{"role": "system", "content": system}]
    for msg in messages[-10:]:
        conversation.append({"role": msg["role"], "content": msg["content"]})
    conversation.append({"role": "user", "content": user_message})

    return _chat(conversation)