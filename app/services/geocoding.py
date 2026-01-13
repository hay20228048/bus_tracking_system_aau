import os
import httpx
from dotenv import load_dotenv

load_dotenv("app/.env")
GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")

class GeocodingService:
    BASE_URL = "https://maps.googleapis.com/maps/api/geocode/json"

    @staticmethod
    async def geocode_address(address: str):
        async with httpx.AsyncClient() as client:
            params = {"address": address, "key": GOOGLE_MAPS_API_KEY}
            response = await client.get(GeocodingService.BASE_URL, params=params)
            data = response.json()
            if data["status"] != "OK" or not data["results"]:
                return None
            loc = data["results"][0]["geometry"]["location"]
            return {"lat": loc["lat"], "lng": loc["lng"], "formatted_address": data["results"][0]["formatted_address"]}

    @staticmethod
    async def reverse_geocode(lat: float, lng: float):
        async with httpx.AsyncClient() as client:
            params = {"latlng": f"{lat},{lng}", "key": GOOGLE_MAPS_API_KEY}
            response = await client.get(GeocodingService.BASE_URL, params=params)
            data = response.json()
            if data["status"] != "OK" or not data["results"]:
                return None
            return {"formatted_address": data["results"][0]["formatted_address"]}
