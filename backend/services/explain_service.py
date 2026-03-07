"""
services/explain_service.py
Code Explanation Service — translates code into plain English,
explains algorithms, data flow, and complexity.
"""
from .llm_service import llm
from ..models.schemas import ExplainResponse


SYSTEM_EXPLAIN = """You are CodeRefine AI — an expert at explaining code clearly.
Break down code for developers of all levels. Be precise, use examples,
and reference line numbers. Return ONLY valid JSON."""


def _build_explain_prompt(code: str, language: str) -> str:
    return f"""Explain this {language} code and return JSON with EXACTLY this structure:

{{
  "language": "<language>",
  "overview": "<2-4 sentence plain English overview of what this code does>",
  "functions": [
    {{
      "name": "<function/class/method name>",
      "lines": "<e.g. 2-15>",
      "purpose": "<what it does in 1 sentence>",
      "parameters": "<list parameters and their types/roles>",
      "returns": "<what it returns>",
      "complexity": "<Big-O time complexity>",
      "explanation": "<step-by-step explanation of the algorithm/logic>"
    }}
  ],
  "algorithms_used": ["<algorithm name, e.g. Bubble Sort, Binary Search>"],
  "complexity_summary": "<overall time and space complexity with explanation>",
  "data_flow": "<how data enters, transforms, and exits the code>",
  "potential_issues": "<brief mention of any notable issues or limitations>"
}}

Code ({language}):
```
{code}
```"""


class ExplainService:

    async def explain(self, code: str, language: str) -> ExplainResponse:
        """Generate a plain English explanation of the code."""

        messages = [
            {"role": "system", "content": SYSTEM_EXPLAIN},
            {"role": "user",   "content": _build_explain_prompt(code, language)},
        ]

        data = await llm.call_json(messages, temperature=0.2, max_tokens=3000)

        return ExplainResponse(
            language           = data.get("language",           language),
            overview           = data.get("overview",           ""),
            functions          = data.get("functions",          []),
            algorithms_used    = data.get("algorithms_used",   []),
            complexity_summary = data.get("complexity_summary", ""),
            data_flow          = data.get("data_flow",          ""),      # FIX: was silently dropped
            potential_issues   = data.get("potential_issues",   ""),      # FIX: was silently dropped
            model_used         = llm.model,
        )


explain_service = ExplainService()
