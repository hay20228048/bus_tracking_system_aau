# app/routers/routes.py
from fastapi import APIRouter
from typing import List
from app.models.schemas import Route
from app.services.cache import GEOCODED_STOPS

router = APIRouter(prefix="/api/routes", tags=["Routes"])

@router.get("/", response_model=List[Route])
async def get_routes():
    if not GEOCODED_STOPS:
        return []
    print(":::::::::::::::::::"*20, GEOCODED_STOPS)
    dynamic_route = {
        "id": 1,
        "name": "Dynamic Route - All Stops",
        "path": [stop["location"] for stop in GEOCODED_STOPS]
    }

    return [dynamic_route]
