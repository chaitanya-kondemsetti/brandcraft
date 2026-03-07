"""
config.py — Application settings loaded from .env
"""
import os
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    openrouter_api_key: str = "your_openrouter_api_key_here"
    openrouter_model: str = "qwen/qwen-2.5-coder-32b-instruct:free"
    openrouter_base_url: str = "https://openrouter.ai/api/v1/chat/completions"

    app_host: str = "0.0.0.0"
    # Render injects PORT at runtime; fall back to 8000 for local dev
    app_port: int = int(os.environ.get("PORT", 8000))
    app_title: str = "CodeRefine AI"
    app_version: str = "1.0.0"
    debug: bool = False

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
