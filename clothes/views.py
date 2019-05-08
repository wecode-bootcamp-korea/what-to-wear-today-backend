import json
from operator import itemgetter

from django.views import View
from django.http import JsonResponse, HttpResponse

from user.models import User
from .models import Cloth
from user.utils import login_decorator

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
        hearts_list = list(Cloth.objects.filter(hearts__id=user.id).values('pk', 'img_ref'))
        cloth_id    = [{'img_id' : d['pk'], 'img_ref' : d['img_ref'], 'total_hearts' : Cloth.objects.get(id = d['pk']).total_hearts} for d in hearts_list]

        return JsonResponse({'heart_list' : list(reversed(cloth_id))})


class TopImageView(View):

    def get(self, request):
        number            = json.loads(request.body)
        top_number        = number['top_number']
        hearts_list       = list(Cloth.objects.all().values('hearts__id').values('pk').distinct())
        total_hearts_list = [{"img_id" : d['pk'], "total_hearts" : Cloth.objects.get(id = d['pk']).total_hearts} for d in hearts_list]
        data              = sorted(total_hearts_list, key = itemgetter('total_hearts'))
        data.reverse()
        top               = data[0 : min(int(top_number),len(data))]
        
        return JsonResponse({'top_list' : top})
