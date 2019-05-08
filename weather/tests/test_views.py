import unittest
from ..views import GetWeatherInfo

class MyTest(unittest.TestCase):

    def test_get_temp_id(self):
        c = GetWeatherInfo.get_temp_id(30)
        self.assertEqual(c,1)

    def test_get_clothes_list(self):
        c = GetWeatherInfo.get_clothes_list(1)
        self.assertEqual(c,[1,2,3,5])
