from django.urls import path, include

urlpatterns = [
    path('shop/', include('shop.urls')),
    path('cart/', include('cart.urls')),
    path('buyer/', include('buyer.urls')),
]
