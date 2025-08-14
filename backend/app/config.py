import os

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
assert OPENAI_API_KEY, "Set OPENAI_API_KEY in your environment."

# Models
MODEL_CONVO = os.getenv("MODEL_CONVO", "gpt-4o-realtime-review")  # conversation (text)
MODEL_STT   = os.getenv("MODEL_STT", "gpt-4o-mini-transcribe")    # speech-to-text
MODEL_TTS   = os.getenv("MODEL_TTS", "gpt-4o-mini-tts")           # text-to-speech
MODEL_DECIDE= os.getenv("MODEL_DECIDE", "gpt-5")                  # SOAP / decision

# Optional: If you manage a Prompt in the OpenAI Dashboard, put its text here or fetch it.
PROMPT_CONVO_TEXT = os.getenv("PROMPT_CONVO_TEXT", "")
PROMPT_ID = os.getenv("PROMPT_ID", "pmpt_689d139950dc81958213fb3ee11e3b7506d30fac4b01cbab")  # for reference only
