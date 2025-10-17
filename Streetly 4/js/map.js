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
    const res = await fetch(`${CONFIG.API_BASE_URL}/weather?city=${city}`);
    const data = await res.json();
    console.log("Weather data:", data);
    alert(`🌤 Weather in ${city}: ${data.temp}°C, ${data.condition}`);
    return data;
  } catch (err) {
    console.error("Weather fetch failed:", err);
    alert("❌ Failed to fetch weather data.");
  }
}

// Fetch weather by coordinates
async function getWeatherByCoords(lat, lon) {
  try {
    const res = await fetch(`${CONFIG.API_BASE_URL}/weather?lat=${lat}&lon=${lon}`);
    const data = await res.json();
    return data;
  } catch (err) {
    console.error("Weather fetch failed:", err);
    return { city: "Unknown", temp: "-", condition: "Error" };
  }
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
