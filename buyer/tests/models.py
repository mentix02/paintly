from django.test import TestCase

from faker import Faker

from buyer.factory import fake_buyer

fake = Faker()


class CustomBuyerModelTests(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.buyer = fake_buyer()
        cls.inactive_buyer = fake_buyer(is_active=False)

    def test_set_full_name(self) -> None:
        full_name = f'{fake.first_name()} {fake.last_name()}'
        self.buyer.set_full_name(full_name)
        self.assertTrue(self.buyer.get_full_name(), full_name)
