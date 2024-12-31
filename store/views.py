from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Product
from .serializers import ProductSerializer

# Create your views here.
@api_view()
def product_list(request):
    queryset = Product.objects.all().order_by('id')
    serializer = ProductSerializer(queryset, many=True)
    return Response(serializer.data)
   
