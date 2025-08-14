import { useState } from "react";

export default function Home() {
  const [userInput, setUserInput] = useState("");
  const [conversation, setConversation] = useState([]); // Stores all chat messages
  const [decision, setDecision] = useState(null);       // Stores GPT-5 JSON

  const sendMessage = async () => {
    if (!userInput.trim()) return;

    const newMessage = { role: "user", content: userInput };
    const updatedConversation = [...conversation, newMessage];
    setConversation(updatedConversation);
    setUserInput("");

    // Call backend API
    const res = await fetch("/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ conversation: updatedConversation })
    });
    const data = await res.json();

    // Append nurse reply
    setConversation([...updatedConversation, { role: "assistant", content: data.nurse_reply }]);

    // Update GPT-5 decision
    setDecision(data.gpt5_decision);
  };

  return (
    <div className="p-6 max-w-3xl mx-auto">
      <h1 className="text-2xl font-bold mb-4">Triage Nurse AI</h1>

      <div className="border p-4 rounded mb-4 h-96 overflow-y-auto">
        {conversation.map((msg, idx) => (
          <div key={idx} className={msg.role === "user" ? "text-right" : "text-left"}>
            <b>{msg.role === "user" ? "You" : "Nurse"}:</b> {msg.content}
          </div>
        ))}
      </div>

      <input
        type="text"
        className="border p-2 w-full mb-2 rounded"
        value={userInput}
        onChange={(e) => setUserInput(e.target.value)}
        onKeyDown={(e) => e.key === "Enter" && sendMessage()}
        placeholder="Type your message..."
      />
      <button
        className="bg-blue-500 text-white px-4 py-2 rounded"
        onClick={sendMessage}
      >
        Send
      </button>

      <div className="mt-6">
        <h2 className="text-xl font-semibold mb-2">GPT-5 Case Analysis</h2>
        <pre className="bg-gray-100 p-4 rounded overflow-x-auto">
          {decision ? JSON.stringify(decision, null, 2) : "No analysis yet."}
        </pre>
      </div>
    </div>
  );
}
