from django.db import models

# Create your models here.

class Arduino(models.Model):
        temperature = models.IntegerField()
        humidity = models.IntegerField();