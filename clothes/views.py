import json

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
        cloth_id = cloth['id']
        cloth    = Cloth.objects.get(id = cloth_id)

        if cloth.hearts.filter(id = user.id).exists():
            cloth.hearts.remove(user)
            message = 'Unheart cloth'
        else:
            cloth.hearts.add(user)
            message = 'Heart cloth'

        return JsonResponse({"hearts_count" : cloth.total_hearts, "message" : message})
    
    @login_decorator
    def get(self, request):
        user        = request.user
        hearts_list = list(Cloth.objects.filter(hearts__id=user.id).values('pk'))
        cloth_id    = [d['pk'] for d in hearts_list]

        return JsonResponse({'cloth_id' : list(reversed(cloth_id))})
