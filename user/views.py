from django.http import JsonResponse, HttpResponse
from .models import User
from django.views import View
import json
import bcrypt

class UserView(View):

    def post(self, request):
        new_user = json.loads(request.body)
        password = bytes(new_user['user_password'], "utf-8")
        hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())

        User(
            user_name = new_user['user_name'],
            user_password = hashed_password.decode("UTF-8"),
            user_gender = new_user['user_gender']
        ).save()

        return HttpResponse(status=200)

class LoginView(View):

    def post(self, request):
        login_user = json.loads(request.body)

        try: 
            user = User.objects.get(user_name=login_user['user_name'])

            if bcrypt.checkpw(login_user['user_password'].encode("UTF-8"), user.user_password.encode("UTF-8")):
                return JsonResponse({"Success" : True})
            else:
                return HttpResponse(status=401)

        except DoesNotExist:
            return HttpResponse(status=401)
        except Exception as e:
            return HttpResponse(status=500)

