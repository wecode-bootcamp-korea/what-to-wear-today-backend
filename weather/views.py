import requests 
import json

from django.shortcuts import render
from django.views import View
from django.http import JsonResponse

# https://openweathermap.org/current openapi 사용
class GetWeatherInfo(View):

    def get(self, request):
        lat = 37.532600
        lon = 127.024612
        location = {
                'lat': lat,
                'lon': lon,
                'APPID': 'd80201d1f829dc07700e3542d9283822',
                'lang':'kr',
                'units':'metric'
        }

        url = 'http://api.openweathermap.org/data/2.5/weather'

        my_response = requests.get(url, params=location).json()

        return JsonResponse(my_response)

    def post(self, request):

        curl_location = json.loads(request.body)
        location = {
                'lat': curl_location['lat'],
                'lon': curl_location['lon'],
                'APPID': 'd80201d1f829dc07700e3542d9283822',
                'lang':'kr',
                'units':'metric'
        }
        url = 'http://api.openweathermap.org/data/2.5/weather'
        my_response = requests.get(url, params=location).json()

        return JsonResponse(my_response)


# Create your views here.
