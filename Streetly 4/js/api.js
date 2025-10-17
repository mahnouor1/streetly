import { Agent } from "./agent.js";

export class APIManager {
  constructor() {
    this.agent = new Agent();

    this.cityCoordinates = {
      "Hunza Valley": { lat: 36.3167, lon: 74.65, timeZone: "Asia/Karachi" },
      Skardu: { lat: 35.2979, lon: 75.6333, timeZone: "Asia/Karachi" },
      Naran: { lat: 34.91, lon: 73.6522, timeZone: "Asia/Karachi" },
      Chitral: { lat: 35.8511, lon: 71.7889, timeZone: "Asia/Karachi" },
      "Swat Valley": { lat: 35.2228, lon: 72.4258, timeZone: "Asia/Karachi" },
      "Neelum Valley": { lat: 34.5869, lon: 73.9014, timeZone: "Asia/Karachi" },
      "Fairy Meadows": { lat: 35.4214, lon: 74.5958, timeZone: "Asia/Karachi" },
    };
  }

  getChatResponse(message, city) {
    return this.agent.getAgentResponse(message, city);
  }

  async getWeather(city) {
    // Provides a stable, static weather result to ensure the UI always works.
    return { temperature: "22", condition: "Sunny" };
  }

  getCityInfo(city) {
    const cityInfo = {
      "Hunza Valley": { population: "100,000", language: "Burushaski" },
      Skardu: { population: "200,000", language: "Balti" },
      Naran: { population: "50,000", language: "Hindko" },
      Chitral: { population: "40,000", language: "Khowar" },
      "Swat Valley": { population: "2.3M", language: "Pashto" },
      "Neelum Valley": { population: "191,000", language: "Kashmiri" },
      "Fairy Meadows": { population: "1,000", language: "Shina" },
    };
    return cityInfo[city] || { population: "---", language: "---" };
  }
}
