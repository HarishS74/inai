from groq import Groq
from app.config import GROQ_API_KEY
import json

client = Groq(api_key=GROQ_API_KEY)


def analyze(text):

    prompt = f"""
You are an insurance AI expert.

Extract every insurance detail from this document.

Return ONLY valid JSON.

{text}
"""

    chat = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0
    )

    content = chat.choices[0].message.content

    # Remove markdown code fences if Groq returns them
    content = content.replace("```json", "").replace("```", "").strip()

    try:
        result = json.loads(content)
        print("===== RAW GROQ JSON =====")
        print(json.dumps(result, indent=2))
        print("==========================")
        return result
    except json.JSONDecodeError:
        return {
            "raw_response": content
        }