from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import audio, chat, triage

app = FastAPI(title="Audio Triage Nurse API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat.router, prefix="/chat", tags=["chat"])
app.include_router(audio.router, prefix="/audio", tags=["audio"])
app.include_router(triage.router, prefix="/triage", tags=["triage"])
