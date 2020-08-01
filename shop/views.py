from rest_framework.generics import ListAPIView

from shop.models import Painting
from shop.serializers import PaintingSerializer


class PaintingListAPIView(ListAPIView):
    queryset = Painting.objects.all()
    serializer_class = PaintingSerializer
