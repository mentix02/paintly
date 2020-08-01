import json

from django.shortcuts import reverse

from rest_framework import status
from rest_framework.test import APITestCase
from shop.serializers import PaintingSerializer

from shop.factory import fake_painting


class PaintingRetrieveTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.paintings = [fake_painting() for _ in range(25)]

    def test_painting_list_api_view(self):
        serialized_paintings = PaintingSerializer(
            data=reversed(self.paintings), many=True
        )
        serialized_paintings.is_valid()
        response = self.client.get(reverse('shop:list'))

        self.assertTrue(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            serialized_paintings.data, json.loads(response.content.decode())
        )
