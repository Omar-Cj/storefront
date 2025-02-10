
from django_filters.rest_framework import FilterSet
from .models import Collection, Customer, Product


class ProductFilter(FilterSet):
    class Meta:
        model = Product
        fields = {
            'collection_id': ['exact'],
            'unit_price': ['gt', 'lt']
        }


class CollectionFilter(FilterSet):
    class Meta:
        model = Collection
        fields = {
            'title': ['exact']
        }        


class CustomerFilter(FilterSet):
    class Meta:
        model = Customer
        fields = {
            'membership': ['exact']
        }
