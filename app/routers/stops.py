from fastapi import APIRouter
from typing import List
from app.models.schemas import Stop
from app.data.mock_data import stops

router = APIRouter(prefix="/api/stops", tags=["Stops"])

@router.get("/", response_model=List[Stop])
def get_stops():
    return stops
