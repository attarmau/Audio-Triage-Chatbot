from fastapi import APIRouter, File, UploadFile, Form
from pydantic import BaseModel
from openai import OpenAI
from ..config import OPENAI_API_KEY
from ..services.stt_service import transcribe_audio
from ..services.tts_service import synthesize_speech
from ..services.gpt_service import convo_reply

client = OpenAI(api_key=OPENAI_API_KEY)
router = APIRouter()

class AudioReply(BaseModel):
    text_reply: str

@router.post("/stt-chat-tts")
async def stt_chat_tts(
    audio: UploadFile = File(...),
    conversation_json: str = Form("[]"),
):
    """
    1) STT -> text
    2) GPT conversation reply
    3) TTS -> audio
    Returns both nurse text and audio (mp3) bytes.
    """
    user_text = await transcribe_audio(audio)
    # Call GPT convo with user's text appended
    nurse_text, updated_convo = await convo_reply(user_text, conversation_json)

    # TTS the nurse reply
    mp3_bytes = await synthesize_speech(nurse_text)

    return {
        "user_text": user_text,
        "nurse_text": nurse_text,
        "audio_base64": mp3_bytes.decode("latin1")  # send as bytes-safe; front-end should request blob
    }
