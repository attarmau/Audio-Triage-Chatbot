import json
from openai import OpenAI
from ..config import OPENAI_API_KEY, MODEL_CONVO
from ..utils.prompt_templates import TRIAGE_MULTILANG_PROMPT

client = OpenAI(api_key=OPENAI_API_KEY)

async def convo_reply(user_text: str, conversation_json: str):
    """
    Append user_text to conversation and get nurse reply.
    conversation_json is a JSON list of {role, content} without system.
    """
    try:
        convo = json.loads(conversation_json)
    except Exception:
        convo = []

    convo.append({"role": "user", "content": user_text})
    messages = [{"role": "system", "content": TRIAGE_MULTILANG_PROMPT}] + convo

    resp = client.chat.completions.create(
        model=MODEL_CONVO,
        messages=messages
    )
    nurse = resp.choices[0].message.content
    convo.append({"role": "assistant", "content": nurse})
    return nurse, json.dumps(convo)
