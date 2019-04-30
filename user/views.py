from django.http import JsonResponse, HttpResponse
from .models import User
from django.views import View
import json

class UserInfo(View):

    def post(self, request):
        new_user = json.loads(request.body)
        
        User(
            user_name = new_user['user_name'],
            user_password = new_user['user_password'],
            user_gender = new_user['user_gender']
        ).save()

        return HttpResponse(status=200)
