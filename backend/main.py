from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

from routes.brand_name import router as brand_name_router
from routes.logo import router as logo_router
from routes.content import router as content_router
from routes.sentiment import router as sentiment_router
from routes.assistant import router as assistant_router

app = FastAPI(title="BrandCraft API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API Routes
app.include_router(brand_name_router, prefix="/api")
app.include_router(logo_router, prefix="/api")
app.include_router(content_router, prefix="/api")
app.include_router(sentiment_router, prefix="/api")
app.include_router(assistant_router, prefix="/api")

# Serve frontend
frontend_path = os.path.join(os.path.dirname(__file__), "..", "frontend")
app.mount("/static", StaticFiles(directory=frontend_path), name="static")

@app.get("/")
def serve_frontend():
    return FileResponse(os.path.join(frontend_path, "index.html"))

@app.get("/health")
def health():
    return {"status": "ok", "message": "BrandCraft API is running"}
