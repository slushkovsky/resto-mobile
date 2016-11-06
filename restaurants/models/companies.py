from django.db import models


class Company(models.Model):
    name = models.CharField(max_length=64)
    inn = models.CharField(max_length=10)
    phone = models.CharField(max_length=25)
    logo = models.ImageField(blank=True, null=True)
    description = models.CharField(max_length=1024, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
