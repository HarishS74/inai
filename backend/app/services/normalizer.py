from typing import Dict

def normalize(ai_data: Dict) -> Dict:
    """
    Converts AI response into a fixed schema.
    Missing keys are added automatically.
    """

    return {

        "company": ai_data.get("insuranceCompany", {}),

        "policy": ai_data.get("policyDetails", {}),

        "claims": ai_data.get("claimsProcedure", {}),

        "network": ai_data.get("networkHospitals", {}),

        "helpline": ai_data.get("helplineNumbers", {}),

        "grievance": ai_data.get("grievances", {}),

        "service": ai_data.get("policyServicing", {}),

        "other": ai_data.get("otherDetails", {})
    }