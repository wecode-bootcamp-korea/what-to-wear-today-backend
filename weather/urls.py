from django.urls import path
from .views import WeatherInfo

urlpatterns = [
        path('', WeatherInfo.as_view(), name='weather'),
        path('/post', WeatherInfo.as_view(), name='weather_post')
]
