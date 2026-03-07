"""
routes/optimize.py — POST /api/optimize
AI-powered code rewriter: fixes all bugs, adds type hints,
docstrings, null guards, and uses the best algorithm.
"""
from fastapi import APIRouter, HTTPException
from ..models.schemas import OptimizeRequest, OptimizeResponse
from ..services import optimizer_service

router = APIRouter(prefix="/api", tags=["Optimization"])


@router.post(
    "/optimize",
    response_model=OptimizeResponse,
    summary="Rewrite code to be production-ready",
    description=(
        "Submit code and optionally pre-detected issues. "
        "The LLM will rewrite the code fixing all bugs, "
        "adding annotations, improving algorithms, and following "
        "the language's official style guide."
    ),
)
async def optimize_code(req: OptimizeRequest) -> OptimizeResponse:
    try:
        return await optimizer_service.optimize(
            req.code,
            req.language or "auto",
            req.issues or [],
        )
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Optimization failed: {str(e)}")
