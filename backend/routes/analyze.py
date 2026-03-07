"""
routes/analyze.py — POST /api/analyze
Full code analysis: language detection, bugs, warnings,
suggestions, complexity, and quality scoring.
"""
from fastapi import APIRouter, HTTPException
from ..models.schemas import AnalyzeRequest, AnalyzeResponse
from ..services import analysis_service

router = APIRouter(prefix="/api", tags=["Analysis"])


@router.post(
    "/analyze",
    response_model=AnalyzeResponse,
    summary="Analyse code for bugs, warnings, and complexity",
    description=(
        "Submit source code for deep AI analysis. "
        "Returns detected bugs, warnings, style suggestions, "
        "Big-O complexity, and a quality score — all powered by an LLM."
    ),
)
async def analyze_code(req: AnalyzeRequest) -> AnalyzeResponse:
    try:
        return await analysis_service.analyze(req.code, req.language or "auto")
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")
