import re


def find(pattern, text):
    match = re.search(pattern, text, re.IGNORECASE)
    if match:
        return match.group(1).strip()
    return None


def extract_basic_information(text: str):

    data = {
        "company": {},
        "policy": {},
        "contact": {}
    }

    # -----------------------------
    # Company
    # -----------------------------
    company = find(
        r"(TATA AIG General Insurance Company Limited|Star Health Insurance|HDFC ERGO General Insurance Company Limited|ICICI Lombard General Insurance Company Limited)",
        text,
    )

    if company:
        data["company"]["insuranceCompany"] = company

    # -----------------------------
    # Policy Name
    # -----------------------------
    policy = find(
        r"(Medicare Premier|Medicare|MediCare Reserve|MediCare Platinum|Arogya Supreme|Optima Secure|Health Suraksha)",
        text,
    )

    if policy:
        data["policy"]["policyName"] = policy

    # -----------------------------
    # UIN
    # -----------------------------
    uin = find(
        r"UIN\s*[:\-]?\s*([A-Z0-9]+)",
        text,
    )

    if uin:
        data["policy"]["UIN"] = uin

    # -----------------------------
    # IRDAI Number
    # -----------------------------
    irdai = find(
        r"IRDAI\s*(?:Reg\.?|Registration)?\s*(?:No\.?|Number)?\s*[:\-]?\s*([A-Za-z0-9\/\-]+)",
        text,
    )

    if irdai:
        data["company"]["IRDAIRegNo"] = irdai

    # -----------------------------
    # CIN
    # -----------------------------
    cin = find(
        r"CIN\s*[:\-]?\s*([A-Z0-9]+)",
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