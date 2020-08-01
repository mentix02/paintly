from django.urls import path

from shop.views import PaintingListAPIView

app_name = 'shop'

urlpatterns = [
    path('', PaintingListAPIView.as_view(), name='list'),
]
