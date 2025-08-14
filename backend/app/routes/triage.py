from fastapi import APIRouter
from pydantic import BaseModel
from ..services.triage_engine import decide_json

router = APIRouter()

class TriageRequest(BaseModel):
    conversation: list[dict]  # [{role, content}, ...] without system

@router.post("")
def triage(req: TriageRequest):
    decision = decide_json(req.conversation)
    return decision
