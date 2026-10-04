from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from sqlalchemy import inspect

from app.api.routes.chat import router as chat_router
from app.core.database import Base, engine, SessionLocal
from app.models.document_chunk import DocumentChunk
from app.services.ingestion_service import ingest_document


app = FastAPI(
    title="AI Travel Operations Assistant",
    version="0.1.0",
)


def initialize_database():
    """Create database tables and load knowledge if necessary."""

    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    try:
        existing_chunks = db.query(DocumentChunk).count()

        if existing_chunks == 0:
            knowledge_file = (
                Path(__file__).resolve().parent.parent
                / "knowledge"
                / "company_faq.txt"
            )

            ingest_document(
                db,
                str(knowledge_file),
            )

    finally:
        db.close()


initialize_database()


@app.get("/")
def health_check():
    return {"status": "ok"}


app.include_router(chat_router)

app.mount(
    "/chat",
    StaticFiles(directory="frontend", html=True),
    name="frontend",
)