from openai import OpenAI
from ..config import OPENAI_API_KEY, MODEL_STT

client = OpenAI(api_key=OPENAI_API_KEY)

async def transcribe_audio(upload_file) -> str:
    """
    Returns transcribed text from uploaded audio file.
    """
    # Load bytes into memory
    audio_bytes = await upload_file.read()
    # OpenAI audio transcription (gpt-4o-mini-transcribe or whisper-1)
    transcript = client.audio.transcriptions.create(
        model=MODEL_STT,
        file=("audio.wav", audio_bytes)
    )
    return transcript.text.strip()
