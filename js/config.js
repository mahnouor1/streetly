// js/config.js
const CONFIG = {
    // Use external APIs directly instead of localhost backend
    // TODO: Replace with your new OpenWeather API key from https://openweathermap.org/api
    OPENWEATHER_API_KEY: "YOUR_NEW_API_KEY_HERE", // Replace with your new API key
    OPENWEATHER_BASE_URL: "https://api.openweathermap.org/data/2.5",
    // Fallback to localhost only for development
    API_BASE_URL: window.location.hostname === 'localhost' ? "http://localhost:8080" : null,
  };
  