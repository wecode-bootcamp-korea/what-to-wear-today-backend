import requests
import json

from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from clothes.views import ClothesRecom 

# https://openweathermap.org/current openapi 사용
class GetWeatherInfo(View):

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

        address_get = GetWeatherInfo.get_address(curl_location['lat'],curl_location['lon'])

        temp_id_get = GetWeatherInfo.get_temp_id(my_response["main"]["temp"])
        icon_lists = ClothesRecom.get_clothesicon_list(temp_id_get)
        comment = ClothesRecom.get_weather_comments(temp_id_get)
        my_response.update(
                {
                    'icon_lists':icon_lists,
                    'comment':comment,
                    'region_name':address_get["documents"][0]["address"]['region_1depth_name']

                }
            )

        return JsonResponse(my_response)

    def get_temp_id(cur_temp):

        if cur_temp >= 28:
            temp_id = 1
        elif cur_temp >= 23 and cur_temp < 27:
            temp_id = 2
        elif cur_temp >= 20 and cur_temp < 23:
            temp_id = 3
        elif cur_temp >= 17 and cur_temp < 20:
            temp_id = 4
        elif cur_temp >= 12 and cur_temp < 17:
            temp_id = 5
        elif cur_temp >= 9 and cur_temp < 12:
            temp_id = 6
        elif cur_temp >= 5 and cur_temp < 9:
            temp_id = 7
        elif cur_temp < 4:
            temp_id = 8

        return temp_id

    def get_address(latitude,longitude):

        url = "https://dapi.kakao.com/v2/local/geo/coord2address.json"
        header = {'Authorization':'KakaoAK 0f5eaded6c5395caef32cd5621bf24ad',}
        pa = {
                'x': longitude,
                'y': latitude
                }

        my_response = requests.get(url, headers=header, params=pa)

        return my_response.json()
