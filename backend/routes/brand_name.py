from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.gemini_service import generate_brand_names

router = APIRouter()


class BrandNameRequest(BaseModel):
    niche: str
    tone: str = "professional"
    audience: str = "general consumers"


@router.post("/brand-name")
async def create_brand_names(request: BrandNameRequest):
    if not request.niche.strip():
        raise HTTPException(status_code=400, detail="Niche cannot be empty")
    try:
        result = generate_brand_names(request.niche, request.tone, request.audience)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Generation failed: {str(e)}")
