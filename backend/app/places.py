import os, requests
KEY = os.environ.get("AIzaSyDJvDcdmau-Jt93UhPI7xjy-CQ0cLh-wqc")

def get_places(location, type="restaurant"):
    url = f"https://maps.googleapis.com/maps/api/place/textsearch/json?query={type}+in+{location}&key={KEY}"
    data = requests.get(url).json()
    results = []
    for place in data.get("results", [])[:8]:
        results.append({
            "name": place["name"],
            "rating": place.get("rating"),
            "address": place.get("formatted_address"),
            "location": place.get("geometry", {}).get("location")
        })
    return results

# Curated hotel and accommodation data for northern Pakistan destinations
NORTHERN_PAKISTAN_HOTELS = {
    "hunza valley": [
        {"name": "Hunza Serena Inn", "price": 25000, "type": "Luxury Hotel", "rating": 4.5},
        {"name": "Eagle's Nest Hotel", "price": 18000, "type": "Mountain Resort", "rating": 4.3},
        {"name": "Hunza View Hotel", "price": 12000, "type": "Mid-range Hotel", "rating": 4.1},
        {"name": "Baltit Fort View Hotel", "price": 15000, "type": "Heritage Hotel", "rating": 4.2},
        {"name": "Hunza Embassy Hotel", "price": 8000, "type": "Budget Hotel", "rating": 3.8},
        {"name": "Hunza Darbar Hotel", "price": 10000, "type": "Traditional Hotel", "rating": 3.9}
    ],
    "hunza": [
        {"name": "Hunza Serena Inn", "price": 25000, "type": "Luxury Hotel", "rating": 4.5},
        {"name": "Eagle's Nest Hotel", "price": 18000, "type": "Mountain Resort", "rating": 4.3},
        {"name": "Hunza View Hotel", "price": 12000, "type": "Mid-range Hotel", "rating": 4.1},
        {"name": "Baltit Fort View Hotel", "price": 15000, "type": "Heritage Hotel", "rating": 4.2},
        {"name": "Hunza Embassy Hotel", "price": 8000, "type": "Budget Hotel", "rating": 3.8},
        {"name": "Hunza Darbar Hotel", "price": 10000, "type": "Traditional Hotel", "rating": 3.9}
    ],
    "naran": [
        {"name": "Naran Valley Hotel", "price": 12000, "type": "Mountain Hotel", "rating": 4.0},
        {"name": "Saif-ul-Malook Resort", "price": 15000, "type": "Lake Resort", "rating": 4.2},
        {"name": "Kaghan Valley Hotel", "price": 8000, "type": "Budget Hotel", "rating": 3.7},
        {"name": "Naran Heights Hotel", "price": 10000, "type": "Mid-range Hotel", "rating": 3.9},
        {"name": "Shogran Resort", "price": 18000, "type": "Hill Station Resort", "rating": 4.1},
        {"name": "Siri Paye Hotel", "price": 6000, "type": "Basic Hotel", "rating": 3.5}
    ],
    "fairy meadows": [
        {"name": "Fairy Meadows Cottages", "price": 20000, "type": "Mountain Cottages", "rating": 4.4},
        {"name": "Nanga Parbat Base Camp Lodge", "price": 15000, "type": "Adventure Lodge", "rating": 4.2},
        {"name": "Fairy Meadows Camp", "price": 8000, "type": "Tent Camping", "rating": 4.0},
        {"name": "Raikot Bridge Hotel", "price": 10000, "type": "Gateway Hotel", "rating": 3.8},
        {"name": "Fairy Meadows Guest House", "price": 12000, "type": "Guest House", "rating": 4.1}
    ],
    "swat": [
        {"name": "Swat Serena Hotel", "price": 22000, "type": "Luxury Resort", "rating": 4.5},
        {"name": "Malam Jabba Resort", "price": 18000, "type": "Ski Resort", "rating": 4.3},
        {"name": "Kalam Valley Hotel", "price": 12000, "type": "Valley Hotel", "rating": 4.0},
        {"name": "Mingora City Hotel", "price": 8000, "type": "City Hotel", "rating": 3.8},
        {"name": "Swat Continental Hotel", "price": 10000, "type": "Mid-range Hotel", "rating": 3.9},
        {"name": "Green Valley Hotel", "price": 6000, "type": "Budget Hotel", "rating": 3.6}
    ],
    "chitral": [
        {"name": "Chitral Serena Hotel", "price": 20000, "type": "Luxury Hotel", "rating": 4.4},
        {"name": "Chitral Inn", "price": 12000, "type": "Traditional Hotel", "rating": 4.0},
        {"name": "Kalash Valley Guest House", "price": 8000, "type": "Cultural Guest House", "rating": 3.9},
        {"name": "Chitral Continental Hotel", "price": 10000, "type": "Mid-range Hotel", "rating": 3.8},
        {"name": "Mastuj Hotel", "price": 6000, "type": "Budget Hotel", "rating": 3.5}
    ],
    "skardu": [
        {"name": "Shangrila Resort", "price": 25000, "type": "Luxury Resort", "rating": 4.6},
        {"name": "Skardu Serena Hotel", "price": 20000, "type": "Luxury Hotel", "rating": 4.4},
        {"name": "K2 Resort", "price": 18000, "type": "Adventure Resort", "rating": 4.2},
        {"name": "Skardu Continental Hotel", "price": 12000, "type": "Mid-range Hotel", "rating": 4.0},
        {"name": "Baltoro Hotel", "price": 10000, "type": "Mountain Hotel", "rating": 3.9},
        {"name": "Skardu Inn", "price": 8000, "type": "Budget Hotel", "rating": 3.7}
    ],
    "neelam valley": [
        {"name": "Neelam Valley Resort", "price": 15000, "type": "Valley Resort", "rating": 4.2},
        {"name": "Muzaffarabad Hotel", "price": 10000, "type": "City Hotel", "rating": 3.9},
        {"name": "Keran Resort", "price": 12000, "type": "Riverside Resort", "rating": 4.0},
        {"name": "Sharda Resort", "price": 18000, "type": "Mountain Resort", "rating": 4.3},
        {"name": "Neelam Continental Hotel", "price": 8000, "type": "Mid-range Hotel", "rating": 3.8},
        {"name": "Jhelum Valley Hotel", "price": 6000, "type": "Budget Hotel", "rating": 3.6}
    ],
    "neelam": [
        {"name": "Neelam Valley Resort", "price": 15000, "type": "Valley Resort", "rating": 4.2},
        {"name": "Muzaffarabad Hotel", "price": 10000, "type": "City Hotel", "rating": 3.9},
        {"name": "Keran Resort", "price": 12000, "type": "Riverside Resort", "rating": 4.0},
        {"name": "Sharda Resort", "price": 18000, "type": "Mountain Resort", "rating": 4.3},
        {"name": "Neelam Continental Hotel", "price": 8000, "type": "Mid-range Hotel", "rating": 3.8},
        {"name": "Jhelum Valley Hotel", "price": 6000, "type": "Budget Hotel", "rating": 3.6}
    ]
}

def get_hotels_for_destination(city, budget=15000):
    """
    Get hotel recommendations for northern Pakistan destinations based on budget
    """
    city_clean = city.lower().strip()
    
    # Get hotels for the destination
    hotels = NORTHERN_PAKISTAN_HOTELS.get(city_clean, [])
    
    if not hotels:
        # If no specific hotels found, return general recommendations
        return [
            {"name": "Local Guest House", "price": 5000, "type": "Budget Accommodation", "rating": 3.5},
            {"name": "Mountain Lodge", "price": 8000, "type": "Mid-range Lodge", "rating": 3.8},
            {"name": "Valley Resort", "price": 12000, "type": "Resort", "rating": 4.0}
        ]
    
    # Filter hotels based on budget
    affordable_hotels = [hotel for hotel in hotels if hotel["price"] <= budget]
    
    # If no hotels within budget, return the cheapest options
    if not affordable_hotels:
        affordable_hotels = sorted(hotels, key=lambda x: x["price"])[:3]
    
    # Add budget-friendly suggestions
    suggestions = []
    for hotel in affordable_hotels[:4]:  # Limit to 4 suggestions
        suggestions.append({
            "name": hotel["name"],
            "price": f"{hotel['price']:,}",
            "type": hotel["type"],
            "rating": hotel["rating"]
        })
    
    return suggestions

