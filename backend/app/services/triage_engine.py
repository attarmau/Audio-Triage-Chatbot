import json
from openai import OpenAI
from ..config import OPENAI_API_KEY, MODEL_DECIDE

client = OpenAI(api_key=OPENAI_API_KEY)

DECISION_SYSTEM_PROMPT = """
You are a clinical triage decision agent.
You receive the latest patient–nurse conversation (no system messages).

Decide exactly one outcome:
- "SOAP": common symptoms with no red flags → generate SOAP
- "Emergency Case": red-flag symptoms (bleeding, severe chest pain, difficulty breathing, loss of consciousness, seizures, stroke signs)
- "No SOAP": irrelevant/complex/unlisted → default dashboard message

Return strict JSON only:
{
  "outcome": "SOAP" | "Emergency Case" | "No SOAP",
  "note": "optional short note",
  "soap": {
    "S": "...",
    "O": "...",
    "A": "...",
    "P": "..."
  } | null
}
"""

def decide_json(conversation:list[dict]):
    user_payload = "Latest conversation:\n" + "\n".join(
        [f'{m["role"]}: {m["content"]}' for m in conversation]
    )

    resp = client.chat.completions.create(
        model=MODEL_DECIDE,
        messages=[
            {"role": "system", "content": DECISION_SYSTEM_PROMPT},
            {"role": "user", "content": user_payload}
        ]
    )
    raw = resp.choices[0].message.content
    try:
        return json.loads(raw)
    except Exception:
        return {"outcome": "No SOAP", "note": "Invalid JSON from model", "soap": None, "raw": raw}
