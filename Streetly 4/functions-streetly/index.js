const functions = require("firebase-functions");
const axios = require("axios");
const cors = require("cors")({ origin: true });

// Your OpenWeatherMap API key is now securely stored in the backend.
const WEATHER_API_KEY = "47499319a9fe758ca1385b2dff731476";

exports.getWeather = functions.https.onRequest((req, res) => {
  cors(req, res, async () => {
    const lat = req.query.lat;
    const lon = req.query.lon;

    if (!lat || !lon) {
      return res
        .status(400)
        .send("Missing required query parameters: lat and lon");
    }

    const url = `https://api.openweathermap.org/data/2.5/onecall?lat=${lat}&lon=${lon}&exclude=minutely,hourly,alerts&appid=${WEATHER_API_KEY}&units=metric`;

    try {
      const response = await axios.get(url);
      res.status(200).send(response.data);
    } catch (error) {
      console.error("Error fetching weather data:", error.message);
      res.status(500).send("Failed to fetch weather data");
    }
  });
});

// You can add other cloud functions here if needed.
exports.getRecommendations = functions.https.onRequest((req, res) => {
  // This is your existing function, left as is.
  res.status(501).send("Not implemented");
});
