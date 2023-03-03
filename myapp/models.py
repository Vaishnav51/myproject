from django.db import models

class Phone(models.Model):
    name = models.CharField(max_length=250)
    price = models.CharField(max_length=25)
    mrp = models.CharField(max_length=25)
    rating = models.CharField(max_length=25)
    image_url = models.CharField(max_length=250)
