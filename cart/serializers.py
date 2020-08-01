from rest_framework import serializers

from shop.models import Painting
from cart.models import Cart, CartItem


class TinyPaintingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Painting
        fields = ('name', 'price')


class CartItemSerializer(serializers.ModelSerializer):

    painting = TinyPaintingSerializer()

    class Meta:
        model = CartItem
        exclude = ('cart',)


class CartSerializer(serializers.ModelSerializer):

    items = CartItemSerializer(many=True)

    class Meta:
        model = Cart
        fields = '__all__'
