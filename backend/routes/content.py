from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Literal
from services.gemini_service import generate_brand_content

router = APIRouter()


class ContentRequest(BaseModel):
    brand_name: str
    niche: str
    tone: str = "professional"
    content_type: Literal["tagline", "bio", "ad_copy", "email", "social"] = "tagline"


@router.post("/content")
async def create_content(request: ContentRequest):
    if not request.brand_name.strip():
        raise HTTPException(status_code=400, detail="Brand name cannot be empty")
    try:
        result = generate_brand_content(
            request.brand_name,
            request.niche,
            request.content_type,
            request.tone
        )
        return {"content_type": request.content_type, "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Content generation failed: {str(e)}")
