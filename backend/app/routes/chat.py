from fastapi import APIRouter
from pydantic import BaseModel
from openai import OpenAI
from ..config import OPENAI_API_KEY, MODEL_CONVO
from ..utils.prompt_templates import TRIAGE_MULTILANG_PROMPT

client = OpenAI(api_key=OPENAI_API_KEY)
router = APIRouter()

class ChatTurn(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    conversation: list[ChatTurn]

@router.post("")
def chat(req: ChatRequest):
    # prepend system prompt
    messages = [{"role": "system", "content": TRIAGE_MULTILANG_PROMPT}]
    for m in req.conversation:
        messages.append({"role": m.role, "content": m.content})

    resp = client.chat.completions.create(
        model=MODEL_CONVO,
        messages=messages
    )
    nurse_reply = resp.choices[0].message.content
    return {"nurse_reply": nurse_reply}
