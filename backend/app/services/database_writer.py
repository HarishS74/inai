import re
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


def as_int_or_none(value):
    """
    Some columns (e.g. hospital_network.network_hospital_count) are
    typed as integer in Supabase, but the AI sometimes returns
    descriptive text like '6000+ hospitals' instead of a bare number.
    Only pass a value through if it's actually a clean integer -
    otherwise return None so the insert doesn't fail with a type
    error the way waiting_periods.duration did earlier.
    """
    if value is None:
        return None
    match = re.search(r"\d+", str(value))
    return int(match.group()) if match else None


def write_database(data: dict):

    company = data.get("company", {})
    policy = data.get("policy", {})
    coverage = data.get("coverage", {})
    benefits = data.get("benefits", {})
    limits = data.get("limits", {})
    claims = data.get("claims", {})
    network = data.get("network", {})
    exclusions = data.get("exclusions", []) or []
    riders = data.get("riders", []) or []

    policy_name = get_value(policy, "productName", "policyName", "name") or "Unknown Policy"
    source_doc = policy_name  # used for source_document columns below

    # ----------------------------
    # COMPANY
    # ----------------------------

    company_name = (
        get_value(company, "name", "insuranceCompany", "company_name", "companyName")
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
                "registration_number": get_value(company, "CIN", "registrationNumber"),
                "irdai_license_number": get_value(
                    company, "irdaRegistrationNo", "IRDAIRegNo", "irdaiNumber"
                ),
                "company_address": get_value(company, "registeredOffice", "address"),
            },
        )
        print(f"✅ New company inserted: {company_name}")

    # ----------------------------
    # POLICY
    # ----------------------------

    existing_policy = (
        supabase.table("policies")
        .select("policy_id")
        .eq("company_id", company_id)
        .eq("policy_name", policy_name)
        .execute()
    )

    if existing_policy.data:
        print("✅ Policy already exists — skipping duplicate insert.")
        policy_id = existing_policy.data[0]["policy_id"]
    else:
        policy_id = str(uuid4())
        insert(
            "policies",
            {
                "policy_id": policy_id,
                "company_id": company_id,
                "policy_name": policy_name,
                "policy_code": get_value(policy, "uin", "UIN", "policyCode"),
                "policy_type": get_value(policy, "policyType"),
                "individual_or_family": get_value(
                    policy, "individualOrFamily", "sumInsuredBasis"
                ),
            },
        )
        print(f"✅ New policy inserted: {policy_name}")

    # ----------------------------
    # COVERAGES
    # Maps into your actual columns: coverage_name, coverage_description,
    # coverage_detail, source_document. Richer columns (coverage_category,
    # coverage_amount, waiting_period, deductible, copayment, etc.) are
    # left for a later pass once the AI prompt is extended to return
    # those as separate structured fields per coverage item, rather
    # than guessed at here.
    # ----------------------------
    for coverage_name, coverage_value in coverage.items():
        if coverage_value in [None, "", [], {}]:
            continue

        insert(
            "coverages",
            {
                "coverage_id": str(uuid4()),
                "policy_id": policy_id,
                "coverage_name": coverage_name,
                "coverage_description": str(coverage_value),
                "coverage_detail": str(coverage_value),
                "source_document": source_doc,
            },
        )

    # ----------------------------
    # BENEFITS
    # ----------------------------
    for benefit_name, benefit_value in benefits.items():
        if benefit_value in [None, "", [], {}]:
            continue

        insert(
            "benefits",
            {
                "benefit_id": str(uuid4()),
                "policy_id": policy_id,
                "benefit_name": benefit_name,
                "benefit_detail": str(benefit_value),
            },
        )

    # ----------------------------
    # WAITING PERIODS
    # Maps into: waiting_period_type, condition, duration, source_document.
    # duration is TEXT (fixed earlier) so descriptive values like
    # "30 days (except for Accident)" are preserved rather than
    # forced into an integer.
    # ----------------------------
    waiting_period = limits.get("waitingPeriod") or {}

    for wp_type, wp_value in waiting_period.items():
        if wp_value in [None, "", [], {}]:
            continue

        insert(
            "waiting_periods",
            {
                "waiting_period_id": str(uuid4()),
                "policy_id": policy_id,
                "waiting_period_type": wp_type,
                "condition": wp_type,
                "duration": str(wp_value),
                "source_document": source_doc,
            },
        )

    # co-payment, deductible, and sub-limits don't have a clean home in
    # waiting_periods, but there's no separate policy-level limits
    # table wired up yet either (your schema has copayment_deductibles,
    # room_rent_limits etc. as SEPARATE dedicated tables - worth mapping
    # into those specifically in a follow-up pass rather than
    # shoehorning here). For now these are still captured, just
    # recorded here so nothing is silently lost in the meantime.
    co_payment = get_value(limits, "coPayment")
    if co_payment:
        insert(
            "waiting_periods",
            {
                "waiting_period_id": str(uuid4()),
                "policy_id": policy_id,
                "waiting_period_type": "co_payment",
                "condition": "co_payment",
                "duration": str(co_payment),
                "source_document": source_doc,
            },
        )

    deductible = get_value(limits, "deductible")
    if deductible:
        insert(
            "waiting_periods",
            {
                "waiting_period_id": str(uuid4()),
                "policy_id": policy_id,
                "waiting_period_type": "deductible",
                "condition": "deductible",
                "duration": str(deductible),
                "source_document": source_doc,
            },
        )

    for sub_limit in (limits.get("subLimits") or []):
        insert(
            "waiting_periods",
            {
                "waiting_period_id": str(uuid4()),
                "policy_id": policy_id,
                "waiting_period_type": "sub_limit",
                "condition": "sub_limit",
                "duration": str(sub_limit),
                "source_document": source_doc,
            },
        )

    # ----------------------------
    # EXCLUSIONS
    # Maps into: exclusion_name (truncated), exclusion_description,
    # exclusion_detail, source_document. exclusion_category and
    # permanent_or_conditional are left null for now - the AI schema
    # only returns exclusions as a flat list of strings, not yet
    # broken into category/permanence, which would need a prompt
    # change in groq_service.py to fill properly.
    # ----------------------------
    for exclusion in exclusions:
        exclusion_text = str(exclusion)
        insert(
            "exclusions",
            {
                "exclusion_id": str(uuid4()),
                "policy_id": policy_id,
                "exclusion_name": exclusion_text[:250],
                "exclusion_description": exclusion_text,
                "exclusion_detail": exclusion_text,
                "source_document": source_doc,
            },
        )

    # ----------------------------
    # RIDERS
    # ----------------------------
    for rider in riders:
        rider_text = str(rider)
        insert(
            "riders",
            {
                "rider_id": str(uuid4()),
                "policy_id": policy_id,
                "rider_name": rider_text[:250],
                "rider_detail": rider_text,
            },
        )

    # ----------------------------
    # CLAIMS
    # Maps into your actual columns.
    # ----------------------------
    if claims:
        required_docs = claims.get("requiredDocuments") or []
        insert(
            "claims",
            {
                "claim_id": str(uuid4()),
                "policy_id": policy_id,
                "cashless_claim_process": get_value(claims, "cashless", "cashlessService"),
                "reimbursement_claim_process": get_value(
                    claims, "reimbursement", "reimbursementProcess"
                ),
                "claim_intimation_method": get_value(claims, "claimIntimation"),
                "claim_document_requirements": (
                    ", ".join(str(d) for d in required_docs) if required_docs else None
                ),
            },
        )

    # ----------------------------
    # NETWORK
    # Maps into your actual columns. network_hospital_count is only
    # set if the AI returned a clean number - otherwise the raw text
    # goes into network_source instead, to avoid the same integer
    # type error we hit on waiting_periods.duration earlier.
    # ----------------------------
    if network:
        raw_count = get_value(network, "cashlessHospitalCount")
        insert(
            "hospital_network",
            {
                "network_id": str(uuid4()),
                "policy_id": policy_id,
                "network_hospital_count": as_int_or_none(raw_count),
                "network_source": get_value(network, "networkDetails", "details")
                or (str(raw_count) if raw_count and as_int_or_none(raw_count) is None else None),
            },
        )

    print(
        f"✅ Database write completed. "
        f"{len(coverage)} coverage fields, {len(exclusions)} exclusions, "
        f"{len(waiting_period)} waiting periods, {len(riders)} riders, "
        f"{len(benefits)} benefits written."
    )
