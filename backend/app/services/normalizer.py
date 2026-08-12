from typing import Dict


def normalize(ai_data: Dict) -> Dict:

    return {

        "company": ai_data.get("insuranceCompany")
                    or ai_data.get("company")
                    or ai_data.get("company_name")
                    or {},

        "policy": ai_data.get("policyDetails")
                    or ai_data.get("policy")
                    or {},

        "claims": ai_data.get("claimsProcedure")
                    or ai_data.get("claims")
                    or {},

        "network": ai_data.get("networkHospitals")
                    or ai_data.get("network")
                    or {},

        "helpline": ai_data.get("helplineNumbers")
                    or ai_data.get("helpline")
                    or {},

        "grievance": ai_data.get("grievances")
                    or ai_data.get("grievance")
                    or {},

        "service": ai_data.get("policyServicing")
                    or ai_data.get("service")
                    or {},

        "other": ai_data.get("otherDetails")
                    or ai_data.get("other")
                    or {}
    }