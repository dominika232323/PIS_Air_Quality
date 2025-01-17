from rest_framework import viewsets

from gios_api.models import District
from gios_api.serializer import DistrictSerializer


class DistrictViewSet(viewsets.ModelViewSet):
    queryset = District.objects.all()
    serializer_class = DistrictSerializer
