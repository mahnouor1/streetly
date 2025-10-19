import fetch from "node-fetch";

export default async function handler(req, res) {
  res.setHeader("Access-Control-Allow-Origin", "*");
  res.setHeader("Access-Control-Allow-Methods", "POST, OPTIONS");
  res.setHeader("Access-Control-Allow-Headers", "Content-Type");

  if (req.method === "OPTIONS") return res.status(200).end();

  if (req.method !== "POST") {
    return res.status(405).json({ success: false, message: "Method not allowed" });
  }

  try {
    const { message, city = "Pakistan" } = req.body;

    if (!message) {
      return res.status(400).json({ success: false, message: "Message is required" });
    }

    // Use Google AI API directly
    const API_KEY = "AIzaSyBvQZJ8K9L2M3N4O5P6Q7R8S9T0U1V2W3X4Y5Z6"; // Replace with your actual API key
    
    const prompt = `You are Streetly, an expert AI travel assistant for Pakistan. You specialize in Northern Pakistan destinations like Hunza Valley, Skardu, Naran, Swat, Chitral, Fairy Meadows, and Neelum Valley.

User's question: "${message}"
Current context: ${city}

Provide helpful, accurate, and friendly travel information. Include practical tips, safety advice, and local insights. Keep responses concise but informative.

If asked about weather, floods, or natural disasters, provide current information and safety advice.
If asked about routes, provide practical travel guidance.
If asked about accommodations, suggest realistic options.
If asked about local culture, share authentic insights.

Respond in a conversational, helpful tone as a local travel expert.`;

    const response = await fetch(`https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key=${API_KEY}`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        contents: [{
          parts: [{
            text: prompt
          }]
        }]
      })
    });

    if (!response.ok) {
      throw new Error(`Gemini API error: ${response.status}`);
    }

    const data = await response.json();
    
    if (data.candidates && data.candidates[0] && data.candidates[0].content) {
      const reply = data.candidates[0].content.parts[0].text;
      return res.status(200).json({ 
        success: true, 
        reply: reply.trim() 
      });
    } else {
      throw new Error("Invalid response from Gemini API");
    }

  } catch (error) {
    console.error("Gemini API Error:", error);
    
    // Fallback response for common questions
    const fallbackResponses = {
      "flood": "I don't have real-time flood data, but I can help you with general safety advice for Northern Pakistan. Always check local weather conditions and avoid traveling during heavy rainfall periods.",
      "weather": "For current weather conditions, I recommend checking local weather services or contacting local authorities. I can provide general climate information for Northern Pakistan destinations.",
      "route": "I can help you plan routes between Northern Pakistan destinations. Popular routes include the Karakoram Highway and various mountain passes. Always check road conditions before traveling.",
      "hotel": "I can suggest accommodation options in Northern Pakistan. Popular areas include Hunza Valley, Skardu, and Swat Valley. Book in advance during peak season.",
      "default": "I'm here to help with your travel questions about Northern Pakistan! Ask me about destinations, routes, local culture, or travel tips."
    };

    const lowerMessage = message.toLowerCase();
    let fallbackReply = fallbackResponses.default;
    
    for (const [key, response] of Object.entries(fallbackResponses)) {
      if (lowerMessage.includes(key)) {
        fallbackReply = response;
        break;
      }
    }

    return res.status(200).json({ 
      success: true, 
      reply: fallbackReply,
      fallback: true 
    });
  }
}
