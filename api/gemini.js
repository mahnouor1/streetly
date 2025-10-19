import fetch from "node-fetch";

export default async function handler(req, res) {
  res.setHeader("Access-Control-Allow-Origin", "*");
  res.setHeader("Access-Control-Allow-Methods", "POST, OPTIONS");
  res.setHeader("Access-Control-Allow-Headers", "Content-Type");

  if (req.method === "OPTIONS") return res.status(200).end();
  if (req.method !== "POST")
    return res.status(405).json({ error: "Method not allowed" });

  try {
    const { prompt } = req.body || {};
    if (!prompt) return res.status(400).json({ error: "Missing prompt" });

    const API_KEY = process.env.GOOGLE_API_KEY || process.env.GEMINI_API_KEY;
    if (!API_KEY)
      return res.status(500).json({
        error: "Missing Google API key. Set GOOGLE_API_KEY in Vercel env.",
      });

    const apiUrl =
      "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent";

    const response = await fetch(`${apiUrl}?key=${API_KEY}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        contents: [{ parts: [{ text: prompt }] }],
      }),
    });

    if (!response.ok) {
      const text = await response.text();
      console.error("Gemini API error:", text);
      return res
        .status(response.status)
        .json({ error: "Gemini API error", detail: text });
    }

    const data = await response.json();
    const reply =
      data?.candidates?.[0]?.content?.parts?.[0]?.text ||
      "Sorry, I couldn't generate a response right now.";

    return res.status(200).json({ success: true, reply });
  } catch (error) {
    console.error("Gemini handler error:", error);
    return res.status(500).json({ error: error.message });
  }
}