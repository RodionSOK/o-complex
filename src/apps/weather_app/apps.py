from django.apps import AppConfig

class WeatherConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'src.apps.weather_app'
    label = 'weather_app'  