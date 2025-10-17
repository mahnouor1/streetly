export class Agent {
  constructor() {
    // IMPORTANT: PASTE YOUR GOOGLE AI API KEY HERE
    const API_KEY = "YOUR_GOOGLE_AI_API_KEY_HERE";

    if (API_KEY === "YOUR_GOOGLE_AI_API_KEY_HERE") {
      console.warn(
        "Please replace 'YOUR_GOOGLE_AI_API_KEY_HERE' with your actual Google AI API key in the script."
      );
    }
    try {
      if (window.google && window.google.generativeai) {
        this.genAI = new window.google.generativeai.GoogleGenerativeAI(API_KEY);
        this.model = this.genAI.getGenerativeModel({ model: "gemini-pro" });
      } else {
        console.error("Google AI SDK not loaded.");
      }
    } catch (error) {
      console.error("Error initializing GoogleGenerativeAI:", error);
    }
  }

  async getAgentResponse(message, city) {
    if (!this.model) {
      return "The AI model is not available. Please check the API key and configuration.";
    }
    const prompt = `You are an expert local guide for ${city}. Provide helpful, concise, and friendly information to tourists. User's question: \"${message}\"`;
    try {
      const result = await this.model.generateContent(prompt);
      const response = await result.response;
      return response.text();
    } catch (error) {
      console.error("Error getting response from Gemini:", error);
      return "Sorry, I'm having trouble connecting to my knowledge base right now.";
    }
  }
}
