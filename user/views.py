import jwt
import json
import bcrypt                  

from django.views import View
from django.http import JsonResponse, HttpResponse
from django.core.exceptions import ObjectDoesNotExist

from .models import User, UserOption
from .utils import login_decorator
from whattowear.settings import wtwt_secret

class UserView(View):

    def post(self, request):
        new_user = json.loads(request.body)

        if User.objects.filter(user_name=new_user['user_name']).exists():
            return JsonResponse({'message' : 'USERNAME_EXIST'}, status=400)
        else:
            password = bytes(new_user['user_password'], "utf-8")
            hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())

            new_user = User(
                user_name = new_user['user_name'],
                user_password = hashed_password.decode("UTF-8"),
                user_gender = new_user['user_gender']
            )
            new_user.save()

            user_settings = UserOption(
                hate_hot = False,
                hate_cold = False,
                user = new_user
            )
            user_setting.save()

            return JsonResponse({'message' : 'SIGNUP_SUCCESS'}, status=200)

    @login_decorator
    def get(self, request):
        return JsonResponse({
            'user_name' : request.user.user_name
        })

class CredentialView(View):

    @login_decorator
    def post(self, request):
        user = request.user
        new_login_user = json.loads(request.body)
       
        if 'user_name' in new_login_user:
            if User.objects.filter(user_name=new_login_user['user_name']).exists():
                return JsonResponse({'message' : 'USERNAME_EXIST'}, status=400)
            else:    
                password = bytes(new_login_user['user_password'], "utf-8")
                hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())
            
                User.objects.filter(id=user.id).update(user_name = new_login_user['user_name'])
                User.objects.filter(id=user.id).update(user_password = hashed_password.decode("UTF-8"))

                return JsonResponse({'message' : 'CREDENTIAL_SUCCESS'}, status=200)
        elif 'user_password' in new_login_user:
            password = bytes(new_login_user['user_password'], "utf-8")
            hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())                                                                        
                           
            User.objects.filter(id=user.id).update(user_password = hashed_password.decode("UTF-8"))                                            

            return JsonResponse({'message' : 'CREDENTIAL_SUCCESS'}, status=200)
        else:
            return JsonResponse({'message' : 'CREDENTIAL_FAIL'}, status=400)
 

class AuthView(View):
    
    def post(self, request):
        login_user = json.loads(request.body)

        try: 
            user = User.objects.get(user_name=login_user['user_name'])
            encoded_jwt_id = jwt.encode({'user_id' : user.id}, wtwt_secret, algorithm='HS256')

            if bcrypt.checkpw(login_user['user_password'].encode("UTF-8"), user.user_password.encode("UTF-8")):
                return JsonResponse({"access_token" : encoded_jwt_id.decode("UTF-8")})
            else:
                return JsonResponse({'message' : 'PASSWORD_INVALID'}, status=400)

        except ObjectDoesNotExist:
            return JsonResponse({'message' : 'USERNAME_NOT_EXIST'}, status=400)
        except Exception as e:
            print(e)
            return HttpResponse(status=500)

class UserSettingView(View):

    @login_decorator
    def get(self, request):
        user_info = UserOption.objects.get(user = request.user.id)
        return JsonResponse({
                'user_name' : request.user.user_name,
                'user_gender' : request.user.user_gender,
                'hate_hot' : user_info.hate_hot,
                'hate_cold' : user_info.hate_cold
            })

class UserSettingUpdateView(View):

    @login_decorator
    def post(self, request):

        try:
            user = request.user
            u_setting = json.loads(request.body)

            user.user_gender = u_setting["user_gender"]
            user.save()

            user_setting = UserOption.objects.get(user = request.user.id)
            user_setting.hate_hot = u_setting["hate_hot"]
            user_setting.hate_cold = u_setting["hate_cold"]
            user_setting.save()

            return HttpResponse(status=200)
        
        except ObjectDoesNotExist:
            return HttpResponse(status=401)

