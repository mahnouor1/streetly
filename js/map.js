// js/map.js
let map;
let directionsService;
let directionsRenderer;

// Initialize the map
function initMap() {
  directionsService = new google.maps.DirectionsService();
  directionsRenderer = new google.maps.DirectionsRenderer();
  map = new google.maps.Map(document.getElementById("map"), {
    center: { lat: 33.6844, lng: 73.0479 }, // Centered on Islamabad
    zoom: 8,
  });
  directionsRenderer.setMap(map);

  // Event listener for the search button
  document.getElementById("search-button").addEventListener("click", () => {
    calculateAndDisplayRoute();
  });

  // Click on map to show weather popup
  map.addListener("click", async (e) => {
    const lat = e.latLng.lat();
    const lon = e.latLng.lng();
    const weather = await getWeatherByCoords(lat, lon);

    new google.maps.InfoWindow({
      content: `<b>${weather.city}</b><br>${weather.temp}°C, ${weather.condition}`,
      position: e.latLng,
    }).open(map);
  });
}

// Fetch weather by city name
async function getWeather(city) {
  try {
    // Use OpenWeather API directly
    const res = await fetch(`${CONFIG.OPENWEATHER_BASE_URL}/weather?q=${city}&appid=${CONFIG.OPENWEATHER_API_KEY}&units=metric`);
    const data = await res.json();
    
    if (data.cod === 200) {
      const weatherData = {
        city: data.name,
        temp: Math.round(data.main.temp),
        condition: data.weather[0].description
      };
      console.log("Weather data:", weatherData);
      alert(`🌤 Weather in ${city}: ${weatherData.temp}°C, ${weatherData.condition}`);
      return weatherData;
    } else {
      throw new Error(data.message || "Weather data not found");
    }
  } catch (err) {
    console.error("Weather fetch failed, using fallback:", err);
    // Use fallback weather data
    const fallbackWeather = getFallbackWeather(city);
    alert(`🌤 Weather in ${city}: ${fallbackWeather.temp}°C, ${fallbackWeather.condition}`);
    return fallbackWeather;
  }
}

function getFallbackWeather(city) {
  const weatherData = {
    "Hunza Valley": { temp: 15, condition: "Clear sky" },
    "Naran": { temp: 8, condition: "Partly cloudy" },
    "Fairy Meadows": { temp: 5, condition: "Clear sky" },
    "Swat": { temp: 22, condition: "Sunny" },
    "Chitral": { temp: 18, condition: "Clear sky" },
    "Skardu": { temp: 12, condition: "Partly cloudy" },
    "Neelam Valley": { temp: 16, condition: "Clear sky" }
  };
  
  return weatherData[city] || { temp: 15, condition: "Clear sky" };
}

// Fetch weather by coordinates
async function getWeatherByCoords(lat, lon) {
  try {
    // Use OpenWeather API directly
    const res = await fetch(`${CONFIG.OPENWEATHER_BASE_URL}/weather?lat=${lat}&lon=${lon}&appid=${CONFIG.OPENWEATHER_API_KEY}&units=metric`);
    const data = await res.json();
    
    if (data.cod === 200) {
      return {
        city: data.name,
        temp: Math.round(data.main.temp),
        condition: data.weather[0].description
      };
    } else {
      throw new Error(data.message || "Weather data not found");
    }
  } catch (err) {
    console.error("Weather fetch failed, using fallback:", err);
    // Use fallback weather data based on coordinates
    return getFallbackWeatherByCoords(lat, lon);
  }
}

function getFallbackWeatherByCoords(lat, lon) {
  // Determine location based on coordinates
  if (lat > 36 && lon > 74) return { city: "Hunza Valley", temp: 15, condition: "Clear sky" };
  if (lat > 35 && lon > 75) return { city: "Skardu", temp: 12, condition: "Partly cloudy" };
  if (lat > 34 && lon > 73) return { city: "Naran", temp: 8, condition: "Partly cloudy" };
  if (lat > 35 && lon > 72) return { city: "Swat", temp: 22, condition: "Sunny" };
  if (lat > 35 && lon > 71) return { city: "Chitral", temp: 18, condition: "Clear sky" };
  if (lat > 34 && lon > 73) return { city: "Neelam Valley", temp: 16, condition: "Clear sky" };
  
  return { city: "Northern Pakistan", temp: 15, condition: "Clear sky" };
}

// Calculate and display route using user’s current location
function calculateAndDisplayRoute() {
  const destination = document.getElementById("destination-input").value.trim();
  if (!destination) {
    alert("Please enter a destination.");
    return;
  }

  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(
      async (position) => {
        const origin = {
          lat: position.coords.latitude,
          lng: position.coords.longitude,
        };

        const request = {
          origin: origin,
          destination: destination,
          travelMode: "DRIVING",
        };

        directionsService.route(request, (result, status) => {
          if (status === "OK") {
            directionsRenderer.setDirections(result);

            const leg = result.routes[0].legs[0];
            const distance = leg.distance.text;
            const duration = leg.duration.text;

            const infoWindow = new google.maps.InfoWindow({
              content: `
                <b>🚗 Route Found!</b><br>
                From: ${leg.start_address}<br>
                To: ${leg.end_address}<br>
                Distance: ${distance}<br>
                Duration: ${duration}
              `,
              position: leg.end_location,
            });
            infoWindow.open(map);
          } else {
            alert("Could not find a route. Try again.");
          }
        });
      },
      () => alert("Geolocation permission denied.")
    );
  } else {
    alert("Your browser doesn’t support location access.");
  }
}
