from django.test import TestCase
from django.shortcuts import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from buyer.factory import fake_buyer
from shop.factory import fake_painting
from cart.models import Cart, CartItem


class CartModelMethodTests(TestCase):
    """
    Tests cart.Cart's custom methods.
    """

    def test_cart_creation(self) -> None:
        buyer = fake_buyer()
        self.assertEqual(buyer.cart, Cart.objects.get())

    def test_cart_add(self):
        painting0, painting1 = fake_painting(), fake_painting()
        buyer = fake_buyer()

        # add new items
        buyer.cart.add(painting0.id)
        buyer.cart.add(painting1.id)
        self.assertEqual(buyer.cart.items.get(painting=painting0).quantity, 1)
        self.assertEqual(buyer.cart.items.get(painting=painting1).quantity, 1)
        self.assertEqual(buyer.cart.items.count(), 2, msg='2 items not found in cart')

        # add old item thus increasing count
        buyer.cart.add(painting0.id)
        self.assertEqual(buyer.cart.items.get(painting=painting0).quantity, 2)


class CartAPIViewTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.buyer = fake_buyer()
        cls.painting0, cls.painting1 = fake_painting(), fake_painting()

    def test_add_cart_item_view(self):
        # noinspection PyUnresolvedReferences
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.buyer.auth_token.key)
        response = self.client.post(
            reverse('cart:add'), {'painting_id': self.painting0.id}
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CartItem.objects.get().painting.id, self.painting0.id)

    def test_add_cart_view_no_credentials(self):
        response = self.client.post(
            reverse('cart:add'), {'painting_id': self.painting1.id}
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_add_cart_invalid_painting_id(self):
        # noinspection PyUnresolvedReferences
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.buyer.auth_token.key)
        response = self.client.post(reverse('cart:add'), {'painting_id': 314931})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_remove_cart_item_view(self):
        # noinspection PyUnresolvedReferences
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.buyer.auth_token.key)
        cart_item = self.buyer.cart.add(self.painting1.id)
        response = self.client.post(
            reverse('cart:remove'), {'cart_item_id': cart_item.id}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_decrement_cart_item_view(self):
        # noinspection PyUnresolvedReferences
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.buyer.auth_token.key)

        # Add items to increment quantity to 2.
        self.buyer.cart.add(self.painting0.id)
        cart_item = self.buyer.cart.add(self.painting0.id)

        # Decrement once.
        response = self.client.post(
            reverse('cart:decrement'), {'cart_item_id': cart_item.id}
        )

        # Check value was decremented by one.
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            CartItem.objects.values_list('quantity', flat=True).get(),
            cart_item.quantity - 1,
        )

        # Decrement and thus delete cart item.
        response = self.client.post(
            reverse('cart:decrement'), {'cart_item_id': cart_item.id}
        )

        # Check cart item was deleted.
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(CartItem.objects.count(), 0)

    def test_increment_cart_item_view(self):
        """
        Similar to test_decrement_cart_item_view except instead of decrementing,
        it increases the quality of the cart_item by 1.
        """
        # noinspection PyUnresolvedReferences
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.buyer.auth_token.key)

        # Add items to increment quantity to 2.
        self.buyer.cart.add(self.painting0.id)
        cart_item = self.buyer.cart.add(self.painting0.id)

        # Increment once.
        response = self.client.post(
            reverse('cart:increment'), {'cart_item_id': cart_item.id}
        )

        # Check value was incremented by one.
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            CartItem.objects.values_list('quantity', flat=True).get(),
            cart_item.quantity + 1,
        )

        # Increment once again.
        response = self.client.post(
            reverse('cart:increment'), {'cart_item_id': cart_item.id}
        )

        # Check cart item's quantity.
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(CartItem.objects.values_list('quantity', flat=True).get(), 4)
