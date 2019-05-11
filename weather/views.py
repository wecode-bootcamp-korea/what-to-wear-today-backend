import json
import random
import requests
import my_settings

from django.shortcuts import render
from django.views import View
from django.http import JsonResponse

from clothes.models import Cloth
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
            'lat'  : curl_location['lat'],
            'lon'  : curl_location['lon'],
            'APPID': my_settings.openweather_key,
            'lang' :'kr',
            'units':'metric'
        }
        url = 'http://api.openweathermap.org/data/2.5/weather'

        my_response = requests.get(url, params=location, timeout=5).json()
        address_get = self.get_address(curl_location['lat'], curl_location['lon'])
        temp_id_get = self.get_temp_id(my_response["main"]["temp"])
        temp_id_adj = self.adjust_temp(request, temp_id_get) 
        
        now_temp   = my_response["main"]["temp"]
        clothes    = ClothesRecom()
        icon_lists = clothes.get_clothesicon_list(temp_id_adj)
        comment    = clothes.get_weather_comments(temp_id_adj)

        temper_filter  = Cloth.objects.filter(temp_max__gte=now_temp).filter(temp_min__lte=now_temp)
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
        location = {           
            'lat'  : request.GET.get("lat"),    
            'lon'  : request.GET.get("lon"),    
            'APPID': my_settings.openweather_key,
            'lang' :'kr',
            'units':'metric'   
        }
        url = 'http://api.openweathermap.org/data/2.5/weather'

        my_response = requests.get(url, params=location, timeout=5).json()
        address_get = self.get_address(request.GET.get("lat"), request.GET.get("lon"))
        
        temp_id_get = self.get_temp_id(my_response["main"]["temp"])
        temp_id_adj = self.adjust_temp(request, temp_id_get) 
        
        now_temp     = my_response["main"]["temp"]
        clothes      = ClothesRecom()                                                                    
        icon_lists   = clothes.get_clothesicon_list(temp_id_adj)
        comment      = clothes.get_weather_comments(temp_id_adj)
        user_gender  = request.GET.get("user_gender")
        
        select_cloth_id = request.GET.get("img_id")
        select_cloth    = list(Cloth.objects.filter(id = select_cloth_id).values('id','img_ref'))

        if hasattr(request, 'user'):
            user = request.user

            select_cloth = [
                {              
                    "img_id"      : d["id"],        
                    "img_ref"     : d["img_ref"],   
                    "heart_check" : Cloth.objects.get(id = d['id']).hearts.filter(id = user.id).exists()                                                                                
                } for d in select_cloth
            ]
            
            try:
                user_option = UserOption.objects.get(user=user)
                if now_temp >= 17 and user_option.hate_hot == True:
                    now_temp += 5
                elif now_temp <= 9 and user_option.hate_cold == True:
                    now_temp -= 5
            except ObjectDoesNotExist:
                pass

            temper_filter  = Cloth.objects.filter(temp_max__gte=now_temp).filter(temp_min__lte=now_temp)
            temp_clothes   = ''
            temp_clothes_F = list(temper_filter.filter(user_gender="F").values('id','img_ref'))
            temp_clothes_M = list(temper_filter.filter(user_gender="M").values('id','img_ref'))

            if user.user_gender == "F":
                temp_clothes = temp_clothes_F
            elif user.user_gender == "M":
                temp_clothes = temp_clothes_M
            else:
                return JsonResponse({'message' : 'GENDER_NOT_EXIST'}, status=400)
            
            my_temp_clothes = [
                {
                    "img_id"      : d['id'],
                    "img_ref"     : d['img_ref'],
                    "heart_check" : Cloth.objects.get(id = d['id']).hearts.filter(id = user.id).exists()
                } for d in temp_clothes
            ]
            
            random_clothes = random.sample(my_temp_clothes, min(10,len(my_temp_clothes)))

            if len(select_cloth) == 0:
                pass
            else:
                for d in random_clothes:
                    if d.get("img_id") == select_cloth_id:
                        random_clothes.remove(d)
                        random_clothes.insert(0, select_cloth[0])
                        break
                    else:
                        random_clothes.insert(0, select_cloth[0])
                        break
        else:
            temp_clothes   = ''
            temper_filter  = Cloth.objects.filter(temp_max__gte=now_temp).filter(temp_min__lte=now_temp)
            temp_clothes_F = list(temper_filter.filter(user_gender="F").values('id','img_ref'))
            temp_clothes_M = list(temper_filter.filter(user_gender="M").values('id','img_ref'))
            select_cloth   = [    
                {              
                    "img_id"      : d["id"],        
                    "img_ref"     : d["img_ref"],   
                    "heart_check" : False                                                                                
                } for d in select_cloth 
            ]
            
            if user_gender == "F":
                temp_clothes = temp_clothes_F
            elif user_gender == "M":
                temp_clothes = temp_clothes_M
            else:
                return JsonResponse({'message' : 'GENDER_INVALID'}, status=400)
            
            my_temp_clothes = [
                {
                    "img_id"      : d['id'],
                    "img_ref"     : d['img_ref'],
                    "heart_check" : False
                } for d in temp_clothes
            ]

            random_clothes = random.sample(my_temp_clothes, min(10,len(my_temp_clothes)))

            if len(select_cloth) == 0:
                pass
            else:
                for d in random_clothes:
                    if d.get("img_id") == select_cloth_id:
                        random_clothes.remove(d)
                        random_clothes.insert(0, select_cloth[0])
                        break
                    else:
                        random_clothes.insert(0, select_cloth[0])
                        break

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
