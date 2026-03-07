"""
main.py — CodeRefine FastAPI Application Entry Point

CodeRefine: Generative AI-Powered Code Review & Optimization Engine
Technologies: FastAPI, OpenRouter (Qwen Coder / Llama / Gemma), Uvicorn

Routes:
  POST /api/analyze   — Bug detection, complexity, quality scoring
  POST /api/optimize  — AI code rewriter
  POST /api/explain   — Plain English explanation
  POST /api/security  — OWASP security audit
  POST /api/chat      — Conversational AI about code
  GET  /api/health    — Server + OpenRouter health check
  GET  /              — Serves the frontend HTML dashboard
"""

import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
# FIX: removed unused `StaticFiles` import

from backend.config import get_settings
from backend.routes import (
    analyze_router,
    optimize_router,
    explain_router,
    security_router,
    chat_router,
    health_router,
)

settings = get_settings()


# ─────────────────────────────────────────────────────────────
# LIFESPAN (startup / shutdown events)
# ─────────────────────────────────────────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    print(f"\n{'='*55}")
    print(f"  CodeRefine AI  v{settings.app_version}")
    print(f"  Model  : {settings.openrouter_model}")
    print(f"  Docs   : http://{settings.app_host}:{settings.app_port}/docs")
    print(f"  App    : http://{settings.app_host}:{settings.app_port}/")
    print(f"{'='*55}\n")
    yield
    print("\nCodeRefine shutting down.")


# ─────────────────────────────────────────────────────────────
# APP INSTANCE
# ─────────────────────────────────────────────────────────────
app = FastAPI(
    title       = settings.app_title,
    description = (
        "Generative AI-Powered Code Review & Optimization Engine. "
        "Paste any code — Python, JavaScript, TypeScript, Java, C++, Go, Rust — "
        "and receive instant bug reports, Big-O complexity analysis, "
        "a production-optimized rewrite, security audit, and AI chat."
    ),
    version     = settings.app_version,
    lifespan    = lifespan,
    docs_url    = "/docs",
    redoc_url   = "/redoc",
)


# ─────────────────────────────────────────────────────────────
# CORS
# FIX: allow_credentials=True is incompatible with allow_origins=["*"].
# Browsers reject this combination. Use explicit origins for production,
# or keep wildcard origins without credentials for open/dev APIs.
# ─────────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins     = ["*"],
    allow_credentials = False,   # FIX: was True — invalid with allow_origins=["*"]
    allow_methods     = ["*"],
    allow_headers     = ["*"],
)


# ─────────────────────────────────────────────────────────────
# API ROUTES
# ─────────────────────────────────────────────────────────────
app.include_router(health_router)
app.include_router(analyze_router)
app.include_router(optimize_router)
app.include_router(explain_router)
app.include_router(security_router)
app.include_router(chat_router)


# ─────────────────────────────────────────────────────────────
# SERVE FRONTEND (index.html)
# ─────────────────────────────────────────────────────────────
FRONTEND_PATH = os.path.join(os.path.dirname(__file__), "frontend", "index.html")

@app.get("/", response_class=HTMLResponse, include_in_schema=False)
async def serve_frontend():
    if os.path.exists(FRONTEND_PATH):
        with open(FRONTEND_PATH, "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    return HTMLResponse(
        content="<h1>Frontend not found.</h1><p>Place index.html in the /frontend directory.</p>",
        status_code=404,
    )


# ─────────────────────────────────────────────────────────────
# GLOBAL ERROR HANDLER
# ─────────────────────────────────────────────────────────────
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"detail": f"Internal server error: {str(exc)}"},
    )


# ─────────────────────────────────────────────────────────────
# ENTRY POINT
# ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host    = settings.app_host,
        port    = settings.app_port,
        reload  = settings.debug,
        workers = 1,
    )
