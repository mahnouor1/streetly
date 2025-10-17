import os, requests
KEY = os.environ.get("AIzaSyDJvDcdmau-Jt93UhPI7xjy-CQ0cLh-wqc")

def get_route(origin, destination):
    url = f"https://maps.googleapis.com/maps/api/directions/json?origin={origin}&destination={destination}&mode=driving&key={KEY}"
    r = requests.get(url).json()
    if not r.get("routes"):
        return {"error": "No route found"}
    leg = r["routes"][0]["legs"][0]
    return {
        "start": leg["start_address"],
        "end": leg["end_address"],
        "distance": leg["distance"]["text"],
        "duration": leg["duration"]["text"],
        "steps": [{"instruction": s["html_instructions"], "distance": s["distance"]["text"]} for s in leg["steps"]]
    }

