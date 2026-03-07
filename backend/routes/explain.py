"""
routes/explain.py — POST /api/explain
Plain English explanation of code: what it does, how it works,
algorithm breakdown, data flow, and complexity.
"""
from fastapi import APIRouter, HTTPException
from ..models.schemas import ExplainRequest, ExplainResponse
from ..services import explain_service

router = APIRouter(prefix="/api", tags=["Explanation"])


@router.post(
    "/explain",
    response_model=ExplainResponse,
    summary="Explain code in plain English",
    description=(
        "Submit code and receive a clear explanation: "
        "what it does, function-by-function breakdown, "
        "algorithms used, data flow, and complexity analysis."
    ),
)
async def explain_code(req: ExplainRequest) -> ExplainResponse:
    try:
        return await explain_service.explain(req.code, req.language or "auto")
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Explanation failed: {str(e)}")
