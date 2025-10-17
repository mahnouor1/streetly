let map;
let directionsService;
let directionsRenderer;

function initMap() {
  directionsService = new google.maps.DirectionsService();
  directionsRenderer = new google.maps.DirectionsRenderer();
  map = new google.maps.Map(document.getElementById("map"), {
    center: { lat: -34.397, lng: 150.644 },
    zoom: 8,
  });
  directionsRenderer.setMap(map);

  document.getElementById("search-button").addEventListener("click", () => {
    calculateAndDisplayRoute();
  });
}

function calculateAndDisplayRoute() {
  const destination = document.getElementById("destination-input").value;
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(
      (position) => {
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
          if (status == "OK") {
            directionsRenderer.setDirections(result);
          }
        });
      },
      () => {
        // Handle geolocation error
      }
    );
  } else {
    // Handle browsers that don't support geolocation
  }
}
