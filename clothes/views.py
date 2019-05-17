import json
from operator import itemgetter

from django.views import View
from django.http import JsonResponse, HttpResponse

from user.models import User
from .models import Cloth, HeartTime
from user.utils import login_decorator,login_decorator_pass

class HeartView(View):

    @login_decorator
    def post(self, request):
        user     = request.user
        cloth    = json.loads(request.body)
        cloth_id = cloth['img_id']
        cloth    = Cloth.objects.get(id = cloth_id)

        if cloth.hearts.filter(id = user.id).exists():
            cloth.hearts.remove(user)
            heart_cloth = False
        else:
            cloth.hearts.add(user)
            heart_cloth = True

        return JsonResponse({"total_hearts" : cloth.total_hearts, "heart_cloth" : heart_cloth})
    
    @login_decorator
    def get(self, request):
        user        = request.user
        hearts      = HeartTime.objects.filter(user_id=user.id).values('cloth_id','heart_time').order_by('-heart_time')
        hearts_list = list(hearts)
        cloth_id    = [
            {
                'img_id'       : d['cloth_id'], 
                'img_ref'      : Cloth.objects.get(id = d['cloth_id']).img_ref,
                'page_ref'     : Cloth.objects.get(id = d['cloth_id']).page_ref,
                'total_hearts' : Cloth.objects.get(id = d['cloth_id']).total_hearts
            } for d in hearts_list
        ]

        return JsonResponse({'hearts_list' : cloth_id})

class ClothesRecom(View):

    def get_clothesicon_list(self, temp_id):

        clothes_icon_list = {
            1: [1,2,3,4],
            2: [2,5,6,7],
            3: [8,9,7,10],
            4: [11,12,13,10],
            5: [14,13,15,16,10,7],
            6: [14,17,15,18,10],
            7: [19,20,21,18,22],
            8: [23,24,25,26],
        }

        return clothes_icon_list[temp_id]

    def get_weather_comments(self, temp_id):

        weather_comment = {
            1: '더워도 이렇게 더울 수 있을까. 에어컨이 필요한 날씨입니다.',
            2: '덥지만, 더더욱 열정적이고 신나는 하루 보내시길 바랍니다.',
            3: '셔츠나 얇은 긴팔을 입어도 좋을 날씨에요!',
            4: '황금 날씨! 나들이 가기 딱 좋아요~',
            5: '옷 잘못 입고 나오셨다가 어깨를 잔뜩 움추린 분들이 보입니다.',
            6: '본격적인 월동준비의 시작이죠.',
            7: '추위에 아랑곳하지 않고, 열심히 땀 흘리며 뛰어 놀던 옛 시절이 그립습니다.',
            8: '완전무장! 목도리와 장갑도 필수!',
        }

        return weather_comment[temp_id]

class TopImageView(View):
    
    @login_decorator_pass
    def get(self, request):
        top_number        = request.GET.get("top_number")
        hearts_list       = list(HeartTime.objects.values('cloth_id').distinct())
        
        if hasattr(request, 'user'):
            user = request.user
            if len(hearts_list) == 0:
                return JsonResponse({"message" : "NO_HEARTS_LIST"})
            else:
                total_hearts_list = [
                        {
                            "img_id"       : d['cloth_id'],
                            "img_ref"      : Cloth.objects.get(id = d['cloth_id']).img_ref,
                            "page_ref"     : Cloth.objects.get(id = d['cloth_id']).page_ref,
                            "total_hearts" : Cloth.objects.get(id = d['cloth_id']).total_hearts,
                            "heart_check"  : Cloth.objects.get(id = d['cloth_id']).hearts.filter(id = user.id).exists()
                        } for d in hearts_list
                ]
        else:
            if len(hearts_list) == 0:
                return JsonResponse({"message" : "NO_HEARTS_LIST"})
            else:
                total_hearts_list = [
                        {
                            "img_id"       : d['cloth_id'],
                            "img_ref"      : Cloth.objects.get(id = d['cloth_id']).img_ref,
                            "page_ref"     : Cloth.objects.get(id = d['cloth_id']).page_ref,
                            "total_hearts" : Cloth.objects.get(id = d['cloth_id']).total_hearts,
                            "heart_check"  : False
                        } for d in hearts_list
                ]
            
        data = sorted(total_hearts_list, key = itemgetter('total_hearts'))
        data.reverse()
        
        top = data[0 : min(int(top_number),len(data))]
        
        return JsonResponse({'top_list' : top})

class HeartCheck(View):
    @login_decorator
    def get(self, request):
        user        = request.user
        cloth_id_get = request.GET.get('cloth_id')

        try:
            cloth_id_exists = HeartTime.objects.filter(user_id=user.id).get(cloth_id=cloth_id_get).cloth_id
            has_heart = True
        except HeartTime.DoesNotExist:
            cloth_id_exists = None
            has_heart = False

        heart_info  = {
                'cloth_id'     : cloth_id_exists, 
                'has_heart': has_heart,
            }

        return JsonResponse({'heart' : heart_info})
