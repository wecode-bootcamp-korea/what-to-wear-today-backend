import json
                               
from user.models import User   
from clothes.models import Cloth

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
    
    def test_user_heart_cloth(self):
        c = Client()           
    
        test1        = {'user_name':'test1', 'user_password':'1234'}
        response     = c.post('/user/auth', json.dumps(test1), content_type="application/json")
        access_token = response.json()['access_token'] 

        test2    = {'img_id':'1'}       
        cloth    = Cloth.objects.get(id = test2['img_id'])
        c.post('/clothes/heart', json.dumps(test2), **{'HTTP_AUTHORIZATION':access_token, 'content_type':"application/json"})
        response = c.get('/clothes/heart', **{'HTTP_AUTHORIZATION':access_token, 'content_type':"application/json"})
        
        hearts_list = list(Cloth.objects.filter(hearts__id=1).values('pk', 'img_ref'))
        cloth_id    = [{'img_id' : d['pk'], 'img_ref' : d['img_ref'], 'total_hearts' : Cloth.objects.get(id = d['pk']).total_hearts} for d in hearts_list]
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"heart_list" : list(reversed(cloth_id))})

    def tearDown(self):
        Cloth.objects.filter(item_id="111").delete()
        User.objects.filter(user_name="test1").delete()

