from typing import Dict

REQUIRED_SECTIONS = [
    "company",
    "policy"
]


def validate(data: Dict) -> Dict:
    """
    Validate normalized insurance data.
    Raises an exception if mandatory sections are missing.
    """

    if not isinstance(data, dict):
        raise ValueError("Normalized data must be a dictionary.")

    for section in REQUIRED_SECTIONS:
        if section not in data:
            raise ValueError(f"Missing required section: {section}")

    company = data["company"]
    policy = data["policy"]

    if not company.get("name"):
        raise ValueError("Company name is missing.")

    if not policy.get("productName"):
        raise ValueError("Policy product name is missing.")

    return data