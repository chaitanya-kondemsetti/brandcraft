from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.ibm_service import analyze_sentiment

router = APIRouter()


class SentimentRequest(BaseModel):
    text: str


@router.post("/sentiment")
async def get_sentiment(request: SentimentRequest):
    if not request.text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty")
    if len(request.text) < 10:
        raise HTTPException(status_code=400, detail="Text must be at least 10 characters")
    try:
        result = analyze_sentiment(request.text)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Sentiment analysis failed: {str(e)}")
