from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from store.serializers import ProductSerializer
from store.models import Product


@api_view()
def product_list(request):
    queryset = Product.objects.all().order_by('id')
    context = {'products': list(queryset)}
    return render(request, 'index.html', context)
