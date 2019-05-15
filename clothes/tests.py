import json
from operator import itemgetter

from user.models import User
from clothes.models import Cloth, HeartTime

from django.test import Client
from django.test import TestCase

class ClothTest(TestCase):

    def setUp(self):
        Cloth.objects.create(
                item_id="111",
                user_gender="M",
                img_ref="www1",
                page_ref="www1",
                temp_min=1,
                temp_max=10
        )

        c = Client()

        test     = {'user_name':'test1', 'user_password':'1234', 'user_gender':'M'}
        response = c.post('/user', json.dumps(test), content_type="application/json")

    def test_user_heart_check(self):
        c = Client()

        test1        = {'user_name':'test1', 'user_password':'1234'}
        response     = c.post('/user/auth', json.dumps(test1), content_type="application/json")
        access_token = response.json()['access_token']

        cloth_img = Cloth.objects.get(item_id='111')
        test2    = {'img_id':cloth_img.id}
        cloth    = Cloth.objects.get(id = test2['img_id'])
        response = c.post('/clothes/heart', json.dumps(test2), **{'HTTP_AUTHORIZATION':access_token, 'content_type':"application/json"})
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"total_hearts" : cloth.total_hearts, "heart_cloth" : True})

    def test_user_heart_list(self):
        c = Client()
        test1        = {'user_name':'test1', 'user_password':'1234'}
        response     = c.post('/user/auth', json.dumps(test1), content_type="application/json")
        access_token = response.json()['access_token']
        
        cloth_img = Cloth.objects.get(item_id='111')
        test2    = {'img_id':cloth_img.id}
        cloth    = Cloth.objects.get(id = test2['img_id'])
        c.post('/clothes/heart', json.dumps(test2), **{'HTTP_AUTHORIZATION':access_token, 'content_type':"application/json"})
        response = c.get('/clothes/heart', **{'HTTP_AUTHORIZATION':access_token, 'content_type':"application/json"})
        
        user = User.objects.get(user_name='test1')
        hearts_list = list(HeartTime.objects.filter(user_id=user.id).values('cloth_id','heart_time').order_by('-heart_time'))
        cloth_id    = [
                {
                    'img_id'       : d['cloth_id'],
                    'img_ref'      : Cloth.objects.get(id = d['cloth_id']).img_ref,
                    'page_ref'     : Cloth.objects.get(id = d['cloth_id']).page_ref,
                    'total_hearts' : Cloth.objects.get(id = d['cloth_id']).total_hearts
                } for d in hearts_list
        ]
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"hearts_list" : cloth_id})
    
    def test_user_top_list(self):
        c = Client()
        test1        = {'user_name':'test1', 'user_password':'1234'}
        response     = c.post('/user/auth', json.dumps(test1), content_type="application/json")
        access_token = response.json()['access_token']
        user         = User.objects.get(user_name='test1')

        cloth_img = Cloth.objects.get(item_id='111')
        test2    = {'img_id':cloth_img.id}
        cloth    = Cloth.objects.get(id = test2['img_id'])        
        c.post('/clothes/heart', json.dumps(test2), **{'HTTP_AUTHORIZATION':access_token, 'content_type':"application/json"})

        parameter  = {'top_number':3}
        response   = c.get('/clothes/top', parameter, **{'HTTP_AUTHORIZATION':access_token, 'content_type':"application/json"})
        top_number = parameter['top_number']

        hearts_list       = list(HeartTime.objects.values('cloth_id').distinct())
        total_hearts_list = [
                        {
                            "img_id"       : d['cloth_id'],
                            "img_ref"      : Cloth.objects.get(id = d['cloth_id']).img_ref,
                            "page_ref"     : Cloth.objects.get(id = d['cloth_id']).page_ref,
                            "total_hearts" : Cloth.objects.get(id = d['cloth_id']).total_hearts,
                            "heart_check"  : Cloth.objects.get(id = d['cloth_id']).hearts.filter(id = user.id).exists()
                        } for d in hearts_list
                ]

        data = sorted(total_hearts_list, key = itemgetter('total_hearts'))
        data.reverse()

        top = data[0 : min(int(top_number),len(data))]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"top_list" : top})

    def test_top_list(self):
        c = Client()
        test1        = {'user_name':'test1', 'user_password':'1234'}
        response     = c.post('/user/auth', json.dumps(test1), content_type="application/json")
        access_token = response.json()['access_token']

        cloth_img = Cloth.objects.get(item_id='111')
        test2    = {'img_id':cloth_img.id}
        cloth    = Cloth.objects.get(id = test2['img_id'])
        c.post('/clothes/heart', json.dumps(test2), **{'HTTP_AUTHORIZATION':access_token, 'content_type':"application/json"})

        parameter = {'top_number':3}
        response = c.get('/clothes/top', parameter, content_type="application/json")
        top_number = parameter['top_number']

        hearts_list       = list(HeartTime.objects.values('cloth_id').distinct())
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

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"top_list" : top})

    def test_no_top_list(self):
        c = Client()
        
        parameter = {'top_number':3}
        response = c.get('/clothes/top', parameter, content_type="application/json")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message" : "NO_HEARTS_LIST"})

    def test_user_heart_check(self):
        c = Client()

        test1        = {'user_name':'test', 'user_password':'test'}
        response     = c.post('/user/auth', json.dumps(test1), content_type="application/json")
        access_token = response.json()['access_token']

        parameter = {'cloth_id' : 3346}
        response = c.get('/clothes/heart/check', parameter, content_type="application/json")
        heart_info  = {
            'img_id'     : 3446, 
            'heart_check': True 
         }
            
        self.assertEqual(response.status_code, 200)

    def tearDown(self):
        Cloth.objects.filter(item_id="111").delete()
        User.objects.filter(user_name="test1").delete()
