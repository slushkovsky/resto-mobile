from django.db import models
from django.contrib.auth.models import AbstractBaseUser


class User(models.Model):
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    email = models.EmailField(null=True)
    photo = models.ImageField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    main_card = models.ForeignKey('restaurants.BankCard', related_name='main_card')
    cards = models.ManyToManyField('restaurants.BankCard')
    auth_type = models.CharField(max_length=20, blank=True, null=True)
    sessions = models.ManyToManyField('restaurants.Session')
    reservations = models.ManyToManyField('restaurants.Reservation')
    # devices = models.ManyToManyField


class PhoneAuthUser(AbstractBaseUser):
    user = models.ForeignKey(User)
    phone = models.CharField(max_length=20)
    USERNAME_FIELD = 'phone'
