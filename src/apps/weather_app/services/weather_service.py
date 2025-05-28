import requests # type: ignore
import logging

logger = logging.getLogger(__name__)

def get_weather(city):
    # Получаем координаты города
    geo_response = requests.get(
        "https://geocoding-api.open-meteo.com/v1/search",
        params={"name": city, "count": 1}
    )
    geo_data = geo_response.json()
    
    if not geo_data.get("results"):
        raise ValueError("Город не найден")
    
    lat = geo_data["results"][0]["latitude"]
    lon = geo_data["results"][0]["longitude"]
    
    # Получаем данные о погоде
    weather_response = requests.get(
        "https://api.open-meteo.com/v1/forecast",
        params={
            "latitude": lat,
            "longitude": lon,
            "hourly": "temperature_2m",
            "current_weather": True
        }
    )
    
    return {
        "latitude": lat,
        "longitude": lon,
        "current": weather_response.json()["current_weather"],
        "hourly": weather_response.json()["hourly"]
    }