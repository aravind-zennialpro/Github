# app/services/weather_service.py
import os
import httpx
from dotenv import load_dotenv

load_dotenv()
OPEN_METEO_BASE = os.getenv("OPEN_METEO_BASE", "https://api.open-meteo.com/v1/forecast")

async def get_weather_summary_for_city(city_name: str, date: str = None):
    # Use Open-Meteo for weather summary
    geocode_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city_name}&count=1"
    async with httpx.AsyncClient(timeout=10) as client:
        geo_r = await client.get(geocode_url)
        geo_r.raise_for_status()
        geo = geo_r.json()
        if not geo.get("results"):
            return {"summary":"unknown","temp_c": None, "precipitation": None}
        loc = geo["results"][0]
        lat, lon = loc["latitude"], loc["longitude"]

        # Build weather request: current_weather at destination
        params = {
            "latitude": lat,
            "longitude": lon,
            "current_weather": True,
            "daily": "precipitation_sum,weathercode",
            "timezone": "auto"
        }
        resp = await client.get(OPEN_METEO_BASE, params=params)
        resp.raise_for_status()
        j = resp.json()

    # mathing the weather to base model:
    current = j.get("current_weather", {})
    temp_c = current.get("temperature")
    weathercode = current.get("weathercode")
    #  weather logics:
    if weathercode is None:
        summary = "Unknown"
    elif weathercode >= 80:
        summary = "Heavy Rain"
    elif weathercode >= 60:
        summary = "Rain"
    elif weathercode >= 45:
        summary = "Fog/Mist"
    elif weathercode >= 1 and weathercode < 45:
        summary = "Cloudy"
    else:
        summary = "Sunny"

    return {"summary": summary, "temp_c": temp_c, "precipitation": None}
