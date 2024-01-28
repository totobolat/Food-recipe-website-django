from django_filters.rest_framework import FilterSet
from .models import Resipi

class ResipiFilter(FilterSet):
  class Meta:
    model = Resipi
    fields = {
      'category_id': ['exact'],
    }