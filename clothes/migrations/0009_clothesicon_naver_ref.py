# Generated by Django 2.2 on 2019-05-15 06:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clothes', '0008_auto_20190513_0548'),
    ]

    operations = [
        migrations.AddField(
            model_name='clothesicon',
            name='naver_ref',
            field=models.CharField(default=None, max_length=2500),
        ),
    ]
