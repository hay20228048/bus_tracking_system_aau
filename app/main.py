from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv
import os
from app.services.cache import populate_stops
from contextlib import asynccontextmanager
# -------------------------------
# Load environment variables
# -------------------------------
load_dotenv("app/.env")

GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")
if not GOOGLE_MAPS_API_KEY:
    raise RuntimeError("GOOGLE_MAPS_API_KEY is missing in .env file")




@asynccontextmanager
async def lifespan(app: FastAPI):
    # Populate geocoded stops once at startup
    await populate_stops()

    yield
 


# -------------------------------
# FastAPI app
# -------------------------------
app = FastAPI(
    title="Bus Tracking System",
    description="FastAPI backend for buses, stops, and routes",
    version="1.0.0",
    lifespan=lifespan   # ✅ THIS IS THE MISSING PIECE
)

# -------------------------------
# Static & Templates
# -------------------------------
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

# -------------------------------
# Routers (API endpoints)
# -------------------------------

from app.routers import buses, stops, routes, geocoding, distance_matrix  

app.include_router(stops.router)
app.include_router(routes.router)
app.include_router(buses.router)
app.include_router(geocoding.router)
app.include_router(distance_matrix.router)  # <-- add this

# -------------------------------
# Frontend route
# -------------------------------
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """
    Serves the main map UI
    """
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "GOOGLE_MAPS_API_KEY": GOOGLE_MAPS_API_KEY
        }
    )


