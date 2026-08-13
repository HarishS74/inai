from typing import Dict


def normalize(ai_data: Dict) -> Dict:
    """
    Passes through the FULL schema returned by groq_service.py.

    Previous version of this function only kept company/policy/claims/
    network and looked for keys (helpline, grievance, service, other)
    that don't even exist in the current AI extraction schema. That
    silently dropped coverage, benefits, limits (waiting periods,
    co-payment, sub-limits), exclusions, and riders on every single
    document - which is why extractions looked "minimal" even when
    the AI itself returned rich data.

    This version simply keeps every top-level key the AI schema
    defines, defaulting missing ones to an empty dict/list of the
    right type so downstream code (validator, database_writer) never
    has to guess.
    """

    return {
        "company": ai_data.get("company") or {},
        "policy": ai_data.get("policy") or {},
        "coverage": ai_data.get("coverage") or {},
        "benefits": ai_data.get("benefits") or {},
        "limits": ai_data.get("limits") or {},
        "claims": ai_data.get("claims") or {},
        "network": ai_data.get("network") or {},
        "contacts": ai_data.get("contacts") or {},
        "exclusions": ai_data.get("exclusions") or [],
        "riders": ai_data.get("riders") or [],
    }
