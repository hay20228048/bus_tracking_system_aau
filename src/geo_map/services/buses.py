# app/services/cache.py
from typing import List
from fastapi.encoders import jsonable_encoder
from src.geo_map.services.geocoding import GeocodingService
from src.helpers.back_fill import buses
from src.geo_map.model import Bus

# Cached geocoded stops

class PopulateBuses:
    def __init__(self):
        self.geocoding = GeocodingService()
        self.geocoding_buses: List[Bus] = []

    async def buses(self):
        """
        Geocode all stops once and store in memory.
        """
        for bus in buses:
            b = dict(bus)
            self.geocoding_buses.append(b)

        return jsonable_encoder(self.geocoding_buses)
 
