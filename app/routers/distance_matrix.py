# app/routers/distance_matrix.py
from fastapi import APIRouter
from typing import List
from app.data.mock_data import buses, stops
from app.services.geocoding import GeocodingService
import os
import httpx
from app.services.cache import GEOCODED_STOPS



GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")
router = APIRouter(prefix="/api/distance", tags=["Distance Matrix"])

@router.get("/eta")
async def get_eta():
    """
    Compute ETA from each bus to each stop using Google Distance Matrix API.
    """
    if not buses or not stops:
        return {"error": "No buses or stops defined"}


    if not GEOCODED_STOPS:
        return []


    # Prepare origins (buses) and destinations (stops)
    # origins = "|".join(f"{bus['location']['lat']},{bus['location']['lng']}" for bus in buses)
    # destinations = [stop["location"] for stop in GEOCODED_STOPS]#"|".join(f"{stop['location']['lat']},{stop['location']['lng']}" for stop in stops if "location" in stop)




    # Prepare origins (buses) and destinations (stops)
    origins = "|".join(f"{bus['location']['lat']},{bus['location']['lng']}" for bus in buses)
    destinations ="|".join(f"{stop["location"]['lat']},{stop["location"]['lng']}" for stop in GEOCODED_STOPS)

    print("\n ++++++++++++++++++++++++++++", destinations)



    if not destinations:
        return {"error": "Stops have no geocoded location yet"}

    # Build the Distance Matrix API URL
    url = (
        "https://maps.googleapis.com/maps/api/distancematrix/json"
        f"?origins={origins}"
        f"&destinations={destinations}"
        f"&key={GOOGLE_MAPS_API_KEY}"
    )

    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        data = response.json()

    # Map result back to buses → stops
    results = []
    for i, bus in enumerate(buses):
        bus_result = {"bus_id": bus["id"], "etas": []}
        for j, stop in enumerate(stops):
            element = data["rows"][i]["elements"][j]
            if element.get("status") == "OK":
                bus_result["etas"].append({
                    "stop_id": stop["id"],
                    "distance_meters": element["distance"]["value"],
                    "duration_seconds": element["duration"]["value"],
                    "duration_text": element["duration"]["text"]
                })
            else:
                bus_result["etas"].append({
                    "stop_id": stop["id"],
                    "error": element.get("status")
                })
        results.append(bus_result)
        print("--------"*20)
    print(results)
    return results
