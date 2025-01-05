from decimal import Decimal
from rest_framework import serializers
from .models import Product, Collection


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['id', 'title','products_count']

    products_count = serializers.IntegerField(read_only=True)     


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'inventory', 'slug', 'unit_price', 'discount', 'collection']
   
    discount = serializers.SerializerMethodField(method_name='calculate_discount')
   #  collection = serializers.StringRelatedField()

    def calculate_discount(self, product: Product):
        return product.unit_price * Decimal(0.5) 
    
   