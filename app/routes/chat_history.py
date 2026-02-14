from fastapi import APIRouter, Request
from app.database import get_chat_history, clear_chat_history

router = APIRouter()

@router.get("/chat-history")
def get_history(request: Request):
    user_id = request.session.get("user_id", "default")
    return {"history": get_chat_history(user_id)}

@router.delete("/chat-history")
def delete_history(request: Request):
    user_id = request.session.get("user_id", "default")
    clear_chat_history(user_id)
    return {"message": "Chat history cleared"}
