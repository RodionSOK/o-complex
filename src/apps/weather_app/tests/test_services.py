from django.test import TestCase
from unittest.mock import patch
from requests.exceptions import RequestException
from services.weather_service import get_weather

class WeatherServiceTest(TestCase):
    @patch('services.weather_service.requests.get')
    def test_valid_city(self, mock_get):
        mock_get.side_effect = [
            self._mock_response(200, {
                "results": [{"latitude": 48.85, "longitude": 2.35}]
            }),
            self._mock_response(200, {
                "hourly": {"temperature_2m": [15.0, 16.0]}
            })
        ]
        
        data = get_weather("Paris")
        self.assertIn("hourly", data)
        self.assertEqual(data["latitude"], 48.85)
        self.assertEqual(len(data["hourly"]["temperature_2m"]), 2)

    @patch('services.weather_service.requests.get')
    def test_invalid_city(self, mock_get):
        mock_get.return_value = self._mock_response(200, {"results": []})
        
        with self.assertRaises(ValueError) as context:
            get_weather("InvalidCity123")
        
        self.assertIn("Город 'InvalidCity123' не найден", str(context.exception))

    @patch('services.weather_service.requests.get')
    def test_api_error(self, mock_get):
        mock_get.side_effect = RequestException("Connection error")
        
        with self.assertRaises(ConnectionError) as context:
            get_weather("London")
        
        self.assertIn("Ошибка соединения", str(context.exception))

    @patch('services.weather_service.requests.get')
    def test_incomplete_weather_data(self, mock_get):
        mock_get.side_effect = [
            self._mock_response(200, {
                "results": [{"latitude": 51.51, "longitude": -0.13}]
            }),
            self._mock_response(200, {"hourly": {}})  
        ]
        
        with self.assertRaises(KeyError) as context:
            get_weather("London")
        
        self.assertIn("Отсутствуют почасовые данные о температуре", str(context.exception))

    def _mock_response(self, status_code, json_data):
        """Создаем мок-объект ответа"""
        class MockResponse:
            def __init__(self, status_code, json_data):
                self.status_code = status_code
                self.json_data = json_data
            
            def json(self):
                return self.json_data
            
            def raise_for_status(self):
                if 400 <= self.status_code < 600:
                    raise RequestException(f"HTTP Error {self.status_code}")
        
        return MockResponse(status_code, json_data)