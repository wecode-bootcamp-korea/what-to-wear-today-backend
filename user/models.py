from django.db import models
from enum import Enum

class Gender(Enum):
    MALE = 'M'
    FEMALE = 'F'

    @classmethod
    def choices(cls):
        return [(tag, tag.value) for tag in Gender]

class User(models.Model):
    user_name = models.CharField(max_length=20)
    user_password = models.CharField(max_length=20)
    user_gender = models.CharField(max_length=3, choices = Gender.choices())    
    class Meta:
        db_table = "users"
    

