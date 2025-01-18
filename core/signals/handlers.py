from store.signals import order_create
from django.dispatch import receiver

@receiver(order_create)
def on_order_create(sender, **kwargs):
    print(kwargs['order'])
