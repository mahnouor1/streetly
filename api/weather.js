import fetch from "node-fetch";

export default async function handler(req, res) {
  res.setHeader("Access-Control-Allow-Origin", "*");
  res.setHeader("Access-Control-Allow-Methods", "GET, OPTIONS");
  res.setHeader("Access-Control-Allow-Headers", "Content-Type");

  if (req.method === "OPTIONS") return res.status(200).end();

  const locations = [
    { name: "Hunza Valley", lat: 36.3167, lon: 74.6500 },
    { name: "Naran", lat: 34.9100, lon: 73.6522 },
    { name: "Fairy Meadows", lat: 35.4000, lon: 74.5833 },
    { name: "Swat", lat: 35.2220, lon: 72.4258 },
    { name: "Chitral", lat: 35.8511, lon: 71.7864 },
    { name: "Skardu", lat: 35.2979, lon: 75.6333 },
    { name: "Neelum Valley", lat: 34.6069, lon: 73.9214 },
  ];

  const apiKey = "cd3d503156309b838b4f9b8db21c646c";

  try {
    const results = await Promise.all(
      locations.map(async (loc) => {
        const url = `https://api.openweathermap.org/data/2.5/weather?lat=${loc.lat}&lon=${loc.lon}&units=metric&appid=${apiKey}`;
        const r = await fetch(url);
        const data = await r.json();

        if (data.cod !== 200) {
          console.warn(`⚠️ Skipping ${loc.name}: ${data.message}`);
          return { location: loc.name, error: data.message };
        }

        return {
          location: loc.name,
          temperature: data.main.temp,
          condition: data.weather[0].main,
          humidity: data.main.humidity,
          wind_speed: data.wind.speed,
          icon: data.weather[0].icon,
        };
      })
    );

    res.status(200).json({ success: true, data: results });
  } catch (err) {
    console.error("🌩 Weather API Error:", err);
    res.status(500).json({ success: false, message: err.message });
  }
}
