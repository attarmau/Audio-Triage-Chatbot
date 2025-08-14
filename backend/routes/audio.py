from fastapi import APIRouter, WebSocket
from websocket_manager import manager
from audio_handler import save_audio_chunk

router = APIRouter()

@router.websocket("/stream")
async def audio_stream(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_bytes()
            save_audio_chunk("live_recording.wav", data)
    except:
        manager.disconnect(websocket)
