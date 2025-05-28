import requests  # noqa: F401
from django.shortcuts import render
from django.http import JsonResponse
from .services.weather_service import get_weather

def index(request):
    # Простая главная страница без истории поиска
    return render(request, "weather/index.html")

def weather_data(request):
    city = request.GET.get('city')
    
    if not city:
        return JsonResponse({"error": "Введите название города"}, status=400)
    
    try:
        raw_data = get_weather(city)
    except Exception as e:
        return JsonResponse({
            "error": f"Ошибка получения данных: {str(e)}",
            "city": city
        }, status=500)
    
    try:
        hourly_data = []
        temperatures = raw_data["hourly"]["temperature_2m"]
        times = raw_data["hourly"]["time"]
        
        for i in range(min(12, len(times))):
            if i == 0:
                trend = "same"
            else:
                current_temp = temperatures[i]
                prev_temp = temperatures[i-1]
                
                if current_temp > prev_temp:
                    trend = "up"
                elif current_temp < prev_temp:
                    trend = "down"
                else:
                    trend = "same"
            
            hourly_data.append({
                "time": times[i],
                "temperature": current_temp,
                "trend": trend
            })
        
        processed_data = {
            "city": city,
            "latitude": round(raw_data["latitude"], 2),
            "longitude": round(raw_data["longitude"], 2),
            "current_temp": temperatures[0],
            "hourly": hourly_data
        }
    except KeyError as e:
        return JsonResponse({
            "error": f"Некорректные данные от API: {str(e)}",
            "debug_data": raw_data
        }, status=500)
    
    return JsonResponse(processed_data)