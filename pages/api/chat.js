import OpenAI from "openai";

const client = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });

export default async function handler(req, res) {
  const { conversation } = req.body;

  // --- GPT-4o-Realtime-Review ---
  const nursePrompt = `
You are a triage nurse for a Singapore GP practice who will ask specific questions to a patient prior to teleconsultation.
Respond in same language as patient (English, Singlish, Bengali, Malay, Mandarin, Tamil).
Follow the structured pre-consult flow.
Return only text reply for patient.
`;

  const nurseResponse = await client.chat.completions.create({
    model: "gpt-4o-realtime-review",
    messages: [
      { role: "system", content: nursePrompt },
      ...conversation
    ]
  });

  const nurseReply = nurseResponse.choices[0].message.content;

  // Append nurse reply to conversation before feeding to GPT-5
  const updatedConversation = [...conversation, { role: "assistant", content: nurseReply }];

  // --- GPT-5 Decision Step ---
  const gpt5Prompt = `
You are a clinical triage decision agent.
Task:
1. If patient symptoms are common and no red flags, generate SOAP.
2. If emergency (bleeding, chest pain, etc.), output "Emergency Case".
3. If complex/out-of-scope, output "No SOAP".

Output JSON only:
{
  "outcome": "SOAP" | "Emergency Case" | "No SOAP",
  "note": "Optional note",
  "soap": { "S": "", "O": "", "A": "", "P": "" } | null
}
Latest conversation:
${updatedConversation.map(m => `${m.role}: ${m.content}`).join("\n")}
`;

  const decisionResponse = await client.chat.completions.create({
    model: "gpt-5",
    messages: [{ role: "system", content: gpt5Prompt }]
  });

  let gpt5_decision;
  try {
    gpt5_decision = JSON.parse(decisionResponse.choices[0].message.content);
  } catch {
    gpt5_decision = { error: "Invalid JSON returned", raw: decisionResponse.choices[0].message.content };
  }

  res.status(200).json({ nurse_reply: nurseReply, gpt5_decision });
}
