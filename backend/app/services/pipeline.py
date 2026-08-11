from app.services.json_normalizer import normalize
from app.services.save_to_db import insert


def run_pipeline(ai_data):

    data = normalize(ai_data)

    # ---------------- COMPANY ----------------

    company = insert(
        "companies",
        data["company"]
    )

    company_id = company.get("company_id")

    # ---------------- POLICY ----------------

    policy_data = data["policy"]
    policy_data["company_id"] = company_id

    policy = insert(
        "policies",
        policy_data
    )

    policy_id = policy.get("policy_id")

    # ---------------- COVERAGES ----------------

    for coverage in data["coverages"]:

        coverage["policy_id"] = policy_id

        insert(
            "coverages",
            coverage
        )

    # ---------------- WAITING PERIODS ----------------

    for waiting in data["waiting_periods"]:

        waiting["policy_id"] = policy_id

        insert(
            "waiting_periods",
            waiting
        )

    # ---------------- CLAIMS ----------------

    claim = data["claims"]

    claim["policy_id"] = policy_id

    insert(
        "claims",
        claim
    )

    # ---------------- HOSPITAL NETWORK ----------------

    network = data["hospital_network"]

    network["policy_id"] = policy_id

    insert(
        "hospital_network",
        network
    )

    return {
        "company_id": company_id,
        "policy_id": policy_id
    }