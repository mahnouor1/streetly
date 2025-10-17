import { APIManager } from "./api.js";
import { ChatManager } from "./chat.js";
import { mockEvents, trendingNow } from "./events.js";

class App {
  constructor() {
    this.currentCity = null;
    this.apiManager = new APIManager();
    this.chatManager = new ChatManager(this.apiManager, this);
    this.map = null;
    this.marker = null;
    this.timeUpdateInterval = null;

    document.addEventListener("DOMContentLoaded", () => {
      this.initMap();
      this.setupEventListeners();
      this.showScreen("citySelection");
    });
  }

  initMap() {
    if (window.L) {
      this.map = L.map("map").setView([33.6844, 73.0479], 5);
      L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
        attribution:
          '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
      }).addTo(this.map);
    } else {
      console.error("Leaflet is not loaded.");
    }
  }

  setupEventListeners() {
    document.querySelectorAll(".popular-city").forEach((btn) => {
      btn.addEventListener("click", () => this.selectCity(btn.dataset.city));
    });
    document
      .getElementById("changeCityBtn")
      .addEventListener("click", () => this.showScreen("citySelection"));

    document.querySelectorAll(".nav-btn").forEach((btn) => {
      btn.addEventListener("click", () => {
        if (this.currentCity) {
          this.showScreen(btn.dataset.view);
        }
      });
    });
  }

  selectCity(city) {
    this.currentCity = city;
    this.updateCityUI();
    this.chatManager.clearMessages();
    this.chatManager.sendWelcomeMessage(city);
    this.loadEvents();
    this.showScreen("chat");
  }

  showScreen(screenName) {
    document
      .querySelectorAll(".screen")
      .forEach((screen) => screen.classList.add("hidden"));

    const activeScreen =
      document.getElementById(`${screenName}Interface`) ||
      document.getElementById(`${screenName}Screen`);
    if (activeScreen) {
      activeScreen.classList.remove("hidden");
    } else {
      document.getElementById("chatInterface").classList.remove("hidden");
    }

    document.querySelectorAll(".nav-btn").forEach((btn) => {
      btn.classList.remove("text-primary", "font-bold");
      if (btn.dataset.view === screenName) {
        btn.classList.add("text-primary", "font-bold");
      }
    });

    if (screenName === "explore" && this.map) {
      setTimeout(() => this.map.invalidateSize(), 10);
    }
  }

  getCurrentCity() {
    return this.currentCity;
  }

  updateLocalTime(timeZone) {
    if (this.timeUpdateInterval) {
      clearInterval(this.timeUpdateInterval);
    }

    const localTimeElement = document.getElementById("localTime");

    if (!timeZone) {
      localTimeElement.textContent = "--:-- --";
      return;
    }

    this.timeUpdateInterval = setInterval(() => {
      try {
        const date = new Date();
        const timeString = date.toLocaleTimeString("en-US", {
          timeZone: timeZone,
          hour: "numeric",
          minute: "2-digit",
          hour12: true,
        });
        localTimeElement.textContent = timeString;
      } catch (e) {
        console.error("Invalid time zone:", timeZone);
        localTimeElement.textContent = "Invalid Timezone";
        clearInterval(this.timeUpdateInterval);
      }
    }, 1000);
  }

  async updateCityUI() {
    document.getElementById("currentCity").textContent = this.currentCity;
    // This line updates the new title in the map section
    document.getElementById(
      "mapCityTitle"
    ).textContent = `Exploring ${this.currentCity}`;

    const cityData = this.apiManager.cityCoordinates[this.currentCity];

    this.updateLocalTime(cityData ? cityData.timeZone : null);

    const weather = await this.apiManager.getWeather(this.currentCity);
    document.getElementById(
      "weather-temp"
    ).textContent = `${weather.temperature}°C`;
    document.getElementById("weather-condition").textContent =
      weather.condition;

    const cityInfo = this.apiManager.getCityInfo(this.currentCity);
    document.getElementById("population").textContent = cityInfo.population;
    document.getElementById("language").textContent = cityInfo.language;

    if (this.map && cityData) {
      const coords = [cityData.lat, cityData.lon];
      this.map.setView(coords, 10);
      if (!this.marker) {
        this.marker = L.marker(coords).addTo(this.map);
      } else {
        this.marker.setLatLng(coords);
      }
    }

    const trending = trendingNow[this.currentCity] || [];
    const trendingContainer = document.getElementById("trendingNowContainer");
    trendingContainer.innerHTML = trending
      .map((item) => `<div class="text-sm text-gray-600">${item}</div>`)
      .join("");
  }

  loadEvents() {
    const events = mockEvents[this.currentCity] || [];
    const eventsList = document.getElementById("eventsList");
    if (events.length === 0) {
      eventsList.innerHTML =
        '<p class="text-gray-500">No events found for this city.</p>';
      return;
    }
    eventsList.innerHTML = events
      .map(
        (event) => `
      <div class="bg-white rounded-lg shadow-sm border p-4">
        <img src="${event.image}" alt="${event.name}" class="w-full h-32 object-cover rounded-md mb-4">
        <h3 class="font-bold text-lg">${event.name}</h3>
        <p class="text-sm text-gray-500">${event.date} - ${event.location}</p>
        <p class="text-sm mt-2">${event.description}</p>
      </div>
    `
      )
      .join("");
  }
}

new App();
