from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from services.gemini_service import branding_assistant_chat

router = APIRouter()


class Message(BaseModel):
    role: str  # "user" or "assistant"
    content: str


class AssistantRequest(BaseModel):
    messages: List[Message] = []
    message: str


@router.post("/assistant")
async def chat_with_assistant(request: AssistantRequest):
    if not request.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty")
    try:
        history = [{"role": m.role, "content": m.content} for m in request.messages]
        response = branding_assistant_chat(history, request.message)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Assistant error: {str(e)}")
