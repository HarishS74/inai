from app.services.save_to_db import insert


def save_all(data):

    # ---------------- COMPANY ----------------

    company = data.get("insuranceCompany", {})

    company_row = insert("companies", {
        "company_name": company.get("name"),
        "irdai_registration_number": company.get("IRDAIRegNo"),
        "cin": company.get("CIN"),
        "registered_office": company.get("registeredOffice")
    })

    company_id = None

    if company_row:
        company_id = company_row["id"]


    # ---------------- POLICY ----------------

    policy = data.get("policyDetails", {})

    policy_row = insert("policies", {
        "company_id": company_id,
        "policy_name": policy.get("productName"),
        "uin": policy.get("UIN"),
        "policy_type": policy.get("policyType"),
        "sum_insured_basis": policy.get("sumInsuredBasis"),
        "financial_limits": policy.get("financialLimits"),
        "exclusions": policy.get("exclusions")
    })

    policy_id = None

    if policy_row:
        policy_id = policy_row["id"]


    # ---------------- COVERAGES ----------------

    for coverage in policy.get("policyCoverage", []):

        insert("coverages", {
            "policy_id": policy_id,
            "coverage_name": coverage
        })


    # ---------------- WAITING PERIOD ----------------

    insert("waiting_periods", {
        "policy_id": policy_id,
        "description": policy.get("waitingPeriod")
    })


    # ---------------- CLAIMS ----------------

    claims = data.get("claimsProcedure", {})

    insert("claims", {
        "policy_id": policy_id,
        "cashless_service": claims.get("cashlessService"),
        "reimbursement_process": claims.get("reimbursementProcess"),
        "turnaround_time": claims.get("turnAroundTime"),
        "claim_form_url": claims.get("claimForm")
    })


    # ---------------- HOSPITAL NETWORK ----------------

    hospitals = data.get("networkHospitals", {})

    insert("hospital_network", {
        "policy_id": policy_id,
        "network_url": hospitals.get("details"),
        "excluded_hospital_url": hospitals.get("excludedHospitals")
    })

    return policy_id