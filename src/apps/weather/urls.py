from django.urls import path
from . import views

app_name = "weather"  # Пространство имен приложения

urlpatterns = [
    # Главная страница
    path("", views.index, name="index"),
    
    # API endpoints
    path("api/weather/", views.weather_data, name="weather_data"),
    path("api/history/", views.search_history, name="search_history"),
    path("api/autocomplete/", views.city_autocomplete, name="autocomplete"),
]