from django.urls import path
from .views import GetWeatherInfo

urlpatterns = [
        path('', GetWeatherInfo.as_view(), name='weather'),
        path('/post', GetWeatherInfo.as_view(), name='weather_post')
]
