from django.shortcuts import render
from django.core.mail import EmailMessage, BadHeaderError
from rest_framework.decorators import api_view
from rest_framework.response import Response
from store.serializers import ProductSerializer
from store.models import Product
from templated_mail.mail import BaseEmailMessage


@api_view()
def product_list(request):
    queryset = Product.objects.all().order_by('id')
    context = {'products': list(queryset)}

    try:
      message = BaseEmailMessage(template_name='emails/hello.html')
      message.send(['warsame@systesa.com'])
    except BadHeaderError:
        pass     

    return render(request, 'index.html', context)
