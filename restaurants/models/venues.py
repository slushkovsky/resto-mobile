from django.db import models


class Venue(models.Model):
    company = models.ForeignKey('restaurants.Company')
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=1024)
    logo = models.ImageField()
    address = models.CharField(max_length=128)
    lat = models.FloatField()
    lon = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
