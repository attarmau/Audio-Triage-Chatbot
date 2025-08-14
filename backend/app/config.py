import os

# ---- ENV ----
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
if not OPENAI_API_KEY:
    raise RuntimeError("Set OPENAI_API_KEY in your environment.")

# Models
# Speech-to-text (use Whisper or your preferred STT)
MODEL_STT = os.getenv("MODEL_STT", "whisper-1")

# Conversation model (realtime-* family is OK to use via chat completions for text replies)
MODEL_CONVO = os.getenv("MODEL_CONVO", "gpt-4o-realtime-preview")

# Decision model (if/when you call GPT-5 for SOAP decision)
MODEL_DECISION = os.getenv("MODEL_DECISION", "gpt-5")

# Optional: your saved Prompts ID for the triage nurse (if you have one)
PROMPT_ID = os.getenv("TRIAGE_PROMPT_ID", "").strip()  # e.g. pmpt_xxx

# Audio settings (what the client will send)
AUDIO_SAMPLE_RATE = int(os.getenv("AUDIO_SAMPLE_RATE", "16000"))   # PCM16 @ 16k
AUDIO_CHANNELS = int(os.getenv("AUDIO_CHANNELS", "1"))

# WebSocket message size limit (bytes)
MAX_WS_MESSAGE_SIZE = int(os.getenv("MAX_WS_MESSAGE_SIZE", str(5 * 1024 * 1024)))  # 5MB
