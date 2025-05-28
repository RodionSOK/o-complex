from django.test import TestCase
from services.weather_service import get_weather

class WeatherServiceTest(TestCase):
    def test_valid_city(self):
        data = get_weather("Paris")
        self.assertIn("hourly", data)
    
    def test_invalid_city(self):
        data = get_weather("InvalidCity123")
        self.assertIn("error", data)