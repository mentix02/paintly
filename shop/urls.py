from django.urls import path

from shop.views import PaintingListAPIView

urlpatterns = [
    path('', PaintingListAPIView.as_view(), name='list'),
]
