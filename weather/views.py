import json
import random
import requests
import my_settings

from django.shortcuts import render
from django.views import View
from django.http import JsonResponse

from .models import TempIcon
from clothes.models import Cloth, ClothesIcon
from clothes.views import ClothesRecom
from user.views import *
from user.models import User, UserOption
from user.utils import login_decorator_pass

# https://openweathermap.org/current openapi 사용
class WeatherInfo(View):
    DEFAULT_LAT_SEOUL=37.5665       
    DEFAULT_LON_SEOUL=126.9780

    def create_random_clothes(select_cloth,temper_filter,select_cloth_id,user_gender,user,random_clothes):

        if len(select_cloth) == 0:
            temp_clothes_F = list(temper_filter.filter(user_gender="F").values('id','img_ref','page_ref'))
            temp_clothes_M = list(temper_filter.filter(user_gender="M").values('id','img_ref','page_ref'))

            if user_gender == "F":
                temp_clothes = temp_clothes_F
            elif user_gender == "M":
                temp_clothes = temp_clothes_M
            else:
                return JsonResponse({'message' : 'GENDER_NOT_EXIST'}, status=400)
            
            if user == None:
                my_temp_clothes = [
                    {   
                        "img_id"      : d["id"],
                        "img_ref"     : d["img_ref"],
                        "page_ref"    : d["page_ref"],
                        "heart_check" : False
                    } for d in temp_clothes
                ]
            else:
                my_temp_clothes = [
                    {
                        "img_id"      : d["id"],
                        "img_ref"     : d["img_ref"],
                        "page_ref"    : d["page_ref"],
                        "heart_check" : Cloth.objects.get(id = d['id']).hearts.filter(id = user.id).exists()
                    } for d in temp_clothes
                ]

            random_clothes = random.sample(my_temp_clothes, min(10,len(my_temp_clothes)))

            return random_clothes

        else:
            temp_clothes_F = list(temper_filter.filter(user_gender="F").exclude(id = int(select_cloth_id)).values('id','img_ref','page_ref'))
            temp_clothes_M = list(temper_filter.filter(user_gender="M").exclude(id = int(select_cloth_id)).values('id','img_ref','page_ref'))

            if user_gender == "F":
                temp_clothes = temp_clothes_F
            elif user_gender == "M":
                temp_clothes = temp_clothes_M
            else:
                return JsonResponse({'message' : 'GENDER_NOT_EXIST'}, status=400)
            
            if user == None:
                my_temp_clothes = [
                    {
                        "img_id"      : d["id"],
                        "img_ref"     : d["img_ref"],
                        "page_ref"    : d["page_ref"],
                        "heart_check" : False
                    } for d in temp_clothes
                ]
            else:
                my_temp_clothes = [
                    {
                        "img_id"      : d["id"],
                        "img_ref"     : d["img_ref"],
                        "page_ref"    : d["page_ref"],
                        "heart_check" : Cloth.objects.get(id = d['id']).hearts.filter(id = user.id).exists()
                    } for d in temp_clothes
                ]

            random_clothes = random.sample(my_temp_clothes, min(9,len(my_temp_clothes)))
            random_clothes.insert(0,select_cloth[0])
            
            return random_clothes


    @login_decorator_pass
    def post(self, request):
        curl_location = {}

        if not request.body:
            lat = self.DEFAULT_LAT_SEOUL
            lon = self.DEFAULT_LON_SEOUL
        else:
            curl_location = json.loads(request.body)
            lat = curl_location.get("lat", self.DEFAULT_LAT_SEOUL)
            lon = curl_location.get("lon", self.DEFAULT_LON_SEOUL)
        
    
        location = {
            'lat'  : lat,
            'lon'  : lon,
            'APPID': my_settings.openweather_key,
            'lang' :'kr',
            'units':'metric'
        }
        url = 'http://api.openweathermap.org/data/2.5/weather'

        my_response = requests.get(url, params=location, timeout=5).json()
        address_get = self.get_address(lat, lon)
        temp_id_get = self.get_temp_id(my_response["main"]["temp"])
        temp_id_adj = self.adjust_temp(request, temp_id_get) 
        
        now_temp   = my_response["main"]["temp"]
        clothes    = ClothesRecom()
        icon_lists = clothes.get_clothesicon_list(temp_id_adj)
        comment    = clothes.get_weather_comments(temp_id_adj)

        temper_filter  = Cloth.objects.filter(temp_max__gte=now_temp, temp_min__lte=now_temp)
        
        temp_clothes_F = list(temper_filter.filter(user_gender="F").values('id','img_ref'))
        temp_clothes_M = list(temper_filter.filter(user_gender="M").values('id','img_ref'))

        my_response.update(
                {
                    'icon_lists'  : icon_lists,
                    'comment'     : comment,
                    'region_name' : address_get["documents"][0]["address"]['region_2depth_name'],
                    'clothes_F'   : random.choice(temp_clothes_F), 
                    'clothes_M'   : random.choice(temp_clothes_M)
                }
            )
        
        return JsonResponse(my_response)

    @login_decorator_pass      
    def get(self, request):

        if request.GET.get("lat") == None and request.GET.get("lon") == None:
            lat = self.DEFAULT_LAT_SEOUL
            lon = self.DEFAULT_LON_SEOUL
        else:
            lat = request.GET.get("lat")
            lon = request.GET.get("lon")

        location = {           
            'lat'  : lat,    
            'lon'  : lon,    
            'APPID': my_settings.openweather_key,
            'lang' :'kr',
            'units':'metric'   
        }
        url = 'http://api.openweathermap.org/data/2.5/weather'

        my_response = requests.get(url, params=location, timeout=5).json()
        address_get = self.get_address(lat, lon)
        
        temp_id_get = self.get_temp_id(my_response["main"]["temp"])
        temp_id_adj = self.adjust_temp(request, temp_id_get) 
        
        now_temp     = my_response["main"]["temp"]
        clothes      = ClothesRecom()                                                                    
        icon_lists   = clothes.get_clothesicon_list(temp_id_adj)
        comment      = clothes.get_weather_comments(temp_id_adj)
        user_gender  = request.GET.get("user_gender")
        
        select_cloth_id = request.GET.get("img_id")
        select_cloth    = list(Cloth.objects.filter(id = select_cloth_id).values('id','img_ref','page_ref'))
        select_icon_ref = list(ClothesIcon.objects.filter(temp_icon_name__temp_id=temp_id_adj).values('id','naver_ref'))

        if hasattr(request, 'user'):
            user        = request.user
            user_option = UserOption.objects.get(user = user.id) 
            
            select_cloth = [
                {              
                    "img_id"      : d["id"],        
                    "img_ref"     : d["img_ref"],
                    "page_ref"    : d["page_ref"],
                    "heart_check" : Cloth.objects.get(id = d['id']).hearts.filter(id = user.id).exists()                                                                                
                } for d in select_cloth
            ]

            if UserOption.objects.filter(user=user).exists():
                if now_temp >= 17 and user_option.hate_hot == True:
                    now_temp += 5
                elif now_temp <= 9 and user_option.hate_cold == True:
                    now_temp -= 5
            
            if user_gender == None:
                user_gender = user.user_gender

            temper_filter  = Cloth.objects.filter(temp_max__gte=now_temp, temp_min__lte=now_temp)
            temp_clothes   = ''
            random_clothes = []

            random_clothes = WeatherInfo.create_random_clothes(select_cloth,temper_filter,select_cloth_id,user_gender,user,random_clothes)

        else:
            user = None
            if user_gender == None:
                user_gender = random.choice(["M","F"])
            
            select_cloth = [
                {
                    "img_id"      : d["id"],
                    "img_ref"     : d["img_ref"],
                    "page_ref"    : d["page_ref"],
                    "heart_check" : False
                } for d in select_cloth
            ]

            temp_clothes   = ''
            temper_filter  = Cloth.objects.filter(temp_max__gte=now_temp, temp_min__lte=now_temp)
            random_clothes = []

            random_clothes = WeatherInfo.create_random_clothes(select_cloth,temper_filter,select_cloth_id,user_gender,user,random_clothes)

        my_response.update(
                {
                    'icon_lists'   : icon_lists,
                    'comment'      : comment,
                    'humid_cat'    : self.humid_category(my_response),
                    'wind_cat'     : self.wind_category(my_response),
                    'rain_cat'     : self.rain_category(my_response),
                    'region_name'  : address_get["documents"][0]["address"]['region_2depth_name'],
                    'clothes_list' : random_clothes
                }
            )
        
        return JsonResponse(my_response)

    def get_temp_id(self, cur_temp):

        if cur_temp >= 27:
            temp_id = 1
        elif 23 <= cur_temp < 27:
            temp_id = 2
        elif 20 <= cur_temp < 23:
            temp_id = 3
        elif 17 <= cur_temp < 20:
            temp_id = 4
        elif 12 <= cur_temp < 17:
            temp_id = 5
        elif 9 <= cur_temp < 12:
            temp_id = 6
        elif 4 <=  cur_temp < 9:
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

    def rain_category(self, weather_info):
        if 'rain' in weather_info:
            if weather_info['rain']['3h'] < 10:
                return "부슬비"
            elif 10 <= weather_info['rain']['3h'] < 35:
                return "강한비"
            else:
                return "호우주의보"
        elif 'snow' in weather_info:
            return "눈내림"
        else:
            return "없음"

    def humid_category(self, weather_info):
        try:
            humidity = weather_info['main']['humidity']

            if humidity < 40:
                return "낮음"
            elif 40 <= humidity < 60: 
                return "적정"
            else:
                return "높음"
        except KeyError:
            return None

    def wind_category(self, weather_info):
        try:    
            wind_speed = weather_info['wind']['speed']

            if wind_speed < 5.4:
                return "산들바람"
            elif 5.4 <= wind_speed < 13.9:
                return "센바람"
            else:
                return "주의보"
        except KeyError:
            return None
