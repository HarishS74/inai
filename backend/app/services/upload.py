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

# BUG FIX: the old MAX_CHARS = 12000 hard truncation meant only the
# first few pages of any real policy wording (usually 20-40 pages)
# ever reached the AI - everything after that, including most
# exclusions, waiting periods, and claims procedure, was silently cut
# off before analysis even started.
#
# Instead of truncating, we now split the FULL document into
# overlapping chunks and run AI extraction on each chunk separately,
# then merge all the partial results together. This means every page
# of the document gets analyzed, regardless of how long it is.
CHUNK_SIZE = 8000       # characters per chunk sent to the AI
CHUNK_OVERLAP = 500     # overlap so a fact split across a chunk boundary isn't lost


def chunk_text(text: str, chunk_size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP):
    chunks = []
    start = 0
    text_len = len(text)

    while start < text_len:
        end = min(start + chunk_size, text_len)
        chunks.append(text[start:end])
        if end == text_len:
            break
        start = end - overlap

    return chunks


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

    print(f"✅ PDF Loaded ({len(text)} characters)")

    # ---------------------------------
    # Regex Extraction (runs on full text, it's cheap and local)
    # ---------------------------------
    print("🔍 Extracting basic information...")

    basic_data = extract_basic_information(text)

    # ---------------------------------
    # Extract Important Sections
    # ---------------------------------
    # split_sections is now a passthrough (see document_splitter.py) -
    # kept in the pipeline shape in case section-aware chunking is
    # added later, but no longer discards content.
    important_text = split_sections(text)

    if not important_text.strip():
        important_text = text

    # ---------------------------------
    # AI Extraction — chunked, so the FULL document gets analyzed
    # ---------------------------------
    chunks = chunk_text(important_text)
    print(f"📦 Document split into {len(chunks)} chunk(s) for AI extraction")

    ai_results = []
    for i, chunk in enumerate(chunks, start=1):
        print(f"🤖 Running AI extraction on chunk {i}/{len(chunks)} ({len(chunk)} chars)")
        try:
            chunk_result = analyze_chunk(chunk)
            ai_results.append(chunk_result)
        except Exception as e:
            # Don't let one bad chunk kill the whole upload - log it
            # and keep going with whatever chunks did succeed.
            print(f"⚠️ Chunk {i} failed extraction: {e}")

    if not ai_results:
        raise HTTPException(
            status_code=502,
            detail="AI extraction failed on every chunk of this document."
        )

    # ---------------------------------
    # Merge all chunk results + regex results into one JSON
    # ---------------------------------
    merged = merge_json([basic_data] + ai_results)

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
        "chunks_processed": len(chunks),
        "chunks_succeeded": len(ai_results),
        "result": validated
    }
