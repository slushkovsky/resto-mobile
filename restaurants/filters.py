import django_filters

from .models import Venue


class VenueFilter(django_filters.FilterSet):
    city = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Venue
        fields = ['Venue']
