from rest_framework import viewsets

from gios_api.models import Measurement
from gios_api.serializer import MeasurementSerializer


class MeasurementViewSet(viewsets.ModelViewSet):
    queryset = Measurement.objects.all()
    serializer_class = MeasurementSerializer
