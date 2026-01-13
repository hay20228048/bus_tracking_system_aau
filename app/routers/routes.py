from fastapi import APIRouter
from typing import List
from app.models.schemas import Route
from app.data.mock_data import routes

router = APIRouter(prefix="/api/routes", tags=["Routes"])

@router.get("/", response_model=List[Route])
def get_routes():
    return routes
