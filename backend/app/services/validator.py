from typing import Dict


def validate(data: Dict) -> Dict:
    """
    Validate normalized data.
    During development, auto-fill missing values instead of raising errors.
    """

    if not isinstance(data, dict):
        raise ValueError("Normalized data must be a dictionary.")

    # Ensure sections exist
    data.setdefault("company", {})
    data.setdefault("policy", {})
    data.setdefault("claims", {})
    data.setdefault("network", {})
    data.setdefault("helpline", {})
    data.setdefault("grievance", {})
    data.setdefault("service", {})
    data.setdefault("other", {})

    # Auto-fill required values
    company = data["company"]
    policy = data["policy"]

    if not company.get("name"):
        company["name"] = "Unknown"

    if not policy.get("productName"):
        policy["productName"] = "Unknown"

    return data