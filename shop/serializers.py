from rest_framework import serializers
from taggit_serializer.serializers import TagListSerializerField, TaggitSerializer

from shop.models import Painting, Image


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        exclude = ('id', 'painting')


class PaintingSerializer(TaggitSerializer, serializers.ModelSerializer):
    tags = TagListSerializerField()
    thumbnail = serializers.ImageField(source='get_thumbnail')

    class Meta:
        model = Painting
        fields = '__all__'
