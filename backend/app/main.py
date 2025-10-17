from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from weather import get_weather_by_city, get_forecast_by_city
from maps import get_route
from places import get_places, get_hotels_for_destination
from fcm_utils import send_push_for_alert
from gemini_chat import get_gemini_response
import os
from dotenv import load_dotenv
load_dotenv()


app = FastAPI(title="Streetly Travel Assistant API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Optional: Initialize Firestore only if credentials are available
try:
    from google.cloud import firestore
    db = firestore.Client()
    print("Firestore client initialized successfully")
except Exception as e:
    print(f"Firestore not available: {e}")
    db = None

@app.get("/")
async def root():
    return {"message": "Streetly Travel Assistant API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# Weather endpoints
@app.get("/weather")
def weather(city: str = "Murree"):
    try:
        return get_weather_by_city(city)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/forecast")
def forecast(city: str = "Murree"):
    try:
        return get_forecast_by_city(city)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Maps endpoints
@app.get("/route")
def route(origin: str, destination: str):
    try:
        return get_route(origin, destination)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Places endpoints
@app.get("/places")
def places(location: str, type: str = "restaurant"):
    try:
        return get_places(location, type)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Hotels endpoint for northern Pakistan destinations
@app.get("/hotels")
def hotels(city: str, budget: int = 15000):
    try:
        return get_hotels_for_destination(city, budget)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/alert")
def create_alert(user_id: str, lat: float, lon: float, level: str = "warning", message: str = "Alert!"):
    if db is None:
        raise HTTPException(status_code=503, detail="Firestore not available")
    
    try:
        # Save into Firestore
        alert = {
            "user_id": user_id,
            "lat": lat,
            "lon": lon,
            "level": level,
            "message": message,
            "created_at": firestore.SERVER_TIMESTAMP
        }
        doc = db.collection("alerts").add(alert)
        # Send push via FCM to user topics or tokens (optional)
        send_push_for_alert(message, lat, lon)
        return {"ok": True, "doc_id": doc[1].id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Chat endpoint for AI assistant integration with Gemini
@app.post("/chat")
def chat_endpoint(request: dict):
    """
    Chat endpoint for AI assistant integration with Gemini API
    Accepts: {"message": "Plan trip to Hunza next week"}
    Returns: {"reply": "Hunza Valley is beautiful this time of year! Expect 12°C with clear skies. You can take the N-35 route via Gilgit."}
    """
    try:
        message = request.get("message", "").strip()
        
        if not message:
            raise HTTPException(status_code=400, detail="Message is required")
        
        # Get AI response from Gemini
        ai_reply = get_gemini_response(message)
        
        return {"reply": ai_reply}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chat processing error: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
