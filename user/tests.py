import json

from user.models import User

from django.test import Client
from django.test import TestCase

class UserTest(TestCase):

    def setUp(self):
        c = Client()

        test     = {'user_name':'test1', 'user_password':'1234', 'user_gender':'M'}
        response = c.post('/user', json.dumps(test), content_type="application/json")
    
    def test_user_signup_check(self):
        c = Client()

        test         = {'user_name':'test2', 'user_password':'1234', 'user_gender':'M'}
        response     = c.post('/user', json.dumps(test), content_type="application/json")
        self.assertEqual(response.status_code, 200)

    def test_user_signup_id_check(self):
        c = Client()

        test         = {'user_name':'test1', 'user_password':'1234'}
        response     = c.post('/user', json.dumps(test), content_type="application/json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message' : '이미 존재하는 아이디입니다.'})

    def test_user_credential_check(self):
        c = Client()

        test         = {'user_name':'test1', 'user_password':'1234'}
        response     = c.post('/user/auth', json.dumps(test), content_type="application/json")
        access_token = response.json()['access_token']

        test         = {'user_name':'test2', 'user_password':'1234'}
        response     = c.post('/user/credential', json.dumps(test), **{'HTTP_AUTHORIZATION':access_token, 'content_type':"application/json"})
        self.assertEqual(response.status_code, 200)

    def test_user_credential_id_check(self):
        c = Client()

        test         = {'user_name':'test1', 'user_password':'1234'}
        response     = c.post('/user/auth', json.dumps(test), content_type="application/json")
        access_token = response.json()['access_token']

        test         = {'user_name':'test1', 'user_password':'1234'}
        response     = c.post('/user/credential', json.dumps(test), **{'HTTP_AUTHORIZATION':access_token, 'content_type':"application/json"})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message' : '이미 존재하는 아이디입니다.'})

    def test_user_credential_pw_check(self):
        c = Client()

        test         = {'user_name':'test1', 'user_password':'1234'}
        response     = c.post('/user/auth', json.dumps(test), content_type="application/json")
        access_token = response.json()['access_token']

        test         = {'user_password':'12qwas'}
        response     = c.post('/user/credential', json.dumps(test), **{'HTTP_AUTHORIZATION':access_token, 'content_type':"application/json"})
        self.assertEqual(response.status_code, 200)

    def test_user_auth_check(self):
        c = Client()

        test         = {'user_name':'test1', 'user_password':'1234'}
        user         = User.objects.get(user_name=test['user_name'])
        response     = c.post('/user/auth', json.dumps(test), content_type="application/json")
        access_token = response.json()['access_token']

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
                response.json(), 
                    {
                        "access_token" : access_token,
                        "user_gender" : user.user_gender
                    }
        )

    def test_user_info_check(self):
        c = Client()

        test         = {'user_name':'test1', 'user_password':'1234'}
        response     = c.post('/user/auth', json.dumps(test), content_type="application/json")
        access_token = response.json()['access_token']
        
        response     = c.get('/user', **{'HTTP_AUTHORIZATION':access_token, 'content_type':"application/json"})
        
        self.assertEqual(response.status_code, 200)

    def tearDown(self):
        User.objects.filter(user_name="test1").delete()
