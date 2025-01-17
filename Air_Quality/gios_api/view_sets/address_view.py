from rest_framework import viewsets

from gios_api.models import Address
from gios_api.serializer import AddressSerializer


class AddressViewSet(viewsets.ModelViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
