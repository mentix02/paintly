import os
import random
from typing import Tuple

from faker import Faker

from django.conf import settings
from django.core.files import File

from shop.models import Painting, Image

fake = Faker()
dimensions: Tuple[Tuple[int, int], Tuple[int, int]] = (
    (17, 12),
    (60, 44),
)


def fake_painting(images: int = 0) -> Painting:
    height, width = random.choice(dimensions)
    painting = Painting.objects.create(
        height=height,
        width=width,
        description=fake.text(150),
        name=' '.join(fake.words()),
    )
    for _ in range(images):
        fake_image(painting.id)
    return painting


def fake_image(painting_id: int) -> Image:
    with open(
        os.path.join(settings.BASE_DIR, 'media/static/dancing-girl.jpg'), 'br'
    ) as file:
        image = Image.objects.create(
            file=File(file), caption=fake.text(15), painting_id=painting_id
        )
    return image
