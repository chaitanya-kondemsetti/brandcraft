"""
routes/health.py — GET /api/health
Health check endpoint — verifies server is up and OpenRouter is reachable.
"""
from fastapi import APIRouter
from ..models.schemas import HealthResponse
from ..services import llm
from ..config import get_settings

router  = APIRouter(prefix="/api", tags=["Health"])
settings = get_settings()


@router.get(
    "/health",
    response_model=HealthResponse,
    summary="Health check",
    description="Returns server status and OpenRouter connection state.",
)
async def health() -> HealthResponse:
    connected = await llm.check_connection()
    return HealthResponse(
        status               = "ok",
        version              = settings.app_version,
        model                = settings.openrouter_model,
        openrouter_connected = connected,
    )
