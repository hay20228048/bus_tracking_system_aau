# app/services/cache.py
from typing import List
from app.data.mock_data import stops as stops_data
from app.services.geocoding import GeocodingService

# Cached geocoded stops
GEOCODED_STOPS: List[dict] = []

async def populate_stops():
    """
    Geocode all stops once and store in memory.
    """
    global GEOCODED_STOPS   # ✅ THIS IS THE FIX

    GEOCODED_STOPS.clear()  # ✅ better than reassigning

 
    for stop in stops_data:
        geo = await GeocodingService.geocode_address(stop["name"])
 

        if geo:
            GEOCODED_STOPS.append({
                "id": stop["id"],
                "name": stop["name"],
                "location": {
                    "lat": geo["lat"],
                    "lng": geo["lng"]
                }
            })

 
