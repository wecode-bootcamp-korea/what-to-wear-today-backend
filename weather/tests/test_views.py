import json

from django.test import Client
from django.test import TestCase
from weather.views import WeatherInfo
from clothes.models import *
from weather.models import *

class WeatherTest(TestCase):

    def setUp(self):
        Cloth.objects.create(
                item_id="111",
                user_gender="M",
                img_ref="www1",
                page_ref="www1",
                temp_min=0,
                temp_max=50
        )
        Cloth.objects.create(
                item_id="112",
                user_gender="F",
                img_ref="www1",
                page_ref="www1",
                temp_min=0,
                temp_max=50
        )

        c = Client()

        test     = {'user_name':'test1', 'user_password':'1234', 'user_gender':'M'}
        response = c.post('/user', json.dumps(test), content_type="application/json")

    def test_get_temp_id(self):
        temp = WeatherInfo()
        c = temp.get_temp_id(30)
        self.assertEqual(c,1)

    def test_post_with_user(self):
        c = Client()
        test1        = {'user_name':'test1', 'user_password':'1234'}
        response     = c.post('/user/auth', json.dumps(test1), content_type="application/json")
        test_location= {'lat':37.54, 'lon':127.02}
        access_token = response.json()['access_token']
        response     = c.post('/weather', json.dumps(test_location), **{'HTTP_AUTHORIZATION':access_token, 'content_type':"application/json"})

        self.assertEqual(response.status_code, 200)

    def test_post_without_user(self):
        c = Client()
        test_location = {'lat':37.54,'lon':127.02}
        response = c.post('/weather', json.dumps(test_location), content_type="application/json")

        self.assertEqual(response.status_code, 200)

    def test_get_with_user(self):
        c = Client()

        test1        = {'user_name':'test1', 'user_password':'1234'}
        response     = c.post('/user/auth', json.dumps(test1), content_type="application/json")
        test_location= {'lat':37.54, 'lon':127.02}
        access_token = response.json()['access_token'] 
        response     = c.get('/weather', test_location, **{'HTTP_AUTHORIZATION':access_token, 'content_type':"application/json"})

        self.assertEqual(response.status_code, 200)

    def test_get_with_user_img(self):
        c = Client()

        test1        = {'user_name':'test1', 'user_password':'1234'}
        response     = c.post('/user/auth', json.dumps(test1), content_type="application/json")
        parameter    = {'lat':37.54, 'lon':127.02, 'img_id':1 }
        access_token = response.json()['access_token']
        response     = c.get('/weather', parameter, **{'HTTP_AUTHORIZATION':access_token, 'content_type':"application/json"})

        self.assertEqual(response.status_code, 200)
    
    def test_get_without_user(self):
        c = Client()

        test_location = {'lat':37.54, 'lon':127.02, 'user_gender':'M'}
        response      = c.get('/weather', test_location, content_type="application/json")

        self.assertEqual(response.status_code, 200)
   
    def test_get_without_user_img(self):
        c = Client()

        parameter    = {'lat':37.54, 'lon':127.02, 'img_id':1, 'user_gender':'M'}
        response     = c.get('/weather', parameter, content_type="application/json")

        self.assertEqual(response.status_code, 200)
   
    def tearDown(self):
        Cloth.objects.filter(item_id="111").delete()
        Cloth.objects.filter(item_id="112").delete()
        User.objects.filter(user_name="test1").delete()
