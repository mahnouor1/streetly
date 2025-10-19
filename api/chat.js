import fetch from "node-fetch";

export default async function handler(req, res) {
  res.setHeader("Access-Control-Allow-Origin", "*");
  res.setHeader("Access-Control-Allow-Methods", "POST, OPTIONS");
  res.setHeader("Access-Control-Allow-Headers", "Content-Type");

  if (req.method === "OPTIONS") return res.status(200).end();
  if (req.method !== "POST") return res.status(405).json({ error: "Method not allowed" });

  try {
    const { message } = req.body;

    if (!message || message.trim() === "") {
      return res.status(400).json({ error: "Message required" });
    }

    // Enhanced rule-based chatbot for Northern Pakistan travel
    const responses = {
      "hello": "Hi! I'm Streetly, your AI travel assistant for Pakistan. How can I help you plan your trip today? 🌄",
      "best routes in skardu": "The best routes to Skardu include the Karakoram Highway (N-35) via Gilgit, or flights from Islamabad (weather permitting). 🚗✈️",
      "weather": "You can check live weather using our integrated weather dashboard on the map. 🌤️",
      "hotels": "Skardu offers great options like Shangrila Resort, Serena Shigar Fort, and local guest houses near Upper Kachura Lake. 🏨",
      "flood": "For flood conditions in Northern Pakistan, check with local authorities and weather services. Avoid traveling during heavy rainfall periods. 🌊",
      "hunza": "Hunza Valley is beautiful! Best time to visit is May-October. Don't miss Altit and Baltit forts, and the stunning Attabad Lake. 🏔️",
      "naran": "Naran offers amazing views of Nanga Parbat! Visit in summer (June-September) and check road conditions before traveling. ⛰️",
      "swat": "Swat Valley is known as the 'Switzerland of Pakistan'. Visit Malam Jabba for skiing and enjoy the beautiful valleys. 🎿",
      "chitral": "Chitral is rich in culture! Visit during summer months and explore the Kalash valleys for unique cultural experiences. 🏛️",
      "fairy meadows": "Fairy Meadows offers incredible views of Nanga Parbat! Best visited in summer with proper hiking gear. 🥾",
      "neelum valley": "Neelum Valley is stunning! Visit during summer months and enjoy the beautiful rivers and mountains. 🌊",
      "bye": "Safe travels! ✨ Don't forget to check weather and road conditions before you go!"
    };

    const lower = message.toLowerCase();
    let reply = "Hi! I'm Streetly, your AI travel assistant for Pakistan. I can help you with information about Northern Pakistan destinations like Hunza Valley, Skardu, Naran, Swat, Chitral, Fairy Meadows, and Neelum Valley. What would you like to know? 🌄";

    // Check for specific keywords and provide relevant responses
    for (const key in responses) {
      if (lower.includes(key)) {
        reply = responses[key];
        break;
      }
    }

    // Special handling for common questions
    if (lower.includes("best hotels") || lower.includes("accommodation")) {
      reply = "🏨 For accommodations in Northern Pakistan: I recommend booking in advance, especially during peak season (May-October). Popular areas include Hunza Valley, Skardu, and Swat Valley with various options from guesthouses to hotels.";
    } else if (lower.includes("weather") || lower.includes("temperature")) {
      reply = "🌤️ For current weather in Northern Pakistan, I suggest checking local weather services. The region experiences cold winters with temperatures often below freezing, especially in higher altitudes like Hunza and Skardu.";
    } else if (lower.includes("route") || lower.includes("road") || lower.includes("travel")) {
      reply = "🛣️ For travel routes in Northern Pakistan: The Karakoram Highway is the main route. Always check road conditions, especially during winter months. Some mountain passes may be closed due to weather.";
    } else if (lower.includes("flood") || lower.includes("flooding")) {
      reply = "🌊 Regarding flood conditions in Northern Pakistan: I recommend checking with local authorities and weather services for real-time updates. Generally, avoid traveling during heavy rainfall periods and stay informed about weather conditions.";
    }

    res.status(200).json({ success: true, reply });
  } catch (error) {
    console.error("Chat API Error:", error);
    res.status(500).json({ success: false, error: error.message });
  }
}
