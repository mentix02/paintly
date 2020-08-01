from __future__ import annotations

from django.db import models
from django.shortcuts import get_object_or_404

from shop.models import Painting


class Cart(models.Model):

    buyer = models.OneToOneField('buyer.Buyer', on_delete=models.CASCADE)

    @property
    def total(self) -> int:
        return sum(item.total for item in self.items.all())

    def add(self, painting_id) -> CartItem:
        painting = get_object_or_404(Painting, id=painting_id)
        item, created = CartItem.objects.get_or_create(painting=painting, cart=self)
        if not created:
            item.quantity += 1
            item.save()
        return item

    def __str__(self) -> str:
        return self.buyer.email


class CartItem(models.Model):

    quantity: int = models.PositiveSmallIntegerField(default=1)
    cart = models.ForeignKey(
        'cart.Cart', on_delete=models.CASCADE, related_name='items'
    )
    painting = models.ForeignKey(
        'shop.Painting', on_delete=models.CASCADE, related_name='+'
    )

    @property
    def total(self) -> int:
        return self.painting.price * self.quantity

    def __str__(self) -> str:
        return self.painting.name
