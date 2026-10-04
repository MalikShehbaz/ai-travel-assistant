from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.conversation import ConversationMessage


def save_message(
    db: Session,
    session_id: str,
    role: str,
    content: str,
) -> ConversationMessage:

    message = ConversationMessage(
        session_id=session_id,
        role=role,
        content=content,
    )

    db.add(message)
    db.commit()
    db.refresh(message)

    return message


def get_history(
    db: Session,
    session_id: str,
) -> list[ConversationMessage]:

    statement = (
        select(ConversationMessage)
        .where(ConversationMessage.session_id == session_id)
        .order_by(ConversationMessage.created_at)
    )

    return list(db.execute(statement).scalars().all())