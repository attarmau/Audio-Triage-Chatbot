let ws;
function connectWS() {
    ws = new WebSocket("ws://localhost:8000/audio/stream");
    ws.onopen = () => console.log("WebSocket connected");
    ws.onclose = () => console.log("WebSocket closed");
}
function sendAudioChunk(chunk) {
    if (ws && ws.readyState === WebSocket.OPEN) {
        ws.send(chunk);
    }
}
export { connectWS, sendAudioChunk };
