"""
services/optimizer_service.py
Code Optimization Service — rewrites code using OpenRouter LLM,
fixing all bugs and applying best practices.
"""
from .llm_service import llm
from ..models.schemas import OptimizeResponse


SYSTEM_OPTIMIZE = """You are CodeRefine AI — an expert code optimizer.
Rewrite the provided code to be production-ready: fix all bugs,
apply best practices, add type hints/annotations, add docstrings,
improve performance, and make it idiomatic for the language.

Return ONLY valid JSON — no markdown fences, no explanation outside JSON."""


def _build_optimize_prompt(code: str, language: str, issues: list) -> str:
    issues_str = ""
    if issues:
        issues_str = "\n\nKnown issues to fix:\n" + "\n".join(
            f"- Line {i.get('line',0)}: {i.get('title','issue')} — {i.get('description','')}"
            for i in issues
        )

    return f"""Optimize this {language} code and return JSON with EXACTLY this structure:

{{
  "optimized_code": "<complete optimized source code as a string>",
  "explanation": "<2-3 sentence summary of all changes made>",
  "changes": [
    {{
      "type": "fix|opt|add|remove",
      "icon": "🔧|⚡|➕|🗑️",
      "line_before": <original line number or 0>,
      "line_after":  <new line number or 0>,
      "description": "<what changed and why>"
    }}
  ]
}}

Rules for the optimized code:
- Fix ALL bugs (wrong logic, null dereferences, wrong comparators, bare returns)
- Add null/empty guards for all parameters
- Add type annotations / type hints where applicable
- Add docstrings to all functions and classes
- Use the most efficient algorithm available
- Follow the language's official style guide (PEP 8 for Python, ESLint standard for JS, etc.)
- Add inline comments for complex logic
- Keep changes minimal and justified — don't rewrite unnecessarily

Original {language} code:{issues_str}
```
{code}
```"""


class OptimizerService:

    async def optimize(
        self,
        code:     str,
        language: str,
        issues:   list = None,  # FIX: was `issues=[]` — mutable default argument
    ) -> OptimizeResponse:
        """Rewrite code using LLM to fix all issues and apply best practices."""

        # FIX: initialise here to avoid shared mutable state across calls
        if issues is None:
            issues = []

        messages = [
            {"role": "system", "content": SYSTEM_OPTIMIZE},
            {"role": "user",   "content": _build_optimize_prompt(code, language, issues)},
        ]

        data = await llm.call_json(messages, temperature=0.15, max_tokens=6000)

        changes = []
        for c in (data.get("changes") or []):
            changes.append({
                "type":        c.get("type",        "fix"),
                "icon":        c.get("icon",        "🔧"),
                "line_before": c.get("line_before",  0),
                "line_after":  c.get("line_after",   0),
                "description": c.get("description", ""),
            })

        return OptimizeResponse(
            original_code  = code,
            optimized_code = data.get("optimized_code", code),
            language       = language,
            changes        = changes,
            explanation    = data.get("explanation", ""),
            model_used     = llm.model,
        )


optimizer_service = OptimizerService()
