import { connectWS, sendAudioChunk } from "./websocket.js";

let mediaRecorder;
let audioChunks = [];

document.getElementById("startBtn").addEventListener("click", async () => {
    connectWS();
    let stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    mediaRecorder = new MediaRecorder(stream);
    mediaRecorder.ondataavailable = e => sendAudioChunk(e.data);
    mediaRecorder.start(250);
});

document.getElementById("stopBtn").addEventListener("click", () => {
    if (mediaRecorder) {
        mediaRecorder.stop();
    }
});
