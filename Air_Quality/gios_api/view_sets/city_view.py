from rest_framework import viewsets

from gios_api.models import City
from gios_api.serializer import CitySerializer


class CityViewSet(viewsets.ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer
