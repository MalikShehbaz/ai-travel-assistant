from sqlalchemy import select
from sqlalchemy.orm import Session

from app.ai.embeddings import generate_embedding
from app.models.document_chunk import DocumentChunk


def search_knowledge(
    db: Session,
    question: str,
    limit: int = 5,
) -> list[str]:

    question_embedding = generate_embedding(
        question,
        task_type="RETRIEVAL_QUERY",
    )

    statement = (
        select(DocumentChunk)
        .order_by(
            DocumentChunk.embedding.cosine_distance(question_embedding)
        )
        .limit(limit)
    )

    results = db.execute(statement).scalars().all()

    return [result.content for result in results]