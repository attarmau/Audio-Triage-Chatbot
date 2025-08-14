from openai import OpenAI
from ..config import OPENAI_API_KEY, MODEL_TTS

client = OpenAI(api_key=OPENAI_API_KEY)

async def synthesize_speech(text: str) -> bytes:
    """
    Returns MP3 bytes for the given text using OpenAI TTS.
    """
    resp = client.audio.speech.create(
        model=MODEL_TTS,
        voice="alloy",
        input=text
    )
    # The SDK returns a bytes-like object in .content for audio
    return resp.content
