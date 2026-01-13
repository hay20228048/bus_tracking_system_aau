# # # FastAPI backend

# from fastapi import FastAPI, Request
# from fastapi.responses import HTMLResponse
# from fastapi.staticfiles import StaticFiles
# from fastapi.templating import Jinja2Templates
# from dotenv import load_dotenv
# import os

# # Load environment variables
# load_dotenv()
# GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")

# app = FastAPI()

# # Mount static folder
# app.mount("/static", StaticFiles(directory="app/static"), name="static")

# # Set templates folder
# templates = Jinja2Templates(directory="app/templates")

# @app.get("/", response_class=HTMLResponse)
# async def get_index(request: Request):
#     return templates.TemplateResponse("index.html", {
#         "request": request,
#         "GOOGLE_MAPS_API_KEY": GOOGLE_MAPS_API_KEY
#     })



from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv
import os

# -------------------------------
# Load environment variables
# -------------------------------
load_dotenv("app/.env")

GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")
if not GOOGLE_MAPS_API_KEY:
    raise RuntimeError("GOOGLE_MAPS_API_KEY is missing in .env file")

# -------------------------------
# FastAPI app
# -------------------------------
app = FastAPI(
    title="Bus Tracking System",
    description="FastAPI backend for buses, stops, and routes",
    version="1.0.0"
)

# -------------------------------
# Static & Templates
# -------------------------------
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

# -------------------------------
# Routers (API endpoints)
# -------------------------------
from app.routers import buses, stops, routes

app.include_router(buses.router)
app.include_router(stops.router)
app.include_router(routes.router)

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
