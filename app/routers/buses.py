from fastapi import APIRouter
from typing import List
from app.models.schemas import Bus
from app.data.mock_data import buses

router = APIRouter(prefix="/api/buses", tags=["Buses"])

@router.get("/", response_model=List[Bus])
async def get_buses():
    return buses