from app.db.supabase import supabase


def write_database(data: dict):
    """
    Save normalized insurance data into all tables.
    Fully deduplicated - safe to re-upload same PDF.
    """

    # ==========================
    # COMPANY (dedup by company_name)
    # ==========================

    company = data.get("company", {})
    company_name = company.get("name")

    existing_company = (
        supabase.table("companies")
        .select("company_id")
        .eq("company_name", company_name)
        .execute()
    )

    if existing_company.data:
        company_id = existing_company.data[0]["company_id"]
    else:
        company_result = (
            supabase.table("companies")
            .insert({
                "company_name": company_name,
                "irdai_license_number": company.get("IRDAIRegNo"),
                "registration_number": company.get("CIN"),
                "company_address": company.get("registeredOffice")
            })
            .execute()
        )
        company_id = company_result.data[0]["company_id"]

    # ==========================
    # POLICY (dedup by policy_code / UIN)
    # ==========================

    policy = data.get("policy", {})
    policy_code = policy.get("UIN")

    existing_policy = (
        supabase.table("policies")
        .select("policy_id")
        .eq("policy_code", policy_code)
        .execute()
    )

    if existing_policy.data:
        policy_id = existing_policy.data[0]["policy_id"]
    else:
        policy_result = (
            supabase.table("policies")
            .insert({
                "company_id": company_id,
                "policy_name": policy.get("productName"),
                "policy_code": policy_code,
                "policy_type": policy.get("policyType"),
                "individual_or_family": policy.get("sumInsuredBasis")
            })
            .execute()
        )
        policy_id = policy_result.data[0]["policy_id"]

    # ==========================
    # COVERAGES (dedup by policy_id + coverage_name)
    # ==========================

    coverages = policy.get("policyCoverage", [])

    for coverage in coverages:
        existing = (
            supabase.table("coverages")
            .select("coverage_id")
            .eq("policy_id", policy_id)
            .eq("coverage_name", coverage)
            .execute()
        )

        if not existing.data:
            (
                supabase.table("coverages")
                .insert({
                    "policy_id": policy_id,
                    "coverage_name": coverage
                })
                .execute()
            )

    # ==========================
    # WAITING PERIOD (dedup by policy_id)
    # ==========================

    waiting = policy.get("waitingPeriod")

    if waiting:
        existing = (
            supabase.table("waiting_periods")
            .select("*")
            .eq("policy_id", policy_id)
            .execute()
        )

        if not existing.data:
            (
                supabase.table("waiting_periods")
                .insert({
                    "policy_id": policy_id,
                    "condition": waiting
                })
                .execute()
            )

    # ==========================
    # EXCLUSIONS (dedup by policy_id)
    # ==========================

    exclusion = policy.get("exclusions")

    if exclusion:
        existing = (
            supabase.table("exclusions")
            .select("*")
            .eq("policy_id", policy_id)
            .execute()
        )

        if not existing.data:
            (
                supabase.table("exclusions")
                .insert({
                    "policy_id": policy_id,
                    "exclusion_description": exclusion
                })
                .execute()
            )

    # ==========================
    # CLAIMS (dedup by policy_id)
    # ==========================

    claims = data.get("claims", {})

    existing = (
        supabase.table("claims")
        .select("*")
        .eq("policy_id", policy_id)
        .execute()
    )

    if not existing.data:
        (
            supabase.table("claims")
            .insert({
                "policy_id": policy_id,
                "cashless_claim_process": claims.get("cashlessService"),
                "reimbursement_claim_process": claims.get("reimbursementProcess"),
                "claim_settlement_information": claims.get("turnAroundTime"),
                "claim_source": claims.get("claimForm")
            })
            .execute()
        )

    # ==========================
    # HOSPITAL NETWORK (dedup by policy_id)
    # ==========================

    network = data.get("network", {})

    existing = (
        supabase.table("hospital_network")
        .select("*")
        .eq("policy_id", policy_id)
        .execute()
    )

    if not existing.data:
        (
            supabase.table("hospital_network")
            .insert({
                "policy_id": policy_id,
                "network_source": network.get("details")
            })
            .execute()
        )

    print("✅ Data saved successfully.")