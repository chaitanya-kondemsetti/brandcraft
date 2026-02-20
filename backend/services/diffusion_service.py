import requests
import os
import base64
import time
from dotenv import load_dotenv

load_dotenv(override=True)

_raw_token = os.getenv("HF_TOKEN", "")
HF_TOKEN = _raw_token.strip().strip("'\"").strip()

HEADERS = {
    "Authorization": f"Bearer {HF_TOKEN}",
    "Content-Type": "application/json"
}

# Updated to new HuggingFace router URL
MODELS = [
    "black-forest-labs/FLUX.1-schnell",
    "stabilityai/stable-diffusion-xl-base-1.0",
    "runwayml/stable-diffusion-v1-5",
]

STYLE_PROMPTS = {
    "minimalist": "minimalist flat vector logo, clean lines, simple geometric shapes",
    "modern": "modern professional logo, bold typography, sleek design",
    "playful": "playful colorful logo, fun shapes, friendly design, cartoon style",
    "luxury": "luxury premium logo, elegant serif, gold accents, sophisticated",
    "tech": "tech startup logo, futuristic geometric, gradient, digital aesthetic",
    "organic": "organic natural logo, hand-drawn feel, earthy, botanical elements",
}


def generate_logo(brand_name: str, style: str, primary_color: str, industry: str) -> dict:
    if not HF_TOKEN:
        return {"success": False, "error": "HF_TOKEN is not set in your .env file."}

    style_desc = STYLE_PROMPTS.get(style, STYLE_PROMPTS["modern"])
    prompt = (
        f"{style_desc} for '{brand_name}' brand in {industry} industry, "
        f"{primary_color} color scheme, white background, professional, "
        f"high quality, vector art style, centered composition"
    )

    for model in MODELS:
        # New router URL format
        api_url = f"https://router.huggingface.co/hf-inference/models/{model}"
        print(f"[Logo] Trying: {api_url}")

        try:
            response = requests.post(
                api_url,
                headers=HEADERS,
                json={"inputs": prompt},
                timeout=90
            )

            print(f"[Logo] Status: {response.status_code}")

            if response.status_code == 200:
                content_type = response.headers.get("content-type", "")
                if "image" in content_type or len(response.content) > 1000:
                    image_b64 = base64.b64encode(response.content).decode("utf-8")
                    print(f"[Logo] Success with {model}")
                    return {
                        "success": True,
                        "image_base64": image_b64,
                        "prompt_used": prompt,
                        "model": model
                    }
                else:
                    print(f"[Logo] Non-image response: {response.text[:200]}")

            elif response.status_code == 401:
                return {"success": False, "error": "HF_TOKEN is invalid. Get a new one from https://huggingface.co/settings/tokens"}

            elif response.status_code == 503:
                try:
                    wait = response.json().get("estimated_time", 20)
                    print(f"[Logo] Model loading, waiting {min(wait,30)}s...")
                    time.sleep(min(wait, 30))
                except:
                    time.sleep(20)
                # Retry
                retry = requests.post(api_url, headers=HEADERS, json={"inputs": prompt}, timeout=90)
                print(f"[Logo] Retry status: {retry.status_code}")
                if retry.status_code == 200:
                    image_b64 = base64.b64encode(retry.content).decode("utf-8")
                    return {"success": True, "image_base64": image_b64, "prompt_used": prompt, "model": model}

            else:
                print(f"[Logo] Error {response.status_code}: {response.text[:300]}")

        except requests.exceptions.Timeout:
            print(f"[Logo] Timeout on {model}, trying next...")
            continue
        except Exception as e:
            print(f"[Logo] Exception: {e}")
            continue

    return {
        "success": False,
        "error": "Logo generation failed. Check terminal logs for details."
    }