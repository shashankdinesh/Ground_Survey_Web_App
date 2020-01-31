from django.db import models

class Users (models.Model):
    username=models.CharField(max_length=50, null=True)
    password=models.CharField(max_length=50, null=True)
    phone_number=models.CharField (max_length=50, null=True)
    object = models.Manager()

class datanew (models.Model):
    lat = models.FloatField(max_length=50, null=True)
    lon = models.FloatField(max_length=50, null=True)
    ele = models.FloatField(max_length=50, null=True)
    loki=models.CharField (max_length=50, null=True)
    object = models.Manager()

class exampledata (models.Model):
    lat = models.FloatField(max_length=50, null=True)
    lon = models.FloatField(max_length=50, null=True)
    ang = models.FloatField(max_length=50, null=True)
    distance= models.FloatField(max_length=50, null=True)
    ele = models.FloatField(max_length=50, null=True)
    chaturloki=models.CharField (max_length=50, null=True)
    totaldistance=models.FloatField (max_length=50, null=True)
    object = models.Manager()
