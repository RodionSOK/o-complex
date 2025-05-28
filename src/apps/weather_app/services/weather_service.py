import requests
import logging
from requests.exceptions import RequestException

logger = logging.getLogger(__name__)

def get_weather(city):
    try:
        geo_response = requests.get(
            "https://geocoding-api.open-meteo.com/v1/search",
            params={"name": city, "count": 1, "language": "en", "format": "json"},
            timeout=10 
        )
        geo_response.raise_for_status()  
        
        geo_data = geo_response.json()
        
        if not geo_data.get("results"):
            raise ValueError(f"Город '{city}' не найден")
        
        location = geo_data["results"][0]
        lat = location["latitude"]
        lon = location["longitude"]
        
        weather_response = requests.get(
            "https://api.open-meteo.com/v1/forecast",
            params={
                "latitude": lat,
                "longitude": lon,
                "hourly": "temperature_2m",
                "forecast_days": 1,  
                "timezone": "auto"
            },
            timeout=10
        )
        weather_response.raise_for_status()
        
        weather_data = weather_response.json()
        
        if "hourly" not in weather_data or "temperature_2m" not in weather_data["hourly"]:
            logger.error(f"Неполные данные погоды для {city}: {weather_data}")
            raise KeyError("Отсутствуют почасовые данные о температуре")
        
        return {
            "latitude": lat,
            "longitude": lon,
            "hourly": {
                "time": weather_data["hourly"]["time"],
                "temperature_2m": weather_data["hourly"]["temperature_2m"]
            }
        }
        
    except RequestException as e:
        logger.error(f"Ошибка сети при получении погоды для {city}: {str(e)}")
        raise ConnectionError(f"Ошибка соединения: {str(e)}")
    except (KeyError, IndexError, TypeError) as e:
        logger.error(f"Ошибка обработки данных для {city}: {str(e)}")
        raise ValueError(f"Ошибка формата данных: {str(e)}")