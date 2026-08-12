import os
import json

from dotenv import load_dotenv
from openai import OpenAI
from openai import RateLimitError

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)

MODELS = [
    "google/gemma-4-26b-a4b-it:free",
    "openai/gpt-oss-20b:free",
    "nvidia/nemotron-3-super-120b-a12b:free",
]

SYSTEM_PROMPT = """
You are an expert health insurance document extractor.

Return ONLY valid JSON.

If a value is not found, return null.

Do not explain anything.

Extract exactly this schema:

{
  "company": {
    "name": null,
    "registeredOffice": null,
    "irdaRegistrationNo": null,
    "cin": null,
    "website": null,
    "email": null,
    "phone": null
  },

  "policy": {
    "productName": null,
    "uin": null,
    "policyType": null,
    "policyTerm": null,
    "entryAge": null,
    "exitAge": null,
    "renewability": null,
    "individualOrFamily": null,
    "sumInsuredOptions": [],
    "premiumStartingFrom": null
  },

  "coverage": {
    "roomRent": null,
    "icu": null,
    "preHospitalization": null,
    "postHospitalization": null,
    "dayCare": null,
    "ambulance": null,
    "organDonor": null,
    "domiciliaryTreatment": null,
    "ayushTreatment": null,
    "maternity": null,
    "newbornBaby": null,
    "healthCheckup": null,
    "vaccination": null,
    "mentalIllness": null,
    "modernTreatment": null
  },

  "benefits": {
    "restoreBenefit": null,
    "noClaimBonus": null,
    "superNoClaimBonus": null,
    "cumulativeBonus": null,
    "airAmbulance": null
  },

  "limits": {
    "coPayment": null,
    "deductible": null,
    "subLimits": [],
    "waitingPeriod": {
      "initial": null,
      "specificDisease": null,
      "preExistingDisease": null
    }
  },

  "claims": {
    "cashless": null,
    "reimbursement": null,
    "claimIntimation": null,
    "requiredDocuments": []
  },

  "network": {
    "cashlessHospitalCount": null,
    "networkDetails": null
  },

  "contacts": {
    "customerCare": [],
    "email": null,
    "website": null,
    "grievanceOfficer": null
  },

  "exclusions": [],

  "riders": []
}

Return ONLY JSON.
"""

def analyze_chunk(text: str):

    last_error = None

    for model in MODELS:

        try:

            print(f"\nUsing model: {model}")

            response = client.chat.completions.create(
                model=model,
                temperature=0,
                messages=[
                    {
                        "role": "system",
                        "content": SYSTEM_PROMPT
                    },
                    {
                        "role": "user",
                        "content": text
                    }
                ]
            )

            output = response.choices[0].message.content.strip()

            output = (
                output.replace("```json", "")
                .replace("```", "")
                .strip()
            )

            return json.loads(output)

        except RateLimitError:
            print(f"{model} is busy. Trying next model...")
            last_error = "Rate limit"

        except json.JSONDecodeError:
            print(f"{model} returned invalid JSON.")
            last_error = "Invalid JSON"

        except Exception as e:
            print(f"{model} failed:")
            print(e)
            last_error = e

    raise Exception(f"All models failed. Last error: {last_error}")