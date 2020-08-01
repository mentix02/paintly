from django.conf import settings

from faker import Faker

from buyer.models import Buyer

fake = Faker()


def fake_buyer(**kwargs) -> Buyer:
    kwargs.setdefault('is_active', True)
    return Buyer.objects.create_user(
        email=fake.email(),
        last_name=fake.last_name(),
        first_name=fake.first_name(),
        is_active=kwargs.pop('is_active'),
        password=settings.TEST_BUYER_PASSWORD,
    )
