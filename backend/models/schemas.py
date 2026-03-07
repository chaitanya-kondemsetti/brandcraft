"""
models/schemas.py — All Pydantic request/response models for CodeRefine API
"""
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List


# ─────────────────────────────────────────────────────────────
# SHARED BASE — suppresses "model_" namespace warning for
# all response models that have a `model_used` field.
# ─────────────────────────────────────────────────────────────
class AIResponse(BaseModel):
    """Base class for all AI response models — clears the protected 'model_' namespace."""
    model_config = ConfigDict(protected_namespaces=())


# ─────────────────────────────────────────────────────────────
# REQUEST MODELS
# ─────────────────────────────────────────────────────────────

class AnalyzeRequest(BaseModel):
    code: str = Field(..., min_length=1, description="Source code to analyse")
    language: Optional[str] = Field("auto", description="Programming language or 'auto' for detection")

    model_config = ConfigDict(
        protected_namespaces=(),
        json_schema_extra={
            "example": {
                "code": "def bubble_sort(arr):\n    n = len(arr)\n    for i in range(n):\n        for j in range(0, n-i-1):\n            if arr[j] < arr[j+1]:\n                arr[j], arr[j+1] = arr[j+1], arr[j]\n    return",
                "language": "auto"
            }
        }
    )


class OptimizeRequest(BaseModel):
    code: str = Field(..., min_length=1, description="Source code to optimize")
    language: str = Field("auto", description="Programming language")
    issues: Optional[List[dict]] = Field(default=[], description="Pre-detected issues to fix")


class ExplainRequest(BaseModel):
    code: str = Field(..., min_length=1, description="Source code to explain")
    language: str = Field("auto", description="Programming language")


class SecurityRequest(BaseModel):
    code: str = Field(..., min_length=1, description="Source code for security audit")
    language: str = Field("auto", description="Programming language")


class ChatRequest(BaseModel):
    code: str = Field(..., description="Code context for the chat")
    language: str = Field("auto", description="Programming language")
    message: str = Field(..., min_length=1, description="User message/question")
    history: Optional[List[dict]] = Field(default=[], description="Previous conversation turns")


# ─────────────────────────────────────────────────────────────
# SHARED SUB-MODELS
# ─────────────────────────────────────────────────────────────

class Issue(BaseModel):
    line: int
    severity: str          # "BUG" | "WARN" | "INFO"
    title: str
    description: str
    code_snippet: str
    suggested_fix: str


class ComplexityInfo(BaseModel):
    time_before: str
    time_after: str
    space: str
    performance_gain: str
    explanation: str


# ─────────────────────────────────────────────────────────────
# RESPONSE MODELS  (all extend AIResponse to silence warning)
# ─────────────────────────────────────────────────────────────

class AnalyzeResponse(AIResponse):
    language: str
    confidence: float
    bugs: List[Issue]
    warnings: List[Issue]
    suggestions: List[Issue]
    complexity: ComplexityInfo
    quality_score_before: int
    quality_score_after: int
    summary: str
    model_used: str


class OptimizeResponse(AIResponse):
    original_code: str
    optimized_code: str
    language: str
    changes: List[dict]
    explanation: str
    model_used: str


class ExplainResponse(AIResponse):
    language: str
    overview: str
    functions: List[dict]
    algorithms_used: List[str]
    complexity_summary: str
    data_flow: str
    potential_issues: str
    model_used: str


class SecurityResponse(AIResponse):
    language: str
    risk_level: str          # "CRITICAL" | "HIGH" | "MEDIUM" | "LOW" | "SAFE"
    vulnerabilities: List[dict]
    secure_version: str
    recommendations: List[str]
    model_used: str


class ChatResponse(AIResponse):
    reply: str
    model_used: str


class HealthResponse(BaseModel):
    status: str
    version: str
    model: str
    openrouter_connected: bool
