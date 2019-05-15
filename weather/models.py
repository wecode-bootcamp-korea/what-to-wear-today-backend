from django.db import models
from clothes.models import ClothesIcon, ClothesComment

class TemperatureCriteria(models.Model):
    temp_id = models.IntegerField()
    temp_min = models.IntegerField()
    temp_max = models.IntegerField()
    clothes = models.ManyToManyField(ClothesIcon)
    clothes_comments = models.ManyToManyField(ClothesComment)
    clothes_icon = models.ManyToManyField(ClothesIcon, through='TempIcon', related_name='temp_icon_name' )

    class Meta:
        ordering = ('temp_id',)
        db_table = "temperature"

class TempIcon(models.Model):
   icon = models.ForeignKey(ClothesIcon, on_delete=models.CASCADE)
   temp = models.ForeignKey(TemperatureCriteria, on_delete=models.CASCADE)

   class Meta:
       db_table = "temp_icon"
