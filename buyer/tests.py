from django.conf import settings
from django.shortcuts import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from buyer.factory import fake_buyer, fake


class BuyerActivateAPIView(APITestCase):

    """ Tests views.BuyerActivateAPIView with invalid token. """

    @classmethod
    def setUpTestData(cls):
        cls.buyer = fake_buyer(is_active=False)
        # noinspection PyUnresolvedReferences
        cls.token = cls.buyer.auth_token

    def test_invalid_token_view(self):
        self.client.post(reverse('buyer:reset'))


class BuyerChangePasswordAPIViewTests(APITestCase):

    """ Tests views.BuyerChangePassword with randomized edge cases for invalid old and new passwords. """

    @classmethod
    def setUpTestData(cls) -> None:
        cls.buyer = fake_buyer()
        cls.new_password = fake.pystr(9, 12)

    def test_invalid_old_password(self) -> None:

        """ Tests changing password with invalid current password provided. """

        # noinspection PyUnresolvedReferences
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.buyer.auth_token.key)

        response = self.client.post(
            reverse('buyer:change',),
            {'new_password': self.new_password, 'old_password': fake.pystr(5, 10)},
        )

        self.buyer.refresh_from_db()
        self.assertTrue(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(self.buyer.check_password(settings.TEST_BUYER_PASSWORD))

    def test_new_password_less_than_8_chars(self) -> None:

        """ Tests changing new password with less than 8 characters. """

        # noinspection PyUnresolvedReferences
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.buyer.auth_token.key)

        response = self.client.post(
            reverse('buyer:change',),
            {
                'new_password': fake.pystr(2, 8),
                'old_password': settings.TEST_BUYER_PASSWORD,
            },
        )

        self.buyer.refresh_from_db()
        self.assertTrue(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(self.buyer.check_password(settings.TEST_BUYER_PASSWORD))

    def test_valid_change_password(self) -> None:

        """ Tests successful changing of password to a new random string. """

        # noinspection PyUnresolvedReferences
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.buyer.auth_token.key)

        response = self.client.post(
            reverse('buyer:change'),
            {
                'new_password': self.new_password,
                'old_password': settings.TEST_BUYER_PASSWORD,
            },
        )

        self.buyer.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(self.buyer.check_password(self.new_password))
