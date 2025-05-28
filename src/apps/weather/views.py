import requests # type: ignore
from django.shortcuts import render
from django.http import JsonResponse
from django.utils import timezone
from .models import CitySearch
from .services.weather_service import get_weather

def index(request):
    if not request.session.session_key:
        request.session.save()
    
    recent_searches = CitySearch.objects.filter(
        session_key=request.session.session_key
    ).order_by("-last_searched")[:5]
    
    return render(request, "weather/index.html", {
        "recent_searches": recent_searches
    })

def weather_data(request):
    city = request.GET.get('city')
    
    if not city:
        return JsonResponse({"error": "Введите название города"}, status=400)
    
    try:
        raw_data = get_weather(city)
        print(f"Raw API data: {raw_data}")  # Логирование для отладки
    except Exception as e:
        return JsonResponse({
            "error": f"Ошибка получения данных: {str(e)}",
            "city": city
        }, status=500)
    
    # Обработка сессии
    if not request.session.session_key:
        request.session.create()
    
    # Сохранение истории поиска
    if request.session.session_key:
        CitySearch.objects.filter(
            session_key=request.session.session_key
        ).order_by("-last_searched")[5:].delete()
        
        obj, created = CitySearch.objects.get_or_create(
            city=city,
            session_key=request.session.session_key,
            defaults={"last_searched": timezone.now()}
        )
        if not created:
            obj.count += 1
            obj.last_searched = timezone.now()
            obj.save()
    
    # Обработка данных
    try:
        processed_data = {
            "city": city,
            "latitude": round(raw_data["latitude"], 2),
            "longitude": round(raw_data["longitude"], 2),
            "current_temp": raw_data["current"]["temperature_2m"],
            "hourly": [
                {
                    "time": timezone.datetime.fromisoformat(raw_data["hourly"]["time"][i]),
                    "temperature": raw_data["hourly"]["temperature_2m"][i],
                    "trend": "up" if raw_data["hourly"]["temperature_2m"][i] > 
                              raw_data["hourly"]["temperature_2m"][i-1] else "down"
                } 
                for i in range(min(12, len(raw_data["hourly"]["time"])))
            ]
        }
    except KeyError as e:
        return JsonResponse({
            "error": f"Некорректные данные от API: {str(e)}",
            "debug_data": raw_data
        }, status=500)
    
    return JsonResponse(processed_data)

def search_history(request):
    if not request.session.session_key:
        return JsonResponse([], safe=False)
    
    history = CitySearch.objects.filter(
        session_key=request.session.session_key
    ).values("city", "count")
    
    return JsonResponse(list(history), safe=False)

def city_autocomplete(request):
    query = request.GET.get("term", "")
    
    try:
        response = requests.get(
            "https://geocoding-api.open-meteo.com/v1/search",
            params={"name": query, "count": 5},
            timeout=3  
        )
        response.raise_for_status()  
        data = response.json()
        cities = [result["name"] for result in data.get("results", [])]
    except Exception:
        cities = []
    
    return JsonResponse(cities, safe=False)