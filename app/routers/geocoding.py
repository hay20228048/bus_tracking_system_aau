from fastapi import APIRouter, Query
from app.services.geocoding import GeocodingService

router = APIRouter(prefix="/api/geocode", tags=["Geocoding"])
@router.get("/address")

#@router.get("/address")
async def geocode_address(address: str = Query(...)):
    geo = await GeocodingService.geocode_address(address)
    if not geo:
        return {"error": "Address not found"}
    return geo

@router.get("/reverse")
async def reverse_geocode(lat: float = Query(...), lng: float = Query(...)):
    geo = await GeocodingService.reverse_geocode(lat, lng)
    if not geo:
        return {"error": "Location not found"}
    return geo
