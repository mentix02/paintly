from rest_framework import serializers

from buyer.models import Address


STATES = tuple(Address.STATES.items())


class AddressSerializer(serializers.ModelSerializer):

    """ Serializer for model Address. """

    primary = serializers.BooleanField(source='is_primary')

    class Meta:
        model = Address
        exclude = ('buyer', 'id')
