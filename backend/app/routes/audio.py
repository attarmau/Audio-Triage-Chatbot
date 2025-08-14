import json
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.config import MAX_WS_MESSAGE_SIZE
from app.services.audio_service import (
    ensure_session,
    add_audio_chunk,
    reset_utterance_buffer,
    transcribe_current_utterance,
    append_user_text,
    append_assistant_text,
    nurse_reply_for_conversation,
)

router = APIRouter()

@router.websocket("/ws")
async def audio_ws(ws: WebSocket):
    # Accept and set max message size
    await ws.accept()
    ws.session_key = str(id(ws))
    ensure_session(ws.session_key)
    await ws.send_json({"type": "ack", "message": "Connected. Send audio_chunk frames, then end_utterance."})

    try:
        while True:
            # `bytes` or `text` frames can arrive; we expect JSON text frames
            raw = await ws.receive_text()
            msg = json.loads(raw)

            mtype = msg.get("type")
            if mtype == "start":
                await ws.send_json({"type": "ack", "message": "Session started."})

            elif mtype == "audio_chunk":
                b64 = msg.get("data", "")
                if not b64:
                    await ws.send_json({"type": "error", "message": "Missing base64 audio in 'data'."})
                    continue
                add_audio_chunk(ws.session_key, b64)

            elif mtype == "end_utterance":
                # STT
                text = transcribe_current_utterance(ws.session_key)
                reset_utterance_buffer(ws.session_key)
                if not text:
                    await ws.send_json({"type": "transcript", "text": ""})
                    continue

                await ws.send_json({"type": "transcript", "text": text})
                append_user_text(ws.session_key, text)

                # Nurse reply
                reply = nurse_reply_for_conversation(ws.session_key)
                append_assistant_text(ws.session_key, reply)
                await ws.send_json({"type": "nurse_reply", "text": reply})

            elif mtype == "finalize":
                # Placeholder: you can call your GPT-5 SOAP decision here and return the result.
                await ws.send_json({
                    "type": "ack",
                    "message": "Finalize received. (Hook GPT-5 SOAP decision here if needed.)"
                })

            else:
                await ws.send_json({"type": "error", "message": f"Unknown message type: {mtype}"})

    except WebSocketDisconnect:
        # Client disconnected
        pass
    except Exception as e:
        await ws.send_json({"type": "error", "message": f"Server error: {e}"})
    finally:
        try:
            await ws.send_json({"type": "session_closed"})
        except Exception:
            pass
        await ws.close()
