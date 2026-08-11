from datetime import datetime


def normalize(data: dict):

    company = data.get("insuranceCompany", {})
    policy = data.get("policyDetails", {})
    claims = data.get("claimsProcedure", {})
    hospitals = data.get("networkHospitals", {})
    helpline = data.get("helplineNumbers", {})
    grievance = data.get("grievances", {})
    servicing = data.get("policyServicing", {})
    other = data.get("otherDetails", {})

    normalized = {

        "company": {
            "company_name": company.get("name"),
            "registration_number": company.get("CIN"),
            "irdai_license_number": company.get("IRDAIRegNo"),
            "company_address": company.get("registeredOffice"),
            "created_at": datetime.utcnow().isoformat()
        },

        "policy": {
            "policy_name": policy.get("productName"),
            "policy_code": policy.get("UIN"),
            "policy_type": policy.get("policyType"),
            "individual_or_family": policy.get("sumInsuredBasis"),
            "policy_description": "",
            "created_at": datetime.utcnow().isoformat()
        },

        "coverages": [],

        "waiting_periods": [
            {
                "waiting_period_type": "General",
                "condition": policy.get("waitingPeriod"),
                "duration": None,
                "unit": None
            }
        ],

        "claims": {
            "claim_process": claims.get("cashlessService"),
            "cashless_claim_process": claims.get("cashlessService"),
            "reimbursement_claim_process": claims.get("reimbursementProcess"),
            "claim_submission_method": claims.get("claimForm"),
            "claim_assistance": servicing.get("companyOfficials"),
            "claim_settlement_information": claims.get("turnAroundTime")
        },

        "hospital_network": {
            "network_type": "Cashless",
            "network_available": True,
            "network_source": hospitals.get("details"),
            "cashless_available": True
        },

        "helpline": {
            "call": helpline.get("call"),
            "senior": helpline.get("seniorCitizenDedicatedHelpline"),
            "women": helpline.get("womenDedicatedHelpline")
        },

        "grievance": grievance,

        "other": other
    }

    for item in policy.get("policyCoverage", []):

        normalized["coverages"].append({
            "coverage_name": item,
            "coverage_category": "Medical",
            "included_or_optional": "Included"
        })

    return normalized