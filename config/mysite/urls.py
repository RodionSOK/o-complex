from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('', include('weather.urls', namespace='weather')),
    path('admin/', admin.site.urls),
    path('', include('src.apps.weather.urls')), 
]