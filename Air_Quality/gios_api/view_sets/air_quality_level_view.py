from rest_framework import viewsets

from gios_api.models import AirQualityLevel
from gios_api.serializer import AirQualityLevelSerializer


class AirQualityLevelViewSet(viewsets.ModelViewSet):
    queryset = AirQualityLevel.objects.all()
    serializer_class = AirQualityLevelSerializer
