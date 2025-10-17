# disasters_api.py (enhanced)
import requests
import time
from flask import Flask, jsonify, request
from flask_cors import CORS
from math import radians, cos, sin, asin, sqrt
import traceback
from ml_disaster_predictor import get_all_predictions, get_high_risk_locations, predict_flood_risk, predict_earthquake_risk

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Sources
GDACS_URL = "https://www.gdacs.org/gdacsapi/api/events/geteventlist/EQ,FL,TC,VO,DR"
USGS_EQ_URL = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_day.geojson"  # last 24h quakes
OPENWEATHER_KEY = "cd3d503156309b838b4f9b8db21c646c"  # your key
OPENWEATHER_ONECALL = "https://api.openweathermap.org/data/2.5/onecall"

# Cache
_cache = {"timestamp": 0, "data": None, "ttl": 120}  # shorter TTL for faster updates (2 min), adjust as needed

# thresholds (tweakable)
MIN_EQ_MAG = 1.0     # show earthquakes magnitudes >= this (low to include small)
PREDICT_RAIN_MM = 10  # if forecasted precipitation in next 48h >= mm -> predicted flood
ALERT_RADIUS_DEFAULT_KM = 150

def haversine_km(lat1, lon1, lat2, lon2):
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1; dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)); return 6371 * c

def fetch_gdacs():
    try:
        r = requests.get(GDACS_URL, timeout=10); r.raise_for_status()
        data = r.json()
        features = data.get("features") or data.get("events") or []
    except Exception as e:
        print("GDACS fetch error:", e)
        return []
    out = []
    for f in features:
        try:
            props = f.get("properties", {}) if isinstance(f, dict) else {}
            geom = f.get("geometry", {}) or {}
            coords = geom.get("coordinates") or []
            if not coords or len(coords) < 2: continue
            lon, lat = coords[0], coords[1]
            out.append({
                "id": props.get("id") or props.get("eventid") or str(hash(str(f))),
                "source": "gdacs",
                "name": props.get("eventname") or props.get("title") or "Unknown",
                "type": props.get("eventtype") or "unknown",
                "lat": lat, "lon": lon,
                "severity": props.get("severity") or props.get("alertlevel") or None,
                "magnitude": props.get("magnitude") or None,
                "start": props.get("start") or None,
                "url": props.get("link") or None,
                "raw": props
            })
        except Exception:
            print("GDACS parse skip", traceback.format_exc())
    return out

def fetch_usgs_quakes():
    try:
        r = requests.get(USGS_EQ_URL, timeout=8); r.raise_for_status()
        data = r.json()
        features = data.get("features", []) or []
    except Exception as e:
        print("USGS fetch error:", e); return []
    out = []
    for f in features:
        try:
            props = f.get("properties", {})
            geom = f.get("geometry", {}) or {}
            coords = geom.get("coordinates") or []
            if not coords or len(coords) < 2: continue
            lon, lat = coords[0], coords[1]
            mag = props.get("mag", None)
            if mag is None: mag = 0.0
            # include even small quakes (>= MIN_EQ_MAG)
            if mag >= MIN_EQ_MAG:
                out.append({
                    "id": props.get("ids") or props.get("url") or str(hash(str(f))),
                    "source": "usgs",
                    "name": props.get("title") or f"Earthquake M{mag}",
                    "type": "EQ",
                    "lat": lat, "lon": lon,
                    "severity": None,
                    "magnitude": mag,
                    "start": props.get("time"),
                    "url": props.get("url"),
                    "raw": props
                })
        except Exception:
            print("USGS parse skip", traceback.format_exc())
    return out

def fetch_openweather_predictions_for_point(lat, lon):
    """Return predicted hazard events based on current weather (simplified version)."""
    try:
        # Use regular weather API instead of One Call API
        params = {"lat": lat, "lon": lon, "units": "metric", "appid": OPENWEATHER_KEY}
        r = requests.get("https://api.openweathermap.org/data/2.5/weather", params=params, timeout=10)
        r.raise_for_status()
        d = r.json()
    except Exception as e:
        print("OpenWeather fetch error:", e); return []
    events = []
    
    # Check current weather conditions for potential hazards
    weather_main = d.get("weather", [{}])[0].get("main", "").lower()
    weather_desc = d.get("weather", [{}])[0].get("description", "").lower()
    
    # Create hazard events based on current conditions
    if "rain" in weather_main or "rain" in weather_desc:
        events.append({
            "id": f"current-rain-{lat}-{lon}-{int(time.time())}",
            "source": "openweather-current",
            "name": "Current Rain Conditions (possible flood risk)",
            "type": "CURRENT_RAIN",
            "lat": lat, "lon": lon,
            "severity": "moderate",
            "magnitude": None,
            "start": None,
            "url": None,
            "raw": {"weather": weather_desc}
        })
    
    return events

def get_cached_events():
    now = time.time()
    if _cache["data"] and (now - _cache["timestamp"] < _cache["ttl"]):
        return _cache["data"]
    # merge sources
    events = []
    try:
        events.extend(fetch_gdacs())
    except Exception as e:
        print("GDACS error", e)
    try:
        events.extend(fetch_usgs_quakes())
    except Exception as e:
        print("USGS error", e)
    # also create prediction points for major destination hubs (north Pakistan)
    # list of points to check (Hunza, Naran, Fairy Meadows, Swat, Chitral, Skardu, Neelam)
    pred_points = [
        (36.3167, 74.6500), (34.9069, 73.6556), (35.4167, 74.5833),
        (34.7717, 72.3600), (35.8511, 71.7864), (35.2976, 75.6337),
        (34.6281, 73.9110)
    ]
    for lat, lon in pred_points:
        try:
            events.extend(fetch_openweather_predictions_for_point(lat, lon))
        except Exception as e:
            print("OpenWeather predict error", e)
    _cache["data"] = events
    _cache["timestamp"] = now
    return events

@app.route("/disasters", methods=["GET"])
def disasters():
    """
    Query params:
      - country=Pakistan
      - lat & lon & radius_km
      - bbox=minLon,minLat,maxLon,maxLat
      - simulate=1 (adds a fake event for testing)
    """
    try:
        events = get_cached_events()
    except Exception as e:
        print("get_cached_events error", e); events = []

    # optional simulate
    simulate = request.args.get("simulate")
    if simulate == "1":
        events = events + [{
            "id": "sim-local-1",
            "source": "simulate",
            "name": "Simulated local hazard",
            "type": "SIM",
            "lat": 36.3167, "lon": 74.65,
            "severity": "test",
            "magnitude": None,
            "start": None,
            "url": None,
            "raw": {}
        }]

    # filtering
    country = request.args.get("country")
    lat = request.args.get("lat", type=float)
    lon = request.args.get("lon", type=float)
    radius_km = request.args.get("radius_km", type=float)
    bbox = request.args.get("bbox")

    filtered = events
    if country:
        country_lower = country.lower()
        def match_country(e):
            raw = e.get("raw") or {}
            txt = " ".join([str(v) for v in raw.values()]).lower()
            return country_lower in txt or country_lower in (e.get("name","").lower())
        filtered = [e for e in filtered if match_country(e)]

    if bbox:
        try:
            minLon, minLat, maxLon, maxLat = map(float, bbox.split(","))
            filtered = [e for e in filtered if (minLon <= e["lon"] <= maxLon) and (minLat <= e["lat"] <= maxLat)]
        except:
            pass

    if lat is not None and lon is not None and radius_km is not None:
        def in_radius(e):
            try:
                return haversine_km(lat, lon, e["lat"], e["lon"]) <= radius_km
            except:
                return False
        filtered = [e for e in filtered if in_radius(e)]

    # normalize
    out = []
    for e in filtered:
        out.append({
            "id": e.get("id"),
            "source": e.get("source"),
            "name": e.get("name"),
            "type": e.get("type"),
            "lat": e.get("lat"),
            "lon": e.get("lon"),
            "severity": e.get("severity"),
            "magnitude": e.get("magnitude"),
            "start": e.get("start"),
            "url": e.get("url"),
            "predicted": True if e.get("source","").startswith("openweather") else False
        })

    return jsonify({"count": len(out), "events": out})

@app.route("/ml-predictions", methods=["GET"])
def ml_predictions():
    """Get ML-based 7-day disaster predictions for northern Pakistan"""
    try:
        predictions = get_all_predictions()
        return jsonify(predictions)
    except Exception as e:
        print(f"ML predictions error: {e}")
        return jsonify({"error": "ML prediction service unavailable"}), 500

@app.route("/ml-high-risk", methods=["GET"])
def ml_high_risk():
    """Get locations with high disaster risk based on ML predictions"""
    try:
        high_risk = get_high_risk_locations()
        return jsonify(high_risk)
    except Exception as e:
        print(f"ML high risk error: {e}")
        return jsonify({"error": "ML risk assessment unavailable"}), 500

@app.route("/ml-predict/<disaster_type>", methods=["GET"])
def ml_predict_specific(disaster_type):
    """Get ML prediction for specific disaster type and location"""
    try:
        lat = request.args.get('lat', type=float)
        lon = request.args.get('lon', type=float)
        
        if not lat or not lon:
            return jsonify({"error": "lat and lon parameters required"}), 400
        
        if disaster_type.lower() == 'flood':
            prediction = predict_flood_risk(lat, lon)
        elif disaster_type.lower() in ['earthquake', 'quake']:
            prediction = predict_earthquake_risk(lat, lon)
        else:
            return jsonify({"error": "disaster_type must be 'flood' or 'earthquake'"}), 400
        
        if prediction:
            return jsonify({
                "disaster_type": disaster_type,
                "coordinates": {"lat": lat, "lon": lon},
                "prediction": prediction
            })
        else:
            return jsonify({"error": "Prediction failed"}), 500
            
    except Exception as e:
        print(f"ML specific prediction error: {e}")
        return jsonify({"error": "Prediction service error"}), 500

if __name__ == "__main__":
    print("Starting disasters_api on http://0.0.0.0:8081 (GDACS + USGS + OpenWeather + ML predictions)")
    app.run(host="0.0.0.0", port=8081, debug=True)