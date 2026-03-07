"""
services/analysis_service.py
Code Analysis Service — uses OpenRouter LLM to detect bugs,
warnings, suggestions, compute complexity, and score quality.
"""
from .llm_service import llm
from ..models.schemas import (
    AnalyzeResponse, Issue, ComplexityInfo
)


SYSTEM_ANALYZE = """You are CodeRefine AI — an expert code review engine.
Your job is to deeply analyse source code and return a structured JSON report.

Always return ONLY valid JSON — no markdown, no explanation outside the JSON.
Be thorough, precise, and developer-friendly in your issue descriptions."""


def _build_analyze_prompt(code: str, language: str) -> str:
    return f"""Analyse this {language} code thoroughly and return a JSON object with EXACTLY this structure:

{{
  "language": "<detected language name>",
  "confidence": <0.0-1.0 float>,
  "bugs": [
    {{
      "line": <line number int>,
      "severity": "BUG",
      "title": "<short title>",
      "description": "<detailed explanation of the bug>",
      "code_snippet": "<the problematic line(s)>",
      "suggested_fix": "<corrected code snippet>"
    }}
  ],
  "warnings": [
    {{
      "line": <line number int>,
      "severity": "WARN",
      "title": "<short title>",
      "description": "<why this is a problem>",
      "code_snippet": "<the line>",
      "suggested_fix": "<improved code>"
    }}
  ],
  "suggestions": [
    {{
      "line": <line number int>,
      "severity": "INFO",
      "title": "<improvement title>",
      "description": "<why this improves the code>",
      "code_snippet": "<original>",
      "suggested_fix": "<improved version>"
    }}
  ],
  "complexity": {{
    "time_before": "<Big-O of original code e.g. O(n²)>",
    "time_after":  "<Big-O if optimized e.g. O(n log n)>",
    "space":       "<space complexity e.g. O(1)>",
    "performance_gain": "<e.g. 31x faster>",
    "explanation": "<2-3 sentence explanation of complexity>"
  }},
  "quality_score_before": <integer 0-100>,
  "quality_score_after":  <integer 0-100 after fixing all issues>,
  "summary": "<2-3 sentence executive summary of the code quality>"
}}

Rules:
- bugs: logic errors, crashes, wrong output, security holes
- warnings: bad practices, performance issues, missing guards
- suggestions: style, readability, modern patterns
- Be specific — include line numbers and exact code snippets
- quality_score_before reflects actual code quality
- quality_score_after shows what the score would be after all fixes

Code to analyse (language: {language}):
```
{code}
```"""


class AnalysisService:

    async def analyze(self, code: str, language: str) -> AnalyzeResponse:
        """Full code analysis via LLM — bugs, warnings, complexity, quality."""

        messages = [
            {"role": "system", "content": SYSTEM_ANALYZE},
            {"role": "user",   "content": _build_analyze_prompt(code, language)},
        ]

        data = await llm.call_json(messages, temperature=0.1, max_tokens=4096)

        def parse_issues(raw: list, default_sev: str) -> list[Issue]:
            issues = []
            for item in (raw or []):
                issues.append(Issue(
                    line         = int(item.get("line", 0)),
                    severity     = item.get("severity", default_sev),
                    title        = item.get("title", "Issue"),
                    description  = item.get("description", ""),
                    code_snippet = item.get("code_snippet", ""),
                    suggested_fix= item.get("suggested_fix", ""),
                ))
            return issues

        cx_raw = data.get("complexity", {})
        complexity = ComplexityInfo(
            time_before     = cx_raw.get("time_before",      "O(n²)"),
            time_after      = cx_raw.get("time_after",       "O(n log n)"),
            space           = cx_raw.get("space",            "O(1)"),
            performance_gain= cx_raw.get("performance_gain", "N/A"),
            explanation     = cx_raw.get("explanation",      ""),
        )

        return AnalyzeResponse(
            language             = data.get("language",              language),
            confidence           = float(data.get("confidence",      0.95)),
            bugs                 = parse_issues(data.get("bugs",        []), "BUG"),
            warnings             = parse_issues(data.get("warnings",    []), "WARN"),
            suggestions          = parse_issues(data.get("suggestions", []), "INFO"),
            complexity           = complexity,
            quality_score_before = int(data.get("quality_score_before", 50)),
            quality_score_after  = int(data.get("quality_score_after",  90)),
            summary              = data.get("summary", ""),
            model_used           = llm.model,
        )


analysis_service = AnalysisService()
