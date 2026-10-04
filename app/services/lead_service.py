from sqlalchemy.orm import Session

from app.models.lead import Lead


def create_lead(
    db: Session,
    name: str,
    phone: str,
    message: str | None = None,
) -> Lead:

    lead = Lead(
        name=name,
        phone=phone,
        message=message,
    )

    db.add(lead)
    db.commit()
    db.refresh(lead)

    return lead