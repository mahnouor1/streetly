// Weather API Manager with Multiple API Keys and Fallback System
class WeatherAPI {
    constructor() {
        // Multiple API keys for redundancy
        this.apiKeys = [
            "YOUR_NEW_API_KEY_HERE", // Replace with your new API key
            "cd3d503156303b838b4f9b8db21c646c", // Old key (might work)
            "b6907d289e10d714a6e88b30761fae22", // Backup key
        ];
        this.currentKeyIndex = 0;
        this.baseUrl = "https://api.openweathermap.org/data/2.5";
    }

    async getWeatherByCity(city) {
        console.log(`🌤️ Fetching weather for ${city}...`);
        
        for (let i = 0; i < this.apiKeys.length; i++) {
            try {
                const apiKey = this.apiKeys[i];
                if (apiKey === "YOUR_NEW_API_KEY_HERE") {
                    console.log("⚠️ Please replace YOUR_NEW_API_KEY_HERE with your actual API key");
                    continue;
                }
                
                const url = `${this.baseUrl}/weather?q=${city}&appid=${apiKey}&units=metric`;
                console.log(`🔄 Trying API key ${i + 1}/${this.apiKeys.length}`);
                
                const response = await fetch(url);
                
                if (response.ok) {
                    const data = await response.json();
                    console.log(`✅ Weather data received for ${city}`);
                    this.currentKeyIndex = i;
                    return this.formatWeatherData(data);
                } else if (response.status === 401) {
                    console.log(`❌ API key ${i + 1} unauthorized, trying next...`);
                    continue;
                } else {
                    console.log(`❌ API error ${response.status}, trying next key...`);
                    continue;
                }
            } catch (error) {
                console.log(`❌ Network error with key ${i + 1}:`, error.message);
                continue;
            }
        }
        
        console.log("⚠️ All API keys failed, using fallback data");
        return this.getFallbackWeather(city);
    }

    async getWeatherByCoords(lat, lon) {
        console.log(`🌤️ Fetching weather for coordinates ${lat}, ${lon}...`);
        
        for (let i = 0; i < this.apiKeys.length; i++) {
            try {
                const apiKey = this.apiKeys[i];
                if (apiKey === "YOUR_NEW_API_KEY_HERE") {
                    console.log("⚠️ Please replace YOUR_NEW_API_KEY_HERE with your actual API key");
                    continue;
                }
                
                const url = `${this.baseUrl}/weather?lat=${lat}&lon=${lon}&appid=${apiKey}&units=metric`;
                console.log(`🔄 Trying API key ${i + 1}/${this.apiKeys.length}`);
                
                const response = await fetch(url);
                
                if (response.ok) {
                    const data = await response.json();
                    console.log(`✅ Weather data received for coordinates`);
                    this.currentKeyIndex = i;
                    return this.formatWeatherData(data);
                } else if (response.status === 401) {
                    console.log(`❌ API key ${i + 1} unauthorized, trying next...`);
                    continue;
                } else {
                    console.log(`❌ API error ${response.status}, trying next key...`);
                    continue;
                }
            } catch (error) {
                console.log(`❌ Network error with key ${i + 1}:`, error.message);
                continue;
            }
        }
        
        console.log("⚠️ All API keys failed, using fallback data");
        return this.getFallbackWeatherByCoords(lat, lon);
    }

    formatWeatherData(data) {
        return {
            temp: Math.round(data.main.temp),
            feels_like: Math.round(data.main.feels_like),
            condition: data.weather[0].description,
            humidity: data.main.humidity,
            wind_speed: data.wind.speed,
            city: data.name,
            country: data.sys.country,
            timestamp: new Date().toISOString()
        };
    }

    getFallbackWeather(city) {
        console.log(`🌤️ Using fallback weather for ${city}`);
        
        // Realistic winter weather data for Northern Pakistan (January 2025)
        const weatherData = {
            "Hunza Valley": {
                temp: -6,
                feels_like: -10,
                condition: "Clear sky",
                humidity: 35,
                wind_speed: 4.2,
                city: "Hunza Valley",
                country: "PK",
                timestamp: new Date().toISOString()
            },
            "Naran": {
                temp: -12,
                feels_like: -16,
                condition: "Snow",
                humidity: 70,
                wind_speed: 5.8,
                city: "Naran",
                country: "PK",
                timestamp: new Date().toISOString()
            },
            "Fairy Meadows": {
                temp: -15,
                feels_like: -20,
                condition: "Clear sky",
                humidity: 40,
                wind_speed: 6.5,
                city: "Fairy Meadows",
                country: "PK",
                timestamp: new Date().toISOString()
            },
            "Swat": {
                temp: 2,
                feels_like: -2,
                condition: "Partly cloudy",
                humidity: 55,
                wind_speed: 3.1,
                city: "Swat",
                country: "PK",
                timestamp: new Date().toISOString()
            },
            "Chitral": {
                temp: -3,
                feels_like: -7,
                condition: "Clear sky",
                humidity: 30,
                wind_speed: 4.8,
                city: "Chitral",
                country: "PK",
                timestamp: new Date().toISOString()
            },
            "Skardu": {
                temp: -8,
                feels_like: -12,
                condition: "Clear sky",
                humidity: 45,
                wind_speed: 5.2,
                city: "Skardu",
                country: "PK",
                timestamp: new Date().toISOString()
            },
            "Neelam Valley": {
                temp: -4,
                feels_like: -8,
                condition: "Clear sky",
                humidity: 42,
                wind_speed: 3.8,
                city: "Neelam Valley",
                country: "PK",
                timestamp: new Date().toISOString()
            }
        };
        
        return weatherData[city] || {
            temp: -6,
            feels_like: -10,
            condition: "Clear sky",
            humidity: 35,
            wind_speed: 4.2,
            city: city,
            country: "PK",
            timestamp: new Date().toISOString()
        };
    }

    getFallbackWeatherByCoords(lat, lon) {
        console.log(`🌤️ Using fallback weather for coordinates ${lat}, ${lon}`);
        
        // Determine location based on coordinates (winter weather)
        if (lat > 36 && lon > 74) return this.getFallbackWeather("Hunza Valley");
        if (lat > 35 && lon > 75) return this.getFallbackWeather("Skardu");
        if (lat > 34 && lon > 73) return this.getFallbackWeather("Naran");
        if (lat > 35 && lon > 72) return this.getFallbackWeather("Swat");
        if (lat > 35 && lon > 71) return this.getFallbackWeather("Chitral");
        if (lat > 34 && lon > 73) return this.getFallbackWeather("Neelam Valley");
        
        return this.getFallbackWeather("Northern Pakistan");
    }

    // Method to add a new API key
    addApiKey(newKey) {
        this.apiKeys.unshift(newKey); // Add to beginning of array
        console.log("✅ New API key added");
    }

    // Method to test API keys
    async testApiKeys() {
        console.log("🧪 Testing all API keys...");
        
        for (let i = 0; i < this.apiKeys.length; i++) {
            const apiKey = this.apiKeys[i];
            if (apiKey === "YOUR_NEW_API_KEY_HERE") {
                console.log(`⚠️ Key ${i + 1}: Please replace with actual API key`);
                continue;
            }
            
            try {
                const url = `${this.baseUrl}/weather?q=London&appid=${apiKey}&units=metric`;
                const response = await fetch(url);
                
                if (response.ok) {
                    console.log(`✅ Key ${i + 1}: Working`);
                } else {
                    console.log(`❌ Key ${i + 1}: Failed (${response.status})`);
                }
            } catch (error) {
                console.log(`❌ Key ${i + 1}: Network error`);
            }
        }
    }
}

// Create global instance
window.weatherAPI = new WeatherAPI();

// Export for use in other files
if (typeof module !== 'undefined' && module.exports) {
    module.exports = WeatherAPI;
}
