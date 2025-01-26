from django.shortcuts import render
from store.models import Product
from .tasks import notify_customers



def product_list(request):
    queryset = Product.objects.all().order_by('id')
    context = {'products': list(queryset)}
    return render(request, 'index.html', context)
