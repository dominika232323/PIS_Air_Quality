from rest_framework import viewsets

from gios_api.models import Province
from gios_api.serializer import ProvinceSerializer


class ProvinceViewSet(viewsets.ModelViewSet):
    queryset = Province.objects.all()
    serializer_class = ProvinceSerializer
