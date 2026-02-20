import os
from dotenv import load_dotenv

load_dotenv()

IBM_API_KEY = os.getenv("IBM_API_KEY")
IBM_URL = os.getenv("IBM_URL")


def analyze_sentiment(text: str) -> dict:
    """Analyze sentiment and emotion using IBM Watson NLU."""
    try:
        from ibm_watson import NaturalLanguageUnderstandingV1
        from ibm_watson.natural_language_understanding_v1 import (
            Features, SentimentOptions, EmotionOptions, KeywordsOptions, CategoriesOptions
        )
        from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

        authenticator = IAMAuthenticator(IBM_API_KEY)
        nlu = NaturalLanguageUnderstandingV1(
            version='2022-04-07',
            authenticator=authenticator
        )
        nlu.set_service_url(IBM_URL)

        response = nlu.analyze(
            text=text,
            features=Features(
                sentiment=SentimentOptions(targets=[text[:50]]),
                emotion=EmotionOptions(),
                keywords=KeywordsOptions(sentiment=True, limit=5),
            )
        ).get_result()

        sentiment = response.get("sentiment", {}).get("document", {})
        emotion = response.get("emotion", {}).get("document", {}).get("emotion", {})
        keywords = response.get("keywords", [])

        # Calculate dominant emotion
        dominant_emotion = max(emotion, key=emotion.get) if emotion else "neutral"
        
        # Brand-specific insights
        brand_insights = _generate_brand_insights(sentiment, emotion, dominant_emotion)

        return {
            "success": True,
            "sentiment": {
                "label": sentiment.get("label", "neutral"),
                "score": round(sentiment.get("score", 0), 3),
            },
            "emotions": {k: round(v, 3) for k, v in emotion.items()},
            "dominant_emotion": dominant_emotion,
            "keywords": [kw["text"] for kw in keywords[:5]],
            "brand_insights": brand_insights,
        }

    except ImportError:
        return _fallback_sentiment(text)
    except Exception as e:
        return _fallback_sentiment(text)


def _generate_brand_insights(sentiment: dict, emotion: dict, dominant_emotion: str) -> list:
    """Generate actionable branding insights from sentiment data."""
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
        joy = emotion.get("joy", 0)
        trust_val = emotion.get("disgust", 0)
        fear = emotion.get("fear", 0)
        
        if joy > 0.5:
            insights.append("😊 High joy score — great for consumer/lifestyle brands.")
        if fear > 0.3:
            insights.append("😰 Fear detected — reduce urgency/scarcity language for a friendlier feel.")
        if dominant_emotion == "trust":
            insights.append("🤝 Trust-forward tone — ideal for financial, health, or professional services.")

    return insights


def _fallback_sentiment(text: str) -> dict:
    """Simple keyword-based fallback if IBM Watson is unavailable."""
    positive_words = ["great", "amazing", "innovative", "love", "best", "excellent", "powerful", "inspiring", "beautiful", "simple", "easy", "fast"]
    negative_words = ["bad", "poor", "terrible", "hard", "difficult", "slow", "complex", "expensive", "limited"]
    
    text_lower = text.lower()
    pos_count = sum(1 for w in positive_words if w in text_lower)
    neg_count = sum(1 for w in negative_words if w in text_lower)
    
    if pos_count > neg_count:
        label, score = "positive", round(0.3 + (pos_count * 0.1), 2)
    elif neg_count > pos_count:
        label, score = "negative", round(-0.3 - (neg_count * 0.1), 2)
    else:
        label, score = "neutral", 0.0

    return {
        "success": True,
        "sentiment": {"label": label, "score": min(score, 1.0)},
        "emotions": {"joy": 0.4, "sadness": 0.1, "anger": 0.0, "fear": 0.1, "disgust": 0.0},
        "dominant_emotion": "joy",
        "keywords": [],
        "brand_insights": ["ℹ️ IBM Watson unavailable. Using basic analysis. Add IBM credentials for deep insights."],
        "fallback": True
    }
