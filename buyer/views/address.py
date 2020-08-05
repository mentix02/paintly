""" API views mutating or retrieving the Address model live here. """

from rest_framework.generics import (
    DestroyAPIView,
    ListCreateAPIView,
    RetrieveUpdateAPIView,
)
from rest_framework.permissions import IsAuthenticated

from buyer.serializers import AddressSerializer


class BuyerAddressListCreateAPIView(ListCreateAPIView):
    serializer_class = AddressSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(buyer=self.request.user)

    def get_queryset(self):
        return self.request.user.addresses.all()


class BuyerAddressDeleteAPIView(DestroyAPIView):
    serializer_class = AddressSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return self.request.user.addresses.all()


class BuyerAddressUpdateAPIView(RetrieveUpdateAPIView):
    serializer_class = AddressSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(buyer=self.request.user)

    def get_queryset(self):
        return self.request.user.addresses.all()
