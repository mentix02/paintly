from typing import Tuple
from random import choice

from faker import Faker

from shop.models import Painting

fake = Faker()
dimensions: Tuple[Tuple[int, int], Tuple[int, int]] = (
    (17, 12),
    (60, 44),
)


def fake_painting() -> Painting:
    height, width = choice(dimensions)
    return Painting.objects.create(
        height=height,
        width=width,
        description=fake.text(150),
        name=' '.join(fake.words()),
    )
