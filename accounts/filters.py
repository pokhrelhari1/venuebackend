import django_filters
from .models import *


class locationFilter(django_filters.FilterSet):
    class Meta:
        model = Venue
        fields= ['address']