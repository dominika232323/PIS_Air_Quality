from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from gios_api.models import Sensor
from gios_api.serializer import SensorSerializer


class SensorViewSet(viewsets.ModelViewSet):
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer

    @action(detail=False, methods=['get'], url_path='station/(?P<station_id>[^/.]+)')
    def get_sensors_by_station(self, request, station_id=None):
        sensors = self.queryset.filter(station__external_station_id=station_id)
        serializer = self.get_serializer(sensors, many=True)
        return Response(serializer.data)
