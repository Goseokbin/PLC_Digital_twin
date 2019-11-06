from django.db import models

# Create your models here.

class Arduino(models.Model):
        temperature = models.IntegerField()
        humidity = models.IntegerField()
        date = models.DateTimeField(auto_now=True)

class Outlier_data(models.Model):
        value = models.IntegerField()
        date = models.DateTimeField(auto_now=True)
        sensor = models.CharField(max_length=10)

class Set_Outlier(models.Model):
        h_max = models.IntegerField()
        h_min = models.IntegerField()
        t_max = models.IntegerField()
        t_min = models.IntegerField()
        e_max = models.IntegerField()
        e_min = models.IntegerField()
        i_max = models.IntegerField()
        i_min = models.IntegerField()
