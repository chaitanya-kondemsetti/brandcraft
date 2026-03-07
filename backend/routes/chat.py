"""
routes/chat.py — POST /api/chat
Conversational AI about the user's code.
Supports multi-turn dialogue via history.
"""
from fastapi import APIRouter, HTTPException
from ..models.schemas import ChatRequest, ChatResponse
from ..services import chat_service

router = APIRouter(prefix="/api", tags=["Chat"])


@router.post(
    "/chat",
    response_model=ChatResponse,
    summary="Chat with AI about your code",
    description=(
        "Ask questions about your code in natural language. "
        "The AI has full context of your code and can answer "
        "questions about how it works, suggest improvements, "
        "explain errors, or walk you through the logic. "
        "Pass conversation history for multi-turn dialogue."
    ),
)
async def chat(req: ChatRequest) -> ChatResponse:
    try:
        return await chat_service.chat(
            req.code,
            req.language or "auto",
            req.message,
            req.history or [],
        )
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chat failed: {str(e)}")
