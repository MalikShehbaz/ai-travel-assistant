from uuid import uuid4

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.ai_service import generate_response
from app.services.conversation_service import get_history, save_message

router = APIRouter(
    prefix="/api/v1/chat",
    tags=["Chat"],
)


class ChatRequest(BaseModel):
    message: str
    session_id: str | None = None


@router.post("")
def chat(
    request: ChatRequest,
    db: Session = Depends(get_db),
):
    session_id = request.session_id or str(uuid4())

    save_message(
        db,
        session_id,
        "user",
        request.message,
    )

    response = generate_response(
        db,
        request.message,
    )

    save_message(
        db,
        session_id,
        "assistant",
        response,
    )

    history = get_history(db, session_id)

    return {
        "session_id": session_id,
        "message": response,
        "history": [
            {
                "role": item.role,
                "content": item.content,
            }
            for item in history
        ],
    }