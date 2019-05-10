from django.db import models
from clothes.models import ClothesIcon, ClothesComment

class TemperatureCriteria(models.Model):
    temp_id = models.IntegerField()
    temp_min = models.IntegerField()
    temp_max = models.IntegerField()
    clothes = models.ManyToManyField(ClothesIcon)
    clothes_comments = models.ManyToManyField(ClothesComment)

    class Meta:
        ordering = ('temp_id',)
        db_table = "temperature"
