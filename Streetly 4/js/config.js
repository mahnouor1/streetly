// js/config.js
const CONFIG = {
    // Use external APIs directly instead of localhost backend
    OPENWEATHER_API_KEY: "cd3d503156303b838b4f9b8db21c646c", // Your OpenWeather API key
    OPENWEATHER_BASE_URL: "https://api.openweathermap.org/data/2.5",
    // Fallback to localhost only for development
    API_BASE_URL: window.location.hostname === 'localhost' ? "http://localhost:8080" : null,
  };
  