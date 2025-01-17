from rest_framework import viewsets

from gios_api.models import AirQualityPollutant
from gios_api.serializer import AirQualityPollutantSerializer


class AirQualityPollutantViewSet(viewsets.ModelViewSet):
    queryset = AirQualityPollutant.objects.all()
    serializer_class = AirQualityPollutantSerializer
