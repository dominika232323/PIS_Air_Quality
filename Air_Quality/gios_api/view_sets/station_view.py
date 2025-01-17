from rest_framework import viewsets

from gios_api.models import Station
from gios_api.serializer import StationSerializer


class StationViewSet(viewsets.ModelViewSet):
    queryset = Station.objects.all()
    serializer_class = StationSerializer
