from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services import gpt_service

router = APIRouter()

class ConversationRequest(BaseModel):
    conversation: list  # [{ "role": "user"|"assistant", "content": "..." }]

@router.post("/triage-decision")
async def triage_decision(req: ConversationRequest):
    try:
        # Step 1 — GPT-4o-Realtime-Review conversation step
        nurse_reply = await gpt_service.get_nurse_reply(req.conversation)

        # Step 2 — Feed into GPT-5 for SOAP decision
        updated_convo = req.conversation + [{"role": "assistant", "content": nurse_reply}]
        decision = await gpt_service.get_triage_decision(updated_convo)

        return {
            "nurse_reply": nurse_reply,
            "gpt5_decision": decision
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
