from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
import requests 
import json

# https://openweathermap.org/current
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

        myResponse = requests.get(url, params=location).json()

        return JsonResponse(myResponse)

    def post(self, request):

        curLocation = json.loads(request.body)
        location = {
                'lat': curLocation['lat'],
                'lon': curLocation['lon'],
                'APPID': 'd80201d1f829dc07700e3542d9283822',
                'lang':'kr',
                'units':'metric'
        }
        url = 'http://api.openweathermap.org/data/2.5/weather'
        myResponse = requests.get(url, params=location).json()

        return JsonResponse(myResponse)


# Create your views here.
