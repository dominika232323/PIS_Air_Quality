from rest_framework import viewsets

from gios_api.models import Sensor
from gios_api.serializer import SensorSerializer


class SensorViewSet(viewsets.ModelViewSet):
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer
