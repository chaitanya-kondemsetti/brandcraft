"""
services/security_service.py
Security Audit Service — scans code for vulnerabilities using LLM:
SQL injection, XSS, hardcoded secrets, insecure deps, OWASP Top 10.
"""
from .llm_service import llm
from ..models.schemas import SecurityResponse


SYSTEM_SECURITY = """You are CodeRefine AI Security Auditor — an expert in application security.
Scan code for vulnerabilities following OWASP Top 10 and SANS/CWE standards.
Be specific, cite line numbers, and provide secure alternatives.
Return ONLY valid JSON."""


def _build_security_prompt(code: str, language: str) -> str:
    return f"""Perform a security audit of this {language} code.
Return JSON with EXACTLY this structure:

{{
  "language": "<language>",
  "risk_level": "<CRITICAL|HIGH|MEDIUM|LOW|SAFE>",
  "vulnerabilities": [
    {{
      "id":          "<CVE or CWE id if applicable, else 'N/A'>",
      "severity":    "<CRITICAL|HIGH|MEDIUM|LOW>",
      "type":        "<e.g. SQL Injection, Hardcoded Secret, XSS, Insecure Deserialization>",
      "line":        <line number>,
      "code":        "<the vulnerable line(s)>",
      "description": "<why this is a vulnerability and how it can be exploited>",
      "fix":         "<secure replacement code>"
    }}
  ],
  "secure_version": "<complete rewritten secure version of the code>",
  "recommendations": [
    "<actionable security recommendation 1>",
    "<actionable security recommendation 2>"
  ]
}}

Check for:
- Hardcoded credentials, API keys, secrets
- SQL/NoSQL injection vulnerabilities  
- Cross-Site Scripting (XSS)
- Insecure HTTP usage (should be HTTPS)
- Missing input validation/sanitisation
- Unsafe file operations
- Missing authentication/authorisation checks
- Insecure random number generation
- Vulnerable dependencies/imports
- Path traversal vulnerabilities
- Command injection

{language} code to audit:
```
{code}
```"""


class SecurityService:

    async def audit(self, code: str, language: str) -> SecurityResponse:
        """Run a full security audit via LLM."""

        messages = [
            {"role": "system", "content": SYSTEM_SECURITY},
            {"role": "user",   "content": _build_security_prompt(code, language)},
        ]

        data = await llm.call_json(messages, temperature=0.05, max_tokens=4096)

        return SecurityResponse(
            language        = data.get("language",        language),
            risk_level      = data.get("risk_level",      "MEDIUM"),
            vulnerabilities = data.get("vulnerabilities", []),
            secure_version  = data.get("secure_version",  code),
            recommendations = data.get("recommendations", []),
            model_used      = llm.model,
        )


security_service = SecurityService()
