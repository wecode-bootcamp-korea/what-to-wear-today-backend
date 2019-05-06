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
            return HttpResponse(status=409)
        else:
            password = bytes(new_user['user_password'], "utf-8")
            hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())

            create_user = User(
                user_name = new_user['user_name'],
                user_password = hashed_password.decode("UTF-8"),
                user_gender = new_user['user_gender']
            )
            create_user.save()

            user_setting = UserOption(
                HATEHOT = False,
                HATECOLD = False,
                user = create_user
            )
            user_setting.save()
            return HttpResponse(status=200)

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
                return HttpResponse(status=409)
            else:    
                password = bytes(new_login_user['user_password'], "utf-8")
                hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())
            
                User.objects.filter(id=user.id).update(user_name = new_login_user['user_name'])
                User.objects.filter(id=user.id).update(user_password = hashed_password.decode("UTF-8"))

                return HttpResponse(status=200)
        elif 'user_password' in new_login_user:
            password = bytes(new_login_user['user_password'], "utf-8")
            hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())                                                                        
                           
            User.objects.filter(id=user.id).update(user_password = hashed_password.decode("UTF-8"))                                            

            return HttpResponse(status=200)
        else:
            return HttpResponse(status=401)
 

class AuthView(View):
    
    def post(self, request):
        login_user = json.loads(request.body)

        try: 
            user = User.objects.get(user_name=login_user['user_name'])
            encoded_jwt_id = jwt.encode({'user_id' : user.id}, wtwt_secret, algorithm='HS256')

            if bcrypt.checkpw(login_user['user_password'].encode("UTF-8"), user.user_password.encode("UTF-8")):
                return JsonResponse({"access_token" : encoded_jwt_id.decode("UTF-8")})
            else:
                return HttpResponse(status=401)

        except ObjectDoesNotExist:
            return HttpResponse(status=401)
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
                'hate_hot' : user_info.HATEHOT,
                'hate_cold' : user_info.HATECOLD
            })


class UserSettingUpdateView(View):


    @login_decorator
    def post(self, request):

        try:
            user = request.user
            u_setting = json.loads(request.body)
            user_setting = UserOption.objects.get(user = request.user.id)
            user.user_gender = u_setting["user_gender"]
            user.save()
            user_setting.HATEHOT = u_setting["hate_hot"]
            user_setting.HATECOLD = u_setting["hate_cold"]
            user_setting.save()
            #print(update_info.values())
            return HttpResponse(status=200)
        
        except ObjectDoesNotExist:
            return HttpResponse(status=401)

