import httpx
from src.utils.config import GOOGLE_MAPS_API_KEY


class GeocodingService:
    def __init__(self):
        self.BASE_URL = "https://maps.googleapis.com/maps/api/geocode/json"


    async def geocode_address(self, address: str):
        async with httpx.AsyncClient() as client:
            params = {"address": address, "key": GOOGLE_MAPS_API_KEY}
            response = await client.get(self.BASE_URL, params=params)
            data = response.json()
            if data["status"] != "OK" or not data["results"]:
                return None
            loc = data["results"][0]["geometry"]["location"]
            return {"lat": loc["lat"], "lng": loc["lng"], "formatted_address": data["results"][0]["formatted_address"]}


    async def reverse_geocode(self, lat: float, lng: float):
        async with httpx.AsyncClient() as client:
            params = {"latlng": f"{lat},{lng}", "key": GOOGLE_MAPS_API_KEY}
            response = await client.get(self.BASE_URL, params=params)
            data = response.json()
            if data["status"] != "OK" or not data["results"]:
                return None
            return {"formatted_address": data["results"][0]["formatted_address"]}

