from sqlalchemy.orm import Session

from app.ai.chunking import chunk_text
from app.ai.embeddings import generate_embedding
from app.models.document_chunk import DocumentChunk


def ingest_document(db: Session, file_path: str) -> int:
    with open(file_path, "r", encoding="utf-8") as file:
        text = file.read()

    chunks = chunk_text(text)

    for chunk in chunks:
        embedding = generate_embedding(chunk)

        document_chunk = DocumentChunk(
            content=chunk,
            embedding=embedding,
        )

        db.add(document_chunk)

    db.commit()

    return len(chunks)