import json
import secrets
import hashlib

from django.conf import settings
from django.shortcuts import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from buyer.models import Buyer
from buyer.factory import fake_buyer, fake


class BuyerSendPasswordResetLinkAPIViewTests(APITestCase):

    """ Tests views.BuyerSendPasswordResetLinkAPIView to send a password link. """


class BuyerRegisterAPIViewTests(APITestCase):

    """ Tests views.BuyerRegisterAPIView to register new buyer accounts. """

    @classmethod
    def setUpTestData(cls) -> None:
        # Set up one fake user to test for existing email registrations
        cls.existing_buyer = fake_buyer()

    def test_incomplete_fields(self) -> None:
        data = {
            'name': fake.name(),
            'email': fake.email(),
            'password': settings.TEST_BUYER_PASSWORD,
        }
        for field in data.keys():
            data_copy = data.copy()
            del data_copy[field]
            response = self.client.post(reverse('buyer:register'), data_copy)
            resp_data = json.loads(response.content.decode())
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertEqual(resp_data['message'], f"'{field}' not provided.")

    def test_existing_email_buyer(self) -> None:
        data = {
            'name': fake.name(),
            'email': self.existing_buyer.email,
            'password': settings.TEST_BUYER_PASSWORD,
        }
        response = self.client.post(reverse('buyer:register'), data)
        resp_data = json.loads(response.content.decode())
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            resp_data['message'], f'User with email {self.existing_buyer.email} exists.'
        )

    def test_valid_buyer_register(self) -> None:
        data = {
            'name': fake.name(),
            'email': fake.email(),
            'password': settings.TEST_BUYER_PASSWORD,
        }
        response = self.client.post(reverse('buyer:register'), data)
        self.assertEqual(Buyer.objects.count(), 2)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class ValidateResetTokenAPIViewTests(APITestCase):

    """ Tests views.ValidateResetTokenAPIView to validate reset tokens. """

    @classmethod
    def setUpTestData(cls) -> None:
        cls.buyer = fake_buyer()
        cls.reset_token = cls.buyer.generate_reset_token()

    def test_valid_token(self) -> None:
        response = self.client.post(
            reverse('buyer:validate'), {'token': self.reset_token.token}
        )
        self.assertEqual(
            response.status_code, status.HTTP_200_OK, msg=response.content.decode()
        )

    def test_invalid_token(self) -> None:
        # test with no token
        response = self.client.post(reverse('buyer:validate'))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.post(
            reverse('buyer:validate'),
            {
                'token': hashlib.sha256(
                    settings.TEST_BUYER_PASSWORD.encode()
                ).hexdigest()
            },
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class BuyerActivateAPIViewTests(APITestCase):

    """ Tests views.BuyerActivateAPIView to activate buyer accounts. """

    @classmethod
    def setUpTestData(cls) -> None:
        cls.buyer = fake_buyer(is_active=False)
        # noinspection PyUnresolvedReferences
        cls.token = cls.buyer.auth_token

    def test_invalid_token(self) -> None:

        # First test with no token.
        response = self.client.post(reverse('buyer:activate'))
        self.buyer.refresh_from_db()
        self.assertFalse(self.buyer.is_active)
        self.assertTrue(response.status_code, 400)

        # Now test with invalid random token
        response = self.client.post(
            reverse('buyer:activate'), {'token': secrets.token_hex(20)}
        )
        self.buyer.refresh_from_db()
        self.assertFalse(self.buyer.is_active)
        self.assertEqual(response.status_code, 400)

    def test_valid_token(self) -> None:
        response = self.client.post(
            reverse('buyer:activate'), {'token': self.token.key}
        )
        self.buyer.refresh_from_db()
        self.assertTrue(self.buyer.is_active)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


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
            reverse('buyer:change'),
            {'new_password': self.new_password, 'old_password': fake.pystr(5, 10)},
        )

        self.buyer.refresh_from_db()
        self.assertTrue(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(self.buyer.check_password(settings.TEST_BUYER_PASSWORD))

    def test_new_password_incomplete_field(self) -> None:

        """ Tests changing new password without providing all required fields. """

        # noinspection PyUnresolvedReferences
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.buyer.auth_token.key)

        response = self.client.post(
            reverse('buyer:change'), {'old_password': settings.TEST_BUYER_PASSWORD}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_new_password_less_than_8_chars(self) -> None:

        """ Tests changing new password with less than 8 characters. """

        # noinspection PyUnresolvedReferences
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.buyer.auth_token.key)

        response = self.client.post(
            reverse('buyer:change'),
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
