from django.http import JsonResponse, HttpResponse
from .models import User
from django.views import View
import json
import bcrypt
import jwt
from django.core.exceptions import ObjectDoesNotExist

def login_decorator(f):
    def wrapper(self, request, *args, **kwargs):
        access_token = request.headers.get('Authorization', None)

        try:
            if access_token:
                decoded = jwt.decode(access_token, 'secret', algorithms=['HS256'])
                print(decoded)
                user_id = decoded["user_id"]
                user = User.objects.get(id=user_id)
                request.user = user

                return f(self, request, *args, **kwargs)
            else:
                return HttpResponse(status=401)
        except jwt.DecodeError:
            print(access_token)
            return HttpResponse(status=401)

    return wrapper


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


class InfoView(View):

    @login_decorator
    def get(self, request):
        return JsonResponse({
            'user_name' : request.user.user_name
        })

class LoginView(View):
    
    def post(self, request):
        login_user = json.loads(request.body)

        try: 
            user = User.objects.get(user_name=login_user['user_name'])
            encoded_jwt_id = jwt.encode({'user_id' : user.id}, 'secret', algorithm='HS256')

            if bcrypt.checkpw(login_user['user_password'].encode("UTF-8"), user.user_password.encode("UTF-8")):
               # print(encoded_jwt_id.decode("UTF-8"))
                return JsonResponse({"access_token" : encoded_jwt_id.decode("UTF-8")})
            else:
                return HttpResponse(status=401)

        except ObjectDoesNotExist:
            return HttpResponse(status=401)
        except Exception as e:
            print(e)
            return HttpResponse(status=500)
