import os
from dotenv import load_dotenv

load_dotenv(override=True)

IBM_API_KEY = os.getenv("IBM_API_KEY", "").strip().strip("'\"").strip()
IBM_URL = os.getenv("IBM_URL", "").strip().strip("'\"").strip()


def analyze_sentiment(text: str) -> dict:
    """Analyze sentiment and emotion using IBM Watson NLU."""

    # ── Pre-flight checks ─────────────────────────────────────────
    if not IBM_API_KEY:
        print("[IBM] ERROR: IBM_API_KEY is not set in .env")
        return _fallback_sentiment(text, reason="IBM_API_KEY is missing from .env")

    if not IBM_URL:
        print("[IBM] ERROR: IBM_URL is not set in .env")
        return _fallback_sentiment(text, reason="IBM_URL is missing from .env")

    print(f"[IBM] API key prefix: {IBM_API_KEY[:8]}...")
    print(f"[IBM] URL: {IBM_URL}")

    # ── Try IBM SDK ────────────────────────────────────────────────
    try:
        from ibm_watson import NaturalLanguageUnderstandingV1
        from ibm_watson.natural_language_understanding_v1 import (
            Features, SentimentOptions, EmotionOptions, KeywordsOptions
        )
        from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
    except ImportError as e:
        print(f"[IBM] ImportError: {e} — run: pip install ibm-watson")
        return _fallback_sentiment(text, reason=f"ibm-watson package not installed: {e}")

    try:
        authenticator = IAMAuthenticator(IBM_API_KEY)
        nlu = NaturalLanguageUnderstandingV1(
            version='2022-04-07',
            authenticator=authenticator
        )

        # Ensure URL has no trailing slash and has https://
        url = IBM_URL.rstrip('/')
        if not url.startswith('http'):
            url = 'https://' + url
        nlu.set_service_url(url)

        # Watson needs at least ~100 chars to detect language reliably
        analysis_text = text
        if len(text) < 100:
            analysis_text = (text + " ") * (100 // len(text) + 1)
            analysis_text = analysis_text[:300].strip()
            print(f"[IBM] Text too short ({len(text)} chars), padding to {len(analysis_text)} chars")

        print(f"[IBM] Sending request ({len(analysis_text)} chars)...")
        response = nlu.analyze(
            text=analysis_text,
            language='en',
            features=Features(
                sentiment=SentimentOptions(),
                emotion=EmotionOptions(),
                keywords=KeywordsOptions(sentiment=True, limit=5),
            )
        ).get_result()

        print(f"[IBM] Success!")

        sentiment = response.get("sentiment", {}).get("document", {})
        emotion   = response.get("emotion", {}).get("document", {}).get("emotion", {})
        keywords  = response.get("keywords", [])
        dominant_emotion = max(emotion, key=emotion.get) if emotion else "neutral"
        brand_insights   = _generate_brand_insights(sentiment, emotion, dominant_emotion)

        return {
            "success": True,
            "sentiment": {
                "label": sentiment.get("label", "neutral"),
                "score": round(sentiment.get("score", 0), 3),
            },
            "emotions":         {k: round(v, 3) for k, v in emotion.items()},
            "dominant_emotion": dominant_emotion,
            "keywords":         [kw["text"] for kw in keywords[:5]],
            "brand_insights":   brand_insights,
            "fallback":         False
        }

    except Exception as e:
        err_str = str(e)
        print(f"[IBM] Exception: {err_str}")

        # Give specific, actionable error messages
        if "401" in err_str or "Unauthorized" in err_str or "invalid_credentials" in err_str.lower():
            reason = "IBM API key is invalid or expired. Generate a new key at cloud.ibm.com"
        elif "403" in err_str or "Forbidden" in err_str:
            reason = "IBM API key lacks access. Check that NLU service is provisioned in IBM Cloud"
        elif "422" in err_str or "not enough text" in err_str.lower():
            reason = "Text too short for Watson to analyze. Please enter at least 3-4 sentences."
        elif "404" in err_str or "Not Found" in err_str:
            reason = f"IBM_URL is wrong. Check your NLU instance URL in IBM Cloud (current: {IBM_URL})"
        elif "Connection" in err_str or "connect" in err_str.lower():
            reason = f"Cannot reach IBM Watson. Check your IBM_URL setting"
        else:
            reason = f"IBM Watson error: {err_str}"

        return _fallback_sentiment(text, reason=reason)


def _generate_brand_insights(sentiment: dict, emotion: dict, dominant_emotion: str) -> list:
    insights = []
    label = sentiment.get("label", "neutral")
    score = sentiment.get("score", 0)

    if label == "positive" and score > 0.5:
        insights.append("✅ Your brand messaging is strongly positive — this builds customer trust.")
    elif label == "positive":
        insights.append("👍 Your messaging leans positive. Consider amplifying emotional language.")
    elif label == "negative":
        insights.append("⚠️ Your brand text reads as negative. Try reframing with benefits instead of problems.")
    else:
        insights.append("💡 Neutral tone detected. Add more passion and personality to stand out.")

    if emotion:
        joy  = emotion.get("joy", 0)
        fear = emotion.get("fear", 0)
        if joy > 0.5:
            insights.append("😊 High joy score — great for consumer/lifestyle brands.")
        if fear > 0.3:
            insights.append("😰 Fear detected — reduce urgency/scarcity language for a friendlier feel.")
        if dominant_emotion == "trust":
            insights.append("🤝 Trust-forward tone — ideal for financial, health, or professional services.")

    return insights


def _fallback_sentiment(text: str, reason: str = "IBM Watson unavailable") -> dict:
    """Keyword-based fallback with specific error reason."""
    positive_words = ["great","amazing","innovative","love","best","excellent","powerful","inspiring","beautiful","simple","easy","fast","accessible","sustainable","joyful"]
    negative_words = ["bad","poor","terrible","hard","difficult","slow","complex","expensive","limited","compromise"]

    text_lower = text.lower()
    pos = sum(1 for w in positive_words if w in text_lower)
    neg = sum(1 for w in negative_words if w in text_lower)

    if pos > neg:
        label, score = "positive", min(round(0.3 + pos * 0.08, 2), 1.0)
    elif neg > pos:
        label, score = "negative", min(round(0.3 + neg * 0.08, 2), 1.0)
    else:
        label, score = "neutral", 0.1

    return {
        "success":          True,
        "sentiment":        {"label": label, "score": score},
        "emotions":         {"joy": 0.4, "sadness": 0.1, "anger": 0.0, "fear": 0.1, "disgust": 0.0},
        "dominant_emotion": "joy",
        "keywords":         [],
        "brand_insights":   [f"⚠️ {reason}", "ℹ️ Showing basic keyword-based analysis instead."],
        "fallback":         True
    }