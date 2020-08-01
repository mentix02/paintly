from django.dispatch import receiver
from django.db.models.signals import post_save

from rest_framework.authtoken.models import Token

from cart.models import Cart
from buyer.models import Buyer
from buyer.tasks import send_activation_email


# noinspection PyUnusedLocal
@receiver(post_save, sender=Buyer)
def create_user_token_and_cart(
    sender, instance: Buyer, created: bool = False, **kwargs
):
    if created:
        Cart.objects.get_or_create(buyer=instance)
        t, _ = Token.objects.get_or_create(user=instance)
        if not instance.is_active:
            send_activation_email(instance.email, t.key)
