from fastapi import APIRouter, UploadFile, File
import os
import shutil

from app.services.document_processor import extract_document
from app.services.groq_service import analyze
from app.services.normalizer import normalize
from app.services.validator import validate
from app.services.database_writer import write_database

router = APIRouter(prefix="/upload", tags=["Upload"])

UPLOAD_FOLDER = "app/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@router.post("/")
async def upload_file(file: UploadFile = File(...)):

    # Save uploaded file
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)

    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Extract text
    text = extract_document(filepath)

    # AI Extraction
    ai_result = analyze(text)

    # Normalize
    normalized = normalize(ai_result)

    # Validate
    validated = validate(normalized)

    # Save to database
    write_database(validated)

    return {
        "status": "success",
        "filename": file.filename,
        "result": validated
    }