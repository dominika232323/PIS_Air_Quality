from rest_framework import viewsets

from gios_api.models import AirQuality
from gios_api.serializer import AirQualitySerializer


class AirQualityViewSet(viewsets.ModelViewSet):
    queryset = AirQuality.objects.all()
    serializer_class = AirQualitySerializer
