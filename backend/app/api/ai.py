from fastapi import APIRouter
from app.services.pdf_reader import read_pdf
from app.services.groq_service import analyze

router = APIRouter(prefix="/ai", tags=["AI"])


@router.get("/pdf")
def analyze_pdf():

    text = read_pdf("app/uploads/sample.pdf")

    result = analyze(text)

    return {
        "result": result
    }