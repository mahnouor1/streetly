import os, requests
OPEN_KEY = os.environ.get("OPENWEATHER_API_KEY", "cd3d503156309b838b4f9b8db21c646c")

# Fallback weather data for testing when API key is not available
FALLBACK_WEATHER = {
    "hunza valley": {"temp": 12, "condition": "Clear Sky", "humidity": 45},
    "hunza": {"temp": 12, "condition": "Clear Sky", "humidity": 45},
    "naran": {"temp": 8, "condition": "Partly Cloudy", "humidity": 60},
    "fairy meadows": {"temp": 5, "condition": "Clear Sky", "humidity": 40},
    "swat": {"temp": 18, "condition": "Sunny", "humidity": 55},
    "chitral": {"temp": 15, "condition": "Clear Sky", "humidity": 50},
    "skardu": {"temp": 10, "condition": "Partly Cloudy", "humidity": 45},
    "neelam valley": {"temp": 16, "condition": "Sunny", "humidity": 60},
    "neelam": {"temp": 16, "condition": "Sunny", "humidity": 60},
    "gilgit": {"temp": 12, "condition": "Clear Sky", "humidity": 45},
    "muzaffarabad": {"temp": 16, "condition": "Sunny", "humidity": 60},
    "mingora": {"temp": 18, "condition": "Sunny", "humidity": 55}
}

# Precise coordinates for northern Pakistan destinations
DESTINATION_COORDINATES = {
    "hunza valley": {"lat": 36.3167, "lon": 74.6500, "name": "Hunza Valley"},
    "hunza": {"lat": 36.3167, "lon": 74.6500, "name": "Hunza Valley"},
    "naran": {"lat": 34.9069, "lon": 73.6556, "name": "Naran"},
    "fairy meadows": {"lat": 35.4167, "lon": 74.5833, "name": "Fairy Meadows"},
    "swat": {"lat": 34.7717, "lon": 72.3600, "name": "Swat"},
    "chitral": {"lat": 35.8511, "lon": 71.7864, "name": "Chitral"},
    "skardu": {"lat": 35.2976, "lon": 75.6337, "name": "Skardu"},
    "neelam valley": {"lat": 34.6281, "lon": 73.9110, "name": "Neelam Valley"},
    "neelam": {"lat": 34.6281, "lon": 73.9110, "name": "Neelam Valley"},
    "gilgit": {"lat": 35.9211, "lon": 74.3081, "name": "Gilgit"},
    "muzaffarabad": {"lat": 34.3700, "lon": 73.4711, "name": "Muzaffarabad"},
    "mingora": {"lat": 34.7795, "lon": 72.3607, "name": "Mingora"}
}

def get_weather_by_city(city):
    # Clean and normalize city name
    city_clean = city.lower().strip()
    
    # Check if we have coordinates for this destination
    coords = DESTINATION_COORDINATES.get(city_clean)
    
    if coords:
        # Use precise coordinates for real-time weather
        try:
            url = f"https://api.openweathermap.org/data/2.5/weather?lat={coords['lat']}&lon={coords['lon']}&units=metric&appid={OPEN_KEY}"
            r = requests.get(url, timeout=10).json()
            
            if r.get("cod") == 200:
                return {
                    "city": coords["name"],
                    "temp": round(r["main"]["temp"]),
                    "condition": r["weather"][0]["description"].title(),
                    "humidity": r["main"]["humidity"],
                    "coord": r.get("coord"),
                    "feels_like": round(r["main"]["feels_like"]),
                    "wind_speed": r["wind"]["speed"],
                    "note": "Real-time weather data"
                }
            else:
                # Fallback to sample data if API fails
                fallback_data = FALLBACK_WEATHER.get(city_clean)
                if fallback_data:
                    return {
                        "city": coords["name"],
                        "temp": fallback_data["temp"],
                        "condition": fallback_data["condition"],
                        "humidity": fallback_data["humidity"],
                        "note": "API unavailable - using sample data"
                    }
        
        except Exception as e:
            # Fallback to sample data on any error
            fallback_data = FALLBACK_WEATHER.get(city_clean)
            if fallback_data:
                return {
                    "city": coords["name"],
                    "temp": fallback_data["temp"],
                    "condition": fallback_data["condition"],
                    "humidity": fallback_data["humidity"],
                    "note": "API error - using sample data"
                }
    
    # If no coordinates found, try city name search
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city},PK&units=metric&appid={OPEN_KEY}"
        r = requests.get(url, timeout=10).json()
        
        if r.get("cod") == 200:
            return {
                "city": r["name"],
                "temp": round(r["main"]["temp"]),
                "condition": r["weather"][0]["description"].title(),
                "humidity": r["main"]["humidity"],
                "coord": r.get("coord"),
                "feels_like": round(r["main"]["feels_like"]),
                "wind_speed": r["wind"]["speed"],
                "note": "Real-time weather data"
            }
    
    except Exception as e:
        pass
    
    # Final fallback to sample data
    fallback_data = FALLBACK_WEATHER.get(city_clean)
    if fallback_data:
        return {
            "city": city.title(),
            "temp": fallback_data["temp"],
            "condition": fallback_data["condition"],
            "humidity": fallback_data["humidity"],
            "note": "Using sample data"
        }
    else:
        return {
            "city": city.title(),
            "temp": 15,
            "condition": "Clear Sky",
            "humidity": 50,
            "note": "Using sample data"
        }

def get_forecast_by_city(city):
    url = f"https://api.openweathermap.org/data/2.5/forecast?q={city},PK&units=metric&appid={OPEN_KEY}"
    r = requests.get(url).json()
    if r.get("cod")!="200":
        return {"error": r.get("message")}
    out=[]
    for item in r["list"][:12]:
        out.append({
            "datetime": item["dt_txt"],
            "temp": item["main"]["temp"],
            "weather": item["weather"][0]["description"]
        })
    return out
