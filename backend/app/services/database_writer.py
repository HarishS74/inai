from uuid import uuid4

from app.database import supabase
from app.services.save_to_db import insert


def get_value(data, *keys):
    if not isinstance(data, dict):
        return None

    for key in keys:
        value = data.get(key)
        if value not in [None, "", [], {}]:
            return value

    return None


def write_database(data: dict):

    company = data.get("company", {})
    policy = data.get("policy", {})
    claims = data.get("claims", {})
    network = data.get("network", {})

    # ----------------------------
    # COMPANY
    # ----------------------------

    company_name = (
        get_value(
            company,
            "name",
            "company_name",
            "insuranceCompany",
            "companyName",
        )
        or "Unknown Company"
    )

    existing_company = (
        supabase.table("companies")
        .select("company_id")
        .eq("company_name", company_name)
        .execute()
    )

    if existing_company.data:
        company_id = existing_company.data[0]["company_id"]
        print(f"✅ Company already exists: {company_name}")
    else:
        company_id = str(uuid4())

        insert(
            "companies",
            {
                "company_id": company_id,
                "company_name": company_name,
                "registration_number": get_value(
                    company,
                    "CIN",
                    "registrationNumber",
                ),
                "irdai_license_number": get_value(
                    company,
                    "IRDAIRegNo",
                    "irdaiNumber",
                ),
                "company_address": get_value(
                    company,
                    "registeredOffice",
                    "address",
                ),
            },
        )

        print(f"✅ New company inserted: {company_name}")

    # ----------------------------
    # POLICY
    # ----------------------------

    policy_name = (
        get_value(
            policy,
            "productName",
            "policyName",
            "name",
        )
        or "Unknown Policy"
    )

    existing_policy = (
        supabase.table("policies")
        .select("policy_id")
        .eq("company_id", company_id)
        .eq("policy_name", policy_name)
        .execute()
    )

    if existing_policy.data:
        print("✅ Policy already exists.")
        return

    policy_id = str(uuid4())

    insert(
        "policies",
        {
            "policy_id": policy_id,
            "company_id": company_id,
            "policy_name": policy_name,
            "policy_code": get_value(policy, "UIN", "policyCode"),
            "policy_type": get_value(policy, "policyType"),
            "individual_or_family": get_value(
                policy,
                "sumInsuredBasis",
            ),
        },
    )

    # ----------------------------
    # COVERAGES
    # ----------------------------

    coverages = get_value(policy, "policyCoverage") or []

    if isinstance(coverages, list):
        for coverage in coverages:
            insert(
                "coverages",
                {
                    "coverage_id": str(uuid4()),
                    "policy_id": policy_id,
                    "coverage_name": str(coverage),
                },
            )

    # ----------------------------
    # CLAIMS
    # ----------------------------

    if claims:
        insert(
            "claims",
            {
                "claim_id": str(uuid4()),
                "policy_id": policy_id,
                "cashless_claim_process": get_value(
                    claims,
                    "cashlessService",
                ),
                "reimbursement_claim_process": get_value(
                    claims,
                    "reimbursementProcess",
                ),
            },
        )

    # ----------------------------
    # NETWORK
    # ----------------------------

    if network:
        insert(
            "hospital_network",
            {
                "network_id": str(uuid4()),
                "policy_id": policy_id,
                "network_source": get_value(
                    network,
                    "details",
                ),
            },
        )

    print("✅ Database write completed.")