from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import triage, audio

app = FastAPI(title="TeleTriage Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(triage.router, prefix="/triage", tags=["Triage"])
app.include_router(audio.router, prefix="/audio", tags=["Audio"])

@app.get("/")
def root():
    return {"message": "TeleTriage API is running"}
