from pydantic import BaseModel
from typing import List

class Location(BaseModel):
    lat: float
    lng: float

class Bus(BaseModel):
    id: int
    location: Location
    speed: float | None = None

class Stop(BaseModel):
    id: int
    name: str
    location: Location

class Route(BaseModel):
    id: int
    name: str
    path: List[Location]
