"""
Previous version of this file only kept 60 lines after each matched
section header, capped at 400 total lines. For a 37-page policy
wording, that threw away almost everything after the first couple of
sections (e.g. the full exclusions list, all specific waiting
periods, the claims document checklist never made it through).

This version no longer tries to guess which lines matter. Instead it
returns the FULL text unchanged. Length is now handled by chunking
in upload.py (chunk_text), which sends the whole document to the AI
in overlapping pieces rather than truncating it - so nothing gets
silently dropped before the model ever sees it.

Kept as its own function/file so the pipeline shape (extract -> split
-> analyze) doesn't have to change elsewhere, and so this is a single
place to add smarter section-aware chunking later if needed.
"""


def split_sections(text: str) -> str:
    return text
