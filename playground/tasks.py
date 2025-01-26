
from time import sleep
from celery import shared_task
from templated_mail.mail import BaseEmailMessage

@shared_task
def notify_customers():
    message = BaseEmailMessage(template_name='emails/hello.html')
    message.attach_file('playground/static/images/coffee.jpg')
    message.send(['warsame@systesa.com'])