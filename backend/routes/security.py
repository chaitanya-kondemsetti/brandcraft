"""
routes/security.py — POST /api/security
Security audit: OWASP Top 10, hardcoded secrets, injection,
XSS, insecure HTTP, missing validation — with secure rewrites.
"""
from fastapi import APIRouter, HTTPException
from ..models.schemas import SecurityRequest, SecurityResponse
from ..services import security_service

router = APIRouter(prefix="/api", tags=["Security"])


@router.post(
    "/security",
    response_model=SecurityResponse,
    summary="Security audit — OWASP Top 10 scan",
    description=(
        "Submit code for a full security audit. "
        "Checks for SQL injection, XSS, hardcoded credentials, "
        "insecure HTTP, missing input validation, path traversal, "
        "command injection, and more. Returns a risk level, "
        "vulnerability list, and a secure rewritten version."
    ),
)
async def security_audit(req: SecurityRequest) -> SecurityResponse:
    try:
        return await security_service.audit(req.code, req.language or "auto")
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Security audit failed: {str(e)}")
