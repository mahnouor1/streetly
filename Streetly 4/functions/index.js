const functions = require("firebase-functions");
const admin = require("firebase-admin");
const fetch = require("node-fetch");
const cors = require("cors")({ origin: true });

admin.initializeApp();

exports.getFloodData = functions.https.onRequest((req, res) => {
  cors(req, res, async () => {
    const { lat, lon } = req.query;

    if (!lat || !lon) {
      res.status(400).send("Latitude and Longitude are required.");
      return;
    }

    const apiUrl = `https://api.open-meteo.com/v1/forecast?latitude=${lat}&longitude=${lon}&daily=river_discharge&forecast_days=1`;

    try {
      const apiResponse = await fetch(apiUrl);
      if (!apiResponse.ok) {
        res.status(apiResponse.status).send("Failed to fetch data from Open-Meteo.");
        return;
      }
      const data = await apiResponse.json();
      res.status(200).send(data);
    } catch (error) {
      console.error("Error fetching flood data:", error);
      res.status(500).send("Internal Server Error");
    }
  });
});
