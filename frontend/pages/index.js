import { useState } from "react";

const API_BASE = process.env.NEXT_PUBLIC_API_BASE || "http://localhost:8000";

export default function Home() {
  const [userInput, setUserInput] = useState("");
  const [conversation, setConversation] = useState([]);
  const [decision, setDecision] = useState(null);

  const sendText = async () => {
    if (!userInput.trim()) return;
    const updated = [...conversation, { role: "user", content: userInput }];
    setConversation(updated);
    setUserInput("");

    const chatRes = await fetch(`${API_BASE}/chat`, {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({ conversation: updated })
    });
    const chatData = await chatRes.json();
    const nurseReply = chatData.nurse_reply;

    const convo2 = [...updated, { role: "assistant", content: nurseReply }];
    setConversation(convo2);

    // decision step
    const triageRes = await fetch(`${API_BASE}/triage`, {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({ conversation: convo2 })
    });
    const triageData = await triageRes.json();
    setDecision(triageData);
  };

  return (
    <div className="p-6 max-w-3xl mx-auto">
      <h1 className="text-2xl font-bold mb-4">Triage Nurse — Audio & SOAP Decision</h1>

      <div className="border p-4 rounded mb-4 h-80 overflow-y-auto bg-white">
        {conversation.map((m, i) => (
          <div key={i} className={`mb-2 ${m.role === "user" ? "text-right" : "text-left"}`}>
            <b>{m.role === "user" ? "You" : "Nurse"}:</b> {m.content}
          </div>
        ))}
      </div>

      <div className="flex gap-2 mb-4">
        <input
          className="border p-2 rounded flex-1"
          value={userInput}
          onChange={(e)=>setUserInput(e.target.value)}
          onKeyDown={(e)=> e.key === "Enter" && sendText()}
          placeholder="Type your message…"
        />
        <button className="bg-blue-600 text-white px-4 py-2 rounded" onClick={sendText}>
          Send
        </button>
      </div>

      <AudioRecorder conversation={conversation} setConversation={setConversation} setDecision={setDecision} />

      <h2 className="text-xl font-semibold mt-6 mb-2">GPT-5 Case Analysis</h2>
      <pre className="bg-gray-100 p-4 rounded overflow-x-auto">
        {decision ? JSON.stringify(decision, null, 2) : "No analysis yet."}
      </pre>
    </div>
  );
}

function AudioRecorder({ conversation, setConversation, setDecision }) {
  const [recording, setRecording] = useState(false);
  const [mediaRecorder, setMediaRecorder] = useState(null);
  const [chunks, setChunks] = useState([]);

  const startRec = async () => {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    const mr = new MediaRecorder(stream);
    mr.ondataavailable = e => setChunks(prev => [...prev, e.data]);
    mr.onstop = async () => {
      const blob = new Blob(chunks, { type: "audio/webm" });
      setChunks([]);
      const formData = new FormData();
      formData.append("audio", blob, "input.webm");
      formData.append("conversation_json", JSON.stringify(conversation));

      const res = await fetch(`${process.env.NEXT_PUBLIC_API_BASE || "http://localhost:8000"}/audio/stt-chat-tts`, {
        method: "POST",
        body: formData
      });
      const data = await res.json();

      const convo2 = [...conversation, { role: "user", content: data.user_text }, { role: "assistant", content: data.nurse_text }];
      setConversation(convo2);

      const triageRes = await fetch(`${process.env.NEXT_PUBLIC_API_BASE || "http://localhost:8000"}/triage`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ conversation: convo2 })
      });
      const triageData = await triageRes.json();
      setDecision(triageData);

      // TODO: play returned audio if you want (convert from latin1 to blob in a real app)
    };
    mr.start();
    setMediaRecorder(mr);
    setRecording(true);
  };

  const stopRec = () => {
    if (mediaRecorder && recording) {
      mediaRecorder.stop();
      setRecording(false);
    }
  };

  return (
    <div className="flex items-center gap-2">
      <button className={`px-4 py-2 rounded ${recording ? "bg-red-600" : "bg-green-600"} text-white`}
              onClick={recording ? stopRec : startRec}>
        {recording ? "Stop Recording" : "Record Audio"}
      </button>
      <span className="text-sm text-gray-600">{recording ? "Recording…" : "Click to record and send voice"}</span>
    </div>
  );
}
