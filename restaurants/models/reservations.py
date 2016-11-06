from django.db import models


class Reservation(models.Model):
    guest_count = models.SmallIntegerField()
    starts_at = models.DateTimeField()
    ends_at = models.DateTimeField()
    user = models.ForeignKey('restaurants.User')
    venue = models.ForeignKey('restaurants.Venue')
    comment = models.CharField(max_length=300, blank=True, null=True)
    deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
