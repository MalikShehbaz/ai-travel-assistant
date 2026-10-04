from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.api.routes.chat import router as chat_router


app = FastAPI(
    title="AI Travel Operations Assistant",
    version="0.1.0",
)


@app.get("/")
def health_check():
    return {"status": "ok"}


app.include_router(chat_router)

app.mount(
    "/chat",
    StaticFiles(directory="frontend", html=True),
    name="frontend",
)