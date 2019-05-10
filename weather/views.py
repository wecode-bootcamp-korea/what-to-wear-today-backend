import requests
import json
import my_settings

from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from clothes.views import ClothesRecom
from user.views import *
from user.models import User, UserOption
from user.utils import login_decorator_pass

# https://openweathermap.org/current openapi 사용
class WeatherInfo(View):

    @login_decorator_pass
    def post(self, request):
        curl_location = json.loads(request.body)
        location = {
            'lat': curl_location['lat'],
            'lon': curl_location['lon'],
            'APPID': my_settings.openweather_key,
            'lang':'kr',
            'units':'metric'
        }
        url = 'http://api.openweathermap.org/data/2.5/weather'
        my_response = requests.get(url, params=location, timeout=5).json()

        address_get = self.get_address(curl_location['lat'], curl_location['lon'])
        
        temp_id_get = self.get_temp_id(my_response["main"]["temp"])
        temp_id_adj = self.adjust_temp(request, temp_id_get) 

        clothes = ClothesRecom()
        icon_lists = clothes.get_clothesicon_list(temp_id_adj)
        comment = clothes.get_weather_comments(temp_id_adj)
        my_response.update(
                {
                    'icon_lists':icon_lists,
                    'comment': comment,
                    'region_name': address_get["documents"][0]["address"]['region_2depth_name'],
                    'humid_cat':self.humid_category(my_response),
                    'wind_cat':self.wind_category(my_response),
                    'rain_cat':self.rain_category(my_response)
                }
            )
        
        return JsonResponse(my_response)

    def get_temp_id(self, cur_temp):

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

    def get_address(self, latitude, longitude):

        url = "https://dapi.kakao.com/v2/local/geo/coord2address.json"
        header = {'Authorization':my_settings.kakao_auth_key,}
        pa = {
            'x': longitude,
            'y': latitude
        }

        my_response = requests.get(url, headers=header, params=pa, timeout=5)

        return my_response.json()

    def adjust_temp(self, request, temp_id):
        try:
            user = request.user
            user_option = UserOption.objects.get(user=user)
            if temp_id <= 4 and user_option.hate_hot == True:
                return temp_id - 1 
            elif temp_id >= 7 and user_option.hate_cold == True:
                return temp_id + 1
            else:
                return temp_id
        except: 
            return temp_id

    def rain_category(self, my_response):
        if 'rain' in my_response:
            if my_response['rain']['3h'] < 10:
                return "부슬비"
            elif 10 <= my_response['rain']['3h'] < 35:
                return "강한비"
            else:
                return "호우주의보"
        elif 'snow' in my_response:
            return "눈내림"
        else:
            return "없음"

    def humid_category(self, my_response):
        humidity = my_response['main']['humidity']

        if humidity < 40:
            return "낮음"
        elif 40 <= humidity < 60: 
            return "적정"
        else:
            return "높음"

    def wind_category(self, my_response):
        wind_speed = my_response['wind']['speed']

        if wind_speed < 5.4:
            return "산들바람"
        elif 5.4 <= wind_speed < 13.9:
            return "센바람"
        else:
            return "주의보"
        
