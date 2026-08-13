import re


def find(pattern, text):
    match = re.search(pattern, text, re.IGNORECASE)
    if match:
        return match.group(1).strip()
    return None


def extract_basic_information(text: str):
    """
    Regex fallback extraction. This runs alongside the AI extraction
    (see groq_service.py) and json_merger.py fills gaps with whichever
    source found a value first. This is NOT the primary extraction
    path - the AI schema in groq_service.py is - this just catches a
    few high-confidence fields via pattern matching as a backup.
    """

    data = {
        "company": {},
        "policy": {},
        "contact": {}
    }

    # -----------------------------
    # Company
    # -----------------------------
    # Previous version only matched a hardcoded whitelist of 4 insurer
    # names (didn't even include Max Bupa, the company in this test
    # document). Widened to match "<Words> Insurance Company Limited"
    # or "<Words> Health Insurance Company Limited" generically, which
    # covers most Indian insurer legal names without needing to keep
    # a whitelist in sync every time you ingest a new insurer.
    company = find(
        r"([A-Z][A-Za-z& ]{2,40}(?:Health )?Insurance Company Limited)",
        text,
    )

    if company:
        data["company"]["insuranceCompany"] = company

    # -----------------------------
    # Policy Name
    # -----------------------------
    # Previous version only matched a hardcoded whitelist of product
    # names. Left as a fallback (AI extraction is the primary source
    # for policy name), but no longer restricted to old known names.
    policy = find(
        r"(?:^|\n)([A-Z][A-Za-z ]{5,60}(?:Health Insurance Product|Insurance Policy|Health Plan))",
        text,
    )

    if policy:
        data["policy"]["policyName"] = policy

    # -----------------------------
    # UIN
    # -----------------------------
    uin = find(
        r"UIN\s*[:\-]?\s*([A-Z0-9\/\.\-]+)",
        text,
    )

    if uin:
        data["policy"]["UIN"] = uin

    # -----------------------------
    # IRDAI Number
    # -----------------------------
    irdai = find(
        r"IRDAI?\s*(?:Reg\.?|Registration)?\s*(?:No\.?|Number)?\s*[:\-]?\s*(\d{2,4})",
        text,
    )

    if irdai:
        data["company"]["IRDAIRegNo"] = irdai

    # -----------------------------
    # CIN
    # -----------------------------
    # BUG FIX: previous regex was `CIN\s*[:\-]?\s*([A-Z0-9]+)`, which
    # grabs ANY run of uppercase letters/digits right after the
    # literal text "CIN" - including partial matches from unrelated
    # nearby text, which is how a real run produced "CIN": "es".
    #
    # An Indian CIN has a fixed, well-defined format: 1 letter + 5
    # digits + 2 letters + 4 digits + 3 letters + 6 digits = 21
    # characters total, e.g. U66030TN2001PLC047977. Matching that
    # exact shape means we only ever capture something that is
    # actually shaped like a real CIN, or nothing at all.
    cin = find(
        r"CIN\s*[:\-]?\s*([A-Z]\d{5}[A-Z]{2}\d{4}[A-Z]{3}\d{6})",
        text,
    )

    if cin:
        data["company"]["CIN"] = cin

    # -----------------------------
    # Phone
    # -----------------------------
    phone = find(
        r"((?:\+91[- ]?)?(?:1800[- ]?\d{3}[- ]?\d{4}|\d{10}))",
        text,
    )

    if phone:
        data["contact"]["phone"] = phone

    # -----------------------------
    # Email
    # -----------------------------
    email = find(
        r"([A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,})",
        text,
    )

    if email:
        data["contact"]["email"] = email

    # -----------------------------
    # Website
    # -----------------------------
    website = find(
        r"(https?://[^\s]+|www\.[^\s]+)",
        text,
    )

    if website:
        data["contact"]["website"] = website

    # -----------------------------
    # Address
    # -----------------------------
    address = find(
        r"Registered Office[:\s]*(.*?)(?:Phone|Email|Website|IRDAI|$)",
        text,
    )

    if address:
        data["company"]["registeredOffice"] = address.replace("\n", " ")

    return data
