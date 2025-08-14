import base64
import io
import json
from typing import List, Dict, Any

from openai import OpenAI
from app.config import OPENAI_API_KEY, MODEL_STT, MODEL_CONVO, PROMPT_ID
from app.services.prompt_templates import TRIAGE_MULTILANG_PROMPT

client = OpenAI(api_key=OPENAI_API_KEY)

# In-memory conversation store per connection (replace with DB if needed)
# key = session_id (we'll use id(ws) from the WebSocket)
SESSIONS: Dict[str, Dict[str, Any]] = {}
# Each session:
# {
#   "buffer": io.BytesIO(),         # audio buffer for current utterance
#   "conversation": [ {role, content}, ...]  # running text conversation (no system)
# }

def ensure_session(session_key: str):
    if session_key not in SESSIONS:
        SESSIONS[session_key] = {
            "buffer": io.BytesIO(),
            "conversation": []
        }

def add_audio_chunk(session_key: str, audio_b64: str):
    """Append base64 PCM16 chunk to session buffer."""
    ensure_session(session_key)
    chunk = base64.b64decode(audio_b64)
    SESSIONS[session_key]["buffer"].write(chunk)

def reset_utterance_buffer(session_key: str):
    ensure_session(session_key)
    SESSIONS[session_key]["buffer"] = io.BytesIO()

def get_conversation(session_key: str) -> List[Dict[str, str]]:
    ensure_session(session_key)
    return SESSIONS[session_key]["conversation"]

def append_user_text(session_key: str, text: str):
    ensure_session(session_key)
    SESSIONS[session_key]["conversation"].append({"role": "user", "content": text})

def append_assistant_text(session_key: str, text: str):
    ensure_session(session_key)
    SESSIONS[session_key]["conversation"].append({"role": "assistant", "content": text})

def transcribe_current_utterance(session_key: str, language_hint: str | None = None) -> str:
    """
    Run STT on the buffered audio for this session and return text.
    Expects PCM16 mono @16k from the frontend (you can change to wav if you prefer).
    """
    ensure_session(session_key)
    audio_bytes = SESSIONS[session_key]["buffer"].getvalue()
    if not audio_bytes:
        return ""

    # Build a temporary in-memory file-like object
    file_like = io.BytesIO(audio_bytes)
    file_like.name = "audio.pcm"  # name hint

    # If you prefer to stream wav, encode as wav client-side and set name="audio.wav"
    # Here we let Whisper try its best on PCM16
    transcription = client.audio.transcriptions.create(
        model=MODEL_STT,
        file=("audio.pcm", file_like, "audio/pcm"),
        # language=language_hint or None,  # optional
        # response_format="text"          # default is fine
    )
    # OpenAI python SDK returns an object; `text` is typically present
    text = getattr(transcription, "text", "")
    return text.strip()

def nurse_reply_for_conversation(session_key: str) -> str:
    """
    Call the conversation model with your triage nurse system prompt + running conversation.
    """
    convo = get_conversation(session_key)
    messages = [{"role": "system", "content": TRIAGE_MULTILANG_PROMPT}] + convo

    # If you want to try your saved Prompt ID, pass via extra_body (SDK forwards unknown fields).
    extra_body = {"prompt_id": PROMPT_ID} if PROMPT_ID else None

    resp = client.chat.completions.create(
        model=MODEL_CONVO,
        messages=messages,
        **({"extra_body": extra_body} if extra_body else {})
    )
    reply = resp.choices[0].message.content
    return reply.strip()
