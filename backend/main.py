import os
from typing import Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

try:
    # Optional: load .env if present
    from dotenv import load_dotenv

    load_dotenv()
except Exception:
    # If python-dotenv is not installed, proceed without it
    pass

try:
    from openai import OpenAI
except Exception as exc:  # pragma: no cover - guard for missing dependency
    OpenAI = None  # type: ignore


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    response: str


app = FastAPI(title="Chat API", version="1.0.0")

# CORS configuration - production ready
allowed_origins = os.getenv("ALLOWED_ORIGINS", "*").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


def get_openai_client() -> OpenAI:
    api_key = os.getenv("OPENAI_API_KEY")
    if OpenAI is None:
        raise HTTPException(status_code=500, detail="OpenAI SDK not installed. Add 'openai' to requirements and install.")
    if not api_key:
        raise HTTPException(status_code=500, detail="OPENAI_API_KEY is not set.")
    return OpenAI(api_key=api_key)


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.get("/")
def root():
    return {"message": "Chat API is running", "docs": "/docs"}

@app.post("/chat", response_model=ChatResponse)
def chat(payload: ChatRequest) -> ChatResponse:
    message = payload.message.strip()
    if not message:
        raise HTTPException(status_code=400, detail="Message must not be empty.")

    client = get_openai_client()
    try:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": message},
            ],
            temperature=0.7,
        )
        content: Optional[str] = completion.choices[0].message.content if completion and completion.choices else None
        if not content:
            raise HTTPException(status_code=502, detail="Empty response from model.")
        return ChatResponse(response=content)
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"Upstream error: {exc}")


