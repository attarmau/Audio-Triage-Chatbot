from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import audio

app = FastAPI(
    title="Real-Time Pre-Consultation Triage",
    description="WebSocket audio streaming + pre-consult triage conversation.",
    version="1.0.0",
)

# CORS (tighten in prod)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],      # e.g. ["http://localhost:5173"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
app.include_router(audio.router, prefix="/audio", tags=["Audio"])

@app.get("/")
def root():
    return {"ok": True, "service": "Real-Time Triage API"}
