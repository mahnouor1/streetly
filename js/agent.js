export class Agent {
  constructor() {
    this.apiUrl = "https://streetly.vercel.app/api/gemini";
  }

  async getAgentResponse(message, city) {
    try {
      console.log("🤖 Sending message to Gemini API:", message);
      
      const response = await fetch(this.apiUrl, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          message: message,
          city: city
        })
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      
      if (data.success) {
        console.log("✅ Gemini response received");
        return data.reply;
      } else {
        throw new Error(data.message || "Invalid response from Gemini API");
      }
    } catch (error) {
      console.error("❌ Error getting response from Gemini:", error);
      
      // Enhanced fallback responses for common questions
      const lowerMessage = message.toLowerCase();
      
      if (lowerMessage.includes("flood") || lowerMessage.includes("flooding")) {
        return "🌊 Regarding flood conditions in Northern Pakistan: I recommend checking with local authorities and weather services for real-time updates. Generally, avoid traveling during heavy rainfall periods and stay informed about weather conditions. The region can experience flash floods, especially in valleys and near rivers.";
      }
      
      if (lowerMessage.includes("weather") || lowerMessage.includes("temperature")) {
        return "🌤️ For current weather in Northern Pakistan, I suggest checking local weather services. The region experiences cold winters with temperatures often below freezing, especially in higher altitudes like Hunza and Skardu.";
      }
      
      if (lowerMessage.includes("route") || lowerMessage.includes("road") || lowerMessage.includes("travel")) {
        return "🛣️ For travel routes in Northern Pakistan: The Karakoram Highway is the main route. Always check road conditions, especially during winter months. Some mountain passes may be closed due to weather.";
      }
      
      if (lowerMessage.includes("hotel") || lowerMessage.includes("accommodation") || lowerMessage.includes("stay")) {
        return "🏨 For accommodations in Northern Pakistan: I recommend booking in advance, especially during peak season (May-October). Popular areas include Hunza Valley, Skardu, and Swat Valley with various options from guesthouses to hotels.";
      }
      
      return "Hi! I'm Streetly, your AI travel assistant for Pakistan. I'm here to help you plan your trip to Northern Pakistan destinations like Hunza Valley, Skardu, Naran, Swat, Chitral, Fairy Meadows, and Neelum Valley. How can I assist you today? 🌄";
    }
  }
}
