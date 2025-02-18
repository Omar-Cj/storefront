from django.core.mail import EmailMessage, BadHeaderError
from django.shortcuts import render
from rest_framework.views import APIView
from templated_mail.mail import BaseEmailMessage

class HelloView(APIView):
    def get(self, request):
        try:
            message = BaseEmailMessage(template_name='emails/hello.html')
            message.send(['omar3166435@gmail.com'])
        except BadHeaderError:
            pass
        return render(request, 'index.html')  
