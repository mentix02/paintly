from django.urls import path

from cart import views

app_name = 'cart'

urlpatterns = [
    path('add/', views.AddCartItemAPIView.as_view(), name='add'),
    path('items/', views.CartItemListAPIView.as_view(), name='list'),
    path('remove/', views.RemoveCartItemAPIView.as_view(), name='remove'),
    path('increment/', views.IncrementCartItemQuantity.as_view(), name='increment'),
    path('decrement/', views.DecrementCartItemQuantity.as_view(), name='decrement'),
]
