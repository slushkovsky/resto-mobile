from django.db import models


# todo: Нужна полная модель сессии
class Session(models.Model):
    venue = models.ForeignKey('restaurants.Venue')
    amount = models.FloatField()
    begined_at = models.DateTimeField(auto_now_add=True)
    end_at = models.DateTimeField(auto_now=True)
