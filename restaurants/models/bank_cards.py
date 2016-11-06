from django.db import models


class BankCard(models.Model):
    # user = models.ForeignKey('restaurants.User')
    holder_name = models.CharField(max_length=45)
    number = models.CharField(max_length=20)
    expiry_year = models.PositiveSmallIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
