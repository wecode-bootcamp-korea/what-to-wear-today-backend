import jwt
import json
import bcrypt

from django.views import View
from django.http import JsonResponse, HttpResponse
from django.core import serializers

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
        user = request.user
        hearts_list = Cloth.objects.filter(hearts__id=user.id)
        print(list(hearts_list))
        return JsonResponse({'hearts_list' : json.loads(serializers.serialize('json', hearts_list))})
