from __future__ import annotations

from typing import Any, Dict

from django.db import models
from django.db.models.fields.files import ImageFieldFile

from taggit.managers import TaggableManager


class Painting(models.Model):

    description: str = models.TextField()
    name: str = models.CharField(max_length=150)
    width: int = models.PositiveSmallIntegerField()
    height: int = models.PositiveSmallIntegerField()
    price: int = models.PositiveIntegerField(default=10000)
    extra_data: Dict[Any, Any] = models.JSONField(null=True, blank=True)

    tags = TaggableManager(blank=True)

    def get_thumbnail(self) -> ImageFieldFile:
        return self.images.first().file

    class Meta:
        ordering = ('-pk',)
        indexes = [models.Index(fields=['price'])]

    def __str__(self) -> str:
        return self.name


class Image(models.Model):
    file: ImageFieldFile = models.ImageField(upload_to='images')
    caption: str = models.CharField(max_length=175, null=True, blank=True)
    painting: Painting = models.ForeignKey(
        'Painting', on_delete=models.CASCADE, related_name='images'
    )

    class Meta:
        indexes = [models.Index(fields=['painting'])]

    def __str__(self) -> str:
        return self.painting.name
