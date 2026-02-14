from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
from app.services.qa_service import answer_question
from app.database import insert_chat_message

router = APIRouter()

class QuestionRequest(BaseModel):
    question: str

@router.post("/ask")
def ask_question(request: Request, req: QuestionRequest):
    if not req.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")

    user_id = request.session.get("user_id", "default")
    result = answer_question(req.question, user_id)
    
    # Save to chat history with user_id
    insert_chat_message(user_id, req.question, result["answer"], result["sources"])
    
    return result
