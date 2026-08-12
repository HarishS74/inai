from fastapi import APIRouter
from pydantic import BaseModel

from app.services.groq_service import analyze_chunk

router = APIRouter(
    prefix="/ai",
    tags=["AI"]
)


class AIRequest(BaseModel):
    text: str


@router.post("/")
async def analyze_document(request: AIRequest):

    result = analyze_chunk(request.text)

    return {
        "status": "success",
        "result": result
    }