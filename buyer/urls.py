from django.urls import path

from rest_framework.authtoken import views

from buyer.views import (
    GoogleSignInAPIView,
    BuyerRegisterAPIView,
    ValidateResetTokenAPIView,
    BuyerResetPasswordAPIView,
    BuyerAddressDeleteAPIView,
    BuyerAddressUpdateAPIView,
    BuyerChangePasswordAPIView,
    BuyerAddressListCreateAPIView,
    BuyerSendPasswordResetLinkAPIView,
)

app_name = 'buyer'

urlpatterns = [
    path('token/', views.obtain_auth_token, name='token'),
    path('social/', GoogleSignInAPIView.as_view(), name='social'),
    path('reset/', BuyerResetPasswordAPIView.as_view(), name='reset'),
    path('register/', BuyerRegisterAPIView.as_view(), name='register'),
    path('change/', BuyerChangePasswordAPIView.as_view(), name='change'),
    path('validate/', ValidateResetTokenAPIView.as_view(), name='validate'),
    path('forget/', BuyerSendPasswordResetLinkAPIView.as_view(), name='forget'),
    path(
        'addresses/list/',
        BuyerAddressListCreateAPIView.as_view(),
        name='list-addresses',
    ),
    path(
        'addresses/update/<int:pk>/',
        BuyerAddressUpdateAPIView.as_view(),
        name='update-address',
    ),
    path(
        'addresses/delete/<int:pk>/',
        BuyerAddressDeleteAPIView.as_view(),
        name='remove-address',
    ),
]
