# app/routers/stops.py
from fastapi import APIRouter
from typing import List
from app.models.schemas import Stop
from app.services.cache import GEOCODED_STOPS

router = APIRouter(prefix="/api/stops", tags=["Stops"])

@router.get("/", response_model=List[Stop])
async def get_stops():
    return GEOCODED_STOPS
