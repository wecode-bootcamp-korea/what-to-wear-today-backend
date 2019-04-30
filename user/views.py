from django.http import JsonResponse, HttpResponse
from .models import User
from django.views import View
import json
import bcrypt

class UserInfo(View):

    def post(self, request):
        new_user = json.loads(request.body)
        password = bytes(new_user['user_password'], "utf-8")
        hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())

        User(
            user_name = new_user['user_name'],
            user_password = hashed_password,
            user_gender = new_user['user_gender']
        ).save()

        return HttpResponse(status=200)
