
from google import genai
from google.genai import types
from sqlalchemy.orm import Session

from app.ai.prompts import TRAVEL_ASSISTANT_SYSTEM_PROMPT
from app.ai.tools import CREATE_LEAD_TOOL
from app.core.config import settings
from app.services.lead_service import create_lead
from app.services.search_service import search_knowledge

client = genai.Client(api_key=settings.gemini_api_key)


def generate_response(db: Session, message: str) -> str:

    knowledge = search_knowledge(db, message)
    context = "\n\n".join(knowledge)

    prompt = f"""
{TRAVEL_ASSISTANT_SYSTEM_PROMPT}

Company knowledge:
{context}

Customer message:
{message}

If the customer wants the travel team to contact them,
use the create_lead tool.

Rules:
- Use information from the company knowledge whenever relevant.
- Do not invent information.
- Keep the answer concise and helpful.
- If the knowledge does not contain the answer, say that you do not have enough information and offer human assistance.
"""

    response = client.models.generate_content(
        model=settings.gemini_model,
        contents=prompt,
        config=types.GenerateContentConfig(
            tools=[CREATE_LEAD_TOOL],
        ),
    )

    # Gemini wants to call a tool
    if response.function_calls:

        function_call = response.function_calls[0]

        if function_call.name == "create_lead":

            args = function_call.args

            lead = create_lead(
                db=db,
                name=args["name"],
                phone=args["phone"],
                message=args.get("message"),
            )

            return (
                f"Thanks, {lead.name}. "
                "I've sent your request to our travel team. "
                "They will contact you soon."
            )

    return response.text