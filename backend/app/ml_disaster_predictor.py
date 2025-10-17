"""
ML Disaster Prediction System
Integrates trained Random Forest models for 7-day flood and earthquake prediction
"""

import pickle
import pandas as pd
import numpy as np
import requests
import os
from datetime import datetime, timedelta
import traceback

# Model paths
MODEL_DIR = os.path.join(os.path.dirname(__file__), 'models')
FLOOD_MODEL_PATH = os.path.join(MODEL_DIR, 'rf_flood_7day_model.pkl')
QUAKE_MODEL_PATH = os.path.join(MODEL_DIR, 'rf_quake_7day_model.pkl')
QUAKE_DEPTH_MODEL_PATH = os.path.join(MODEL_DIR, 'rf_quake_depth_model.pkl')
QUAKE_FEATURES_PATH = os.path.join(MODEL_DIR, 'top_quake_features.csv')

# OpenWeather API configuration
OPENWEATHER_KEY = "cd3d503156309b838b4f9b8db21c646c"
OPENWEATHER_BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

# Northern Pakistan coordinates for prediction points
PREDICTION_POINTS = {
    "Hunza Valley": {"lat": 36.3167, "lon": 74.6500},
    "Naran": {"lat": 34.9069, "lon": 73.6556},
    "Fairy Meadows": {"lat": 35.4167, "lon": 74.5833},
    "Swat": {"lat": 34.7717, "lon": 72.3600},
    "Chitral": {"lat": 35.8511, "lon": 71.7864},
    "Skardu": {"lat": 35.2976, "lon": 75.6337},
    "Neelam Valley": {"lat": 34.6281, "lon": 73.9110}
}

# Global model cache
_models_cache = {}
_features_cache = {}

def load_models():
    """Load ML models and feature information"""
    global _models_cache, _features_cache
    
    try:
        # Load models with compatibility handling
        if 'flood_model' not in _models_cache:
            try:
                with open(FLOOD_MODEL_PATH, 'rb') as f:
                    _models_cache['flood_model'] = pickle.load(f)
                print("✅ Flood prediction model loaded")
            except Exception as e:
                print(f"⚠️ Flood model loading failed: {e}")
                print("📝 Using fallback prediction system")
                _models_cache['flood_model'] = None
        
        if 'quake_model' not in _models_cache:
            try:
                with open(QUAKE_MODEL_PATH, 'rb') as f:
                    _models_cache['quake_model'] = pickle.load(f)
                print("✅ Earthquake prediction model loaded")
            except Exception as e:
                print(f"⚠️ Earthquake model loading failed: {e}")
                print("📝 Using fallback prediction system")
                _models_cache['quake_model'] = None
        
        if 'quake_depth_model' not in _models_cache:
            try:
                with open(QUAKE_DEPTH_MODEL_PATH, 'rb') as f:
                    _models_cache['quake_depth_model'] = pickle.load(f)
                print("✅ Earthquake depth model loaded")
            except Exception as e:
                print(f"⚠️ Earthquake depth model loading failed: {e}")
                print("📝 Using fallback prediction system")
                _models_cache['quake_depth_model'] = None
        
        # Load feature information
        if 'quake_features' not in _features_cache:
            try:
                df = pd.read_csv(QUAKE_FEATURES_PATH)
                _features_cache['quake_features'] = df['0'].tolist()[1:]  # Skip header
                print("✅ Earthquake features loaded")
            except Exception as e:
                print(f"⚠️ Features loading failed: {e}")
                _features_cache['quake_features'] = []
        
        return True
        
    except Exception as e:
        print(f"❌ Error loading models: {e}")
        return False

def get_weather_data(lat, lon):
    """Fetch current weather data from OpenWeather API"""
    try:
        params = {
            'lat': lat,
            'lon': lon,
            'units': 'metric',
            'appid': OPENWEATHER_KEY
        }
        
        response = requests.get(OPENWEATHER_BASE_URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        return {
            'temperature_2m_max': data['main']['temp_max'],
            'temperature_2m_min': data['main']['temp_min'],
            'T2M': data['main']['temp'],
            'RH2M': data['main']['humidity'],
            'WS2M': data['wind']['speed'],
            'precipitation': data.get('rain', {}).get('1h', 0) if 'rain' in data else 0
        }
        
    except Exception as e:
        print(f"❌ Weather API error for {lat}, {lon}: {e}")
        # Return default values if API fails
        return {
            'temperature_2m_max': 20.0,
            'temperature_2m_min': 10.0,
            'T2M': 15.0,
            'RH2M': 50.0,
            'WS2M': 5.0,
            'precipitation': 0.0
        }

def prepare_flood_features(lat, lon, weather_data):
    """Prepare features for flood prediction model"""
    now = datetime.now()
    
    features = {
        'latitude': lat,
        'longitude': lon,
        'day_of_year': now.timetuple().tm_yday,
        'month': now.month,
        'temperature_2m_max': weather_data['temperature_2m_max'],
        'temperature_2m_min': weather_data['temperature_2m_min'],
        'T2M': weather_data['T2M'],
        'RH2M': weather_data['RH2M'],
        'WS2M': weather_data['WS2M'],
        'precipitation': weather_data['precipitation']
    }
    
    return features

def prepare_quake_features(lat, lon, weather_data):
    """Prepare features for earthquake prediction model"""
    now = datetime.now()
    
    features = {
        'latitude_quake': lat,
        'longitude_quake': lon,
        'magnitude': 0.0,  # Default magnitude for prediction
        'day_of_year': now.timetuple().tm_yday,
        'month': now.month,
        'temperature_2m_min': weather_data['temperature_2m_min'],
        'temperature_2m_max': weather_data['temperature_2m_max'],
        'T2M': weather_data['T2M'],
        'RH2M': weather_data['RH2M'],
        'WS2M': weather_data['WS2M']
    }
    
    return features

def predict_flood_risk(lat, lon):
    """Predict 7-day flood risk for a location"""
    try:
        if not load_models():
            return None
        
        # Get current weather data
        weather_data = get_weather_data(lat, lon)
        
        # Check if ML model is available
        flood_model = _models_cache.get('flood_model')
        
        if flood_model is not None:
            # Use ML model
            features = prepare_flood_features(lat, lon, weather_data)
            feature_df = pd.DataFrame([features])
            
            prediction = flood_model.predict(feature_df)[0]
            probability = flood_model.predict_proba(feature_df)[0]
            
            # Determine risk level
            if prediction == 1:
                risk_level = "HIGH" if probability[1] > 0.7 else "MEDIUM"
            else:
                risk_level = "LOW"
            
            return {
                'prediction': int(prediction),
                'probability': float(probability[1]),
                'risk_level': risk_level,
                'confidence': float(max(probability)),
                'weather_conditions': weather_data,
                'method': 'ml_model'
            }
        else:
            # Use fallback heuristic prediction
            return predict_flood_risk_fallback(lat, lon, weather_data)
        
    except Exception as e:
        print(f"❌ Flood prediction error: {e}")
        traceback.print_exc()
        return None

def predict_flood_risk_fallback(lat, lon, weather_data):
    """Fallback flood prediction using weather heuristics"""
    try:
        # Simple heuristic based on precipitation and humidity
        precipitation = weather_data.get('precipitation', 0)
        humidity = weather_data.get('RH2M', 50)
        temperature = weather_data.get('T2M', 15)
        
        # Risk factors
        risk_score = 0
        
        # High precipitation increases risk
        if precipitation > 10:
            risk_score += 0.4
        elif precipitation > 5:
            risk_score += 0.2
        
        # High humidity increases risk
        if humidity > 80:
            risk_score += 0.3
        elif humidity > 70:
            risk_score += 0.1
        
        # Temperature affects snowmelt (higher temp = more snowmelt = flood risk)
        if temperature > 15:
            risk_score += 0.2
        elif temperature > 10:
            risk_score += 0.1
        
        # Determine risk level
        if risk_score > 0.6:
            risk_level = "HIGH"
            probability = min(risk_score, 0.9)
        elif risk_score > 0.3:
            risk_level = "MEDIUM"
            probability = risk_score
        else:
            risk_level = "LOW"
            probability = max(risk_score, 0.1)
        
        return {
            'prediction': 1 if risk_level in ['HIGH', 'MEDIUM'] else 0,
            'probability': probability,
            'risk_level': risk_level,
            'confidence': 0.7,  # Lower confidence for heuristic
            'weather_conditions': weather_data,
            'method': 'heuristic_fallback'
        }
        
    except Exception as e:
        print(f"❌ Fallback flood prediction error: {e}")
        return None

def predict_earthquake_risk(lat, lon):
    """Predict 7-day earthquake risk for a location"""
    try:
        if not load_models():
            return None
        
        # Get current weather data
        weather_data = get_weather_data(lat, lon)
        
        # Check if ML model is available
        quake_model = _models_cache.get('quake_model')
        depth_model = _models_cache.get('quake_depth_model')
        
        if quake_model is not None and depth_model is not None:
            # Use ML model
            features = prepare_quake_features(lat, lon, weather_data)
            feature_df = pd.DataFrame([features])
            
            quake_prediction = quake_model.predict(feature_df)[0]
            quake_probability = quake_model.predict_proba(feature_df)[0]
            depth_prediction = depth_model.predict(feature_df)[0]
            
            # Determine risk level
            if quake_prediction == 1:
                risk_level = "HIGH" if quake_probability[1] > 0.6 else "MEDIUM"
            else:
                risk_level = "LOW"
            
            return {
                'prediction': int(quake_prediction),
                'probability': float(quake_probability[1]),
                'risk_level': risk_level,
                'confidence': float(max(quake_probability)),
                'predicted_depth': float(depth_prediction),
                'weather_conditions': weather_data,
                'method': 'ml_model'
            }
        else:
            # Use fallback heuristic prediction
            return predict_earthquake_risk_fallback(lat, lon, weather_data)
        
    except Exception as e:
        print(f"❌ Earthquake prediction error: {e}")
        traceback.print_exc()
        return None

def predict_earthquake_risk_fallback(lat, lon, weather_data):
    """Fallback earthquake prediction using geological heuristics"""
    try:
        # Simple heuristic based on location and weather patterns
        # Northern Pakistan is in a seismically active region
        
        # Base risk from location (Northern Pakistan is earthquake-prone)
        base_risk = 0.2
        
        # Weather factors that might affect seismic activity
        temperature = weather_data.get('T2M', 15)
        humidity = weather_data.get('RH2M', 50)
        wind_speed = weather_data.get('WS2M', 5)
        
        risk_score = base_risk
        
        # Temperature variations can affect ground stress
        if temperature > 20 or temperature < 0:
            risk_score += 0.1
        
        # High humidity might indicate atmospheric pressure changes
        if humidity > 80:
            risk_score += 0.05
        
        # Wind patterns might indicate atmospheric pressure changes
        if wind_speed > 10:
            risk_score += 0.05
        
        # Determine risk level
        if risk_score > 0.4:
            risk_level = "HIGH"
            probability = min(risk_score, 0.8)
        elif risk_score > 0.25:
            risk_level = "MEDIUM"
            probability = risk_score
        else:
            risk_level = "LOW"
            probability = max(risk_score, 0.1)
        
        # Estimate depth (Northern Pakistan earthquakes are typically shallow to intermediate)
        estimated_depth = 15.0  # km, typical for the region
        
        return {
            'prediction': 1 if risk_level in ['HIGH', 'MEDIUM'] else 0,
            'probability': probability,
            'risk_level': risk_level,
            'confidence': 0.6,  # Lower confidence for heuristic
            'predicted_depth': estimated_depth,
            'weather_conditions': weather_data,
            'method': 'heuristic_fallback'
        }
        
    except Exception as e:
        print(f"❌ Fallback earthquake prediction error: {e}")
        return None

def get_all_predictions():
    """Get flood and earthquake predictions for all northern Pakistan locations"""
    predictions = {
        'flood_predictions': {},
        'earthquake_predictions': {},
        'timestamp': datetime.now().isoformat(),
        'model_status': 'active'
    }
    
    for location, coords in PREDICTION_POINTS.items():
        lat, lon = coords['lat'], coords['lon']
        
        # Get flood prediction
        flood_pred = predict_flood_risk(lat, lon)
        if flood_pred:
            predictions['flood_predictions'][location] = {
                'coordinates': coords,
                'prediction': flood_pred
            }
        
        # Get earthquake prediction
        quake_pred = predict_earthquake_risk(lat, lon)
        if quake_pred:
            predictions['earthquake_predictions'][location] = {
                'coordinates': coords,
                'prediction': quake_pred
            }
    
    return predictions

def get_high_risk_locations():
    """Get locations with high disaster risk"""
    all_predictions = get_all_predictions()
    high_risk = {
        'flood_high_risk': [],
        'earthquake_high_risk': [],
        'timestamp': all_predictions['timestamp']
    }
    
    # Check flood risks
    for location, data in all_predictions['flood_predictions'].items():
        if data['prediction']['risk_level'] in ['HIGH', 'MEDIUM']:
            high_risk['flood_high_risk'].append({
                'location': location,
                'coordinates': data['coordinates'],
                'risk_level': data['prediction']['risk_level'],
                'probability': data['prediction']['probability']
            })
    
    # Check earthquake risks
    for location, data in all_predictions['earthquake_predictions'].items():
        if data['prediction']['risk_level'] in ['HIGH', 'MEDIUM']:
            high_risk['earthquake_high_risk'].append({
                'location': location,
                'coordinates': data['coordinates'],
                'risk_level': data['prediction']['risk_level'],
                'probability': data['prediction']['probability'],
                'predicted_depth': data['prediction']['predicted_depth']
            })
    
    return high_risk

# Initialize models on import
if __name__ == "__main__":
    print("🤖 Initializing ML Disaster Prediction System...")
    load_models()
    print("✅ System ready!")
    
    # Test predictions
    test_predictions = get_all_predictions()
    print(f"📊 Generated predictions for {len(test_predictions['flood_predictions'])} locations")
else:
    # Load models when module is imported
    load_models()
