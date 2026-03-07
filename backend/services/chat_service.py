"""
services/chat_service.py
Chat Service — conversational AI about the user's code.
Maintains conversation history for multi-turn dialogue.
"""
from .llm_service import llm
from ..models.schemas import ChatResponse


SYSTEM_CHAT = """You are CodeRefine AI — a helpful, expert coding assistant.
The user will ask questions about their code. Answer clearly and concisely.
Reference specific line numbers when relevant.
Use code examples in your answers when helpful.
Be friendly, precise, and educational."""


class ChatService:

    async def chat(
        self,
        code:     str,
        language: str,
        message:  str,
        history:  list[dict] = None,  # FIX: was `history=[]` — mutable default argument
    ) -> ChatResponse:
        """
        Multi-turn conversational chat about a code snippet.
        history: list of {"role": "user"|"assistant", "content": "..."}
        """

        # FIX: initialise here to avoid shared mutable state across calls
        if history is None:
            history = []

        system_msg = {
            "role": "system",
            "content": (
                f"{SYSTEM_CHAT}\n\n"
                f"The user's current {language} code:\n"
                f"```{language.lower()}\n{code}\n```\n"
                "Refer to this code when answering questions."
            ),
        }

        messages = [system_msg] + list(history) + [
            {"role": "user", "content": message}
        ]

        reply = await llm.call_text(messages, temperature=0.4, max_tokens=1500)

        return ChatResponse(
            reply      = reply,
            model_used = llm.model,
        )


chat_service = ChatService()
