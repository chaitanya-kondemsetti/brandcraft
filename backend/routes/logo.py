from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.diffusion_service import generate_logo

router = APIRouter()


class LogoRequest(BaseModel):
    brand_name: str
    style: str = "modern"
    primary_color: str = "blue"
    industry: str = "technology"


@router.post("/logo")
async def create_logo(request: LogoRequest):
    if not request.brand_name.strip():
        raise HTTPException(status_code=400, detail="Brand name cannot be empty")
    try:
        result = generate_logo(
            request.brand_name,
            request.style,
            request.primary_color,
            request.industry
        )
        # Always return result — let frontend show the error message
        return result
    except Exception as e:
        return {"success": False, "error": str(e)}