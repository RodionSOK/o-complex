from django.urls import path
from . import views

app_name = 'weather_app'  

urlpatterns = [
    path('', views.index, name='index'),
    path('api/weather/', views.weather_data, name='weather_data'),
]