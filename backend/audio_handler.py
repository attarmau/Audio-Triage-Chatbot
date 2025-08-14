import os
from config import AUDIO_SAVE_PATH

if not os.path.exists(AUDIO_SAVE_PATH):
    os.makedirs(AUDIO_SAVE_PATH)

def save_audio_chunk(filename: str, chunk: bytes):
    with open(os.path.join(AUDIO_SAVE_PATH, filename), "ab") as f:
        f.write(chunk)
