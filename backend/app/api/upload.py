import os
import shutil

from fastapi import APIRouter, UploadFile, File, HTTPException

from app.services.pdf_reader import extract_document
from app.services.extractor import extract_basic_information
from app.services.document_splitter import split_sections
from app.services.groq_service import analyze_chunk
from app.services.json_merger import merge_json
from app.services.normalizer import normalize
from app.services.validator import validate
from app.services.database_writer import write_database

router = APIRouter(
    prefix="/upload",
    tags=["Upload"]
)

UPLOAD_FOLDER = "app/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

MAX_CHARS = 12000


@router.post("/")
async def upload_file(file: UploadFile = File(...)):

    # ---------------------------------
    # Save Uploaded PDF
    # ---------------------------------
    filepath = os.path.join(
        UPLOAD_FOLDER,
        file.filename
    )

    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # ---------------------------------
    # Read PDF
    # ---------------------------------
    text = extract_document(filepath)

    if not text.strip():
        raise HTTPException(
            status_code=400,
            detail="No text found in document."
        )

    print("✅ PDF Loaded")

    # ---------------------------------
    # Regex Extraction
    # ---------------------------------
    print("🔍 Extracting basic information...")

    basic_data = extract_basic_information(text)

    # ---------------------------------
    # Extract Important Sections
    # ---------------------------------
    print("📄 Extracting important sections...")

    important_text = split_sections(text)

    if not important_text.strip():
        important_text = text

    # Limit AI input
    important_text = important_text[:MAX_CHARS]

    print(f"📦 Sending {len(important_text)} characters to AI")

    # ---------------------------------
    # AI Extraction
    # ---------------------------------
    print("🤖 Running AI extraction...")

    ai_result = analyze_chunk(important_text)

    # ---------------------------------
    # Merge
    # ---------------------------------
    merged = merge_json([
        basic_data,
        ai_result
    ])

    # ---------------------------------
    # Normalize
    # ---------------------------------
    normalized = normalize(merged)

    # ---------------------------------
    # Validate
    # ---------------------------------
    validated = validate(normalized)

    # ---------------------------------
    # Save to Database
    # ---------------------------------
    write_database(validated)

    return {
        "status": "success",
        "result": validated
    }